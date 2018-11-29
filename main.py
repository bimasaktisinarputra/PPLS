from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import urllib.parse
import datetime, urllib.parse
import os
import json
import requests

cred = credentials.Certificate('kunci.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

port = int(os.environ.get('PORT', 33507))
app = Flask(__name__)


def datamobil(id, name, loc, date):
    data = {
        u'id': id,
        u'name': name,
        u'location': loc,
        u'date': date,
    }
    return data


def invoice(date, idm, idp, ddate, stat):
    data = {
        'date': date,
        'mobil': db.document("mobil/" + idm),
        'passenger': db.document("passenger/" + idp),
        'todate': ddate,
        'status': stat
    }
    return data


def kontrak(idv, idm, idp, ddate):
    data = {
        'date': datetime.datetime.now(),
        'vendor': db.document("vendor/" + idv),
        'mobil': db.document("mobil/" + idm),
        'passenger': db.document("passenger/" + idp),
        'ddate': ddate,
    }
    return data


def rec(url):
    url = ''
    req = requests.get(url)

    data = json.loads(req)

    return jsonify(data)


@app.route('/')
def home():
    return jsonify({'Hai': 'Halo',
                    'Tes': 123}), 200, {'ContentType': 'application/json'}


@app.route('/search')
@app.route('/mobil')
def availability():
    global data
    global temp
    data = []
    temp = {}
    ploc = request.args.get('loc')
    pdate = request.args.get('date')  # DD/MM/YYYY H:M:S
    dn = urllib.parse.unquote_plus(pdate)
    dnn = datetime.datetime.strptime(dn, "%d/%m/%Y %H:%M:%S")
    mobil_ref = db.collection('mobil')

    car = mobil_ref.where('location', '==', ploc).where('date', '<', dnn).where('status', '==', 'available').get()

    for mobil in car:
        temp = mobil.to_dict()
        temp['id'] = mobil.id
        data.append(datamobil(temp['id'], temp['name'], temp['location'], temp['date']))

    return jsonify(data)


@app.route('/notif', methods=['POST'])
def notif():
    data = request.data

    print(json.loads(data))
    # kirim ke suatu hal

    return jsonify({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/setmobil')
def set_mobil():
    idm = request.args.get('idm')
    dloc = request.args.get('loc')
    stat = request.args.get('stat')
    ddate = request.args.get('date')
    dn = urllib.parse.unquote_plus(ddate)
    dnn = datetime.datetime.strptime(dn, "%d/%m/%Y %H:%M:%S")
    db.collection('mobil').document(idm).update({
        'status': stat,
        'dropLocation': dloc,
        'dropDate': dnn
    })
    return jsonify({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/geninv')
def generate_invoice():
    idm = request.args.get('idm')
    idp = request.args.get('idp')
    ddate = request.args.get('date')
    dn = urllib.parse.unquote_plus(ddate)
    dnn = datetime.datetime.strptime(dn, "%d/%m/%Y %H:%M:%S")
    inv_ref = invoice(datetime.datetime.now(), idm, idp, dnn, "belum bayar")
    db.collection('transaksi').add(inv_ref)

    return jsonify({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/getinv')
def get_inv():
    idi = request.args.get('idi')

    data = db.collection('transaksi').document(idi).get().get("status")

    return jsonify({
        'status': data,
    })


@app.route('/setinv')
def set_inv():
    idi = request.args.get('idi')
    stat = request.args.get('stat')

    db.collection('transaksi').document(idi).update({
        'status': stat
    })

    return jsonify({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/gencont')
def gen_cont():
    idv = request.args.get('idv')
    idp = request.args.get('idp')
    idm = request.args.get('idm')
    ddate = request.args.get('date')
    dn = urllib.parse.unquote_plus(ddate)
    dnn = datetime.datetime.strptime(dn, "%d/%m/%Y %H:%M:%S")
    kon_ref = kontrak(idv, idm, idp, dnn)

    db.collection('kontrak').add(kon_ref)

    return jsonify({'success': True}), 200, {'ContentType': 'application/json'}


app.run(host='0.0.0.0', port=port)
