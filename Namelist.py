# Studentenliste
import tkinter as tk
from tkinter import ttk
import sqlite3


def showAllStudents():
    zeiger.execute("Select * From Student;")
    res = zeiger.fetchall()
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
        matrNr = student.split(', ')[2]
        print("---",matrNr,"---")
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
        return False
    if any(letter.isdigit() for letter in nachname.get()) | (nachname.get() == ''):
        return False
    if any((not digit.isdigit() | (len(matrikelnummer.get()) != 7)) for digit in matrikelnummer.get()):
        return False
    if any((not digit.isdigit() |(len(alter.get()) not in [1, 2])) for digit in alter.get()):
        return False
    if geschlecht.get() not in ['m', 'w']:
        return False
    if any(not digit.isdigit() for digit in semester.get()) | (semester.get() == ''):
        return False
    zeiger.execute("SELECT * FROM Student Where matrikelnummer = " + matrikelnummer.get())
    connection.commit()
    res = zeiger.fetchone()
    if res != None:
        print("Ein anderer Student ist bereits unter dieser Matrikelnummer eingetragen.")
        return False
    return True

def insertedData():
    zeiger.execute("SELECT * FROM Student;")
    studentslist = []
    for data in zeiger.fetchall():
        studentslist.append(data[0] + ", " + data[1] + ", " + data[2] + ", " + data[3] + ", " + data[4] + ", " + data[5])
    return studentslist

def saveData():
    if dataisValid():
        #zeiger.execute("DELETE FROM Student;")
        #connection.commit()
        zeiger.execute("INSERT INTO Student VALUES ('" + vorname.get() + "', '" + nachname.get() + "', " + matrikelnummer.get() + ", " + alter.get() + ", '" + geschlecht.get() + "', " + semester.get() + ");")
        connection.commit()     # Committen ist wirklich wichtig, bevor naechste Operation ausgefuehrt wird
        deleteEntries()
        print("Daten erfolgreich gespeichert.")
        cb["values"] = insertedData()



def closing():
    connection.commit()
    connection.close()
    master.quit()

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

    tk.Button(master, text='Schließen', command=closing).grid(row=7, column=0, pady=4)
    tk.Button(master, text='Save', command=saveData).grid(row=6, column=0, pady=4)
    tk.Button(master, text='Anzeigen', command=showAllStudents).grid(row=7, column=1, pady=4)
    tk.Button(master, text='Löschen', command=deleteStudent).grid(row=0, column=3, pady=4)

    studentslist = insertedData()
    #insertData()

    cb = ttk.Combobox(master, state="readonly", values=studentslist)
    cb.grid(row=0, column=2, pady=5)
    if len(list(cb["values"])) > 0:
        cb.current(0)
    print("Studentslist:",studentslist)
    tk.mainloop()
