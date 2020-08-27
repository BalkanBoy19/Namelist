# Studentenliste
import tkinter as tk
from tkinter import ttk
import sqlite3


def showAllStudents():
    zeiger.execute("Select * From Student;")
    res = zeiger.fetchall()
    print("Alle eingetragenen Studenten:")
    for data in res:
        print(data[0] + ", " + data[1] + ", " + data[2] + ", " + data[3] + ", " + data[4] + ", " + data[5])
    print()

def deleteEntries():
    vorname.set("")
    nachname.set("")
    matrikelnummer.set("")
    alter.set("")
    geschlecht.set("")
    semester.set("")

def deleteStudent():
    global cb
    if (len(cb["values"]) > 0) & (cb.get() != ''):
        student = cb.get()
        matrNr = student.split('/')[2]
        print("---",matrNr,"wurde geloescht ---")
        zeiger.execute("DELETE FROM Student Where matrikelnummer = " + matrNr)
        connection.commit()

        options = list(cb["values"])
        options.remove(student)
        cb["values"] = options
        if len(list(cb["values"])) == 0:
            cb.set("")
        else:
            cb.current(0)
    else:
        print("Liste ist leer.")

def dataisValid():
    if any(letter.isdigit() for letter in vorname.get()) | (vorname.get() == ''):
        print("Bitte einen Vornamen ins Feld 'Vorname' eintragen.")
        return False
    if any(letter.isdigit() for letter in nachname.get()) | (nachname.get() == ''):
        print("Bitte einen Nachnamen ins Feld 'Nachname' eintragen.")
        return False
    if any((not digit.isdigit()) for digit in matrikelnummer.get()) | (len(matrikelnummer.get()) != 7):
        print("Bitte eine Matrikelnummer mit genau 7 Ziffern ins Feld 'Matrikelnummer' eintragen.")
        return False
    if any(not digit.isdigit() for digit in alter.get()) |(alter.get() == ''):
        print("Bitte nur Zahlen ins Feld 'Alter' eintragen")
        return False
    else:
        age = int(alter.get())   # wird nur ausgefuehrt wenn es auf jeden Fall eine Zahl ist, kann also keine Exception auslösen
        if (age <= 14) | (age >= 50):
            print("Bitte ein Alter zwischen 14 und 50 ins Feld 'Alter' eintragen.")
            return False
    if geschlecht.get() not in ['m', 'w']:
        print("Bitte nur 'm' oder 'w' ins Feld 'Geschlecht' eintragen")
        return False
    if any(not digit.isdigit() for digit in semester.get()) | (semester.get() == ''):
        print("Bitte nur eine Zahl zwischen 1 und 20 ins Feld 'Semester' eintragen")
        return False
    zeiger.execute("SELECT * FROM Student Where matrikelnummer = " + matrikelnummer.get())
    connection.commit()
    res = zeiger.fetchone()
    if res != None:
        print("Die Matrikelnummer",matrikelnummer.get(),"ist bereits vergeben.")
        return False
    return True

def insertData():
    zeiger.execute("SELECT * FROM Student;")
    studentslist = []
    for data in zeiger.fetchall():
        studentslist.append(data[0] + "/" + data[1] + "/" + data[2] + "/" + data[3] + "/" + data[4] + "/" + data[5])
    return studentslist

def saveData():
    if dataisValid():
        zeiger.execute("INSERT INTO Student VALUES ('" + vorname.get() + "', '" + nachname.get() + "', " + matrikelnummer.get() + ", " + alter.get() + ", '" + geschlecht.get() + "', " + semester.get() + ");")
        connection.commit()     # Committen ist wirklich wichtig, bevor naechste Operation ausgefuehrt wird
        deleteEntries()
        print("Daten erfolgreich gespeichert.")
        cb["values"] = insertData()

def closing():
    connection.commit()
    connection.close()
    master.quit()
    print("Anwendung wurde beendet")

if __name__ == '__main__':
    master = tk.Tk()

    connection = sqlite3.connect("/Users/nedimdrekovic/Python/Namelist/list.db")
    zeiger = connection.cursor()
    #zeiger.execute("DROP TABLE IF EXISTS Student;")
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

    tk.Button(master, text='Quit', command=closing).grid(row=7, column=3, pady=4)
    tk.Button(master, text='Save', command=saveData, width=20).grid(row=6, column=1, pady=4)
    tk.Button(master, text='Show', command=showAllStudents).grid(row=7, column=1, pady=4)
    tk.Button(master, text='Delete', command=deleteStudent).grid(row=0, column=3, pady=4)

    studentslist = insertData()
    cb = ttk.Combobox(master, state="readonly", values=studentslist)
    cb.grid(row=0, column=2, pady=5, padx=10)
    if len(list(cb["values"])) > 0:
        cb.current(0)
    tk.mainloop()
