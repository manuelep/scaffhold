#!/usr/bin/env bash

: s'

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

TODO:
  - https://stackoverflow.com/a/246128/1039510
'

version="1.0"
tag="R-2.18.5"
clean="y"

# Getting script options
while [[ "$1" =~ ^- && ! "$1" == "--" ]]; do case $1 in
  -V | --version )
    echo $version
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
esac; shift; done
if [[ "$1" == '--' ]]; then shift; fi

SRC="https://github.com/web2py/web2py.git"
scaffhold="welcome"

echo "1. [MSG] Cloning repo $SRC"
git clone $SRC tmp

cd tmp

if [[ -n $tag ]]; then
    echo "2. [MSG] Moving to tagged commit: $tag"
    git checkout tags/$tag
fi

mv applications/$scaffhold ../
echo "[MSG] 3. Scaffhold application extracted"
cd -
if [[ $clean == "y" ]]; then
    rm -rf tmp
fi
echo "[MSG] 3.1. Removed repo for filesystem cleaning purposes"

cd $scaffhold
git init
git add .
git commit -am "welcome $tag"
git tag -a v0.0.1 -m "welcome $tag"
cd -
echo "[MSG] 7. New repository initialized"

echo "[MSG] 5. and 6. From welcome to my scaffholding app"
if [[ -d resources ]]; then
    rsync -av resources/* $scaffhold/
    cd $scaffhold
    git add .
    git commit -am "scaffhold"
    git tag -a v0.0.2 -m "scaffhold"
fi

echo "[MSG] Updating remote repository"
if [[ -n $repo ]]; then
    git remote add origin $repo
    git push -u origin master
fi

cd -

if [[ -n $name ]]; then
    echo "[MSG] Renaming project to $name"
    mv $scaffhold $name
fi
