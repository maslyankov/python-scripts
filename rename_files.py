# Python 3 code to rename multiple
# files in a directory or folder's subdirectories
# Script uses arguments files located at each subdir - suffixes.txt
# Arg files should contain suffixes seperated by new line
# First line of arg files - "cases" will rename images with caseN name base, otherwise if for ex first line is "gosho" will rename files to gosho_...
# Second line (argument) specifies if we should start parsing files in ASCending (asc) or DESCending order (desc).

# importing modules
import logging, os, glob

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

# Function to go through the passed folder's subfolders
def go_through_subfolders(basepath):
    global cases_cont_from, files_last_list_len
    # TODO:
    # 1 Add functionality that checks subfolder names and takes that into account for case numbers

    child_dirs = glob.glob(os.path.join(basepath, "*", ""))
    print(child_dirs)


    for count, folder in enumerate(child_dirs):
        print("\nNow at fld:" + folder)

        # Go through the subfolders
        childs_child_dirs = glob.glob(os.path.join(folder, "*", ""))
        childs_child_dirs_count = len(child_dirs)

        print(cases_cont_from)

        print(files_last_list_len)

        if childs_child_dirs_count == count+1:
            print("Last subfolder!")
            cases_cont_from = files_last_list_len

        print(">>" + str(childs_child_dirs))

        # Iterate through subfolders
        for count_childs, folder_child in enumerate(childs_child_dirs):
            rename_files_in_dir(folder_child)


# Function to rename multiple files
def rename_files_in_dir(basepath):
    global cases_cont_from, files_last_list_len

    basepath += os.path.sep
    parentdir = os.path.dirname(os.path.dirname(basepath)) + os.path.sep
    logging.info("Parent Dir: \n" + str(parentdir) + "\n")

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logfile = os.path.dirname(parentdir) + os.path.sep + 'LogFile.txt' #TODO - Add folder name to log file name
    print("Log File:" + logfile)
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

    files_count = len(files_list)
    files_last_list_len = files_count if prefix == "cases" else 0

    if files_count != (len(SuffixesList)-ADDIT_SUFFIX_PARAMS):
        # Handle file/arguments inconsistencies
        print('Not enough files or suffixes!')
        print("Files:", files_count)
        print("Suffixes:", len(SuffixesList)-ADDIT_SUFFIX_PARAMS)
        logging.error("Files:" + str(files_count) + " | " + "Suffixes:" + str(len(SuffixesList)-ADDIT_SUFFIX_PARAMS) + "\n")
        return

    # Add prefix delimiter if not empty
    prefix_delim = "_" if prefix != "" else ""

    print("Beginning renaming in" + basepath + "\n")
    logging.info("Beginning renaming in" + basepath + "\n")

    # Iterate through the files in the dir
    for count, filename in enumerate(files_list):
        if SuffixesList[0].strip() == "cases":
            prefix = "case" + str(cases_cont_from + count + 1)

        dst = parentdir + prefix + prefix_delim + SuffixesList[count+ADDIT_SUFFIX_PARAMS].strip() + prefix_delim + os.path.basename(os.path.dirname(basepath)) +  ".jpg"
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
    # - Move them files to one folder afterwards

if __name__ == '__main__':
    # Calling main() function
    main()
