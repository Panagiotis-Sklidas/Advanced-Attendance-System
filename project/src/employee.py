from database import *
from functions import *


class Employee:
    def __init__(self, cuid: str, firstname: str, lastname: str, email: str, phone: str, dob: str, joineddate: str,
                 position: str, sectorid: int):
        self.cuid = cuid
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone = phone
        self.dob = dob
        self.joineddate = joineddate
        self.position = position
        self.sectorid: sectorid
