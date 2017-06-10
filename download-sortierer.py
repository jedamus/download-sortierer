#!/usr/bin/env python3
# coding=utf8

# erzeugt Donnerstag, 08. Juni 2017 19:05 (C) 2017 von Leander Jedamus
# modifiziert Samstag, 10. Juni 2017 11:29 von Leander Jedamus
# modifiziert Freitag, 09. Juni 2017 20:49 von Leander Jedamus
# modifiziert Donnerstag, 08. Juni 2017 19:05 von Leander Jedamus

import pyinotify
import re

path_to_watch = "/home/leander/Downloads";

dict_regex_and_path = {
 path_to_watch + "/.*\.dmg": path_to_watch + "/dmg",
 path_to_watch + "/.*\.pkg": path_to_watch + "/dmg",
 path_to_watch + "/.*\.iso": path_to_watch + "/iso"
                      };

dict_compiled_regex_and_path = {};
for key in dict_regex_and_path:
  compiled_key = re.compile(key, re.UNICODE);
  dict_compiled_regex_and_path.update({ compiled_key: dict_regex_and_path[key] });

wm = pyinotify.WatchManager();  # Watch Manager
mask = pyinotify.IN_CLOSE_WRITE # watched events

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CLOSE_WRITE(self, event):
      pathname = event.pathname;
      for key in dict_compiled_regex_and_path:
        if key.match(pathname):
          print("moving ", pathname, " to ", dict_compiled_regex_and_path[key]);
          break;

handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch(path_to_watch, mask, rec=False);

notifier.loop()
