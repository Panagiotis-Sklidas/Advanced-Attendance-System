# Importing useful libraries and modules
import urllib.request
from datetime import datetime
import time
import numpy as np


chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
         'U', 'V', 'W', 'Y', 'X', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def createname():
    filename = ''
    for i in range(0, 8):
        filename += chars[np.random.randint(0, 35)]
    return filename


def acquirefaceimages():
    rng = int(input('How many face images to you need from \"thispersondoesnotexist.com\"? '))
    start = datetime.now()
# Downloading images from thispersondoesnotexist.com
    for i in range(0, rng):
        filename = createname() + '.jpg'
        req = urllib.request.build_opener()
        req.addheaders = [('User-Agent', '')]
        urllib.request.install_opener(req)
        urllib.request.urlretrieve("https://thispersondoesnotexist.com/image", filename)
        print('Downloading image:', i+1, '/', rng)
        # Add a delay before the next loop so that you don't get duplicates and the server does not block the IP as spam
        time.sleep(1.5)

    # Displaying how much time it took to download the images
    print('\nDownloading', rng, 'images took', datetime.now() - start)


createname()
acquirefaceimages()
