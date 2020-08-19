# Python 3 code to rename multiple
# files in a directory or folder's subdirectories
# Script uses arguments files located at each subdir - suffixes.txt
# Arg files should contain suffixes seperated by new line
# First line of arg files - "cases" will rename images with caseN name base, otherwise if for ex first line is "gosho" will rename files to gosho_...
# Second line (argument) specifies if we should start parsing files in ASCending (asc) or DESCending order (desc).

# importing modules
import logging, os, glob, sys, getopt

# Constants
ADDIT_SUFFIX_PARAMS = 3

# Globals
cases_cont_from = 0
files_last_list_len = 0


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

# Function to rename multiple files
def rename_files_in_dir(basepath, beg_with, ext):
    global cases_cont_from, files_last_list_len

    basepath += os.path.sep

    print("Basepath is: " + basepath)
    print("arg0 is: " + sys.argv[0])

    i = 1
    while os.path.exists("case%s.mp4" % i):
        i += 1
    cases_cont_from = i-1
    
    print("Cont from: " + str(cases_cont_from))
    
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logfile = basepath + 'renaming.log' #TODO - Add folder name to log file name
    print("Log File:" + logfile)
    logging.basicConfig(filename=logfile, level=logging.DEBUG, format='%(asctime)s %(message)s')

    logging.info('-----------------------------')
    logging.info('Log started!')

    logging.info('Starting at dir: ' + basepath + "\n")

    files_list = sorted(glob.glob(basepath + beg_with +'*.' + ext), key = natural_key, reverse = False)
    logging.info("Files List: \n" + str(files_list) + "\n")

    files_count = len(files_list)
    files_last_list_len = files_count

    if files_count == 0:
        print("No new files found! Terminating...")
        logging.info("No new files found! Terminating...")
        return
    

    print("Beginning renaming in " + basepath + "\n")
    logging.info("Beginning renaming in " + basepath + "\n")

    # Iterate through the files in the dir
    for count, filename in enumerate(files_list):
        prefix = "case" + str(cases_cont_from + count + 1)

        dst = basepath + prefix + "." + ext
        src = filename

        # rename() function will
        # try to rename all the files one by one
        try:
            os.rename(src, dst)
            logging.info("Renaming file: " + src + " -> " + dst)
        except OSError:
            print("Files with those names already exist! Aborting!")
            logging.error("Files with those names already exist! Aborting!\n")
            return
    logging.info("Done with this folder.\n")

def main():
    # Set defaults
    begins_with = "VID"
    extension = "mp4"

    # list of command line arguments
    path_arg = sys.argv[1]
    begins_with = sys.argv[2]
    extension = sys.argv[3]

    try:
        path_arg
    except NameError:
        path = "."
    else:
        path = "." + os.path.sep + path_arg

    print("Path -> " + path + " begins with -> " + begins_with + " Ext -> " + extension)

        # Calling rename_files_in_dir() function
    #path = input("Enter directory path (press enter for current dir) : ") or '.'
    #print("\nI got: " + path + "\n")
    rename_files_in_dir(path, begins_with, extension)

    # TODO:
    # - Move them files to one folder afterwards

if __name__ == '__main__':
    # Calling main() function
    main()
