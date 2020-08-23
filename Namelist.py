# Studentenliste
import tkinter as tk
import sqlite3


def show_entry_fields():
   print("First Name: %s\nLast Name: %s" % (vorname.get(), name.get()))

def deleteEntries():
    vorname.set("")
    nachname.set("")
    matrikelnummer.set("")
    alter.set("")
    geschlecht.set("")
    semester.set("")

def dataisValid():
    if any(letter.isdigit() for letter in vorname.get()):
        return False
    if any(letter.isdigit() for letter in nachname.get()):
        return False
    if any((not digit.isdigit() | (len(matrikelnummer.get()) != 7)) for digit in matrikelnummer.get()):
        return False
    if any((not digit.isdigit() |(len(alter.get()) not in [1, 2])) for digit in alter.get()):
        return False
    if geschlecht.get() not in ['m', 'w']:
        return False
    if any(not digit.isdigit() for digit in semester.get()):
        return False
    return True

def saveData():
    if dataisValid():
        zeiger = connection.cursor()
        zeiger.execute("INSERT INTO Student VALUES ('" + vorname.get() + "', '" + nachname.get() + "', '" + matrikelnummer.get() + "', " + alter.get() + ", '" + geschlecht.get() + "', " + semester.get() + ");")
        zeiger.execute("SELECT * FROM Student;")
        data = zeiger.fetchone()
        print(data)
        print("Daten erfolgreich gespeichert.")
        deleteEntries()

def closing():
    connection.commit()
    connection.close()
    master.quit()

if __name__ == '__main__':
    master = tk.Tk()

    connection = sqlite3.connect("/Users/nedimdrekovic/Python/Namelist/list.db")
    zeiger = connection.cursor()
    zeiger.execute("DROP TABLE IF EXISTS Student;")
    zeiger.execute("""CREATE TABLE IF NOT EXISTS Student (
                        `vorname` TEXT NOT NULL,
                        `name` TEXT NOT NULL,
                        `matrikelnummer` VARCHAR(7) NOT NULL PRIMARY KEY,
                        `alter` VARCHAR(2) NOT NULL,
                        `geschlecht` CHAR(1),
                        `semester` VARCHAR(2) NOT NULL
                    );""")
    tk.Label(master, text="Vorname").grid(row=0)
    tk.Label(master, text="Nachname").grid(row=1)
    tk.Label(master, text="Matrikelnummer").grid(row=2)
    tk.Label(master, text="Alter").grid(row=3)
    tk.Label(master, text="Geschlecht").grid(row=4)
    tk.Label(master, text="Semester").grid(row=5)

    vorname = tk.StringVar()
    nachname = tk.StringVar()
    matrikelnummer = tk.StringVar()
    alter = tk.StringVar()
    geschlecht = tk.StringVar()
    semester = tk.StringVar()

    tk.Entry(master, textvariable=vorname).grid(row=0, column=1)
    tk.Entry(master, textvariable=nachname).grid(row=1, column=1)
    tk.Entry(master, textvariable=matrikelnummer).grid(row=2, column=1)
    tk.Entry(master, textvariable=alter).grid(row=3, column=1)
    tk.Entry(master, textvariable=geschlecht).grid(row=4, column=1)
    tk.Entry(master, textvariable=semester).grid(row=5, column=1)

    tk.Button(master, text='Schließen', command=closing).grid(row=7, column=0, pady=4)
    tk.Button(master, text='Save', command=saveData).grid(row=6, column=0, pady=4)
    tk.Button(master, text='Anzeigen', command=show_entry_fields).grid(row=7, column=1, pady=4)

    tk.mainloop()
"""
            for letter in vorname.get():
                if isinstance(letter, int):
                    return False
            for letter in nachname.get():
                if isinstance(letter, int):
                    return False
            for digit in matrikelnummer.get():
                if isinstance(digit, str) || (len(matrikelnummer.get()) != 7):
                    return False
            for digit in alter.get():
                if isinstance(digit, str) || (len(alter.get()) > 3):
                    return False
            if geschlecht.get() not in ['m', 'w']:
                return False
            for digit in semester.get():
                if isinstance(digit, str):
                    return False
"""
