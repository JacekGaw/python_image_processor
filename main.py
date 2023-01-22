from multiprocessing import Process, Lock
import PIL.Image
import os
import time

start_time = time.time()

source_folder_path = "rawS/"


def create_thumbnail(img, img_name):
    img.thumbnail((500, 500))
    img_conv = img.convert('L')
    if not os.path.exists("finals/thumbnails"):
        os.makedirs("finals/thumbnails")
    img_conv.save(f"finals/thumbnails/{img_name}", "JPEG")


def sort_image(img, img_name, l):
    img_exif = img._getexif()[36867]

    if img_exif:
        date_str = img_exif.split(" ")[0]
        year = date_str.split(":")[0]
        month = date_str.split(":")[1]
        day = date_str.split(":")[2]
        with l:
            if not os.path.exists(f"finals/{year}"):
                os.makedirs(f"finals/{year}")
                if not os.path.exists(f"finals/{year}/{month}"):
                    os.makedirs(f"finals/{year}/{month}")
                else:
                    if not os.path.exists(f"finals/{year}/{month}/{day}"):
                        os.makedirs(f"finals/{year}/{month}/{day}")
                        img.save(f"finals/{year}/{month}/{day}/{img_name}", "JPEG")
                    else:
                        img.save(f"finals/{year}/{month}/{day}/{img_name}", "JPEG")
            else:
                if not os.path.exists(f"finals/{year}/{month}"):
                    os.makedirs(f"finals/{year}/{month}")
                else:
                    if not os.path.exists(f"finals/{year}/{month}/{day}"):
                        os.makedirs(f"finals/{year}/{month}/{day}")
                        img.save(f"finals/{year}/{month}/{day}/{img_name}", "JPEG")
                    else:
                        img.save(f"finals/{year}/{month}/{day}/{img_name}", "JPEG")
    else:
        if not os.path.exists(f"finals/unsorted"):
            os.makedirs(f"finals/unsorted")
            img.save(f"finals/unsorted/{img_name}", "JPEG")
        else:
            img.save(f"finals/unsorted/{img_name}", "JPEG")


def open_image(img_name, l):
    img = PIL.Image.open(f"{source_folder_path}{img_name}")
    sort_image(img, img_name, l)
    create_thumbnail(img, img_name)


def get_names(path):
    files = os.listdir(path)
    return files


def main():
    procs = []
    files = get_names(source_folder_path)
    print(files)
    l = Lock()

    for x in files:
        # open_image(x)
        proc = Process(target=open_image, args=(x,l, ))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()


if __name__ == '__main__':
    main()
    end = time.time()
    print('Processing time standard: {0} [sec]'.format(end - start_time))


# https://docs.python.org/3/library/multiprocessing.html
# https://github.com/andrewning/sortphotos
