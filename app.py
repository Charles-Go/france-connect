from urllib.parse import urlencode

import requests
from flask import Flask, redirect, request, render_template_string, session

app = Flask(__name__)

url_callback = '<YOUR_NGROK_URL>'
client_id = '<YOUR_CLIENT_ID>'
client_secret = '<YOUR_CLIENT_SECRET>'
app.secret_key = '<YOUR APP SECRET>'

fc_url = 'https://fcp.integ01.dev-franceconnect.fr'
fc_url_authorize = fc_url + '/api/v1/authorize'
fc_url_token = fc_url + '/api/v1/token'
fc_url_userinfo = fc_url + '/api/v1/userinfo'
fc_url_logout = fc_url + '/api/v1/logout'


@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'POST':
        data = {
            'response_type': 'code',
            'client_id': client_id,
            'state': 'test',
            'nonce': 'test',
            'redirect_uri': url_callback + '/france_connect',
            'scope': 'openid identite_pivot something_obviously_wrong',
        }
        return redirect(fc_url_authorize + '?' + urlencode(data))
    else:
        html = """
<!DOCTYPE html>
<html lang="en">
    <body>
        <form method=post enctype=multipart/form-data>
            <input type="image" src="https://partenaires.franceconnect.gouv.fr/images/fc_bouton_v2.png">
        </form>
    </body>
</html>
        """
        return render_template_string(html)


@app.route('/france_connect', methods=['GET', 'POST'])
def france_connect():
    print(request.args)
    code = request.args.get('code')
    data = {
        'grant_type': 'authorization_code',
        'redirect_uri': url_callback + '/france_connect',
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
    }
    response = requests.post(fc_url_token, data=data)
    if response.status_code == 200:
        token_data = response.json()
        params = {
            'schema': 'openid',
        }
        headers = {
            'Authorization': 'Bearer %s' % token_data['access_token']
        }
        session['id_token'] = token_data.get('id_token')
        user_info_response = requests.get(fc_url_userinfo, params=params, headers=headers)
        html = """
<!DOCTYPE html>
<html lang="en">
    <body>
    {% for key, value in user_info_response.json().items() %}
        <div>{{key}}: {{value}}</div>
    {% endfor %}
        <form method=post action={{url_for('.logout')}} enctype=multipart/form-data>
            <button>Logout</button>
        </form>
    </body>
</html>
        """
        return render_template_string(html, user_info_response=user_info_response)
    return 'Something failed'


@app.route('/logout', methods=['POST'])
def logout():
    id_token = session.pop('id_token')
    data = {
        'id_token_hint': id_token,
        'state': 'test',
        'post_logout_redirect_uri': url_callback,
    }
    return redirect(fc_url_logout + '?' + urlencode(data))


if __name__ == '__main__':
    app.run(port=5000)
