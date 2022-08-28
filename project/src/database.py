import os
import sqlite3
from os import *


def createdb():
    """
    Create the database

    Firstly checks if the db already exists in progam folder and if not it creates it
    :return:
    """
    if path.exists('C:/AdvancedAttendanceSystem/AdvancedAttendanceSystem.db'):
        # print('DB already exists')
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
    """
    Insert sector

    Opens a connection to db and makes a create request for a new sector, which will be named as the parameter passed
    :param sectorname: str
    :return:
    """
    conn = sqlite3.connect('C:/AdvancedAttendanceSystem/AdvancedAttendanceSystem.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO SECTOR (sector_name) VALUES (?);", (sectorname.upper(),))
    conn.commit()
    conn.close()
    return


def fetchsectors():
    """
    Bring all sector

    :return: res: list
    """
    conn = sqlite3.connect('C:/AdvancedAttendanceSystem/AdvancedAttendanceSystem.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM SECTOR;")
    res = cur.fetchall()
    conn.commit()
    conn.close()
    return res


def fetchsector(sectorid: int):
    """
    Bring a specific sector

    Brings the information of the sector with the same id as the parameter
    :param sectorid: int
    :return: res: list of one
    """
    conn = sqlite3.connect('C:/AdvancedAttendanceSystem/AdvancedAttendanceSystem.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM SECTOR WHERE sector_id=(?);", (sectorid,))
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res


def updatesector(sectorid: int, sectorname: str):
    """
    Update sector

    Updates the name of a specific record passing to the sector_name field the value of the second parameter
    :param sectorid: int
    :param sectorname: str
    :return:
    """
    sector = (sectorname, sectorid)
    conn = sqlite3.connect('C:/AdvancedAttendanceSystem/AdvancedAttendanceSystem.db')
    cur = conn.cursor()
    cur.execute("""UPDATE SECTOR SET sector_name=? WHERE sector_id=?;""", sector)
    conn.commit()
    conn.close()
    return


def deletesector(sectorid: int):
    """
    Delete sector

    Deletes a specific sector
    :param sectorid: int
    :return:
    """
    conn = sqlite3.connect('C:/AdvancedAttendanceSystem/AdvancedAttendanceSystem.db')
    cur = conn.cursor()
    res = selectemployeebysector(sectorid)
    if res == []:
        cur.execute("DELETE FROM SECTOR WHERE sector_id=(?);", (sectorid,))
        conn.commit()
    else:
        raise conn.Error()
    conn.close()
    return


def insertemployee(cuid: str, firstname: str, lastname: str, email: str, phone: str, dob: str, jaineddate: str,
                   position: str, sectorid: int):
    """
    Create a new employee

    :param cuid: str
    :param firstname: str
    :param lastname: str
    :param email: str
    :param phone: str
    :param dob: str
    :param jaineddate: str
    :param position: str
    :param sectorid: int
    :return:
    """
    conn = sqlite3.connect('C:/AdvancedAttendanceSystem/AdvancedAttendanceSystem.db')
    cur = conn.cursor()
    cur.execute("""INSERT INTO EMPLOYEE (uid,first_name,last_name,email,phone,dob,joined_date,job_position,sector_id)
     VALUES (?,?,?,?,?,?,?,?,?);""", (cuid, firstname.upper(), lastname.upper(), email, phone, dob, jaineddate,
                                      position.upper(), sectorid))
    conn.commit()
    conn.close()
    return


def fetchemployees():
    """
    Fetch all employees

    :return: res: list
    """
    conn = sqlite3.connect('C:/AdvancedAttendanceSystem/AdvancedAttendanceSystem.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM EMPLOYEE;")
    res = cur.fetchall()
    conn.commit()
    conn.close()
    return res


def selectemployee(cuid: str):
    """
    Fetch a specific employee correspoding to the parameter uid

    :param cuid: str
    :return: res: list of one
    """
    conn = sqlite3.connect('C:/AdvancedAttendanceSystem/AdvancedAttendanceSystem.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM EMPLOYEE WHERE uid=(?);", (cuid,))
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res


def selectemployeebyemail(email: str):
    """
    Fetch employees correspoding to the parameter email

    :param email: str
    :return: res: list
    """
    conn = sqlite3.connect('C:/AdvancedAttendanceSystem/AdvancedAttendanceSystem.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM EMPLOYEE WHERE email=(?);", (email,))
    res = cur.fetchall()
    conn.commit()
    conn.close()
    return res


def selectemployeebysector(sectorid: int):
    """
    Fetch all the employees that work in a specific sector

    :param sectorid: int
    :return: res: list
    """
    conn = sqlite3.connect('C:/AdvancedAttendanceSystem/AdvancedAttendanceSystem.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM EMPLOYEE WHERE sector_id=(?);", (sectorid,))
    res = cur.fetchall()
    conn.commit()
    conn.close()
    return res


def updateemployee(cuid: str, firstname: str, lastname: str, email: str, phone: str, position: str, sectorid: int):
    """
    Update a specific employee

    :param cuid: str
    :param firstname: str
    :param lastname: str
    :param email: str
    :param phone: str
    :param position: str
    :param sectorid: int
    :return:
    """
    employee = (firstname.upper(), lastname.upper(), email.lower(), phone, position.upper(), sectorid, cuid)
    conn = sqlite3.connect('C:/AdvancedAttendanceSystem/AdvancedAttendanceSystem.db')
    cur = conn.cursor()
    cur.execute("""UPDATE EMPLOYEE SET first_name=?, last_name=?, email=?, phone=?, job_position=?, sector_id=?
    WHERE uid=?;""", employee)
    conn.commit()
    conn.close()
    return


def deleteemployee(cuid: str):
    """
    Delete a user

    :param cuid: int
    :return:
    """
    conn = sqlite3.connect('C:/AdvancedAttendanceSystem/AdvancedAttendanceSystem.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM EMPLOYEE WHERE uid=(?);", (cuid,))
    conn.commit()
    conn.close()

    employeeimg = 'C:/AdvancedAttendanceSystem/FaceImages/' + cuid + '.jpg'
    os.remove(employeeimg)
    return
