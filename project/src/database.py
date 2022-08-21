import os
import sqlite3
from os import *


def createdb():
    if path.exists('C:/AdvancedAttendanceSystem/AdvancedAttendanceSystem.db'):
        # 'D:/Documents/GitHub/Controlled-entry-using-RFID-FaceRecognition/project/src/AdvancedAttendanceSystem.db'):
        print('DB already exists')
        pass
    else:
        print('Create DB')
        conn = sqlite3.connect('C:/AdvancedAttendanceSystem/AdvancedAttendanceSystem.db')
        cur = conn.cursor()

        cur.execute("CREATE TABLE SECTOR(sector_id INTEGER PRIMARY KEY AUTOINCREMENT, sector_name TEXT NOT NULL);")
        conn.commit()

        cur.execute("INSERT INTO SECTOR (sector_name) VALUES ('HUMAN RESOURCES')")

        cur.execute("""
            CREATE TABLE EMPLOYEE(uid TEXT(8) PRIMARY KEY, first_name TEXT(30) NOT NULL, last_name TEXT(30) NOT NULL,
            email TEXT NOT NULL UNIQUE, phone TEXT NOT NULL UNIQUE, dob TEXT NOT NULL, joined_date TEXT NOT NULL, 
            job_position TEXT NOT NULL, sector_id INTEGER NOT NULL, FOREIGN KEY (sector_id) REFERENCES SECTOR(sector_id) 
            );
        """)
        conn.commit()

        conn.close()


def insertsector(sectorname: str):
    conn = sqlite3.connect('C:/AdvancedAttendanceSystem/AdvancedAttendanceSystem.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO SECTOR (sector_name) VALUES (?);", (sectorname.upper(),))
    conn.commit()
    conn.close()
    return


def fetchsectors():
    conn = sqlite3.connect('C:/AdvancedAttendanceSystem/AdvancedAttendanceSystem.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM SECTOR;")
    res = cur.fetchall()
    conn.commit()
    conn.close()
    return res


def fetchsector(sectorid: int):
    conn = sqlite3.connect('C:/AdvancedAttendanceSystem/AdvancedAttendanceSystem.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM SECTOR WHERE sector_id=(?);", (sectorid,))
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res


def updatesector(sectorid: int, sectorname: str):
    sector = (sectorname, sectorid)
    conn = sqlite3.connect('C:/AdvancedAttendanceSystem/AdvancedAttendanceSystem.db')
    cur = conn.cursor()
    cur.execute("""UPDATE SECTOR SET sector_name=? WHERE sector_id=?;""", sector)
    conn.commit()
    conn.close()


def deletesector(sectorid: int):
    conn = sqlite3.connect('C:/AdvancedAttendanceSystem/AdvancedAttendanceSystem.db')
    cur = conn.cursor()
    res = selectemployeebysector(sectorid)
    if res == []:
        cur.execute("DELETE FROM SECTOR WHERE sector_id=(?);", (sectorid,))
        conn.commit()
    else:
        raise conn.Error()
    conn.close()


def insertemployee(cuid: str, firstname: str, lastname: str, email: str, phone: str, dob: str, jaineddate: str,
                   position: str, sectorid: int):
    conn = sqlite3.connect('C:/AdvancedAttendanceSystem/AdvancedAttendanceSystem.db')
    cur = conn.cursor()
    cur.execute("""INSERT INTO EMPLOYEE (uid,first_name,last_name,email,phone,dob,joined_date,job_position,sector_id)
     VALUES (?,?,?,?,?,?,?,?,?);""", (cuid, firstname.upper(), lastname.upper(), email, phone, dob, jaineddate,
                                      position.upper(), sectorid))
    conn.commit()
    conn.close()


def fetchemployees():
    conn = sqlite3.connect('C:/AdvancedAttendanceSystem/AdvancedAttendanceSystem.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM EMPLOYEE;")
    res = cur.fetchall()
    conn.commit()
    conn.close()
    return res


def selectemployee(cuid: str):
    conn = sqlite3.connect('C:/AdvancedAttendanceSystem/AdvancedAttendanceSystem.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM EMPLOYEE WHERE uid=(?);", (cuid,))
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res


def selectemployeebyemail(email: str):
    conn = sqlite3.connect('C:/AdvancedAttendanceSystem/AdvancedAttendanceSystem.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM EMPLOYEE WHERE email=(?);", (email,))
    res = cur.fetchall()
    conn.commit()
    conn.close()
    return res


def selectemployeebysector(sectorid: int):
    conn = sqlite3.connect('C:/AdvancedAttendanceSystem/AdvancedAttendanceSystem.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM EMPLOYEE WHERE sector_id=(?);", (sectorid,))
    res = cur.fetchall()
    conn.commit()
    conn.close()
    return res


def updateemployee(cuid: str, firstname: str, lastname: str, email: str, phone: str, position: str, sectorid: int):
    employee = (firstname.upper(), lastname.upper(), email.lower(), phone, position.upper(), sectorid, cuid)
    conn = sqlite3.connect('C:/AdvancedAttendanceSystem/AdvancedAttendanceSystem.db')
    cur = conn.cursor()
    cur.execute("""UPDATE EMPLOYEE SET first_name=?, last_name=?, email=?, phone=?, job_position=?, sector_id=?
    WHERE uid=?;""", employee)
    conn.commit()
    conn.close()


def deleteemployee(cuid: str):
    conn = sqlite3.connect('C:/AdvancedAttendanceSystem/AdvancedAttendanceSystem.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM EMPLOYEE WHERE uid=(?);", (cuid,))
    conn.commit()
    conn.close()
