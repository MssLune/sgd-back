# SGD backend

SGD backend application (Servicios Generales a Domicilio).

Make sure that Python 3.7.x version or above is used to use this software.
Use python3.8 may cause dependency installation to be a bit slower than with python3.7 (check [this](https://github.com/explosion/spaCy/issues/6158#issuecomment-810717517) for more information).

## Installation
- Create a virtualenv
    ```bash
    # linux
    # first install virtualenv packages, then
    virtualenv venv

    # windows, macos
    python3 -m venv venv
    ```

- Active virtualenv and install dependencies
    ```bash
    # linux, macos
    source venv/bin/activate

    # windows
    venv/Scripts/activate.bat

    # install dependencies
    # with pip
    pip install -r requirements.txt  # maybe pip3
    
    # with poetry
    poetry install
    ```

## Project information
This project is made up with 3 main packages: django, grpcio and chatterbot
- Django is the main package
- grpcio is used to build a grpc server for stream comunication
- Chatterbot for make a chat bot (works over gRPC server)

Before debug the applications or update they, is required follow some steps (for gRPC and chatterbot, go inside of ``sgd_grcp`` folder)
- Django:

  Load the initial data
  ```bash
  python manage.py loaddata data/initial.json
  ```
  This load permissions and an admin user(admin|admin1234).
    
- gRPC:
  
  When you update [``sgd.proto``](https://github.com/marcovelarde/sgd-back/blob/master/sgd_grpc/proto/sgd.proto) file, execute:
  ```bash
  python codegen.py
  ```
  This update the code required for grpc server.

- Chatterbot:

  For training data, create ``training`` folder inside of ``sgd_grpc`` and add your training data in yml format ([see](https://github.com/gunthercox/chatterbot-corpus/tree/master/chatterbot_corpus/data/spanish) some examples). This files will be loaded for the bot.
  
  Excute the following command for download some data model needed for chhatterbot (spacy dependency)
  ```bash
  python spacy_download
  ```

## Debug
- You need create a `.env` file for settings configuration. Check the ``.env.example`` file for view the current variables. Update the `DATABASE CONFIGURATION` section with your local database credentials (for django application).

- For run the django application:
    ```bash
    python manage.py runserver
    ```

- For run the gRPC application, go inside ``sgd_grcp`` folder and then:
    ```bash
    python server.py
    ```
    Chatbot run over gRPC server.

## Developed with
- [Django Rest Framework](https://www.django-rest-framework.org/), a powerful and flexible toolkit for building Web APIs, built on [Django](https://www.djangoproject.com/)
- [gRPC](https://grpc.io/docs/languages/python/quickstart/), a python implementation for build a high performance, open source universal RPC framework.
- [Chatterbot](https://chatterbot.readthedocs.io/en/stable/), a machine-learning based conversational dialog engine build in Python.

