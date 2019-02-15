export FLASK_ENV="development"
export APP_SETTINGS=wikifier.cfg
export FLASK_APP=server.py
nohup flask run --port=4444 --host=0.0.0.0 > wiki.log & 
