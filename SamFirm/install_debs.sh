#!/bin/sh
WINEARCH=win32 WINEPREFIX=~/.wine wine wineboot
DISPLAY=:1 winetricks -q dotnet48 vcrun2008 vcrun2010
