import sqlite3

conn = sqlite3.connect('info.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS settings (
          name_of_setting text,
          on_off text)''')

def get_setting(setting_name):
    c.execute("SELECT on_off FROM settings WHERE name_of_setting='{}'".format(setting_name))
    grabber = c.fetchone()
    return grabber[0]

def setting_configure(setting_name, change_to):
    c.execute('''UPDATE settings SET on_off='{}' WHERE name_of_setting='{}' '''.format(change_to, setting_name))
    conn.commit()

#c.execute("INSERT INTO settings (name_of_setting, on_off) VALUES ('theme', 'dark')")

# --------------- TABLES ---------------
# 
# settings
    # name_of_setting | on_off
    # 'theme'           'dark'

