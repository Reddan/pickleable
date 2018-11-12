import tempfile
import os
import shutil
from io import BytesIO
from copy import copy
from subprocess import call
from pathlib import Path
from random import random

def ensure_dir(directory):
  if not os.path.exists(directory):
    try:
      os.makedirs(directory)
    except OSError as e:
      if e.errno != os.errno.EEXIST:
        raise

def get_tmp_path():
  tmp_dir = tempfile.gettempdir()
  destination = 'tmp' + str(random())[2:]
  return tmp_dir + '/' + destination

def get_tmp_directory():
  dir_path = get_tmp_path() + '/'
  os.makedirs(dir_path)
  return dir_path

def read_bytes(path):
  with open(path, 'rb') as file:
    return BytesIO(file.read())

def write_bytes(path, data):
  with open(path, 'wb') as file:
    file.write(data)

def path_to_byte_map(path):
  p = Path(path)
  if p.is_file():
    return read_bytes(path)
  else:
    sub_paths = [x.name for x in p.iterdir() if x.name not in ['.DS_Store', 'thumbs.db']]
    return {
      sub_path: path_to_byte_map(path + '/' + sub_path)
      for sub_path in sub_paths
    }

def byte_map_to_files(path, byte_map):
  if not isinstance(byte_map, dict):
    data = copy(byte_map).read()
    dir = '/'.join(path.split('/')[:-1])
    ensure_dir(dir)
    write_bytes(path, data)
  else:
    for sub_path in byte_map:
      byte_map_to_files(path + '/' + sub_path, byte_map[sub_path])

class BinaryWrapper:
  def __init__(self):
    self.tmp_dir = get_tmp_directory()

  def __enter__(self):
    return self

  def __exit__(self, *_):
    self.byte_map = path_to_byte_map(self.tmp_dir)
    shutil.rmtree(self.tmp_dir)
    self.tmp_dir = None

  def unwrap(self):
    return BinaryUnwrapper(self.byte_map)

class BinaryUnwrapper:
  def __init__(self, byte_map):
    self.tmp_dir = get_tmp_directory()
    self.byte_map = byte_map

  def __enter__(self):
    byte_map_to_files(self.tmp_dir, self.byte_map)
    return self.tmp_dir

  def __exit__(self, *_):
    try:
      shutil.rmtree(self.tmp_dir)
    except FileNotFoundError:
      pass
