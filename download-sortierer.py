#!/usr/bin/env python3
# Notifier example from tutorial
#
# See: http://github.com/seb-m/pyinotify/wiki/Tutorial
# modifiziert Samstag, 10. Juni 2017 10:24 von Leander Jedamus
# modifiziert Freitag, 09. Juni 2017 20:49 von Leander Jedamus
#
# modifiziert Freitag, 09. Juni 2017 19:01 von Leander Jedamus
# modifiziert Donnerstag, 08. Juni 2017 19:05 von Leander Jedamus
import pyinotify
import re

class IncludeFilter(pyinotify.ExcludeFilter):
  def __call__(self, path):
    for regex in self._lregex:
      if self._match(regex, path):
        return False
    return True

path_to_watch = "/home/leander/Downloads";

incfilter = pyinotify.ExcludeFilter(["/tmp/download/test.*", "/tmp/download/*.iso"]);

dict_regex_and_path = {
 path_to_watch + "/.*\.dmg": "/home/leander/Downloads/dmg",
 path_to_watch + "/.*\.pkg": "/home/leander/Downloads/dmg",
 path_to_watch + "/.*\.iso": "/home/leander/Downloads/iso"
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
wdd = wm.add_watch(path_to_watch, mask, rec=False, exclude_filter=incfilter);

notifier.loop()
