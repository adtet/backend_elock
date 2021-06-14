from os import curdir
import mysql.connector
import json

from mysql.connector import cursor

def koneksi_sql():
    db = mysql.connector.connect(host="localhost",
                                 user="root",
                                 password="",
                                 database="db_elock")
    return db

def input_user(plat_nomor,nik,nama,password,jenis_kendaraan):
    db = koneksi_sql()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO `users`(`ID_Kendaraan`, `NIK_KTP`, `Nama`, `Password`, `Jenis_Kendaraan`) VALUES (%s,%s,%s,%s,%s)",(plat_nomor,nik,nama,password,jenis_kendaraan))
        db.commit()
    except(mysql.connector.Error,mysql.connector.Warning) as e:
        print(e)


def cek_platnomor(plat_nomor):
    db = koneksi_sql()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT `ID_Kendaraan` FROM `users` WHERE `ID_Kendaraan`=%s",(plat_nomor,))
        c = cursor.fetchone()
    except(mysql.connector.Error,mysql.connector.Warning) as e:
        print(e)
        c = None
    if c == None:
        return False
    else:
        return True
    

def input_lokasi(plat_nomor,lat,long):
    db = koneksi_sql()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO `lokasi`(`ID_Kendaraan`, `latitude`, `longitude`, `time`) VALUES (%s,%s,%s,now())",(plat_nomor,lat,long))
        db.commit()
    except(mysql.connector.Error,mysql.connector.Warning) as e:
        print(e)


def cek_user(nik,password):
    db = koneksi_sql()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT `NIK_KTP`, `Password` FROM `users` WHERE `NIK_KTP`=%s  AND `Password`=%s ",(nik,password))
        c = cursor.fetchone()
    except(mysql.connector.Error,mysql.connector.Warning) as e:
        print(e)
        c = None
    
    if c == None:
        return False
    else:
        return True

def update_lokasi(lat,long,plat_nomor):
    db = koneksi_sql()
    cursor = db.cursor()
    try:
        cursor.execute("UPDATE `lokasi` SET `latitude`=%s,`longitude`=%s,`time`=now() WHERE `ID_Kendaraan`=%s",(lat,long,plat_nomor))
        db.commit()
    except(mysql.connector.Error,mysql.connector.Warning) as e:
        print(e)

def cek_plat_nomor_lokasi(plat_nomor):
    db = koneksi_sql()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT `ID_Kendaraan` FROM `lokasi` WHERE `ID_Kendaraan`=%s",(plat_nomor,))
        c = cursor.fetchone()
    except(mysql.connector.Error,mysql.connector.Warning) as e:
        print(e)
        c = None
    if c == None:
        return False
    else:
        return True

def get_lokasi(plat_nomor):
    db =koneksi_sql()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT `latitude`, `longitude` FROM `lokasi` WHERE `ID_Kendaraan`=%s",(plat_nomor,))
        c = cursor.fetchone()
    except(mysql.connector.Error,mysql.connector.Warning) as e:
        print(e)
        c = None
    if c==None:
        return None
    else:
        return c
    
def get_plat_nomor_base_nik_and_password(nik,password):
    db = koneksi_sql()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT `ID_Kendaraan` FROM `users` WHERE `NIK_KTP`=%s AND `Password`=%s",(nik,password))
        c = cursor.fetchone()
    except(mysql.connector.Error,mysql.connector.Warning) as e:
        print(e)
        c = None
    return c[0]
