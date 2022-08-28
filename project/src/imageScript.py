# Importing useful libraries and modules
import urllib.request
from datetime import datetime
import time
import numpy as np
import cv2


chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
         'U', 'V', 'W', 'Y', 'X', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


# Returns random 8 char long name for the image
def createname():
    """
    Create random 8 chars long name for the download image

    :return: filename: str
    """
    filename = ''
    for i in range(0, 8):
        filename += chars[np.random.randint(0, 35)]
    return filename


def acquirefaceimages():
    """
    Download n images from thispersondoesnotexist.com

    Makes a download request for the face image that has been return by the website
    :return:
    """
    rng = int(input('How many face images to you need from \"thispersondoesnotexist.com\"? '))
    start = datetime.now()
    # Downloading images from thispersondoesnotexist.com
    for i in range(0, rng):
        filename = 'C:/AdvancedAttendanceSystem/FaceImages/' + createname() + '.jpg'
        req = urllib.request.build_opener()
        req.addheaders = [('User-Agent', '')]
        urllib.request.install_opener(req)
        urllib.request.urlretrieve("https://thispersondoesnotexist.com/image", filename)
        print('Downloading image:', i+1, '/', rng)
        # Add a delay before the next loop so that you don't get duplicates and the server does not block the IP as spam
        time.sleep(1.5)

    # Displaying how much time it took to download the images
    print('\nDownloading', rng, 'images took', datetime.now() - start)


def load_images():
    loadimg = cv2.imread('C:/AdvancedAttendanceSystem/FaceImages/7R450EVX.jpg', cv2.IMREAD_COLOR)
    loadimg = cv2.resize(loadimg, (0, 0), fx=0.5, fy=0.5)

    cv2.imwrite('C:/AdvancedAttendanceSystem/FaceImages/7R450EVX.jpg', loadimg)


acquirefaceimages()
# load_images()
