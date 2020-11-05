# MasterSoundBackend

## Installing on UNIX systems

1. Create a virtual environment with python module `venv`:

```$ python3 -m venv venv```

2. Add the following lines at the bottom of the `activate` file inside `venv/bin/`:

```
export FLASK_ENV="development"
export FLASK_APP="entrypoint:app"
export APP_SETTINGS_MODULE="config.default"
```

3. Activate the virtual environment:

```$ source venv/bin/activate```

4. Install the required libraries from the `requirements.txt` file with pip:

```$ pip install -r requirements.txt```

5. Start flask server running:

```$ flask run```
