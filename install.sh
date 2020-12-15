#!/usr/bin/env sh

# erzeugt Montag, 14. Dezember 2020 14:21 (C) 2020 von Leander Jedamus
# modifiziert Dienstag, 15. Dezember 2020 09:04 von Leander Jedamus
# modifiziert Montag, 14. Dezember 2020 14:22 von Leander Jedamus

autostart=$HOME/.config/autostart

modify_desktop_file()
{
  echo "installing $2"
  cat $1 | sed "s/USER/$USER/g" | sed "s/PRINTER/$3/g" > $2
};# modify_desktop_file

mkdir -p $autostart

cp -Rvp download-sortierer.py locale $HOME/bin
echo ""

modify_desktop_file download-sortierer.desktop $autostart/download-sortierer.desktop

# vim:ai sw=2

