import curses
import atexit
import time
import sys
import os

if sys.platform == 'win32':
    os.system('') 

_stdscr = curses.initscr()
atexit.register(curses.endwin)
_line_lengths = {}
class _init_:
    pass

_init_ = _init_()

lines = 0
cleanf = {}

class output:
    def __init__(self, text, y=None, x=0, end=True):
        global lines, cleanf
        lines += 1
        cleanf[lines] = len(text)
        max_y, max_x = _stdscr.getmaxyx()
        if y is None:
            y, _ = _stdscr.getyx()
        y = max(0, min(y, max_y - 1))
        x = max(0, min(x, max_x - 1))
        _stdscr.move(y, x)
        _stdscr.addstr(str(text))
        _stdscr.clrtoeol()
        if end:
            _stdscr.addstr('\n')
        _stdscr.refresh()
        _line_lengths[y] = len(str(text))
        final_y, _ = _stdscr.getyx()
        if final_y >= max_y - 1:
            _stdscr.move(max_y - 1, 0)
            _stdscr.refresh()

class line:
    def __init__(self, y=None, x=0):
        if y is None:
            y, _ = _stdscr.getyx()
        _stdscr.move(y, x)
        _stdscr.clrtoeol()
        _stdscr.addstr('\n')
        _stdscr.refresh()

class clean:
    def __init__(self, line=None):
        global cleanf
        sy, _ = _stdscr.getyx()
        y = line if line is not None else sy
        y -= 1
        max_y, _ = cleanf[line]
        y = min(max(y, 0), max_y)
        _stdscr.move(y, 0)
        _stdscr.clrtoeol()
        _stdscr.refresh()
        cleanf[line] = 0

def put(prompt='', y=None, x=0, max_len=50):
    global lines, cleanf
    lines += 1
    cleanf[lines] = len(prompt)
    if y is None:
        y, _ = _stdscr.getyx()
    _stdscr.move(y, x)
    _stdscr.addstr(prompt)
    _stdscr.refresh()
    curses.echo()
    result = _stdscr.getstr(y, x + len(prompt), max_len)
    curses.noecho()
    return result.decode('utf-8')

class outs:
    def __init__(self, text, y=None, x=0, end=True):
        max_y, max_x = _stdscr.getmaxyx()
        global lines, cleanf
        lines += 1
        cleanf[lines] = len(text)
        if y is None:
            y, _ = _stdscr.getyx()
        y = max(0, min(y, max_y - 1))
        x = max(0, min(x, max_x - 1))
        
        _stdscr.move(y, x)
        text_str = str(text)
        for i in text_str:
            cur_y, cur_x = _stdscr.getyx()
            if cur_x >= max_x - 1:
                if cur_y < max_y - 1:
                    _stdscr.move(cur_y + 1, 0)
                else:
                    break
            _stdscr.addstr(i)
            if end:
                _stdscr.addstr('\n')
            _stdscr.refresh()
            time.sleep(0.02)
        final_y, _ = _stdscr.getyx()
        if final_y < max_y - 1:
            _stdscr.move(final_y + 1, 0)
        _stdscr.clrtoeol()
        _stdscr.refresh()

class cleans:
    def __init__(self, line=None):
        sy, _ = _stdscr.getyx()
        y = line if line is not None else sy
        y -= 1
        max_y, max_x = _stdscr.getmaxyx()
        y = min(max(y, 0), max_y - 1)
        n = _line_lengths.get(y, max_x - 1)
        _stdscr.move(y, 0)
        _stdscr.refresh()
        for x in range(n):
            _stdscr.move(y, x)
            _stdscr.addstr(' ')
            _stdscr.refresh()
            time.sleep(0.05)
        _stdscr.move(y, 0)
        _stdscr.clrtoeol()
        _stdscr.refresh()
class move:
    def __init__(self, y, x=None):
        max_y, max_x = _stdscr.getmaxyx()
        y = min(max(y, 0), max_y - 1) - 1
        if x is None:
            x = 0
        x = min(max(x, 0), max_x - 1)
        _stdscr.move(y, x)
        _stdscr.refresh()