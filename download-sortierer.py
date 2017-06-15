#!/usr/bin/env python
# coding=utf8

# erzeugt Donnerstag, 08. Juni 2017 19:05 (C) 2017 von Leander Jedamus
# modifiziert Freitag, 16. Juni 2017 01:30 von Leander Jedamus
# modifiziert Montag, 12. Juni 2017 18:47 von Leander Jedamus
# modifiziert Samstag, 10. Juni 2017 12:07 von Leander Jedamus
# modifiziert Freitag, 09. Juni 2017 20:49 von Leander Jedamus
# modifiziert Donnerstag, 08. Juni 2017 19:05 von Leander Jedamus

import os
import sys
import pyinotify
import pynotify
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

if not pynotify.init("Download-Sortierer"):
  sys.exit(1);

dict_compiled_regex_and_path = {};
for key in dict_suffix_and_path:
  suffix = re.sub("[.]","[.]","." + key);
  path = dict_suffix_and_path[key];
  if path[0] != "/":
    path = path_to_watch + "/" + path;
  regex = path_to_watch + "/" + ".*" + suffix;
  compiled_key = re.compile(regex, re.UNICODE);
  dict_compiled_regex_and_path.update({ compiled_key: [key, suffix, path] });

wm = pyinotify.WatchManager();  # Watch Manager
mask = pyinotify.IN_CLOSE_WRITE # watched events

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CLOSE_WRITE(self, event):
      pathname = event.pathname;
      for key in dict_compiled_regex_and_path:
        if key.match(pathname):
          new_path = dict_compiled_regex_and_path[key][2];
          suffix_regex = dict_compiled_regex_and_path[key][1];
          suffix = dict_compiled_regex_and_path[key][0];

          print(new_path);
          print(suffix_regex);
          print(suffix);
          if not os.access(new_path, os.F_OK | os.X_OK):
            os.makedirs(new_path);
          filename = re.sub(".*/(.*" + suffix_regex + ")","\g<1>",pathname);
          filename_without_suffix = re.sub("(.*)" + suffix_regex,"\g<1>",
                                           filename);
          print(filename);
          print(filename_without_suffix);

          new_filename = new_path + "/" + filename;
          if os.access(new_filename, os.F_OK):
            for i in range(2,99):
              new_filename = filename_without_suffix + "({i:02d})".format(i=i) \
                + "." + suffix;
              if not os.access(new_path + "/" + new_filename, os.F_OK):
                break;
          n = pynotify.Notification("Download-Sortierer",
                "Moved {filename:s} from {frompath:s} to {topath:s} as {newfile:s}".format(filename=filename, frompath=path_to_watch, topath=new_path, newfile=new_filename));
          if not n.show():
            print("Failed to send notification");
          os.rename(pathname, new_path + "/" + new_filename);
          break;

handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch(path_to_watch, mask, rec=False);

notifier.loop()

# vim:ai sw=2 sts=4 expandtab

