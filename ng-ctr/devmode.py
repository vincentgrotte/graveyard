#!/usr/local/bin/python3
import os, shutil, subprocess, sys
try:
    import _variables
except:
    print("[***] devmode hasn't been installed or configured for a project yet.")
    print("[***] Please run \"/path/to/devmode/dir/install.sh\" \"path/to/angular/src/dir\"")
    sys.exit()
command = _variables.Command()
environment = _variables.Environment()
injection = _variables.Injection()
INVALID_OPTION = "Invalid option"

def main():
    commands = {
        command.inject : inject,
        command.remove : remove,
        command.save : save,
        command.test : test,
    }
    action = commands.get(sys.argv[1], INVALID_OPTION)
    if (action != INVALID_OPTION):
        action()
    else:
        print("[***] " + str(action) + " is " + INVALID_OPTION)
    print("[***] Done.")

def inject():
    remove() # Clean first
    _tryDo(_putLineTop, [environment.TARGET_MODULE, injection.IMPORT_LINE])
    _tryDo(_putLineAfter, [environment.TARGET_MODULE, injection.CLASS_NAME_LINE, injection.MODULE_PREDICATES])
    _tryDo(_putLineAfter, [environment.TARGET_HTML, injection.HTML_TAG, injection.HTML_PREDICATE])
    print("[***] Injecting component and asset files.")
    _tryDo(shutil.copytree, [environment.SOURCE_COMPONENT, environment.TARGET_COMPONENT])
    _tryDo(shutil.copytree, [environment.SOURCE_ASSETS, environment.TARGET_ASSETS])

def remove():
    _tryDo(_removeLines, [environment.TARGET_MODULE, injection.CLASS_NAME])
    _tryDo(_removeLines, [environment.TARGET_HTML, injection.HTML_TAG])
    print("[***] Removing component and asset files")
    _tryDo(shutil.rmtree, [environment.TARGET_COMPONENT])
    _tryDo(shutil.rmtree, [environment.TARGET_ASSETS])

def save():
    # TODO make safe (rollback operation if it fails)
    print("[***] Overwriting source component and asset files with changes from project.")
    _tryDo(shutil.rmtree, [environment.SOURCE_COMPONENT])
    _tryDo(shutil.rmtree, [environment.SOURCE_ASSETS])
    _tryDo(shutil.copytree, [environment.TARGET_COMPONENT, environment.SOURCE_COMPONENT])
    _tryDo(shutil.copytree, [environment.TARGET_ASSETS, environment.SOURCE_ASSETS])

def test():
    print("[***] devmode test works")

# [***] Utility functions

def _putLineAfter(PATH, INJECTION, PREDICATES):
    with open(PATH, "r+") as file:
        lines = file.readlines()
        file.seek(0)
        for x, line in enumerate(lines):
            file.write(line)
            for predicate in PREDICATES:
                if line.__contains__(predicate):
                    file.write(INJECTION)
                    file.write("\n")
                    print("[***] Inserted \"" + INJECTION + "\" at line " + str(x) + " of " + file.name)

def _putLineTop(PATH, INJECTION):
    with open(PATH, "r+") as file:
        lines = [INJECTION , "\n"] + file.readlines()
        file.seek(0)
        for line in lines:
            file.write(line)
        print("[***] Inserted \"" + INJECTION + "\" at line 0 of " + file.name)

def _removeLines(PATH, PREDICATE):
    print("[***] Removing lines containing \"" + PREDICATE + "\" from " + PATH)
    with open(PATH, "r+") as file:
        lines = file.readlines()
        file.seek(0)
        for x, line in enumerate(lines):
            if PREDICATE in line:
                print("[***] Removed line " + str(x))
            else:
                file.write(line)
        file.truncate()

def _tryDo(FUNCTION, ARGS):
    try:
        FUNCTION(*ARGS)
    except Exception as e:
        print("[***] Applying " + str(ARGS) + " to " + str(FUNCTION) + " failed with")
        print("[***] -- Exception: " + str(e))

if __name__ == "__main__":
    main()

