import multiprocessing
import PIL.Image
import os
import time

start_time = time.time()

def openImage(imgName):
    img = PIL.Image.open(f"raw/{imgName}")
    img.thumbnail((100,100))
    if not os.path.exists("finals"):
        os.makedirs("finals")
    img.save(f"finals/{imgName}","JPEG")
    exif_data = img._getexif()
    return exif_data

def getNames(path):
    files = os.listdir(path);
    return files


if __name__ == '__main__':
    files = getNames("C:\\Users\\gawjo\\PycharmProjects\\obrazy\\raw\\")
    print(files)

    for x in files:
        print(openImage(x))

print('Processing time standard: {0} [sec]'.format(time.time() - start_time))


# https://docs.python.org/3/library/multiprocessing.html
# https://github.com/andrewning/sortphotos