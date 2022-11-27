#!/usr/bin/env python3

from micro_func import Debug

db = Debug("repl")


import uasyncio
from api import coro, run_coro
run_coro()
