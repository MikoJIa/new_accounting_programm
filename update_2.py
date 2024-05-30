import sqlite3
from tkinter import messagebox

from main import table2, get_selected_row_table2, db_name, entry_fio_id, entry_place_work, entry_job_title, \
    entry_salary_advance, entry_salary, entry_bet, entry_vacation_pay


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