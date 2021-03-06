#!/bin/bash
cd /python-env/A2C

while getopts ":c:e:" opt; do
  case $opt in
    c)
      pipenv run xvfb-run -a -s "-screen 0 128x128x24" -- python main.py --config experiments/$OPTARG
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done