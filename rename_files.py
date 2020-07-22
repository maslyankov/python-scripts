# Pythono3 code to rename multiple
# files in a directory or folder

# importing modules
import logging, os, glob

# Constants
ADDIT_SUFFIX_PARAMS = 3

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

# Function to go through the passed folder's subfolders
def go_through_subfolders(basepath):
    # TODO:
    # 1 Add functionality that checks subfolder names and takes that into account for case numbers

    child_dirs = glob.glob(os.path.join(basepath, "*", ""))
    print(child_dirs)

    for count, folder in enumerate(child_dirs):
        print("\nNow at fld:" + folder)

        # Go through the subfolders
        childs_child_dirs = glob.glob(os.path.join(folder, "*", ""))
        print(">>" + str(childs_child_dirs))
        # rename_files_in_dir(folder)


# Function to rename multiple files
def rename_files_in_dir(basepath):
    basepath += os.path.sep

    logfile = basepath + 'LogFile' + '.txt' #TODO - Add folder name to log file name
    logging.basicConfig(filename=logfile, level=logging.DEBUG, format='%(asctime)s %(message)s')

    logging.info('-----------------------------')
    logging.info('Log started!')

    logging.info('Starting at dir: ' + basepath + "\n")

    # Try to open arguments file
    argsfile = basepath + "suffixes.txt"
    try:
        SuffixesList = open(argsfile).readlines()
    except OSError:
        print("Could not find or open/read args file:", argsfile)
        logging.error("Could not find or open/read args file:" + argsfile + "\n")
        return

    prefix = SuffixesList[0].strip()
    order = SuffixesList[1].strip()
    logging.info("Suffixes List: \n" + str(SuffixesList) + "\n")

    files_list = sorted(glob.glob(basepath + '*.jpg'), key = natural_key, reverse = False if order == "asc" else True)
    logging.info("Files List: \n" + str(files_list) + "\n")

    if len(files_list) != (len(SuffixesList)-ADDIT_SUFFIX_PARAMS):
        # Handle file/arguments inconsistencies
        print('Not enough files or suffixes!')
        print("Files:", len(files_list))
        print("Suffixes:", len(SuffixesList)-ADDIT_SUFFIX_PARAMS)
        logging.error("Files:" + str(len(files_list)) + " | " + "Suffixes:" + str(len(SuffixesList)-ADDIT_SUFFIX_PARAMS) + "\n")
        return

    # Add prefix delimiter if not empty
    prefix_delim = "_" if prefix != "" else ""

    print("Beginning renaming in" + basepath + "\n")
    logging.info("Beginning renaming in" + basepath + "\n")

    # Iterate through the files in the dir
    for count, filename in enumerate(files_list):
        if SuffixesList[0].strip() == "cases":
            prefix = "case" + str(count+1)

        dst = basepath + prefix + prefix_delim + SuffixesList[count+ADDIT_SUFFIX_PARAMS].strip() + ".jpg"
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
    # Calling rename_files_in_dir() function
    path = input("Enter directory path (press enter for current dir) : ") or './'
    print("\nI got: " + path + "\n")

    go_through_subfolders(path)

    # TODO:
    # 2 Move them files to one folder afterwards

if __name__ == '__main__':
    # Calling main() function
    main()
