#!/bin/sh
#
# Docker container startup script for Quantiphyse

# Add the host user to the container so files saved
# on host filesystem have the right owner
useradd -u $HOST_UID $HOST_USER

# Set Quantiphyse as already registered otherwise the license
# dialog will appear every time it's run
su $HOST_USER --command "python3 /set_registered.py"

# Run Quantiphyse as host user
su $HOST_USER --command "/usr/local/bin/quantiphyse"
