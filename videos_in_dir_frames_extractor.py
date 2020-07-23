#TODO Fix some issues with this script

import os, sys, glob, getopt, datetime
import cv2

# Sorting Functions
def find_first_digit(s, non=False):
    for i, x in enumerate(s):
        if x.isdigit() ^ non:
            return i
    return -1

def split_digits(s, case=False):
    non = True
    while s:
        i = find_first_digit(s, non)
        if i == 0:
            non = not non
        elif i == -1:
            yield int(s) if s.isdigit() else s if case else s.lower()
            s = ''
        else:
            x, s = s[:i], s[i:]
            yield int(x) if x.isdigit() else x if case else x.lower()

def natural_key(s, *args, **kwargs):
    return tuple(split_digits(s, *args, **kwargs))

def extract_frames(file_name, starting_seconds, frames_range, save_path):

    print('File name :', file_name)
    print('Seconds to start dumping :', starting_seconds)
    print('Range of dumped frames :', frames_range)
    #########################################################################################################
    print(file_name)

    video = cv2.VideoCapture(file_name);

    # Find OpenCV version
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

    if int(major_ver) < 3:
        fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
    else:
        fps = video.get(cv2.CAP_PROP_FPS)

    video.release()
    ##########################################################################################################

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    vidcap = cv2.VideoCapture(file_name)
    count = 0
    while True:
        success, image = vidcap.read()
        if not success:
            break
        if ((fps * float(starting_seconds)) < count) and (
                (fps * float(starting_seconds) + float(frames_range)) > count):
            cv2.imwrite(  os.path.join( save_path , file_name + "frame{:d}.jpg".format(count) ), image  )
            print("img file: "+os.path.join( save_path , file_name + "frame{:d}.jpg".format(count) ))
        count += 1
    print("frames", count)

def main(argv):
    basepath = '.' + os.path.sep
    savepath = basepath + 'frames' + os.path.sep
    starting_seconds0 = ''
    frames_range0 = ''

    # Parse Passed Arguments
    try:
        opts, args = getopt.getopt(argv, "hs:f:d:", ["startingseconds=", "framesrange=","dir=",])
    except getopt.GetoptError:
        print('python test.py -s<starting_seconds> -f<frames_range> -d<dir (default ./)>')
        sys.exit(2)
    if len(sys.argv) != 3 and len(sys.argv) != 2:
        print("\nYou didn't give arguments! Run python <test.py> -h")
        sys.exit(0)
    for opt, arg in opts:
        if (opt == '-h'):
            print('python <test.py> -s<starting_seconds> -f<frames_range> -d<dir (default ./)>')
            sys.exit()
        elif opt in ("-s", "--startingseconds"):
            starting_seconds0 = arg
        elif opt in ("-f", "--framesrange"):
            frames_range0 = arg
        elif opt in ("-d", "--dir"):
            basepath = arg

    basepath += os.path.sep
    files_list = sorted(glob.glob(basepath + '*.mp4'), key=natural_key, reverse=False)
    
    for count, filename in enumerate(files_list):
        extract_frames( os.path.splitext(filename)[0], starting_seconds0, frames_range0, savepath)

if __name__ == "__main__":
   main(sys.argv[1:])
