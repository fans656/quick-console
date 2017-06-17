from flask import Flask, request
from f6.win32 import from_clipboard, to_clipboard

app = Flask(__name__)

@app.route('/clip', methods=['GET'])
def get_clip():
    data = from_clipboard()
    return data if data else ''

@app.route('/clip', methods=['POST'])
def post_clip():
    data = request.data
    data = data.replace('\n', '\r\n')
    to_clipboard(data)
    return data

if __name__ == '__main__':
    app.run(host='192.168.56.1', port=6563, threaded=True, debug=True)
