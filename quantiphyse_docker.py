#!/usr/bin/env python
"""
Simple(ish) wrapper script for docker run for Quantiphyse application
  - Passes DISPLAY settings to allow GUI display
  - Passes FSLDIR and FSLDEVDIR environment and maps the corresponding 
    folders, if set
  - Sets user ID and name so container can create an equivalent user, also
    maps HOME to corresponding homedir on container
  - Parses the config file $HOME/.quantiphyse-docker and maps folders and
    environment as required
"""

import os
import sys
import socket

def mac_get_display():
    """
    Get IP address and display index for Mac XQuartz setup
    """
    host_name = socket.gethostname() 
    host_ip = socket.gethostbyname(host_name)
    return host_ip, "%s:0" % host_ip

def copy_env(mapped_env, key, mapped_folders=None, tgt_key=None):
    """
    Copy and environment variable to the container, optionally
    under a different key name. Also optionally map the folder
    it points to
    """
    if tgt_key is None:
        tgt_key = key
    if key in os.environ:
        mapped_env[tgt_key] = os.environ[key]
        if mapped_folders is not None:
            mapped_folders.append(os.environ[key])

if "--update" in sys.argv:
    os.system("docker pull ibmequbic/quantiphyse")
    sys.argv = [a for a in sys.argv if a != "--update"]
    
# Get local user ID and set it in the environment
# The container will create a matching user on startup to
# ensure that files are saved to the host using the correct permissions
uid = os.getuid()
os.environ["UID"] = str(uid)

cmd = "docker run --rm -it"

# Need to map the X windows socket to allow GUI display
mapped_folders = ["/tmp/.X11-unix"]
mapped_env = {}

copy_env(mapped_env, "UID", tgt_key="HOST_UID")
copy_env(mapped_env, "USER", tgt_key="HOST_USER")
copy_env(mapped_env, "DISPLAY")
copy_env(mapped_env, "FSLDIR", mapped_folders)
copy_env(mapped_env, "FSLDEVDIR", mapped_folders)

if sys.platform == "darwin":
    # On Mac we need a third-party X server (XQuartz) and do some detective work to 
    # set DISPLAY correctly and give permission to the container to use the X server
    ip, display = mac_get_display()
    xquartz_ret = os.system("open -a xquartz")
    if xquartz_ret != 0:
        raise RuntimeError("You must install XQuartz on Mac first - visit www.xquartz.org")
    xhost_ret = os.system("xhost + %s" % ip)
    if xhost_ret != 0:
        raise RuntimeError("WARNING: xhost + %s failed - Quantiphyse may not display" % ip)
    mapped_env["DISPLAY"] = display

# Make sure the homedir is mapped to where a Linux machine expects it to be
if "HOME" in os.environ:
    cmd += " -v %s:/home/%s" % (os.environ["HOME"], os.environ["USER"])

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
if len(sys.argv) > 1:
    # Optional startup command (bash is useful for debugging)
    cmd += " " + sys.argv[1]

print(cmd)
ret = os.system(cmd)
if ret != 0:
    print("ERROR: Quantiphyse failed to start")
    if sys.platform == "darwin":
        print(" - On Mac ensure that XQuartz accepts network connections in Preferences -> Security")
        print(" - Also ensure that your FSLDIR is added to the list of folders that Docker is allowed to share in Preferences->Resources->File Sharing")
