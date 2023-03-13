from multiprocessing import Process, Lock
import PIL.Image
import PIL.ImageFilter
from PIL import ImageEnhance
import os
import time
import matplotlib.pyplot as plt


times_arr = []
files_arr = []

source_folder_path = ["raw"]


def create_thumbnail(img, img_name):
    img.thumbnail((1000, 1000))
    img_conv = img.convert('L')
    img_sharpen = img_conv.filter(PIL.ImageFilter.SHARPEN)
    factor = 1.5
    enhancer = ImageEnhance.Contrast(img_sharpen)
    img_finish = enhancer.enhance(factor)
    if not os.path.exists("finals/thumbnails"):
        os.makedirs("finals/thumbnails")
    img_finish.save(f"finals/thumbnails/{img_name}", "JPEG")


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


def open_image(img_name, l, i):
    img = PIL.Image.open(f"{source_folder_path[i]}/{img_name}")
    sort_image(img, img_name, l)
    create_thumbnail(img, img_name)


def get_names(path):
    files = os.listdir(path)
    return files


def generate_graph(times, files):
    times.sort()
    files.sort()
    max_time = times[len(times)-1]
    max_file = files[len(files)-1]

    plt.plot([0, files[len(files)-3], files[len(files)-2], max_file], [0, times[len(times)-3], times[len(times)-2], max_time])
    plt.title("Using multiprocessing")
    plt.ylabel('time (s)')
    plt.xlabel('files')
    plt.savefig('graph_multi.png')
    plt.close()

def main():
    source_catalogs = len(source_folder_path)
    for i in range(source_catalogs):
        start_time = time.time()
        print("working...")
        procs = []
        source = source_folder_path[i]
        files = get_names(source)
        files_arr.append(len(files))
        print(f"Files to process: {len(files)}")
        l = Lock()

        start_time = time.time()
        for x in files:
              # open_image(x, l, i)  instrukcja do wywoływania liniowego
            proc = Process(target=open_image, args=(x,l,i, ))
            procs.append(proc)
            proc.start()

        for proc in procs:
            proc.join()

        end = time.time()
        end_time = round((end - start_time),2)
        times_arr.append(end_time)
        print('Processing time standard: {0} [sec]'.format(end - start_time))



if __name__ == '__main__':
    main()
    # generate_graph(times_arr, files_arr)