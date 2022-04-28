#!/bin/bash

maude maude/additional_modules/test.maude > logs/maude_log
python plot_tools/plot_maude_data.py
