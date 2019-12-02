#!/bin/bash
cd /python-env/mldriver-discrete-steering

pipenv run xvfb-run -a -s "-screen 0 128x128x24" -- python main.py --config config/mldriver.json