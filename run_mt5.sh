#!/bin/bash

# Start Xvfb
Xvfb :99 -screen 0 1024x768x16 &
export DISPLAY=:99

# Run MetaTrader 5 terminal using Wine
wine "C:\\Program Files\\MetaTrader 5\\terminal.exe"
