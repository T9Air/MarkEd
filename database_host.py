import sqlite3
import os
import sys

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = (getattr(sys, '_MEIPASS', os.path.abspath("."))
                 if hasattr(sys, '_MEIPASS') else os.path.abspath("."))
    return os.path.join(base_path, relative_path)


Conn = sqlite3.connect(resource_path('info.db'))
c = Conn.cursor()

def initialize_settings():
    # Check if theme setting exists
    c.execute("SELECT COUNT(*) FROM settings WHERE name_of_setting='theme'")
    if c.fetchone()[0] == 0:
        # Insert default theme setting if it doesn't exist
        c.execute("INSERT INTO settings (name_of_setting, on_off) VALUES ('theme', 'dark')")
        Conn.commit()

# Call initialize_settings after creating the table
c.execute('''CREATE TABLE IF NOT EXISTS settings (
          name_of_setting text,
          on_off text)''')

initialize_settings()

def get_setting(setting_name):
    c.execute("SELECT on_off FROM settings WHERE name_of_setting=?", (setting_name,))
    grabber = c.fetchone()
    return grabber[0]

def setting_configure(setting_name, change_to):
    c.execute("UPDATE settings SET on_off=? WHERE name_of_setting=?", (change_to, setting_name))
    Conn.commit()

# Ensure connection is closed properly when the program exits
def close_connection():
    Conn.commit()
    Conn.close()

import atexit
atexit.register(close_connection)