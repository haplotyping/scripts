#/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
(cd $SCRIPT_DIR &&  python constructDatabase.py && eval $1)
