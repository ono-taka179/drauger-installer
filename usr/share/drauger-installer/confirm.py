#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  confirm.py
#
#  Copyright 2020 Thomas Castleman <contact@draugeros.org>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
from os import getenv
from sys import argv
from gi.repository import Gtk, Gdk
import gi
gi.require_version('Gtk', '3.0')

info = argv[1]
action = argv[2]

LANG = list(getenv("LANG"))
length = len(LANG) - 1
while (length >= 5):
    del (LANG[length])
    length = length - 1
LANG = "".join(LANG)

try:
    with open("/etc/drauger-locales/%s/drauger-installer.conf" % (LANG), "r") as FILE:
        contents = FILE.read()
    contents = contents.split("\n")
    for each in range(len(contents)):
        contents[each] = list(contents[each])
    length = len(contents) - 1
    while (length >= 0):
        if ((contents[length] == []) or (contents[length][0] == "#")):
            del (contents[length])
        length = length - 1
    for each in range(len(contents)):
        contents[each] = "".join(contents[each])
    for each in range(len(contents)):
        if "\t" in contents[each]:
            key, value = contents[each].split("\t", 1)
            if value.startswith('"') and value.endswith('"'):
                value = value.strip('"')
            value = value.replace("\\n", "\n").replace("\\t", "\t")
            contents[each] = [key, value]
    for each in contents:
        if (each[0] == "confirm_gui"):
            confirm = each[1]
        elif (each[0] == "YES"):
            YES = each[1]
        elif (each[0] == "NO"):
            NO = each[1]
    confirm = confirm.split("$info")
    confirm = "%s".join(confirm)
    confirm = confirm.split("$action")
    confirm = "%s".join(confirm)
    confirm = confirm % (info, action)

except:
    confirm = """
    Package Info:

    %s

    Would you like to %s this package?
    """ % (info, action)
    YES = "YES"
    NO = "NO"


class confirm_UI(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Drauger Installer")
        self.grid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL,)
        self.set_icon_from_file(
            "/usr/share/icons/Drauger/720x720/Menus/install-drauger.png")
        self.add(self.grid)

        self.label = Gtk.Label()
        self.label.set_markup(confirm)
        self.label.set_justify(Gtk.Justification.LEFT)
        self.grid.attach(self.label, 1, 1, 8, 1)

        self.button1 = Gtk.Button.new_with_label(YES)
        self.button1.connect("clicked", self.onyesclicked)
        self.grid.attach(self.button1, 7, 2, 1, 1)

        self.button1 = Gtk.Button.new_with_label(NO)
        self.button1.connect("clicked", self.onnoclicked)
        self.grid.attach(self.button1, 5, 2, 1, 1)

    def onyesclicked(self, button):
        exit(0)

    def onnoclicked(self, button):
        exit(1)


def show_conf():
    window = confirm_UI()
    window.set_decorated(True)
    window.set_resizable(False)
    window.set_position(Gtk.WindowPosition.CENTER)
    window.connect("delete-event", Gtk.main_quit)
    window.show_all()
    Gtk.main()


show_conf()
