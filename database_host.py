import sqlite3
import os
import sys

def get_db_path():
    """Get the path to the database file in the same directory as the executable"""
    if getattr(sys, 'frozen', False):
        # If running as compiled executable
        return os.path.join(os.path.dirname(sys.executable), 'info.db')
    else:
        # If running as script
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'info.db')

# Create database connection
Conn = sqlite3.connect(get_db_path())
c = Conn.cursor()

# Create tables if they don't exist
c.execute('''CREATE TABLE IF NOT EXISTS settings (
          name_of_setting text,
          on_off text)''')

def get_setting(setting_name):
    c.execute("SELECT on_off FROM settings WHERE name_of_setting=?", (setting_name,))
    grabber = c.fetchone()
    return grabber[0] if grabber else None

def setting_configure(setting_name, change_to):
    # First try to update existing setting, if it doesn't exist, insert it
    c.execute("""UPDATE settings SET on_off=? WHERE name_of_setting=?""", (change_to, setting_name))
    if c.rowcount == 0:  # If no row was updated, insert new setting
        c.execute("""INSERT INTO settings (name_of_setting, on_off) VALUES (?, ?)""", 
                 (setting_name, change_to))
    Conn.commit()

def check_if_exists():
    c.execute("SELECT on_off FROM settings WHERE name_of_setting='theme'")
    grabber = c.fetchone()
    if grabber is None:
        c.execute("INSERT INTO settings (name_of_setting, on_off) VALUES ('theme', 'dark')")
        Conn.commit()

# Initialize settings
check_if_exists()

# Ensure connection is closed when the program exits
import atexit
atexit.register(Conn.close)
#c.execute("INSERT INTO settings (name_of_setting, on_off) VALUES ('theme', 'dark')")

# --------------- TABLES ---------------

# settings
    # name_of_setting | on_off
    # 'theme'           'dark'

