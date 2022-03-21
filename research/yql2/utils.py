import os
import logging

def get_logger():
  logger = logging.getLogger("utils")
  logger.setLevel(logging.DEBUG)
  
  logHandler = logging.StreamHandler()
  logHandler.setFormatter(logging.Formatter(
    '[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt = "%Y-%m-%dT%H:%M:%S%z"
  ))
  logger.addHandler(logHandler)

  return logger

logger = get_logger() # package wide logger


def folder(x):
  """get the folder of this file path"""
  return os.path.split(os.path.abspath(x))[0]

def join(x, *args):
  """convienience function for os.path.join"""
  return os.path.join(x, *args)

def get_files_in_folder(folder, ext = ["proto"]):
  """Get files with ``ext`` in ``folder``"""
  # this method is faster than glob
  all_paths = []
  _all = "*" in ext # wildcard means everything so speed up

  for root,_,files in os.walk(folder):
    if _all:
      all_paths.extend([join(root, f) for f in files])
      continue

    for f in files:
      for e in ext:
        if f.endswith(e):
          all_paths.append(os.path.join(root,f))
  return all_paths
