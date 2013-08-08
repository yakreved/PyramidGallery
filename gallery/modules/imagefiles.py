#This module work with files on HDD

import os
import threading
import time


def deleteFile(filename):
    print("waiting for delete 5s")
    time.sleep(5)
    print("delete "+ filename)
    os.remove(filename)
    return


def deleteImageFile(image):
    _here = os.path.split(os.path.dirname(__file__))[0]
    tmp = os.path.join(_here, 'static', 'images', os.path.split(image.url)[1])
    t = threading.Thread(target=deleteFile, args=(tmp,))
    t.daemon = True
    t.start()


def addImageFile(filename, input_file):
    _here = os.path.split(os.path.dirname(__file__))[0]
    tmp = os.path.join(_here, 'static', 'images', filename)
    open(tmp, 'wb').write(input_file.read())