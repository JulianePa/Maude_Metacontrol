#!/bin/bash

maude maude/additional_modules/test.maude > logs/maude_log
python3 plot_tools/plot_maude_data.py
