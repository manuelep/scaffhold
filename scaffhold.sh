#!/usr/bin/env bash

: '

1. Clone a web2py repository
2. Checkout to the desidered version
3. Extract the scaffholding welcome application

4. Rename application (-)
5. Substitute some file:
    - db.py
    - appconfig.template.ini
6. Add some usefull file:
    - .gitignore
7. init the local new git repository
8. update the remote repository (if given)
'

version="1.0"
tag="R-2.18.5"
clean="y"
name="scaffhold"

Help() {
    # Display Help
    echo "-V --version : Prints the script version and exit;"
    echo "-h --help : Prints this help and exit;"
    echo "-t --tag [TAG] : The tag name of network checkout (default: $tag);"
    echo "-n --name [NAME] : The name of the resulting application (default: %name);"
    echo "-r --repo [URL] : URL of the repo destination (OPTIONAL);"
}

# Getting script options
while [[ "$1" =~ ^- && ! "$1" == "--" ]]; do case $1 in
  -V | --version )
    echo "Script version: $version"
    exit ;;
  -h | --help )
    Help
    exit
    ;;
  -t | --tag )
    shift; tag=$1
    ;;
  -n | --name )
    shift; name=$1
    ;;
  -l | --leave )
    clean="n"
    ;;
  -r | --repo )
    repo=$1
    ;;
  * )
    echo "ERROR! Invalid option: $1"
    exit ;;
esac; shift; done
if [[ "$1" == '--' ]]; then shift; fi

# Courtesy of: https://stackoverflow.com/a/246128
SCRIPT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

SRC="https://github.com/web2py/web2py.git"
welcome="welcome"

echo "1. [MSG] Cloning repo $SRC"
git clone $SRC tmp

cd tmp

if [[ -n $tag ]]; then
    echo "2. [MSG] Moving to tagged commit: $tag"
    git checkout tags/$tag
fi

mv applications/$welcome ../$name
echo "[MSG] 3. Scaffhold application extracted"
cd -
if [[ $clean == "y" ]]; then
    rm -rf tmp
fi
echo "[MSG] 3.1. Removed repo for filesystem cleaning purposes"

cd $name
git init
git add .
git commit -am "welcome $tag"
git tag -a v0.0.1 -m "welcome $tag"
cd -
echo "[MSG] 7. New repository initialized"

echo "[MSG] 5. and 6. From welcome to my scaffholding app"
resources="$SCRIPT_PATH/resources"
if [[ -d $resources ]]; then
    rsync -av $resources/ $name/
    cd $name
    git add .
    git commit -am "scaffhold"
    git tag -a v0.0.2 -m "scaffhold"

    echo "[MSG] Updating remote repository"
    if [[ -n $repo ]]; then
        git remote add origin $repo
        git push -u origin master
    fi

    cd -
else
    echo "[WARNING] $resources NOT found"
fi
