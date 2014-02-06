#!/usr/bin/python
from gi.repository import Gtk
import dwarfmodeltest
from elftools.elf.elffile import ELFFile
from dwarfmodel import DwarfModelBuilder, ChildrenGroup

import signal
import sys


class DwarfUi(Gtk.Window):

    def __init__(self, root_element = None):
        Gtk.Window.__init__(self, title="Hello World")

        self.connect("delete-event", Gtk.main_quit)

        self.maximize()

        box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.add(box)

        menubar, toolbar = self.build_menus("menus.xml")

        box.pack_start(menubar, False, False, 0)
        box.pack_start(toolbar, False, False, 0)

        self.tree = self.build_tree_view()
        store = self.build_tree_store(root_element)
        self.tree.set_model(store)

        box.add(self.tree)

    def build_menus(self, menus_xml_file):
        uimanager = self.create_ui_manager(menus_xml_file)

        action_group = Gtk.ActionGroup("actions")

        # File menu
        action_filemenu = Gtk.Action("FileMenu", "File", None, None)
        action_group.add_action(action_filemenu)

        action_fileopen = Gtk.Action("FileOpen", "Open", "Open a DWARF file", Gtk.STOCK_OPEN)
        action_group.add_action(action_fileopen)
        action_fileopen.connect("activate", self.on_menu_file_open)

        action_filequit = Gtk.Action("FileQuit", None, None, Gtk.STOCK_QUIT)
        action_group.add_action(action_filequit)
        action_filequit.connect("activate", self.on_menu_file_quit)

        # Edit menu
        action_editmenu = Gtk.Action("EditMenu", "Edit", None, None)
        action_group.add_action(action_editmenu)

        action_editfind = Gtk.Action("EditFind", "Find", None, Gtk.STOCK_FIND)
        action_group.add_action(action_editfind)
        action_editfind.connect("activate", self.on_menu_edit_find)

        uimanager.insert_action_group(action_group)

        menubar = uimanager.get_widget("/MenuBar")
        toolbar = uimanager.get_widget("/ToolBar")

        return menubar, toolbar

    def create_ui_manager(self, menus_xml_file):
        uimanager = Gtk.UIManager()

        uimanager.add_ui_from_file(menus_xml_file)
        accelgroup = uimanager.get_accel_group()
        self.add_accel_group(accelgroup)

        return uimanager


    def build_tree_view(self):
        tree = Gtk.TreeView()

        tree.append_column(Gtk.TreeViewColumn("Element", Gtk.CellRendererText(), text = 0))
        tree.append_column(Gtk.TreeViewColumn("Offset",  Gtk.CellRendererText(), text = 1))

        return tree

    def build_tree_store(self, root_element):
        store = Gtk.TreeStore(str, str)

        if root_element is not None:

            # Create root element
            root_iter = store.append(None, [root_element.name, ""])

            self.build_tree_store_rec(store, root_iter, root_element)

        return store


    def build_tree_store_rec(self, store, parent_iter, parent):
        for group_id in parent.children_groups:
            children_list = parent.children_groups[group_id]
            if group_id is not None:
                group_name = ChildrenGroup.name(group_id)
                # Add a tree element for the group
                add_to_iter = store.append(parent_iter, [group_name, ""])
            else:
                add_to_iter = parent_iter

            for child in children_list:
                print("Appending")
                child_iter = store.append(add_to_iter, [child.name, "0x%x" % (child.die.offset)])

                self.build_tree_store_rec(store, child_iter, child)

    def open_file(self, filename):
        with open(filename, 'rb') as f:
            elf = ELFFile(f)

            if not elf.has_dwarf_info():
                print("%s has no dwarf info." % filename)
                return

            di = elf.get_dwarf_info()

            builder = DwarfModelBuilder(di)
            root_elem = builder.build()

            dwarfmodeltest.print_rec(root_elem)

            store = self.build_tree_store(root_elem)
            self.tree.set_model(store)

    def on_menu_file_open(self, widget):
        dialog = Gtk.FileChooserDialog(
            "Choose an ELF binary",
            self, Gtk.FileChooserAction.OPEN,
            (
                Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OPEN, Gtk.ResponseType.OK
            )
        )

        resp = dialog.run()

        if resp == Gtk.ResponseType.OK:
            self.open_file(dialog.get_filename())

        dialog.destroy()

    def on_menu_edit_find(self, widget):
        print("Pressed find")

    def on_menu_file_quit(self, widget):
        Gtk.main_quit()

if __name__ == "__main__":
    #filename = sys.argv[1]
    """

    """
    win = DwarfUi()

    win.show_all()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Gtk.main()


