#!/usr/bin/env python

from gi.repository import Gtk, Gdk
import string
import random


class PasswordGen(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.builder = Gtk.Builder()
        self.builder.add_from_file("countersign.glade")
        # Initialize Widgets
        self.init_widgets()
        # Connect Signals to Handlers
        self.connect_signals()
        # Set Widgets Default States
        self.default_states()
        # Show the Main Window
        self.win.show_all()

    def init_widgets(self):
		# Main Window
        self.win = self.builder.get_object("main_win")
        # Length Adjustment
        self.length_adj = self.builder.get_object("length_adj")
        # Length Scale
        self.length_scale = self.builder.get_object("length_scale")
        # Password TextView
        self.password_list = self.builder.get_object("password_list")
        # Password TextView Buffer
        self.password_list_buffer = self.password_list.get_buffer()
        # Quantity Adjustment
        self.quantity_adj = self.builder.get_object("quantity_adj")
        # Quantity Scale
        self.quantity_scale = self.builder.get_object("quantity_scale")
        # Lowercase Checkbutton (checkbox)
        self.lowercase_ckbtn = self.builder.get_object("lowercase_ckbtn")
        # Uppercase Checkbutton (checkbox)
        self.uppercase_ckbtn = self.builder.get_object("uppercase_ckbtn")
        # Numeral Checkbutton (checkbox)
        self.numerals_ckbtn = self.builder.get_object("numerals_ckbtn")
        # Symbol Checkbutton (checkbox)
        self.symbols_ckbtn = self.builder.get_object("symbols_ckbtn")
        # Generate Button
        self.generate_btn = self.builder.get_object("generate_btn")
        # Copy Button
        self.copy_btn = self.builder.get_object("copy_btn")
        # Clipboard Object
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        # Reset Button
        self.reset_btn = self.builder.get_object("reset_btn")
        # Close Button
        self.close_btn = self.builder.get_object("close_btn")

    def connect_signals(self):
        handlers = {
			# Close Button Signal
            "close_cb": self.close_cb,
            # Generate Button Signal
            "generate_btn_clicked_cb": self.generate_btn_clicked_cb,
            # Copy Button Signal
            "copy_clicked_cb": self.copy_clicked_cb,
            # Reset Button Signal
            "reset_cb": self.reset_cb,
        }
        # Connect the signals to the handlers
        self.builder.connect_signals(handlers)

    def default_states(self):
        self.win.set_title("Countersign")
        # Password Textview Iterator
        self.password_list_iter_start = self.password_list_buffer.get_start_iter()
        self.lowercase_ckbtn.set_active(True)

	# Handlers
	# Generate button handler
    def generate_btn_clicked_cb(self, widget):
		# Check if passsword textview has a(ny) generated password(s) in it and 
		# if it does, clear the passwords and reset the password textview
		# iterator.
        if self.password_list_buffer.get_char_count() > 0:
            self.password_list_buffer.set_text('')
            self.password_list_iter_start = self.password_list_buffer.get_start_iter()

		# Length of password(s), as selected
        length = int(self.length_adj.get_value())
        # Number of passwords to generate, as selected.
        quantity = int(self.quantity_adj.get_value())

		# To store the character types, as selected.
        self.password_character_list = ''
        # Password list.
        self.passwords = []
		
		# Check if no options are selected.  If no options are selected, select
		# at least the lower case option.
        if not self.lowercase_ckbtn.get_active() and\
            not self.uppercase_ckbtn.get_active() and\
            not self.numerals_ckbtn.get_active() and\
            not self.symbols_ckbtn.get_active():
                self.lowercase_ckbtn.set_active(True)
		
		# Determine if character type was selected and add them to the password
		# character list string.
        if self.lowercase_ckbtn.get_active():
            self.password_character_list += string.ascii_lowercase

        if self.uppercase_ckbtn.get_active():
            self.password_character_list += string.ascii_uppercase

        if self.numerals_ckbtn.get_active():
            self.password_character_list += string.digits

        if self.symbols_ckbtn.get_active():
            self.password_character_list += string.punctuation
		
		# Generate n passwords where n is the quantity of passwords to generate.
        for i in range(quantity):
            password = ''
            # Randomly select n amount of characters from the password character
            # list, where n is the number characters to generate.
            for j in range(length):
                password += random.choice(self.password_character_list)
            self.passwords.append(password)
		
		# Add passwords to password textview.
        for i in range(len(self.passwords)):
			# No new line before the first password
            if i == 0:
                self.password_list_buffer.insert(self.password_list_iter_start, self.passwords[i])
            # No new line before / after the last password
            elif i == len(self.passwords):
                self.password_list_buffer.insert(self.password_list_iter_start, self.passwords[i])
            # Prepend a new line to each password except as noted above.
            else:
                self.password_list_buffer.insert(self.password_list_iter_start, '\n' + self.passwords[i])
	
	# Copy button handler
    def copy_clicked_cb(self, widget):
        buf_start = self.password_list_buffer.get_start_iter()
        buf_end = self.password_list_buffer.get_end_iter()
        passwords = self.password_list_buffer.get_text(buf_start, buf_end, True)
        if len(passwords) > 0:
            self.clipboard.set_text(passwords, -1) # -1 guesses length
	
	# Reset button handler
    def reset_cb(self, widget):
        self.length_adj.set_value(8)
        self.quantity_adj.set_value(1)
        self.uppercase_ckbtn.set_active(False)
        self.numerals_ckbtn.set_active(False)
        self.symbols_ckbtn.set_active(False)
        self.password_list_buffer.set_text('')
        self.password_list_iter_start = self.password_list_buffer.get_start_iter()
	# Close button and Main window 'destroy' handler.
    def close_cb(self, widget):
        Gtk.main_quit()
	
	# MAIN
    def main(self):
        Gtk.main()


if __name__ == "__main__":
    main_win = PasswordGen()
    main_win.main()
