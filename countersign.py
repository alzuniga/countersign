#!/usr/bin/env python

from gi.repository import Gtk, Gdk
import string
import random


class PasswordGen(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.builder = Gtk.Builder()
        self.builder.add_from_file("countersign.glade")
        self.init_widgets()
        self.connect_signals()
        self.default_states()
        self.win.show_all()

    def init_widgets(self):
        self.win = self.builder.get_object("main_win")
        self.length_adj = self.builder.get_object("length_adj")
        self.length_scale = self.builder.get_object("length_scale")
        self.password_list = self.builder.get_object("password_list")
        self.password_list_buffer = self.password_list.get_buffer()
        self.quantity_adj = self.builder.get_object("quantity_adj")
        self.quantity_scale = self.builder.get_object("quantity_scale")
        self.lowercase_ckbtn = self.builder.get_object("lowercase_ckbtn")
        self.uppercase_ckbtn = self.builder.get_object("uppercase_ckbtn")
        self.numerals_ckbtn = self.builder.get_object("numerals_ckbtn")
        self.symbols_ckbtn = self.builder.get_object("symbols_ckbtn")
        self.generate_btn = self.builder.get_object("generate_btn")
        self.copy_btn = self.builder.get_object("copy_btn")
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.reset_btn = self.builder.get_object("reset_btn")
        self.close_btn = self.builder.get_object("close_btn")

    def connect_signals(self):
        handlers = {
            "close_cb": self.close_cb,
            "generate_btn_clicked_cb": self.generate_btn_clicked_cb,
            "copy_clicked_cb": self.copy_clicked_cb,
            "reset_cb": self.reset_cb,
        }
        self.builder.connect_signals(handlers)

    def default_states(self):
        self.win.set_title("Countersign")
        self.password_list_iter_start = self.password_list_buffer.get_start_iter()
        self.lowercase_ckbtn.set_active(True)

    def generate_btn_clicked_cb(self, widget):
        if self.password_list_buffer.get_char_count() > 0:
            self.password_list_buffer.set_text('')
            self.password_list_iter_start = self.password_list_buffer.get_start_iter()

        length = int(self.length_adj.get_value())
        quantity = int(self.quantity_adj.get_value())

        self.password_character_list = ''
        self.passwords = []

        if not self.lowercase_ckbtn.get_active() and\
            not self.uppercase_ckbtn.get_active() and\
            not self.numerals_ckbtn.get_active() and\
            not self.symbols_ckbtn.get_active():
                self.lowercase_ckbtn.set_active(True)

        if self.lowercase_ckbtn.get_active():
            self.password_character_list += string.ascii_lowercase

        if self.uppercase_ckbtn.get_active():
            self.password_character_list += string.ascii_uppercase

        if self.numerals_ckbtn.get_active():
            self.password_character_list += string.digits

        if self.symbols_ckbtn.get_active():
            self.password_character_list += string.punctuation

        for i in range(quantity):
            password = ''
            for j in range(length):
                password += random.choice(self.password_character_list)
            self.passwords.append(password)

        for i in range(len(self.passwords)):
            if i == 0:
                self.password_list_buffer.insert(self.password_list_iter_start, self.passwords[i])
            elif i == len(self.passwords):
                self.password_list_buffer.insert(self.password_list_iter_start, self.passwords[i])
            else:
                self.password_list_buffer.insert(self.password_list_iter_start, '\n' + self.passwords[i])

        # The following is for debugging / testing
        #self.password_list_buffer = self.password_list.get_buffer()
        #self.password_list_buffer.set_text("Hello.")
        #self.password_list_iter_end = self.password_list_buffer.get_end_iter()
        #self.password_list_buffer.insert(self.password_list_iter_end, "\nGoodbye")
        #popup = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
        #                          Gtk.ButtonsType.OK, "Info")
        #pass_len = int(self.length_adj.get_value())
        #pass_qty = int(self.length_scale.get_value())
        #popup.format_secondary_text(self.passwords)
        #popup.run()
        #popup.destroy()

    def copy_clicked_cb(self, widget):
        buf_start = self.password_list_buffer.get_start_iter()
        buf_end = self.password_list_buffer.get_end_iter()
        passwords = self.password_list_buffer.get_text(buf_start, buf_end, True)
        if len(passwords) > 0:
            self.clipboard.set_text(passwords, -1) # -1 guesses length

    def reset_cb(self, widget):
        self.length_adj.set_value(8)
        self.quantity_adj.set_value(1)
        self.uppercase_ckbtn.set_active(False)
        self.numerals_ckbtn.set_active(False)
        self.symbols_ckbtn.set_active(False)
        self.password_list_buffer.set_text('')
        self.password_list_iter_start = self.password_list_buffer.get_start_iter()

    def close_cb(self, widget):
        Gtk.main_quit()

    def main(self):
        Gtk.main()


if __name__ == "__main__":
    main_win = PasswordGen()
    main_win.main()
