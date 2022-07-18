# Importing useful libraries and modules
import urllib.request
from datetime import datetime
import time


def acquirefaceimages():
    rng = int(input('How many face images to you need from \"thispersondoesnotexist.com\"? '))
    start = datetime.now()
# Downloading images from thispersondoesnotexist.com
    for i in range(0, rng):
        filename = str(i+1) + '.jpg'
        req = urllib.request.build_opener()
        req.addheaders = [('User-Agent', '')]
        urllib.request.install_opener(req)
        urllib.request.urlretrieve("https://thispersondoesnotexist.com/image", filename)
        print('Downloading image:', i+1, '/', rng)
        # Add a delay before the next loop so that you don't get duplicates and the server does not block the IP as spam
        time.sleep(1.5)

    # Displaying how much time it took to download the images
    print('\nDownloading', rng, 'images took', datetime.now() - start)


def checkfaceimage():
    print("Reduce face set coming soon")


action = int(input('To download face images press \"1\" to reduce the dataset press \"2\": '))

if action == 1:
    acquirefaceimages()
else:
    checkfaceimage()
