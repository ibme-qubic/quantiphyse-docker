#!/usr/bin/env python
"""
Simple pre-run script for a Docker container which disables the registration dialog

Copyright (c) 2013-2018 University of Oxford
"""
try:
    from PySide import QtCore
except ImportError:
    from PySide2 import QtCore

QtCore.QCoreApplication.setOrganizationName("ibme-qubic")
QtCore.QCoreApplication.setOrganizationDomain("eng.ox.ac.uk")
QtCore.QCoreApplication.setApplicationName("Quantiphyse")
QtCore.QSettings().setValue("license_accepted", 1)
