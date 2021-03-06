#!/usr/bin/python

import os
import sys
import re
import fileinput

key = ""
metadata = {}
title = {}
maintainerurl = {}

for line in fileinput.input([sys.argv[1]]) :

    regexp = re.compile('^Filename: (.*)$')
    m = regexp.match(line)
    if (m):
        key = m.group(1)

    regexp = re.compile('^Title: (.*)$')
    m = regexp.match(line)
    if (m):
        title[key] = m.group(1)

    regexp = re.compile('^Source: (.*)$')
    m = regexp.match(line)
    if (m):
        metadata[key] = m.group(1)

    regexp = re.compile('^MaintainerURL: (.*)$')
    m = regexp.match(line)
    if (m):
        maintainerurl[key] = m.group(1)

packagedata = ""
maintainer = ""
description = ""
sourcejson = ""

for line in fileinput.input([sys.argv[2]]) :

    if line == "\n":
        continue

    keepline = 1

    # A Package: line denotes the start of a package
    regexp = re.compile('^Package: (.*)$')
    m = regexp.match(line)
    if (m):
        packagedata = ""
        maintainer = ""
        description = ""
        sourcejson = ""

    # Save Source: lines for later processing
    regexp = re.compile('^Source: (.*)$')
    m = regexp.match(line)
    if (m):
        sourcejson = m.group(1)
        keepline = 0

    # Save Maintainer: lines for later processing
    regexp = re.compile('^Maintainer: (.*)$')
    m = regexp.match(line)
    if (m):
        maintainer = m.group(1)
        keepline = 0

    # Save Description: lines for later processing
    regexp = re.compile('^Description: (.*)$')
    m = regexp.match(line)
    if (m):
        description = m.group(1)
        keepline = 0

    if (keepline):
        packagedata += line

    regexp = re.compile('^Filename: (.*)$')
    m = regexp.match(line)
    if (m):
        key = m.group(1)

        if key in title:
            packagedata += "Description: " + title[key] + "\n"

        if maintainer:
            regexp = re.compile('^(.*\S)\s*<(.*)>$')
            m = regexp.match(maintainer)
            if m:
                if (m.group(2) == "nobody@example.com"):
                    if (key in maintainerurl):
                        regexp = re.compile('.*/([^/]+)\.html')
                        m = regexp.match(maintainerurl[key])
                        if m:
                            packagedata += "Maintainer: " + m.group(1) + " <" + maintainerurl[key] + ">" + "\n"
                        else:
                            packagedata += "Maintainer: <" + maintainerurl[key] + ">" + "\n"
                    else:
                        packagedata += "Maintainer: " + m.group(1) + "\n"
                elif (m.group(2) == "palm@palm.com"):
                    if (key in maintainerurl):
                        packagedata += "Maintainer: " + m.group(1) + " <" + maintainerurl[key] + ">" + "\n"
                    else:
                        packagedata += "Maintainer: " + m.group(1) + "\n"
                else:
                    packagedata += "Maintainer: " + maintainer + "\n"
                    
            else:
                if (key in maintainerurl):
                    packagedata += "Maintainer: " + maintainer + " <" + maintainerurl[key] + ">" + "\n"
                else:
                    packagedata += "Maintainer: " + maintainer + "\n"
                
                
    regexp = re.compile('^Description: (.*)$')
    m = regexp.match(line)
    if (m):
        if not key in title:
            packagedata += "Description: " + description + "\n"

        if key in metadata:

            if (sourcejson and (sourcejson[0] == "{")):
                packagedata += "Source: " + sourcejson + "\n"
            else:
                packagedata += "Source: " + metadata[key] + "\n"
                    
            print packagedata
            print
