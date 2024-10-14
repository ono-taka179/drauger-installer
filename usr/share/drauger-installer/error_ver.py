#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  error_ver.py
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
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from sys import argv
from os import getenv

pak=argv[1]

LANG = list(getenv("LANG"))
length = len(LANG) - 1
while (length >= 5):
	del(LANG[length])
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
			del(contents[length])
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
		if (each[0] == "already_installed"):
			confirm = each[1]
		elif (each[0] == "EXIT"):
			EXIT = each[1]
	confirm = confirm.split("$pak")
	confirm = "%s".join(confirm)
	confirm = confirm % (pak)

except:
	confirm = "\n\tThis version of %s is already installed.\t\n" % (pak)
	EXIT = "EXIT"

class error(Gtk.Window):
	def __init__(self):
			Gtk.Window.__init__(self, title="Drauger Installer")
			self.set_icon_from_file("/usr/share/icons/Drauger/720x720/Menus/install-drauger.png")
			self.grid=Gtk.Grid(orientation=Gtk.Orientation.VERTICAL,)
			self.add(self.grid)

			self.label = Gtk.Label()
			self.label.set_markup(confirm)
			self.label.set_justify(Gtk.Justification.CENTER)
			self.grid.attach(self.label, 1, 1, 8, 1)

			self.button1 = Gtk.Button.new_with_label(EXIT)
			self.button1.connect("clicked", self.onexitclicked)
			self.grid.attach(self.button1, 7, 2, 1, 1)

	def onexitclicked(self, button):
		exit(2)



def show_error():
	window = error()
	window.set_decorated(True)
	window.set_resizable(False)
	window.set_position(Gtk.WindowPosition.CENTER)
	window.connect("delete-event", Gtk.main_quit)
	window.show_all()
	Gtk.main()


show_error()
