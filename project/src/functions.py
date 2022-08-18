from smartcard.System import readers
from smartcard.util import toHexString
import cv2
import numpy as np
from database import *

# os.makedirs('C:/AdvancedAttendanceSystem')
def createfilepath():
    if os.path.exists('C:/AdvancedAttendanceSystem'):
        pass
    else:
        os.makedirs('C:/AdvancedAttendanceSystem')


def readuid():
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
        print('Card uid: ', carduid)
        if (sw1, sw2) == (0x90, 0x0):
            print('Status: The operation completed successfully.')
        elif (sw1, sw2) == (0x63, 0x0):
            print('Status: The operation failed.')

    return carduid


def generateemail(firstname: str, lastname: str):
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


def faceimage():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        cv2.imshow('Camera', frame)

        if cv2.waitKey(1) == 13:  # watch every 1ms if enter has been pressed
            break

    cap.release()
    cv2.destroyAllWindows()
