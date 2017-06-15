#!/usr/bin/env python3
# coding=utf8

# erzeugt Donnerstag, 08. Juni 2017 19:05 (C) 2017 von Leander Jedamus
# modifiziert Freitag, 16. Juni 2017 00:51 von Leander Jedamus
# modifiziert Montag, 12. Juni 2017 18:47 von Leander Jedamus
# modifiziert Samstag, 10. Juni 2017 12:07 von Leander Jedamus
# modifiziert Freitag, 09. Juni 2017 20:49 von Leander Jedamus
# modifiziert Donnerstag, 08. Juni 2017 19:05 von Leander Jedamus

import os
import pyinotify
import re

home = os.environ["HOME"];
path_to_watch = home + "/" + "Downloads";

dict_suffix_and_path = {
  "dmg":       "dmg",
  "pkg":       "dmg",
  "iso":       "iso",
  "zip":       "zip",
  "deb":       "deb",
  "pdf":       home + "/" + "Documents" + "/" + "pdf" + "/" + "download PDFs",
  "tar.gz":    "tgz",
  "tar.xz":    "tgz",
  "tar.bzip2": "tgz",
  "a.b.c.d":   "abcd",
};

dict_compiled_regex_and_path = {};
for key in dict_suffix_and_path:
  suffix = re.sub("[.]","[.]",key);
  path = dict_suffix_and_path[key];
  if path[0] != "/":
    path = path_to_watch + "/" + path;
  regex = path_to_watch + "/" + ".*" + suffix;
  compiled_key = re.compile(regex, re.UNICODE);
  dict_compiled_regex_and_path.update({ compiled_key: [suffix, path] });

wm = pyinotify.WatchManager();  # Watch Manager
mask = pyinotify.IN_CLOSE_WRITE # watched events

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CLOSE_WRITE(self, event):
      pathname = event.pathname;
      for key in dict_compiled_regex_and_path:
        if key.match(pathname):
          new_path = dict_compiled_regex_and_path[key][1];
          suffix = dict_compiled_regex_and_path[key][0];
          print(new_path);
          print(suffix);
          if not os.access(new_path, os.F_OK | os.X_OK):
            os.makedirs(new_path);
          filename = re.sub(".*/(.*[.].*)","\g<1>",pathname);
          os.rename(pathname, new_path + "/" + filename);
          break;

handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch(path_to_watch, mask, rec=False);

notifier.loop()

# vim:ai sw=2 sts=4 expandtab

