from flask import Flask,jsonify,request
from sqllib import input_user,cek_platnomor,input_lokasi,cek_user,cek_plat_nomor_lokasi,update_lokasi,get_lokasi,get_plat_nomor_base_nik_and_password
from sqllib import input_laporan,get_laporan_base_on_plat_nomor,cek_plat_nomor_on_laporan
import hashlib
import json
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
            lng = json_data['long']
            cek = cek_platnomor(plat_nomor)
            if cek==False:
                result = {"message": "Unregisted Vehicle"}
                resp = jsonify(result)
                return resp, 203
            else:
                input_lokasi(plat_nomor,lat,lng)
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
                return resp, 403
            else:
                plat_nomor = get_plat_nomor_base_nik_and_password(nik,password)
                data = get_lokasi(plat_nomor)
                if data==None:
                    result = {"message": "vehicle undetected"}
                    resp = jsonify(result)
                    return resp, 203
                else:
                    result = {"pesan" : " Selamat Datang",
                          "Lat":data[0],
                          "Lng":data[1],
                          "plat_nomor":plat_nomor}
                    resp= jsonify(result)
                    return resp, 200

@app.route('/elock/user/update/lokasi/<lat>/<lng>/<plat_nomor>',methods=['POST'])
def lokasi_update(lat,lng,plat_nomor):
    cek = cek_plat_nomor_lokasi(plat_nomor)
    if cek==False:
        result = {"message": "Unregisted account"}
        resp = jsonify(result)
        return resp, 203
    else:
        update_lokasi(lat,lng,plat_nomor)
        result = {"message": "Update success"}
        resp = jsonify(result)
        return resp, 200

@app.route('/elock/input/laporan',methods=['POST'])
def laporan_input():
    json_data = request.json
    if json_data==None:
        result = {"message": "process failed"}
        resp = jsonify(result)
        return resp, 400
    else:
        if 'plat_nomor' not in json_data or 'laporan' not in json_data or 'latitude' not in json_data or 'longitude' not in json_data:
            result = {"message": "error request"}
            resp = jsonify(result)
            return resp, 401
        else:
            plat_nomor = json_data['plat_nomor']
            laporan = json_data['laporan']
            latitude = json_data['latitude']
            longitude = json_data['longitude']
            cek = cek_plat_nomor_lokasi(plat_nomor)
            if cek == False:
                result = {"message": "Unregisted vehicle"}
                resp = jsonify(result)
                return resp, 403
            else:
                input_laporan(plat_nomor,laporan,latitude,longitude)
                result = {"message": "Input success"}
                resp = jsonify(result)
                return resp, 200

@app.route('/elock/get/laporan',methods=['POST'])
def laporan_show():
    json_data = request.json
    if json_data==None:
        result = []
        resp = json.dumps(result)
        return resp, 400
    else:
        if 'plat_nomor' not in json_data:
            result = []
            resp = json.dumps(result)
            return resp, 401
        else:
            plat_nomor =  json_data['plat_nomor']
            cek = cek_plat_nomor_on_laporan(plat_nomor)
            if cek == False:
                result = []
                resp = json.dumps(result)
                return resp, 403
            else:
                resp = get_laporan_base_on_plat_nomor(plat_nomor)
                return resp,200
                
@app.route('/elock/welcome',methods=['GET'])
def welcome():
    result = {"message":"welcome"}
    resp = jsonify(result)
    return resp,200

if __name__ == "__main__":
    # serve(app, host="0.0.0.0", port=8005)
    app.run(port=8005, debug=True)