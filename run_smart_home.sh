#!/bin/bash

maude maude/test.maude > logs/maude_log
python plot_tools/plot_maude_data.py
