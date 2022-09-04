import face_recognition
from smartcard.System import readers
from smartcard.util import toHexString
import cv2
import numpy as np
from database import *
from PIL import Image, ImageTk


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
    :return: email
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


# def faceimage():
#     cap = cv2.VideoCapture(0)
#
#     while True:
#         ret, frame = cap.read()
#
#         cv2.imshow('Camera', frame)
#
#         if cv2.waitKey(1) == 13:  # watch every 1ms if enter has been pressed
#             break
#
#     cap.release()
#     cv2.destroyAllWindows()

def encodefaces():
    global encodedimages
    encodedimages = {}
    for dirpath, dnames, fnames in os.walk('C:/AdvancedAttendanceSystem/FaceImages/'):
        for f in fnames:
            if f.endswith('.jpg'):
                faceimage = face_recognition.load_image_file('C:/AdvancedAttendanceSystem/FaceImages/' + f)
                encoding = face_recognition.face_encodings(faceimage)[0]
                encodedimages[f.split(".")[0]] = encoding
    return encodedimages
