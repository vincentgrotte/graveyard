#!/bin/bash
WORK_DIR=$(pwd)
echo "[***] Installing devmode from $WORK_DIR"
VARIABLES_FILE="$WORK_DIR/_variables.py"

if [ "$1" = "" ]; then
    echo "[***] Use: ./install.sh \"path/to/target\""
else
    echo "[***] Target angular project src directory: $TARGET_DIR"
    NOT_INSTALLED=$(grep "\# \[\*\] Install Points" "$WORK_DIR/_variables.py")
    if [ "$NOT_INSTALLED" = "" ]; then
        echo "[***] _variables file has already been edited."
        echo "[***] If something is broken, consider looking at _variables.py"
    else
        COMMENT="\(# \[\*] Install Points -- Run install.sh\)"
        SOURCE="\(# \[\*] _SOURCE\)"
        TARGET="\(# \[\*] _TARGET\)"
        COMMENT_INSTALLED="\# \[\*\*\*] \_SOURCE and \_TARGET were generated by \"install.sh\""
        SOURCE_INSTALLED="\_SOURCE = \"$WORK_DIR\""
        TARGET_INSTALLED="\_TARGET = \"$1\""
        sed -i '' "s,$COMMENT,$COMMENT_INSTALLED," $VARIABLES_FILE
        sed -i '' "s,$SOURCE,$SOURCE_INSTALLED," $VARIABLES_FILE
        sed -i '' "s,$TARGET,$TARGET_INSTALLED," $VARIABLES_FILE
    fi
    PYTHON3INSTALL=$(which python3)
    if [ "$PYTHON3INSTALL" = "" ]; then
        brew install python3
    else
        echo "[***] python3 already installed at $PYTHON3INSTALL"
    fi
    echo "[***] Force symlink from \"$WORK_DIR/devmode.py\" to \"/usr/local/bin/devmode\""
    ln -sF "$WORK_DIR/devmode.py" "/usr/local/bin/devmode"
fi
echo "[***] Done."



