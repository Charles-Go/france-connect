# france-connect

This tutorial is meant to set up with a working test for France Connect using Python/Flask. 

## Installation

After cloning the repo, here are the few steps to get you started:

### Python

Follow the [dev setup guide](https://alan-eu.atlassian.net/wiki/display/101/Dev+setup) to install Python 3.

### Flask server

- Create and prepare your virtual env:

Create the virtual env (you might need to replace `python3` by a complete path if you use Anaconda, like `/usr/local/bin/python3`):

```
python3 -m venv env
```

- Activate it: 

```
source env/bin/activate
```

- Upgrade pip:

```
pip install --upgrade pip
```

- Install dependencies:

```
pip install -r requirements.txt
```

## Add the right keys and tokens
Visit [France Connect](https://partenaires.franceconnect.gouv.fr/monprojet/decouverte).
Click the `Editer le FS` button.

On top, you'll get the `client_id` and the `client_secret`. You will need these in your `app.py`.

You also need to generate a random id (it can be anything) as your `app.secret_key`.

### Setup ngrok to handle callbacks
Install ngrok from [here](https://ngrok.com/download).

Run it with your favorite port (we'll use 5000 here):

`ngrok http 5000`

Ngrok will provide you with a callback address, such as `https://7f132061.ngrok.io`.

Put it in the `Urls de callback` from France Connect's partenaire page.

You can also add `https://7f132061.ngrok.io/france_connect` as an `Url de déconnexion`.

## Run the server
`python app.py` should run on `127.0.0.1:5000`.
You can access `127.0.0.1:5000/france_connect` to test your endpoint.

### Create test data
You can create test data using France Connect's tool [here](https://fip1.integ01.dev-franceconnect.fr/user/create).

## Enjoy
And you're all set to test France Connect by clicking on your [local site](http://127.0.0.1:5000/france_connect)!
