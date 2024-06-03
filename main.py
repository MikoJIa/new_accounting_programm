import sqlite3
import os
from tkinter import ttk
import tkinter as tk
from datetime import datetime
from tkcalendar import DateEntry
from tkinter import messagebox


window = tk.Tk()
window.title('Мини бухгалтерия')
window.geometry('1450x800')

db_name = 'accounting.db'


def add_to_table():
    lst_get = [ent_date.get(), entry_fio.get()]
    if all(lst_get):
        reply = messagebox.askyesno('Успех', 'Действительно добавить?')
        if reply == True:
            appointment_date = ent_date.get()
            date = ent_date.get()
            fio = entry_fio.get()
            fio_id = entry_fio_id.get()
            place_of_work = entry_place_work.get()
            job_title = entry_job_title.get()
            salary_advance = entry_salary_advance.get()
            salary = entry_salary.get()
            bet = entry_bet.get()
            vacation_pay = entry_vacation_pay.get()
            if checking_the_record() is True:
                if check_name(date, fio):
                    if check_data(fio_id):
                        with sqlite3.connect(db_name) as sqlite_conn:
                            sqlite_conn.execute('PRAGMA foreign_keys = ON')
                            insert_table = """INSERT INTO employees(
                            appointment_date, fio) VALUES(?, ?)"""
                            cursor = sqlite_conn.cursor()
                            cursor.execute(insert_table, (appointment_date, fio))
                            sqlite_conn.commit()
                            conn = sqlite3.connect(db_name)
                            cursor1 = conn.cursor()
                            [table.delete(i) for i in table.get_children()]
                            cursor1.execute("""SELECT * FROM employees ORDER BY appointment_date""")
                            rows = cursor1.fetchall()
                            print(rows)
                            for row in rows:
                                table.insert('', tk.END, values=row)
                        with sqlite3.connect(db_name) as sqlite_conn2:
                            sqlite_conn2.execute('PRAGMA foreign_keys = ON')
                            insert_table2 = """INSERT INTO info_employees(date, fio_id,
                            place_of_work, job_title, salary_advance, salary, bet, vacation_pay)
                             VALUES(?, ?, ?, ?, ?, ?, ?, ?)"""
                            cursor = sqlite_conn2.cursor()
                            cursor.execute(insert_table2, (date, fio_id, place_of_work, job_title,
                                                            salary_advance, salary, bet, vacation_pay))
                            sqlite_conn2.commit()
                            add_id = cursor.lastrowid
                            if check_data(fio_id):
                                messagebox.showinfo('Успех', 'Новая информация добавлена. Такое id- уже существует')
                            else:
                                table.insert('', tk.END, values=(add_id, date, fio))
                                ent_date.delete(0, tk.END)
                                entry_fio.delete(0, tk.END)
                                messagebox.showinfo('Успех', 'Новая информация добавлена')

            else:
                save_data()
        else:
            messagebox.showinfo('Неудача', 'В другой раз!')
    else:
        messagebox.showinfo('Внимание', 'Необходимо заполнить все обязательные поля:\n'
                                        'Дата\n'
                                        'ФИО\n')


def check_data(fio_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("""SELECT fio_id FROM info_employees WHERE fio_id=?""", (fio_id))
    row = cursor.fetchone()
    conn.close()
    if row:
        return False
    else:
        return True


def check_name(date, fio):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""INSERT OR IGNORE INTO employees(appointment_date, fio) VALUES(?, ?)""", (date, fio))
    conn.commit()
    cursor.execute("""SELECT id FROM employees WHERE fio=? and appointment_date=?""", (fio, date))
    id_name = cursor.fetchone()
    conn.close()
    if id_name:
        return False
    return True


def save_data():
    date = ent_date.get()
    fio = entry_fio.get()
    fio_id = entry_fio_id.get()
    place_of_work = entry_place_work.get()
    job_title = entry_job_title.get()
    salary_advance = entry_salary_advance.get()
    salary = entry_salary.get()
    bet = entry_bet.get()
    vacation_pay = entry_vacation_pay.get()
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    # cursor.execute('PRAGMA foreign_keys = ON')
    # if check_name(fio):
    #     cursor.execute("""INSERT INTO employees(date, fio) VALUES(?, ?)""", (date, fio))
    #     conn.commit()

    cursor.execute('PRAGMA foreign_keys = ON')
    cursor.execute("""INSERT INTO info_employees (date, fio_id, place_of_work, job_title,
                    salary_advance, salary,
                    bet, vacation_pay) VALUES(?, ?, ?, ?, ?, ?, ?, ?)""",
                   (date, fio_id, place_of_work, job_title,
                    salary_advance, salary, bet, vacation_pay)
                   )
    conn.commit()
    conn.close()
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    curr_row = table2.item(table2.focus())
    table2.delete(*table2.get_children())
    id_row = curr_row['values'][2]
    cursor.execute(f"""SELECT * FROM info_employees WHERE fio_id={id_row}""")
    rows = cursor.fetchall()
    for row in rows:
        table2.insert('', tk.END, values=row)


def get_selected_row(event):
    for i in table.selection():
        content = table.item(i, 'values')
        ent_date.delete(0, tk.END)
        ent_date.insert(tk.END, content[1])
        entry_fio.delete(0, tk.END)
        entry_fio.insert(tk.END, content[2])
        entry_fio_id.delete(0, tk.END)
        entry_fio_id.insert(tk.END, content[0])


def get_selected_row_table2(event):
    if table2.selection():
        item = table2.selection()[0]
        content2 = table2.item(item, 'values')
        entry_fio_id.delete(0, tk.END)
        entry_fio_id.insert(0, content2[2])
        entry_place_work.delete(0, tk.END)
        entry_place_work.insert(0, content2[3])
        entry_job_title.delete(0, tk.END)
        entry_job_title.insert(0, content2[4])
        entry_salary_advance.delete(0, tk.END)
        entry_salary_advance.insert(0, content2[5])
        entry_salary.delete(0, tk.END)
        entry_salary.insert(0, content2[6])
        entry_bet.delete(0, tk.END)
        entry_bet.insert(0, content2[7])
        entry_vacation_pay.delete(0, tk.END)
        entry_vacation_pay.insert(0, content2[8])


def on_select(event):
    select_item = table2.selection()[0]
    select_item_table1 = table.selection()
    if select_item:
        values = table2.item(select_item, option='values')
    table.selection_remove(select_item_table1)
    # print(values, select_item[-1:])


def update_data():
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

    select_item = table2.selection()
    if select_item:
        if not get_selected_row_table2:
            messagebox.showerror("Строка изменения не выброна", "Выберите строку для изменения")
            return
        reply = messagebox.askyesno('Успех', 'Выбранные вами данные будут изменены.\n '
                                             'Действительно изменить?\n')
        if reply:
            #  values = table2.item(select_item, option='values')
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            cursor.execute("""UPDATE info_employees SET date= :date, 
                                                                fio_id= :fio_id, 
                                                                place_of_work= :place_of_work,
                                                                job_title= :job_title,
                                                                salary_advance= :salary_advance,
                                                                salary= :salary,
                                                                bet= :bet,
                                                                vacation_pay= :vacation_pay
                                                                WHERE id=:id""",
                           {
                               'date': ent_date.get(),
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
            table2.item(select_item, values=(ent_date.get(), entry_fio_id.get(), entry_place_work.get(),
                                             entry_job_title.get(), entry_salary_advance.get(), entry_salary.get(),
                                             entry_bet.get(), entry_vacation_pay.get()))
        else:
            messagebox.showinfo('Error', 'В другой раз!!!')


# Проверка на наличие повторяющейся записи в первой таблице
def checking_the_record():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    item_row = table.selection()
    print(item_row)
    fio_id = entry_fio_id.get()
    id_of_the_row = None
    for row in cursor.execute(f"""SELECT * FROM employees WHERE id={fio_id}"""):
        id_of_the_row = row[0]
    if id_of_the_row is None:
        return True
    return False


def delete_data():
    id_fio = table.item(table.focus())
    cur_id = id_fio['values'][0]
    # print(cur_id)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f"""SELECT fio_id FROM info_employees WHERE fio_id={cur_id}""")
    count = len(cursor.fetchall())

    # curr_row = table.item(table.focus())
    # #curr_row = table.selection()[0]
    #
    # if curr_row:
    #     if count > 0:
    #         action = messagebox.showerror("Error", 'Эту запись вы удалить не можете!!!\n'
    #                              'У текущей записи есть значения во второй таблице')


    curr_row = table2.item(table2.focus())
    if curr_row:
        item_row = table2.selection()
        if item_row:
            action = messagebox.askyesno('info', 'Вы действительно хотите удалить?')
            if action == True:
                id_name = curr_row['values'][0]
                cursor.execute(f"""DELETE FROM info_employees WHERE id={id_name}""")
                conn.commit()
                conn.close()
                conn = sqlite3.connect(db_name)
                cursor = conn.cursor()
                messagebox.showinfo('Success', 'Информация успешно удалена!')
                table2.delete(*table2.get_children())
                id_row = curr_row['values'][2]
                cursor.execute(f"""SELECT * FROM info_employees WHERE fio_id={id_row}""")
                rows = cursor.fetchall()
                for row in rows:
                    table2.insert('', tk.END, values=row)
                conn.close()

            else:
                messagebox.showinfo('Error1', 'В другой раз!')
    curr_row = table.item(table.focus())
    if curr_row:
        if count == 0:
            action1 = messagebox.askyesno('Удаление', 'Вы действительно хотите удалить?')
            if action1 == True:
                id_item = curr_row['values'][0]
                cursor.execute(f"""DELETE FROM employees WHERE id={id_item}""")
                conn.commit()
                conn.close()
                conn = sqlite3.connect(db_name)
                cursor = conn.cursor()
                [table.delete(i) for i in table.get_children()]
                cursor.execute(f"""SELECT * FROM employees""")
                rows = cursor.fetchall()
                for row in rows:
                    table.insert('', tk.END, values=row)
                messagebox.showinfo('Успех', 'Информация успешно удалена')
            else:
                messagebox.showinfo('Error111', 'В другой раз!')
    else:
        messagebox.showinfo('info', 'В другой раз!')

    # curr_row = table.item(table.focus())
    curr_row = table.selection()
    if curr_row:
        if count > 0:
            action = messagebox.showerror("Error", 'Эту запись вы удалить не можете!!!\n'
                                                   'У текущей записи есть значения во второй таблице')


def search():
   search_window = tk.Tk()
   search_window.title('Окно поиска')
   search_window.geometry('400x250')
   search_window['bg'] = '#EEEED1'
   search_entry = tk.Entry(master=search_window, width=20,
                           font=('Arial', 20, 'bold'), relief=tk.SUNKEN, borderwidth=5)
   search_entry.place(x=50, y=50)
   search_btn = tk.Button(master=search_window, text='Найти', width=10,
                            font=('arial', 20, 'bold'), relief=tk.RAISED, borderwidth=5)
   search_btn.place(x=112, y=120)


def main_page():
    [table.delete(x) for x in table.get_children()]
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM employees ORDER BY appointment_date""")
    rows = cursor.fetchall()
    for row in rows:
        table.insert('', tk.END, values=row)


def clear_rows():
    ent_date.delete(0, tk.END)
    entry_fio.delete(0, tk.END)
    entry_fio_id.delete(0, tk.END)
    entry_place_work.delete(0, tk.END)
    entry_job_title.delete(0, tk.END)
    entry_salary_advance.delete(0, tk.END)
    entry_salary.delete(0, tk.END)
    entry_bet.delete(0, tk.END)
    entry_vacation_pay.delete(0, tk.END)


up_frame = tk.Frame(master=window,
                     relief=tk.SOLID,
                     borderwidth=2, bg='black')
up_frame.pack(anchor='nw', fill='x', padx=5, pady=5)

lbl_date = tk.Label(master=up_frame, text='Дата', font=('Aria', 12, 'bold'), bg='black', fg='yellow')
lbl_date.grid(row=0, column=0, sticky='e')
ent_date = DateEntry(up_frame, width=19, font=('Aria', 12), relief=tk.SUNKEN, borderwidth=3, date_pattern='dd.mm.yy')
ent_date.grid(row=0, column=1, padx=5, pady=5)

lbl_fio = tk.Label(master=up_frame, text='Ф.И.О', font=('Aria', 12, 'bold'), bg='black', fg='yellow')
lbl_fio.grid(row=1, column=0, sticky='e')
entry_fio = tk.Entry(master=up_frame, width=20, font=('Arial', 12, 'bold'), borderwidth=3)
entry_fio.grid(row=1, column=1, sticky='e', ipadx=6, ipady=6,)

lbl_fio_id = tk.Label(master=up_frame, text='ФИО_id', font=('Aria', 12, 'bold'), bg='black', fg='yellow')
lbl_fio_id.grid(row=2, column=0, sticky='e')
entry_fio_id = tk.Entry(master=up_frame, width=20, font=('Arial', 12, 'bold'), borderwidth=3)
entry_fio_id.grid(row=2, column=1, sticky='e', ipadx=6, ipady=6,)

lbl_place_work = tk.Label(master=up_frame, text='Место работы', font=('Aria', 12, 'bold'), bg='black', fg='yellow')
lbl_place_work.grid(row=0, column=2, sticky='e')
entry_place_work = tk.Entry(master=up_frame, width=20, font=('Arial', 12, 'bold'), borderwidth=3)
entry_place_work.grid(row=0, column=3, sticky='e', ipadx=6, ipady=6,)

lbl_job_title = tk.Label(master=up_frame, text='Должность', font=('Aria', 12, 'bold'), bg='black', fg='yellow')
lbl_job_title.grid(row=1, column=2, sticky='e')
entry_job_title = tk.Entry(master=up_frame, width=20, font=('Arial', 12, 'bold'), borderwidth=3)
entry_job_title.grid(row=1, column=3, sticky='e', ipadx=6, ipady=6,)

lbl_salary_advance = tk.Label(master=up_frame, text='Аванс', font=('Aria', 12, 'bold'), bg='black', fg='yellow')
lbl_salary_advance.grid(row=2, column=2, sticky='e')
entry_salary_advance = tk.Entry(master=up_frame, width=20, font=('Arial', 12, 'bold'), borderwidth=3)
entry_salary_advance.grid(row=2, column=3, sticky='e', ipadx=6, ipady=6,)

lbl_salary = tk.Label(master=up_frame, text='Зарплата', font=('Aria', 12, 'bold'), bg='black', fg='yellow')
lbl_salary.grid(row=0, column=4, sticky='e')
entry_salary = tk.Entry(master=up_frame, width=20, font=('Arial', 12, 'bold'), borderwidth=3)
entry_salary.grid(row=0, column=5, sticky='e', ipadx=6, ipady=6,)

lbl_bet = tk.Label(master=up_frame, text='Ставка', font=('Aria', 12, 'bold'), bg='black', fg='yellow')
lbl_bet.grid(row=1, column=4, sticky='e')
entry_bet = tk.Entry(master=up_frame, width=20, font=('Arial', 12, 'bold'), borderwidth=3)
entry_bet.grid(row=1, column=5, sticky='e', ipadx=6, ipady=6,)

lbl_vacation_pay = tk.Label(master=up_frame, text='Отпускные', font=('Aria', 12, 'bold'), bg='black', fg='yellow')
lbl_vacation_pay.grid(row=2, column=4, sticky='e')
entry_vacation_pay = tk.Entry(master=up_frame, width=20, font=('Arial', 12, 'bold'), borderwidth=3)
entry_vacation_pay.grid(row=2, column=5, sticky='e', ipadx=6, ipady=6,)

# Кнопки
btn_add_to_db = tk.Button(master=up_frame, text='Добавить', font=('Aria', 12, 'bold'),
                          width=15, bg='#E3CF57', command=add_to_table)
btn_add_to_db.place(x=890, y=4)

btn_delete = tk.Button(master=up_frame, text='Удалить', font=('Aria', 12, 'bold'), width=15, bg='#FF4040', command=delete_data)
btn_delete.place(x=890, y=42)

btn_update = tk.Button(master=up_frame, text='Изменить', font=('Aria', 12, 'bold'), width=15, bg='#CAFF70',
                       command=update_data)
btn_update.place(x=890, y=80)

btn_clear = tk.Button(master=up_frame, text='Очистить поля', font=('Aria', 12, 'bold'), width=15, bg='#CAFF70',
                      command=clear_rows)
btn_clear.place(x=1060, y=4)

btn_return_main = tk.Button(master=up_frame, text='Главная', font=('Aria', 12, 'bold'), width=15, bg='#CAFF70',
                            command=main_page)
btn_return_main.place(x=1060, y=42)

btn_search = tk.Button(master=up_frame, text='Поиск',
                       font=('Aria', 12, 'bold'),
                       width=15, bg='#FCE6C9', command=search)
btn_search.place(x=1060, y=80)

left_frame = tk.LabelFrame(master=window, relief=tk.SUNKEN, borderwidth=5, width=650, height=100, bg='silver')
left_frame.pack(side=tk.LEFT, fill=tk.BOTH)

right_frame = tk.LabelFrame(master=window, relief=tk.SUNKEN, borderwidth=5, width=700, height=100, bg='silver')
right_frame.pack(side=tk.RIGHT, fill='y')

# treeview 1

table = ttk.Treeview(left_frame, columns=('id', 'appointment_date', 'fio'), show='headings')
table.pack(side=tk.LEFT, fill=tk.BOTH)
# table['columns'] = ('id', 'date', 'fio')

scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=table.yview())
table.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


# table.column('#0', anchor='c', width=0)
table.column('id', anchor='c', width=40)
table.column('appointment_date', anchor='c', width=200)
table.column('fio', anchor='w', width=200)


def current_row(event):
    curr_item = table.item(table.focus())
    curr_item2 = table2.item(table2.focus())
    fio_id = curr_item['values'][0]
    with sqlite3.connect(db_name) as sqlite_conn:
        sqlite_request = f"""SELECT * FROM info_employees WHERE fio_id = {fio_id} ORDER BY fio_id"""
        cursor = sqlite_conn.cursor()
        cursor.execute(sqlite_request)
        sqlite_conn.commit()
        rows_info = cursor.fetchall()
        [table2.delete(item) for item in table2.get_children()]
    for row_info in rows_info:

        table2.insert('', tk.END, values=row_info)


# table.heading('#0', text='')
table.heading('id', text='ID')
table.heading('appointment_date', text='Дата назначения')
table.heading('fio', text='Ф.И.О')
table.bind('<ButtonRelease-1>', current_row)
table.bind("<<TreeviewSelect>>", get_selected_row)


# treeview 2
table2 = ttk.Treeview(right_frame, columns=('id', 'date', 'fio_id', 'place_of_work',
                                            'job_title', 'salary_advance',
                                            'salary', 'bet', 'vacation_pay'), show='headings')
table2.pack(side=tk.RIGHT, fill=tk.BOTH)
# table2['columns'] = ('fio_id', 'lbl_place_work',
#                      'job_title', 'salary_advance',
#                      'salary', 'bet', 'vacation_pay')

# table2.column('#0', width=0)
table2.column('id', anchor='c', width=25)
table2.column('date', anchor='c', width=60)
table2.column('fio_id', anchor='c', width=50)
table2.column('place_of_work', anchor='c', width=150)
table2.column('job_title', anchor='c', width=150)
table2.column('salary_advance', anchor='c', width=150)
table2.column('salary', anchor='c', width=150)
table2.column('bet', anchor='c', width=100)
table2.column('vacation_pay', anchor='c', width=100)

# table2.heading('#0', text='')
table2.heading('id', text='ID')
table2.heading('date', text='Дата')
table2.heading('fio_id', text='ФИО_id')
table2.heading('place_of_work', text='Место работы')
table2.heading('job_title', text='Должность')
table2.heading('salary_advance', text='Аванс')
table2.heading('salary', text='Зарплата')
table2.heading('bet', text='Ставка')
table2.heading('vacation_pay', text='Отпускные')
table2.bind('<ButtonRelease-1>', current_row)
table2.bind("<<TreeviewSelect>>", get_selected_row_table2)
table2.bind('<ButtonRelease-1>', on_select)

# Таблица №1 employees
try:
    with sqlite3.connect(db_name) as sqlite_conn:
        sqlite_conn.execute("PRAGMA foreign_keys = ON")
        if sqlite_conn:
            sql_request = """
             CREATE TABLE IF NOT EXISTS employees(
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             appointment_date DATE NOT NULL,
             fio TEXT NOT NULL
             )"""
            cursor = sqlite_conn.cursor()
            print('Successfully: The database is connected to sqlite3')
            cursor.execute(sql_request)
            sqlite_conn.commit()
            print('The table SQlite has been created')
except Exception as e:
    print(f'Error connecting to the database sqlite3: {e}')
finally:
    if sqlite_conn:
        print('Sqlite close!!!')

# Таблица №2 info_employees

try:
    with sqlite3.connect(db_name) as sqlite_conn:
        sqlite_conn.execute("PRAGMA foreign_keys = ON")
        create_table = """CREATE TABLE IF NOT EXISTS info_employees(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE,
        fio_id INTEGER,
        place_of_work TEXT,
        job_title TEXT,
        salary_advance TEXT,
        salary TEXT,
        bet TEXT,
        vacation_pay TEXT,
        FOREIGN KEY (fio_id) REFERENCES employees(id)
        )"""
        cursor = sqlite_conn.cursor()
        sqlite_conn.execute(create_table)
        print('Successfully: The database is connected to sqlite3')
        sqlite_conn.execute(create_table)
        sqlite_conn.commit()
        print(f'The table: info_employees SQlite has been created')
except Exception as e:
    print(f'Error connecting to the database sqlite3: {e}')
finally:
    if sqlite_conn:
        print('Sqlite close!!!')


def display_date():
    with sqlite3.connect(db_name) as sqlite_conn:
        display_db = """SELECT id, appointment_date, fio FROM employees ORDER BY appointment_date"""
        cursor = sqlite_conn.cursor()
        cursor.execute(display_db)
        rows = cursor.fetchall()
        rows_name = []
        item = []
        for row in rows:
            if row[2] not in rows_name:
                rows_name.append(row[2])
                item.append(row)
            else:
                rows_name = rows_name
        for i in item:
            table.insert('', tk.END, values=i)


display_date()
window.mainloop()
