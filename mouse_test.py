#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 08:45:50 2022

@author: carljohan
"""

import autopy.mouse as mouse
from time import sleep

while True:
    x, y = mouse.location()
    if y < 5:
        mouse.move(x, 5)
    sleep(0.01)