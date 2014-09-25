#!/usr/bin/env python

from gi.repository import Gtk, Gdk, GLib
# import os
import random
import re
import string
import sys


class Countersign(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        # Use sys.argv[0] to get the directory from where the program was
        # executed.  Follow it to its original directory using os.readlink
        # if it is a symlink. Get the directory where the actual program
        # resides with os.path.dirname '''
        # program_directory = os.path.dirname(os.readlink(sys.argv[0]))
        #
        # Prepend the programs directory to the glade file name
        # gui_file = os.path.join(program_directory, 'countersign.glade')
        gui_file = 'countersign.glade'
        #
        # Attempt to load *.glade file
        try:
            # Use Gtk.Builder to build UI from *.glade file.
            self.builder = Gtk.Builder()
            self.builder.add_from_file(gui_file)
        except GLib.GError, e:
            sys.exit("Gtk.Builder error({0}): {1}".format(e.code, e.message))

        # Initialize the widgets.
        self.init_widgets()
        # Connect the signals to the handlers
        self.connect_signals()
        # Sets the widgets to the program default state.
        self.default_states()

        # Show the main window with all its widgets.
        self.win.show_all()

    def init_widgets(self):
        '''Initiialize widgets.'''
        # Import widgets from *.glade file and initialize.
        #
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

    # ----- Signals -----
    def connect_signals(self):
        '''Connect signals to callbacks.'''
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
        # Connects the signals to the handlers.
        self.builder.connect_signals(handlers)

    def default_states(self):
        '''Sets widgets to default states.'''
        self.win.set_title("Countersign")
        # Password Textview Iterator
        self.password_list_iter_start = \
            self.password_list_buffer.get_start_iter()
        self.lowercase_ckbtn.set_active(True)

    #
    # ----- Handlers -----
    #
    #
    # Generate button handler
    def generate_btn_clicked_cb(self, widget):
        '''Generates password(s).'''
        # Check and store character types checkbox state
        self.selected_char_type = [self.lowercase_ckbtn.get_active(),
                                   self.uppercase_ckbtn.get_active(),
                                   self.numerals_ckbtn.get_active(),
                                   self.symbols_ckbtn.get_active()]
        self.check_options()
        #
        # Get the number of passwords to generate
        number_of_passwords = int(self.quantity_adj.get_value())
        # Buffer to hold generated password(s)
        self.password_buffer = []
        # Check and store character types checkbox state
        self.selected_char_type = [self.lowercase_ckbtn.get_active(),
                                   self.uppercase_ckbtn.get_active(),
                                   self.numerals_ckbtn.get_active(),
                                   self.symbols_ckbtn.get_active()]
        # self.check_options()
        self.clear_password_list()
        # Generate n number of passwords where n is the quantity selected by
        # the user, then append it to the buffer.
        for count in range(number_of_passwords):
            self.password_buffer.append(self.generate_password())

        self.add_password(self.password_buffer)

    # Copy button handler
    def copy_clicked_cb(self, widget):
        '''Copies generated passwords to the clipboard.'''
        buf_start = self.password_list_buffer.get_start_iter()
        buf_end = self.password_list_buffer.get_end_iter()
        passwords = self.password_list_buffer.get_text(buf_start,
                                                       buf_end, True)
        if len(passwords) > 0:
            self.clipboard.set_text(passwords, -1)  # -1 guesses length

    # Reset button handler
    def reset_cb(self, widget):
        ''' Reset program/widgets to default values. '''
        self.length_adj.set_value(8)
        self.quantity_adj.set_value(1)
        self.uppercase_ckbtn.set_active(False)
        self.numerals_ckbtn.set_active(False)
        self.symbols_ckbtn.set_active(False)
        self.password_list_buffer.set_text('')
        self.password_list_iter_start = \
            self.password_list_buffer.get_start_iter()

    # Close button and Main window 'destroy' handler.
    def close_cb(self, widget):
        ''' Quit/terminate program. '''
        Gtk.main_quit()

    def generate_lower(self):
        '''Generate a random lower case character.'''
        return string.lowercase[random.randint(0, len(string.lowercase) - 1)]

    def generate_upper(self):
        '''Generates a random upper case character.'''
        return string.uppercase[random.randint(0, len(string.uppercase) - 1)]

    def generate_numeral(self):
        '''Generates a random numerical character.'''
        return string.digits[random.randint(0, len(string.digits) - 1)]

    def generate_symbol(self):
        '''Generates a random symbol.'''
        return string.punctuation[random.randint(0,
                                                 len(string.punctuation) - 1)]

    def check_options(self):
        # Verify at least one character type is selected; if no character types
        # are selected, select lowercase character type as the default
        try:
            if not self.selected_char_type[0] and\
               not self.selected_char_type[1] and\
               not self.selected_char_type[2] and\
               not self.selected_char_type[3]:
                self.lowercase_ckbtn.set_active(True)
        except GLib.GError, e:
            e_runtime = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                                          Gtk.ButtonsType.OK,
                                          "Runtime Error")
            e_runtime.format_secondary_text(
                "Gtk.Builder error({0}): {1}".format(e.code, e.message))
            e_runtime.run()
            e_runtime.destroy()

    def clear_password_list(self):
        '''Clears the password list (textview) widget.'''
        if self.password_list_buffer.get_char_count() > 0:
            self.password_list_buffer.set_text('')
            self.password_list_iter_start = \
                self.password_list_buffer.get_start_iter()

    def generate_password(self):
        # Generates a password n number of characters long, where n is a
        # length selected by the user.
        password_length = int(self.length_adj.get_value())
        password_character = ''
        password = ''
        # random_char_choice calls the appropriate function to generate a
        # random character associated with its index.
        random_char_choice = {0: self.generate_lower,
                              1: self.generate_upper,
                              2: self.generate_numeral,
                              3: self.generate_symbol}

        while not password_length == 0:
            # Select a random character type to generate
            element = random.randint(0, 3)
            # If the randomly selected character type is an active selection
            # generate a random character of that type.
            if self.selected_char_type[element]:
                password_character = random_char_choice[element]()
                # If this is the first character of the password string,
                # assign it to password.
                if password == '':
                    password += password_character
                    password_length -= 1
                # If this is not the first character of the password string,
                # compare it to the character(s) already in the password
                # string and verify it is unique.  If it is not unique, do not
                # add it to the string.

                # re.escape is used to escape any special symbols used by
                # regular expressions.

                # *.lower() changes the generated character and the password
                # string to lowercase, to compare if there are any duplicate
                # letters.
                elif re.search(re.escape(password_character.lower()),
                               password.lower()):
                    pass
                else:
                    passwd_char = ord(str(password_character))
                    passwd_elmnt = ord(str(password[len(password)-1]))
                    if (passwd_char - passwd_elmnt) < -1 or\
                       (passwd_char - passwd_elmnt) > 1:
                        # If the character not consecutive and is unique,
                        # add it to the string.
                        password += password_character
                        password_length -= 1
                    else:
                        pass

        return password

    def add_password(self, password_buff):
        # Adds the generated password(s) to the password_list textview.
        for element in range(len(password_buff)):
            if element == 0:
                self.password_list_buffer.insert(self.password_list_iter_start,
                                                 password_buff[element])
            elif element == len(password_buff):
                self.password_list_buffer.inster(self.password_list_iter_start,
                                                 password_buff[element])
            else:
                self.password_list_buffer.insert(self.password_list_iter_start,
                                                 '\n' + password_buff[element])

    def main(self):
        # Main function of Countersign.
        Gtk.main()


if __name__ == "__main__":
    main_win = Countersign()
    main_win.main()
