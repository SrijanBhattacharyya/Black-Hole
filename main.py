##################################################
### Importing Libraries and Defining Variables ###
##################################################

import os

mainDir = os.path.abspath (os.path.dirname (__file__))
manFile = os.path.join (mainDir, 'manual.txt')

import setup
setup.main (mainDir)

from github import Github
from google.colab import drive
import json, sys

app_data_file = os.path.join (mainDir, "app-dat.json")
trial = 0


#########################
### Default Functions ###
#########################

def print_error (error: str):
    print (f"\033[38;2;255;0;0;1m[-] {error}\033[0m")

def print_success (succ: str):
    print (f"\033[38;2;0;255;0;1m[-] {succ}\033[0m")

def print_dict (d: dict):
    print (json.dumps (d, indent = 4))

def show_help ():
    with open (manFile) as f:
        print (f.read)

    exit ()

def get_wd () -> (str|None):
    try:
        arg = sys.argv [1]

        if arg [0] == '-':
            if (arg.lower () == '-h') or (arg.lower () == '-help'): show_help ()
            else: print_error ("FlagNotFoundError: Flag not mentioned in the system.")

        if arg [0] != '-':
            if "/" not in arg: ret = os.path.join (os.getcwd (), arg)
            else: ret = arg

    except IndexError: show_help ()
    return ret


################################
### Function to Get App Data ###
################################

def get_app_data () -> dict:
    with open (app_data_file) as f:
        return dict (json.load (f))


##################################
### Check if Repository Exists ###
##################################

def check_repo_exists () -> bool:
    usr = git.get_user ()

    try:
        repo = usr.get_repo (app_data ['repo-name'])
        return True

    except:
        if trial < 5:
            usr.create_repo (app_data ['repo-name'])
            trial += 1
            return check_repo_exists ()

        else: return False


#############################################
### Function to Add to a Given Repository ###
#############################################

def add_to_repo (filePath: str, fileContent: str or list) -> bool:
    repo = git.get_repo (f"{app_data ['user-name']}/{app_data ['repo-name']}")

    try:
        contents = repo.get_contents (filePath)
        print_error (f"FileExistsError: File '{filePath}' already exists in the repository.")
        return False

    except: pass

    try:
        if isinstance (fileContent, str):
            fileContent = fileContent.encode('utf-8')

        repo.create_file (filePath, f"Add {filePath}", fileContent, branch = "main")
        return True

    except Exception as e:
        print_error (e)
        return False


################################
### Function to Get App Data ###
################################

def get_files_description (path: os.path) -> dict:
    list_dir = os.listdir (path)
    data = {}

    for elem in list_dir:
        elem = os.path.join (path, elem)

        if not os.path.isdir (elem):
            with open (elem, "r") as data_file:
                data [elem] = data_file.read ()

    return data


#####################
### Main Function ###
#####################

def main ():
    global app_data, git

    app_data = get_app_data ()
    git = Github (app_data ["auth-token"])
    wd = get_wd ()
    print (wd)
    files_description = get_files_description (wd)

    if check_repo_exists ():
        for fp, cont in files_description.items ():
            if fp != "FILE-PATH":
                if add_to_repo (fp, cont):
                    print_success (f"Successfully file uploaded to the path '{fp}'.")

    else: print_error ("Jani na ki holo !")

if __name__ == "__main__":
    main ()
