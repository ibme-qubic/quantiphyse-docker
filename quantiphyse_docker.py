#!/usr/bin/env python
"""
Simple wrapper script for docker run for Quantiphyse application
  - Passes DISPLAY settings to allow GUI display
  - Passes FSLDIR and FSLDEVDIR environment and maps the corresponding 
    folders, if set
  - Parses the config file $HOME/.quantiphyse-docker and maps folders and
    environment as required
"""

import os

def copy_env(mapped_env, key, mapped_folders=None, tgt_key=None):
    if tgt_key is None:
        tgt_key = key
    if key in os.environ:
        mapped_env[tgt_key] = os.environ[key]
        if mapped_folders is not None:
            mapped_folders.append(os.environ[key])

uid = os.getuid()
os.environ["UID"] = str(uid)

cmd = "docker run --rm -it"

mapped_folders = ["/tmp/.X11-unix"]
mapped_env = {}

copy_env(mapped_env, "UID", tgt_key="HOST_UID")
copy_env(mapped_env, "USER", tgt_key="HOST_USER")
copy_env(mapped_env, "DISPLAY")
copy_env(mapped_env, "FSLDIR", mapped_folders)
copy_env(mapped_env, "FSLDEVDIR", mapped_folders)
print(mapped_env)

if "HOME" in os.environ:
    mapped_folders.append(os.environ["HOME"])

config_file = os.path.join(os.environ.get("HOME", "/"), ".quantiphyse-docker")
if not os.path.exists(config_file):
    # Create an empty config file
    try:
        os.utime(config_file, None)
    except OSError:
        open(config_file, 'a').close()

with open(config_file, "r") as f:
    for line in f.readlines():
        line = line[:line.find("#")].strip()
        if line:
            kv = tuple(line.split(":", 1))
            if len(kv) == 2:
                value = kv[1].strip()
                if kv[0] == "folder":
                    mapped_folders.append(value)
                elif kv[0] == "env":
                    copy_env(mapped_env, value)

for folder in mapped_folders:
    print("Mapping folder: %s" % folder)
    cmd += " -v %s:%s" % (folder, folder)

for env in mapped_env.items():
    print("Mapping environment: %s=%s" % env)
    cmd += " -e %s=%s" % env

cmd += " ibmequbic/quantiphyse"

print(cmd)
os.system(cmd)
