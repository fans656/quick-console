import flask
import requests


FME_LOCAL = 'http://localhost.fans656.me:10656/'
DEFAULT_ALLOWED_ORIGIN = 'https://fans656.me'
ALLOWED_ORIGINS = set([
    DEFAULT_ALLOWED_ORIGIN,
    'http://localhost.fans656.me',
])
app = flask.Flask(__name__)


@app.after_request
def after_request(res):
    origin = flask.request.environ.get('HTTP_ORIGIN') or DEFAULT_ALLOWED_ORIGIN
    if origin in ALLOWED_ORIGINS:
        res.headers['access-control-allow-origin'] = origin
        res.headers['access-control-allow-methods'] = '*'
    return res


@app.route('/<path:path>', methods = ['GET'])
def get(path):
    url = FME_LOCAL + path
    try:
        res = requests.get(url)
    except Exception:
        return 'fme.local not active', 500
    return res.text, res.status_code


@app.route('/<path:path>', methods = ['POST'])
def post(path):
    url = FME_LOCAL + path
    args = flask.request.get_json(force = True)
    try:
        res = requests.post(url, json = args)
    except Exception:
        return 'fme.local not active', 500
    return res.text, res.status_code


def main():
    app.run(port = 9000, threaded = True)


if __name__ == '__main__':
    main()
