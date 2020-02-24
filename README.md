# samsung-firmware-bot

## SamFirm Configuration
- Install wine and winetricks
- Run the following
```shell script
WINEARCH=win32 WINEPREFIX=~/.wine wine wineboot
winetricks -q dotnet48
winetricks -q vcrun2008
winetricks -q vcrun2010
```
