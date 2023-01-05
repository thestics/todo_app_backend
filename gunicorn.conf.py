#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# Author: Danylo Kovalenko

import multiprocessing

bind = "0.0.0.0:80"
workers = multiprocessing.cpu_count() * 2 + 1
