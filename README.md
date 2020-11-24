# Shop4me Application

## Description

Shop4me allows users to request a product in a shop. Volunteers can deliver the requested products to the requester.

## Technologies

The technologies used to develop the shop4me application.

### Front

- HTML
- CSS
- Sass
- JS
- React

### Back End

- Python
- Flask
- MongoDB
- Cloudinary(to store images)

## How to run the application

### On Windows

First start the front end application, using the following commands. From the project directory run do the following steps

```sh
cd front-react
yarn install
yarn start
```

From the project directory run the following commands to activate the virtual environment

```sh
cd back-flask
cd env
cd Scripts
. activate
```

Return to the back-flask directory and run and start the back end by writing

```sh
export FLASK_APP=main.py
python -m flask run
```

### On Linux and MacOs

First start the front end application, using the following commands. From the project directory run do the following steps

```sh
cd front-react
yarn install
yarn start
```

From the project directory run the following commands to activate the virtual environment

```sh
cd back-flask
cd env
source env/bin/activate
```

Return to the back-flask directory and run and start the back end by writing

```sh
export FLASK_APP=main.py
python -m flask run
```
