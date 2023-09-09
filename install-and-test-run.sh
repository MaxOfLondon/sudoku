#! /bin/bash

# Usage:
# chmod +x ./install-and-test-run.sh
# # for development:
# source ./install-and-test-run.sh dev
# # for production:
# source ./install-and-test-run.sh
# # or for production:
# source ./install-and-test-run.sh prod

DEFAULT_ENV="prod"
PROCEED_ENV=$1
PROCEED_ENV="${PROCEED_ENV:-${DEFAULT_ENV}}"
echo "requirements/$PROCEED_ENV.txt"
[[ -f "requirements/$PROCEED_ENV.txt" ]] || {
    echo -e "\033[31m[!] Invalid parameter specified, valid values [dev/prod]\033[0m"
    exit 2
}


confirm() {
    DEFAULT="y"
    echo -e "\033[32m"
    read -e -p "$* " PROCEED
    echo -e "\033[0m\n"
    PROCEED="${PROCEED:-${DEFAULT}}"
    [[ $PROCEED = [Yy] ]]
}

# cleanup
in_venv=$(python3 -c 'import sys; print ("1" if hasattr(sys, "real_prefix") else "0")')

[[ $in_venv ]] && deactivate
[ -d .venv ] && rm -rf .venv
[ -d src/build ] && rm -rf src/build
[ -d src/sudoku/__pycache__ ] && rm -rf src/sudoku/__pycache__

# install dependencies
python3 -m pip install --user virtualenv
virtualenv -q -p /usr/bin/python3 .venv
source .venv/bin/activate
pip install -r "requirements/$PROCEED_ENV.txt"

# run
cd src
confirm '[+] Run main.py without pygbag? (Y/n)' && python3 main.py

confirm '[+] Run main.py with pygbag? (Y/n)' && {
    relative_pwd=${PWD##*/}
    pygbag --ume_block=0 ../$relative_pwd &>/dev/null &
    pid=$!
    echo -ne "\033[32m"; printf "=%.0s" {1..80}; echo -e "\033[0m"
    echo -e "\033[32m[+]\033[0m Launch in browser:\033[32m xdg-open http://localhost:8000 \033[0m"
    echo -e "\033[32m[+]\033[0m After testing press ENTER then kill pygbag with:\033[32m kill $pid \033[0m"
    echo -ne "\033[32m"; printf "=%.0s" {1..80}; echo -e "\033[0m\n"
}
