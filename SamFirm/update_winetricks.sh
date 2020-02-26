#!/bin/sh
# update_winetricks

wget https://raw.githubusercontent.com/Winetricks/winetricks/master/src/winetricks
wget https://raw.githubusercontent.com/Winetricks/winetricks/master/src/winetricks.bash-completion
chmod +x winetricks
sudo mv winetricks /usr/bin ; sudo mv winetricks.bash-completion /usr/share/bash-completion/completions/winetricks

chmod +x update_winetricks
sudo mv update_winetricks /usr/bin/
