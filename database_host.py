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

c.execute('''CREATE TABLE IF NOT EXISTS settings (
          name_of_setting text,
          on_off text)''')

def get_setting(setting_name):
    c.execute("SELECT on_off FROM settings WHERE name_of_setting=?", (setting_name,))
    grabber = c.fetchone()
    return grabber[0]

def setting_configure(setting_name, change_to):
    c.execute("UPDATE settings SET on_off=? WHERE name_of_setting=?", (change_to, setting_name))
    Conn.commit()

def update_theme_in_db(theme):
    c.execute("UPDATE settings SET on_off=? WHERE name_of_setting='theme'", (theme,))
    Conn.commit()

def check_if_exists():
    c.execute("SELECT on_off FROM settings WHERE name_of_setting='dark' OR name_of_setting='light'")
    grabber = c.fetchone()
    if grabber == None:
        c.execute("INSERT INTO settings (name_of_setting, on_off) VALUES ('theme', 'dark')")
        Conn.commit()
check_if_exists()
#c.execute("INSERT INTO settings (name_of_setting, on_off) VALUES ('theme', 'dark')")

# --------------- TABLES ---------------

# settings
    # name_of_setting | on_off
    # 'theme'           'dark'
