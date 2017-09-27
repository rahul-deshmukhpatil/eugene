#!/bin/bash
dirName=`dirname $0`
cd $dirName
cd ..
git pull --no-edit origin master
