#!/usr/bin/env python
# coding=utf8

# erzeugt Donnerstag, 08. Juni 2017 19:05 (C) 2017 von Leander Jedamus
# modifiziert Donnerstag, 22. Juni 2017 17:20 von Leander Jedamus
# modifiziert Freitag, 16. Juni 2017 01:57 von Leander Jedamus
# modifiziert Montag, 12. Juni 2017 18:47 von Leander Jedamus
# modifiziert Samstag, 10. Juni 2017 12:07 von Leander Jedamus
# modifiziert Freitag, 09. Juni 2017 20:49 von Leander Jedamus
# modifiziert Donnerstag, 08. Juni 2017 19:05 von Leander Jedamus

import os
import sys
import pyinotify
import pynotify
import re
import gettext
import logging

home = os.environ["HOME"]
path_to_watch = os.path.join(home,"Downloads")
log_path_and_filename = os.path.join("/tmp","download-sortierer.log")

dict_suffix_and_path = {
  "dmg":       os.path.join("MacOS","dmg"),
  "pkg":       os.path.join("MacOS","dmg"),
  "iso":       "iso",
  "zip":       "zip",
  "deb":       "deb",
  "pdf":       os.path.join(home,"Documents","pdf","download PDFs"),
  "tgz":       "tgz",
  "tar.gz":    "tgz",
  "tar.xz":    "tgz",
  "tar.bzip2": "tgz",
  "a.b.c.d":   "abcd",
};

file_handler = logging.FileHandler(log_path_and_filename)
stdout_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s",
                              "%d.%m.%Y %H:%M:%S")
file_handler.setFormatter(formatter)
stdout_handler.setFormatter(formatter)
log = logging.getLogger()
log.addHandler(file_handler)
log.addHandler(stdout_handler)
log.setLevel(logging.INFO)

scriptpath = os.path.abspath(os.path.dirname(sys.argv[0]))
try:
  trans = gettext.translation("download-sortierer.py",os.path.join(scriptpath, \
                                                       "translate"))
  trans.install(unicode=True)
except IOError:
  log.error("Fehler in gettext")
  def _(s):
    return s

if not pynotify.init(_("Download-Sorter")):
  log.critical(_("Can't initialize pynotify"))
  sys.exit(1);

dict_compiled_regex_and_path = {}
for key in dict_suffix_and_path:
  suffix = re.sub("[.]","[.]","." + key)
  path = dict_suffix_and_path[key]
  log.debug(_("path = {path:s}").format(path=path))
  if path[0] != "/":
    path = os.path.join(path_to_watch,path)
  regex = os.path.join(path_to_watch,".*" + suffix);
  compiled_key = re.compile(regex, re.UNICODE)
  dict_compiled_regex_and_path.update({ compiled_key: [key, suffix, path] })

wm = pyinotify.WatchManager();  # Watch Manager
mask = pyinotify.IN_CLOSE_WRITE # watched events

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CLOSE_WRITE(self, event):
      pathname = event.pathname
      for key in dict_compiled_regex_and_path:
        if key.match(pathname):
          new_path = dict_compiled_regex_and_path[key][2]
          suffix_regex = dict_compiled_regex_and_path[key][1]
          suffix = dict_compiled_regex_and_path[key][0]

          log.debug(_("new_path = {new_path:s}").format(new_path=new_path))
          log.debug(_("suffix_regex = {suffix_regex:s}").format(suffix_regex=suffix_regex))
          log.debug(_("suffix = {suffix:s}").format(suffix=suffix))
          if not os.access(new_path, os.F_OK | os.X_OK):
            try:
              os.makedirs(new_path)
            except OSError:
              log.error(_("Can't create dirs {dirs:s}").format(dirs=new_path))
              break
          filename = re.sub(os.path.join(".*","(.*") + suffix_regex + ")",
            "\g<1>",pathname)
          filename_without_suffix = re.sub("(.*)" + suffix_regex,"\g<1>",
                                           filename)
          log.debug(_("filename = {filename:s}").format(filename=filename))
          log.debug(_("filename_without_suffix = {filename_without_suffix:s}").format(filename_without_suffix=filename_without_suffix))

          new_filename = os.path.join(new_path,filename)
          if os.access(new_filename, os.F_OK):
            for i in range(2,99):
              new_filename = filename_without_suffix + "({i:02d})".format(i=i) \
                + "." + suffix;
              if not os.access(os.path.join(new_path,new_filename), os.F_OK):
                break;
          try:
            os.rename(pathname, os.path.join(new_path,new_filename))
            message = _("Moved {filename:s} from {frompath:s} to {topath:s} as {newfile:s}").format(filename=filename, frompath=path_to_watch, topath=new_path, newfile=new_filename)
            n = pynotify.Notification(_("Download-Sorter"), message)
            log.info(message)

            if not n.show():
              log.error(_("Failed to send notification"))
            break;
          except OSError:
            log.error(_("Can't move file {filename:s} from {frompath:s} to {topath:s} as {newfile:s}").format(filename=filename, frompath=path_to_watch, topath=new_path, newfile=new_filename))

handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch(path_to_watch, mask, rec=False)

notifier.loop()

# vim:ai sw=2 sts=4 expandtab

