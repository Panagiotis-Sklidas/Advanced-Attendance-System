import face_recognition
from smartcard.System import readers
from smartcard.util import toHexString
import cv2
import numpy as np
from database import *
import csv
import io
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


def createfilepath():
    """
    Check if the program folder exists on the c drive

    Ιf it doesn't exist then it creates it
    :return:
    """
    if os.path.exists('C:/AdvancedAttendanceSystem'):
        pass
    else:
        os.makedirs('C:/AdvancedAttendanceSystem')
        os.makedirs('C:/AdvancedAttendanceSystem/FaceImages/')
        try:
            with io.open('C:/AdvancedAttendanceSystem/presencebook.csv', mode='w', newline='') as csvw:
                prbo_write = csv.writer(csvw)
                prbo_write.writerow(['UID', 'First name', 'Last name', 'Sector', 'Entrance date', 'Year', 'Week',
                                     'Entrance time', 'Exit time', 'Residence time'])
        except:
            print(csv.Error())


def readuid():
    """
    Read RFID/NFC card's uid

    First checks if an RFID reader is connected and opens a connection,
    creates the read command and then transmitting it to the reader
    :return: RFID/NFC card's uid
    """
    r = readers()
    if len(r) < 1:
        print('No readers available')

    reader = r[0]

    connection = reader.createConnection()
    connection.connect()

    command = [0xFF, 0xCA, 0x00, 0x00, 0x00]  # Read card's UID

    if type(command) == list:
        data, sw1, sw2 = connection.transmit(command)
        carduid = str(toHexString(data)).replace(' ', '')  # Remove spaces and convert from hex to string
        # print('Card uid: ', carduid)
        if (sw1, sw2) == (0x90, 0x0):
            # print('Status: The operation completed successfully.')
            pass
        elif (sw1, sw2) == (0x63, 0x0):
            print('Status: The operation failed.')

    return carduid


# A function that creates business email using first and last name
# Also checks if the generated email has already been taken and if this is true then adds an extra random letter
def generateemail(firstname: str, lastname: str):
    """
    Generate business email

    After generating the 7 chars long email makes a request to the database and checks if this email has already been
    given to another employee and if this is true then adds a random extra letter

    :param firstname: str
    :param lastname: str
    :return: email str
    """
    email = firstname.lower()[:2] + lastname.lower()[:5] + '@company.com'
    res = selectemployeebyemail(email)  # Search if there is a user with the same email
    if res != []:
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u', 'v', 'w', 'y', 'x', 'z']
        extra = letters[np.random.randint(0, 25)]
        start = firstname.lower()[:2] + lastname.lower()[:5] + extra

        email = start + '@company.com'
    else:
        pass
    return email


def encodefaces(cuid):
    """
    Encode a specific face image

    :param cuid: str
    :return: encodedimages an array of 128 values which is the encoded face image
    """
    encodedimages = {}
    for dirpath, dnames, fnames in os.walk('C:/AdvancedAttendanceSystem/FaceImages/'):
        photoname = cuid + '.jpg'
        for f in fnames:
            if f == photoname:
            # if f.endswith('.jpg'):
            #     faceimage = face_recognition.load_image_file('C:/AdvancedAttendanceSystem/FaceImages/' + f)
                faceimage = face_recognition.load_image_file('C:/AdvancedAttendanceSystem/FaceImages/' + photoname)
                encoding = face_recognition.face_encodings(faceimage)[0]
                encodedimages[f.split(".")[0]] = encoding
    return encodedimages


def f_recognition(cuid):
    """
    Compare the encoded input image from the webcam with the encoded image that has the same name as the parameter

    :param cuid: str
    :return: name str
    """
    startnow = datetime.now()
    images = encodefaces(cuid)
    faces = list(images.values())
    names = list(images.keys())

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        frame_small = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        frame_small = cv2.cvtColor(frame_small, cv2.COLOR_BGR2RGB)

        face_loc_frame = face_recognition.face_locations(frame_small)
        face_encode_frame = face_recognition.face_encodings(frame_small, face_loc_frame)

        face_name = []
        for encodedface in face_encode_frame:
            matches = face_recognition.compare_faces(faces, encodedface)
            name = "Unknown"

            fdistance = face_recognition.face_distance(faces, encodedface)
            bestmatch = np.argmin(fdistance)
            if matches[bestmatch]:
                name = names[bestmatch]

            face_name.append(name)

        if ret:
            cv2.imshow('Video', frame)
            if cv2.waitKey(1000):
                break

    cap.release()
    cv2.destroyAllWindows()

    print(datetime.now() - startnow)
    return name


def enter_work_area(employee: tuple):
    """
    Κeeps the details and presence of the particular employee

    :param employee: tuple
    """
    entrancedate_time = datetime.today()
    year = entrancedate_time.isocalendar()[0]
    week = entrancedate_time.isocalendar()[1]
    with io.open('C:/AdvancedAttendanceSystem/presencebook.csv', mode='a', newline='') as csvw:
        prbo_write = csv.writer(csvw)
        prbo_write.writerow([employee[0], employee[1], employee[2], employee[8], entrancedate_time.date().isoformat(),
                             year, week, entrancedate_time.time().strftime('%H:%M:%S'), 'N', 'N'])


def exit_work_area(empuid):
    """
    Adds the exit time of a particular user

    :param empuid: str
    """
    outdate_time = datetime.today()
    indate = outdate_time.date().isoformat()
    found = False
    newl = []

    file = io.open('C:/AdvancedAttendanceSystem/presencebook.csv', 'r')
    prbo_read = csv.reader(file)

    for row in prbo_read:
        if (row[0] == empuid) and (row[4] == indate) and (row[8] == 'N') and (row[9] == 'N'):
            found = True
            row[8] = outdate_time.time().strftime('%H:%M:%S')
            out_time = str(row[8])
            in_time = str(row[7])
            fmt = '%H:%M:%S'
            row[9] = datetime.strptime(out_time, fmt) - datetime.strptime(in_time, fmt)
            newl.append(row)
        else:
            newl.append(row)
    file.close()

    if not found:
        print('no employee')
    else:
        file = io.open('C:/AdvancedAttendanceSystem/presencebook.csv', 'w+', newline='', encoding='utf-8')
        prbo_write = csv.writer(file)
        prbo_write.writerows(newl)
        file.seek(0)
    file.close()


def calculate_time_in_sectors_week(sector):
    """
    Calculates time spend in a specific sector

    :param sector: str
    :return: time_in
    """
    count = 0
    time_in = 0

    file = io.open('C:/AdvancedAttendanceSystem/presencebook.csv', 'r')
    prbo_read = csv.reader(file)

    for row in prbo_read:
        sectorid = row[3]
        if (sectorid == str(sector)) and not ((row[9] == 'N') or (row[9] is None)) and \
                str(row[6]) == str(datetime.today().isocalendar()[1]):
            count += 1
            hh, mm, ss = row[9].split(':')
            # seconds = (int(hh) * 3600) + (int(mm) * 60) + int(ss)
            minute = (int(hh) * 60) + int(mm) + (int(ss) / 60)
            # time_in += seconds
            time_in += minute
    file.close()

    return time_in


def create_week_graphs():
    """
    Create week's graph

    :return: graphs
    """
    sectors = fetchsectors()
    sid = []
    sname = []
    data = {}
    for sector in sectors:
        sid.append(sector[0])
        sname.append(sector[1])

    for sector in sectors:
        data.__setitem__(sector[1], calculate_time_in_sectors_week(sector[0]))

    plt.bar(data.keys(), data.values(), width=0.4)
    plt.xticks(rotation=45)
    plt.ylabel('minutes')
    plt.grid(axis='y')
    plt.title('Minutes spend in each sector this week=' + str(datetime.today().isocalendar()[1]))
    plt.show()


def calculate_time_in_sectors_year(sector):
    """
    Calculates time spend in a specific sector

    :param sector: str
    :return: time_in
    """
    count = 0
    time_in = 0

    file = io.open('C:/AdvancedAttendanceSystem/presencebook.csv', 'r')
    prbo_read = csv.reader(file)

    for row in prbo_read:
        sectorid = row[3]
        if (sectorid == str(sector)) and not ((row[9] == 'N') or (row[9] is None)) and \
                str(row[5]) == str(datetime.today().isocalendar()[0]):
            count += 1
            hh, mm, ss = row[9].split(':')
            # seconds = (int(hh) * 3600) + (int(mm) * 60) + int(ss)
            minute = (int(hh) * 60) + int(mm) + (int(ss) / 60)
            # time_in += seconds
            time_in += minute / 60
    file.close()

    return time_in


def create_year_graphs():
    """
    Create year's graph

    :return: graphs
    """
    sectors = fetchsectors()
    sid = []
    sname = []
    data = {}
    for sector in sectors:
        sid.append(sector[0])
        sname.append(sector[1])

    for sector in sectors:
        data.__setitem__(sector[1], calculate_time_in_sectors_year(sector[0]))

    plt.bar(data.keys(), data.values(), width=0.4)
    plt.xticks(rotation=45)
    plt.ylabel('hours')
    plt.grid(axis='y')
    plt.title('Hours spend in each sector this year=' + str(datetime.today().isocalendar()[0]))
    plt.show()
