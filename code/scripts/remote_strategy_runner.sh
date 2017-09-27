#!/bin/bash
dirName=`dirname $0`
cd $dirName
cd ../strategy_runner
python -B ./strategy_runner.py "$@" 
