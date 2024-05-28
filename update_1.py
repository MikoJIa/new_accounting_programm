import sqlite3
import os
from tkinter import ttk
import tkinter as tk
from datetime import datetime
from tkcalendar import DateEntry
from tkinter import messagebox
from main import table, get_selected_row, ent_date, entry_fio, db_name


def update_data_date_fio():
    item_row = table.selection()
    if item_row:
        if not get_selected_row:
            messagebox.showerror("Строка изменения не выброна", "Выберите строку для изменения")
            return
        reply = messagebox.askyesno('Успех', 'Выбранные вами данные будут изменены.\n'
                                             'Действительно изменить?\n')
        if reply:
            tran_id = table.set(item_row, '#1')
            date = ent_date.get()
            fio = entry_fio.get()
            for select in item_row:
                ent_date.insert(0, select)
                entry_fio.insert(0, select)

            with sqlite3.connect(db_name) as conn:
                sqlite_update = """UPDATE employees SET date=?, fio=? WHERE id=?"""
                cursor = conn.cursor()
                cursor.execute(sqlite_update, (date, fio, tran_id))
            table.item(item_row, values=(tran_id, date, fio))
            conn.commit()
        else:
            messagebox.showinfo('Error', 'В другой раз!!!')