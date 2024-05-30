import sqlite3
from tkinter import messagebox
from main import *


def update_table1():
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


def update_table2():
    select_item = table2.selection()
    if select_item:
        if not get_selected_row_table2:
            messagebox.showerror("Строка изменения не выброна", "Выберите строку для изменения")
            return
        reply = messagebox.askyesno('Успех', 'Выбранные вами данные будут изменены.\n '
                                             'Действительно изменить?\n')
        if reply:
            values = table2.item(select_item, option='values')
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            cursor.execute("""UPDATE info_employees SET fio_id= :fio_id, 
                                                            place_of_work= :place_of_work,
                                                            job_title= :job_title,
                                                            salary_advance= :salary_advance,
                                                            salary= :salary,
                                                            bet= :bet,
                                                            vacation_pay= :vacation_pay
                                                            WHERE id=:id""",
                           {
                               'fio_id': entry_fio_id.get(),
                               'place_of_work': entry_place_work.get(),
                               'job_title': entry_job_title.get(),
                               'salary_advance': entry_salary_advance.get(),
                               'salary': entry_salary.get(),
                               'bet': entry_bet.get(),
                               'vacation_pay': entry_vacation_pay.get(),
                               'id': table2.set(select_item, '#1'),
                           })
            conn.commit()
            conn.close()
            add_id = select_item[-1:]
            table2.item(select_item, values=(add_id, entry_fio_id.get(), entry_place_work.get(),
                                             entry_job_title.get(), entry_salary_advance.get(), entry_salary.get(),
                                             entry_bet.get(), entry_vacation_pay.get()))
        else:
            messagebox.showinfo('Error', 'В другой раз!!!')
    else:
        update_table1()