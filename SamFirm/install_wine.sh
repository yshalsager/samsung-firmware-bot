#!/bin/sh
sudo dpkg --add-architecture i386 
wget -nc https://dl.winehq.org/wine-builds/winehq.key
sudo apt-key add winehq.key
sudo apt-get update
sudo apt install --install-recommends winehq-stable
