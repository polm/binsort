import argparse
import fileinput
import sys
import os

parser = argparse.ArgumentParser(prog="binsort")

parser.add_argument("labels", default="yes,no")

args = parser.parse_args()

labels = args.labels.split(",")

import urwid

candidates = list([ii.strip() for ii in fileinput.input([])])
candw = urwid.Pile([])

def build_candidates():
    cands = []
    if not candidates:
        return cands
    
    # first one is styled
    pick = urwid.Text( ('selected', candidates[0]), wrap="ellipsis")
    cands.append( (pick, candw.options()) )
    for cand in candidates[1:]:
        ww = urwid.Text(cand, wrap="ellipsis")
        cands.append( (ww, candw.options()) )
    return cands

candw.contents = build_candidates()

keys = [str(ii) for ii in range(1, len(labels) + 1)]
headers = [f"{kk} {label}" for kk, label in zip(keys, labels)]
header = urwid.Text("\n".join(headers))


hr = urwid.Divider("-")
view = urwid.Pile([header, hr, candw])
out = []

def handle_input(key):
    if key in keys:
        label = labels[keys.index(key)]
        out.append( (label, candidates.pop(0)) )
        candw.contents = build_candidates()
    # seen everything, so it's done
    if not candidates:
        raise urwid.ExitMainLoop()

palette = [
        ('selected', 'white', 'black', 'standout'),
        ]

# don't use stdin for input
# https://www.mail-archive.com/urwid@lists.excess.org/msg00665.html
tty_in = open('/dev/tty', 'r') # the file object for Urwid input
screen = urwid.raw_display.Screen(input=tty_in)
wrap = urwid.Filler(view, valign='top')
loop = urwid.MainLoop(wrap, palette, screen=screen, unhandled_input=handle_input)

loop.run()

for label, val in out:
    print(label, val, sep="\t")
