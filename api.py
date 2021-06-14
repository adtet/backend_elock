from flask import Flask,jsonify,request
from sqllib import input_user,cek_platnomor,input_lokasi,cek_user,cek_plat_nomor_lokasi,update_lokasi
import hashlib

app = Flask(__name__)

@app.route('/elock/user/input',methods=['POST'])
def user_input():
    json_data = request.json
    if json_data==None:
        result = {"message": "process failed"}
        resp = jsonify(result)
        return resp, 400
    else:
        if 'plat_nomor' not in json_data or 'nik' not in json_data or 'nama' not in json_data or 'password' not in json_data or 'jenis_kendaraan' not in json_data:
            result = {"message": "error request"}
            resp = jsonify(result)
            return resp, 401
        else:
            plat_nomor = json_data['plat_nomor']
            nik = json_data['nik']
            nama = json_data['nama']
            password = json_data['password']
            password = hashlib.sha256(password.encode()).hexdigest()
            jenis_kendaraan = json_data['jenis_kendaraan']

            input_user(plat_nomor,nik,nama,password,jenis_kendaraan)
            result = {"message": "Input success"}
            resp = jsonify(result)
            return resp, 200

@app.route('/elock/user/lokasi/input',methods=['POST'])
def lokasi_input():
    json_data = request.json
    if json_data==None:
        result = {"message": "process failed"}
        resp = jsonify(result)
        return resp, 400
    else:
        if 'plat_nomor' not in json_data or 'lat' not in json_data or 'long' not in json_data :
            result = {"message": "error request"}
            resp = jsonify(result)
            return resp, 401
        else:
            plat_nomor = json_data['plat_nomor']
            lat = json_data['lat']
            long = json_data['long']
            cek = cek_platnomor(plat_nomor)
            if cek==False:
                result = {"message": "Unregisted Vehicle"}
                resp = jsonify(result)
                return resp, 203
            else:
                input_lokasi(plat_nomor,lat,long)
                result = {"message": "Input success"}
                resp = jsonify(result)
                return resp, 200


@app.route('/elock/user/login',methods=['POST'])
def login_user():
    json_data = request.json
    if json_data == None:
        result = {"message": "process failed"}
        resp = jsonify(result)
        return resp, 400
    else:
        if 'nik' not in json_data or 'password' not in json_data:
            result = {"message": "error request"}
            resp = jsonify(result)
            return resp, 401
        else:
            nik = json_data['nik']
            password = json_data['password']
            password = hashlib.sha256(password.encode()).hexdigest()
            cek = cek_user(nik,password)
            if cek==False:
                result = {"message": "Unregisted account"}
                resp = jsonify(result)
                return resp, 203
            else:
                result = {"pesan" : " Selamat Datang"}
                resp= jsonify(result)
                return resp, 200

@app.route('/elock/user/update/lokasi',methods=['POST'])
def lokasi_update():
    json_data = request.json
    if json_data== None:
        result = {"message": "process failed"}
        resp =jsonify(result)
        return resp, 400

    else:
        if 'lat' not in json_data or 'long' not in json_data or 'plat_nomor' not in json_data:
            result = {"message": "error request"}
            resp = jsonify(result)
            return resp, 401
        else:
            lat = json_data['lat']
            long = json_data['long']
            plat_nomor = json_data['plat_nomor']
            cek = cek_plat_nomor_lokasi(plat_nomor)
            if cek==False:
                result = {"message": "Unregisted account"}
                resp = jsonify(result)
                return resp, 203
            else:
                update_lokasi(lat,long,plat_nomor)
                result = {"message": "Update success"}
                resp = jsonify(result)
                return resp, 200


if __name__ == "__main__":
    # serve(app, host="0.0.0.0", port=8001)
    app.run(port=8001, debug=True)