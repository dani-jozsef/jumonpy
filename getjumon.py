#!/usr/bin/env python3
# coding: utf-8

# This script is a convenience installer to be used in the Pythonista3 iOS app

from functools import partial
import os
import requests
import shutil

URL = "https://github.com/dani-jozsef/jumonpy/archive/refs/heads/master.zip"
DOWNLOADTO = "Documents/jumonpy-master.zip"
TEMPDIR = "Documents/_tmp_jumonpy_master"
PACKAGEDIR = "jumonpy-master/jumon"
ADDITIONAL_FILES = [ 'jumonpy-master/LICENSE', 'jumonpy-master/iOS_launcher.py' ]
INSTALLDIR = "Documents/site-packages/jumon"

##

def postinst(install_path):
  homedir = os.path.join(os.environ['HOME'], 'Documents')
  # Create launcher symlink in home directory
  os.symlink(os.path.join(install_path, 'iOS_launcher.py'), os.path.join(homedir, 'jumonlauncher.py'))
  # Create jumonconfig.py in home directory if not already there
  config_path = os.path.join(homedir, 'jumonconfig.py')
  if not os.path.exists(config_path):
    shutil.copy2(os.path.join(install_path, 'jumonconfig_example.py'), config_path)
  # Symlink it to package directory
  os.symlink(config_path, os.path.join(install_path, 'jumonconfig.py'))

##

def _httpget_internal(url, dst):
  with requests.get(url, stream=True) as r:
    r.raw.read = partial(r.raw.read, decode_content=True)
    with open(dst, 'wb') as f:
      shutil.copyfileobj(r.raw, f)

def _alreadyexists(path):
  return FileExistsError(f"File or directory already exists: '{path}")

def install(
    url = URL,
    downloadto = DOWNLOADTO,
    tempdir = TEMPDIR,
    packagedir = PACKAGEDIR,
    additional_files = ADDITIONAL_FILES,
    installdir = INSTALLDIR):
  
  homedir = os.environ['HOME']
  download_path = os.path.join(homedir, downloadto)
  expand_path = os.path.join(homedir, tempdir)
  package_path = os.path.join(expand_path, packagedir)
  install_path = os.path.join(homedir, installdir)

  if os.path.exists(download_path):
    raise _alreadyexists(download_path)

  if os.path.exists(expand_path):
    raise _alreadyexists(expand_path)

  if os.path.exists(install_path):
    raise _alreadyexists(download_path)

  print(f"Attempting to download '{url}' to '{download_path}'")
  _httpget_internal(url, download_path)
  print(" done..")
  
  print(f"Attempting to unpack to '{expand_path}'")
  shutil.unpack_archive(download_path, expand_path)
  print(" done..")

  print(f"Attempting to install to '{install_path}'")
  shutil.move(package_path, install_path)
  for file in additional_files:
    file_path = os.path.join(expand_path, file)
    shutil.move(file_path, install_path)
  print(" done!")

  print(f"Attempting to remove '{download_path}' and '{expand_path}'")
  os.remove(download_path)
  shutil.rmtree(expand_path)
  print(" done..")

  print("Running post-install script..")
  postinst(install_path)

  print("Bye! <3")


if __name__ == "__main__":
  install()
