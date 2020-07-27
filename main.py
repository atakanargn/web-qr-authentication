"""
WHATSAPP WEB QR AUTHENTICATION
"""

from flask import redirect, jsonify, Flask, make_response, render_template, request, send_from_directory, url_for, json
from flask_cors import CORS
from time import localtime, strftime
import subprocess

def ipAL():
    ipAddr = subprocess.check_output('hostname -I', shell=True).decode('utf-8')
    ipAddr = ipAddr.split(" ")[0].rstrip().strip()
    print("IP . "+ipAddr)
    return ipAddr

app = Flask(__name__)
app.config['SECRET_KEY'] = '_2+)q(s^0j6fzdf+=qs$2i3dm5*t7m1yghvk3=hwn(i5c=9a1%'

CORS(app)
cors = CORS(app, ressources={
    r"/*": {
        "origins": "*"
    }
})

hashler = []
data = {'basarili':0}

@app.route('/giris')
@app.route('/')
def giris():
    return render_template('index.html',ipAddr=ipAL())

@app.route('/api/qr/e/<string:gHash>')
def api_ekle(gHash):
    hashler.append(gHash)
    return "1"

@app.route('/api/qr/s/<string:gHash>')
def api_sil(gHash):
    hashler.remove(hashler[hashler.index(gHash)])
    return "1"

@app.route('/api/qr/k/<string:gHash>')
def api_kontrol(gHash):
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/api/qr/b')
def api_sifirla():
    data['basarili'] = 0
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/api/qr/g/<string:gHash>')
def api_guncelle(gHash):
    print(hashler)
    if(hashler.count(gHash)>0):
        print("BAŞARILII")
        data['basarili'] = 1
    else:
        data['basarili'] = 0
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/<path:path>')
def send_dir(path):
    return send_from_directory('static/', path)


if __name__ == '__main__':
    try:
        ipAL()
        app.run(host='0.0.0.0', port=1234, debug=True)
    finally:
        app.do_teardown_appcontext()
        print("SUNUCU KAPATILDI.")
