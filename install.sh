#!/usr/bin/env bash

mkdir -p $HOME/.local/bin/

ln -s $PWD/pyfetch.py $HOME/.local/bin/pyfetch
chmod +x $HOME/.local/bin/pyfetch
echo "Make sure to add ~/.local/bin to PATH"
