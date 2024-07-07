import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

from PIL import ImageTk, Image

import pandas as pd

from database.database import *


#Фундамент приложения
class Application(tk.Tk):
    
    global database
    database = Database()

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.title("Pharmacy Information System")
        self.geometry("1000x600+150+50")
        
        menu = tk.Menu(self)
        submenu = tk.Menu(menu, tearoff=0)

        submenu.add_command(label="About program", command=lambda: self.show_frame("AboutProgramPage"))
        submenu.add_command(label="Exit", command=lambda: self.destroy())
 
        menu.add_cascade(label="Menu", menu=submenu)
        
        self.config(menu=menu)
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MainPage, EntryPage, AdminLoginPage, MenuPage, MedicinesPage, 
                OrdersPage, PatientsPage, TechnologiesPage, AboutProgramPage):
            
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        
    def show_frame_if_authorized(self, page_name, login, password):        
        if login == "admin" and password == "admin":
            frame = self.frames[page_name]
            frame.tkraise()
        else:
            showinfo("ERROR", "Неправильный логин и/или пароль!")
        
#Главная страница
class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        main_canvas = tk.Canvas(
            self,
            bg="White",
            width=1000,
            height=600
        )
        main_canvas.pack()
        
        self.main_image = ImageTk.PhotoImage(Image.open("images/main.png"))
        self.main_image.image = self.main_image
        
        main_canvas.create_image(500, 300, image=self.main_image)
        
        main_canvas.create_text(500, 250, font="Verdana 28", text="Pharmacy Information System", fill="#555")
        
        main_button = tk.Button(
            self,
            text="ENTRY",
            font=("Verdana", 14),
            fg="#555",
            border=0,
            width=10,
            height=3,
            command=lambda: controller.show_frame("EntryPage")
        )
        main_canvas.create_window(500, 320, window=main_button)

#Страница входа
class EntryPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        entry_canvas = tk.Canvas(
            self,
            bg="White",
            width=1000,
            height=600
        )
        entry_canvas.pack()
        
        entry_canvas.create_text(500, 150, font="Verdana 24", text="LOGIN AS", fill="#555")
        
        entry_canvas.create_text(500, 250, font="Verdana 18", text="EMPLOYEE")
        
        self.admin_login_image = ImageTk.PhotoImage(Image.open("images/employee.png").resize((100, 100)))
        self.admin_login_image.image = self.admin_login_image
        admin_login_button = tk.Button(
            self,
            image=self.admin_login_image,
            border=0,
            width=100,
            height=100,
            command=lambda: controller.show_frame("AdminLoginPage")
        )
        entry_canvas.create_window(500, 320, window=admin_login_button)
        
#Страница входа в роли админа
class AdminLoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller 
        
        admin_login_canvas = tk.Canvas(
            self, 
            bg="White",
            width=1000,
            height=600
        )
        admin_login_canvas.pack()
        
        admin_login_canvas.create_text(500, 150, font="Verdana 18", text="SIGN IN")
        
        admin_login_canvas.create_text(400, 220, font="Verdana 16", text="Login")
        admin_login_entry_login = tk.Entry(
            self
        )
        admin_login_canvas.create_window(550, 220, window=admin_login_entry_login)
        
        admin_login_canvas.create_text(400, 270, font="Verdana 16", text="Password")
        admin_login_entry_password = tk.Entry(
            self,
            show="*"
        )
        admin_login_canvas.create_window(550, 270, window=admin_login_entry_password)
        
        login_button = tk.Button(
            self,
            text="ENTER",
            border=0,
            width=4,
            height=2,
            command=lambda: controller.show_frame_if_authorized("MenuPage", 
                                                                admin_login_entry_login.get(), 
                                                                admin_login_entry_password.get())
            )
        admin_login_canvas.create_window(490, 350, window=login_button)
        
        back_button = tk.Button(
            self,
            text="BACK",
            border=0,
            width=4,
            height=2,
            command=lambda: controller.show_frame("EntryPage")
        )
        admin_login_canvas.create_window(580, 350, window=back_button)

#Страница меню
class MenuPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        menu_label = tk.Label(
            self,
            text="Manage tables",
            font=("Verdana", 24)
        )
        menu_label.pack(pady=120)
        
        medicines_button = tk.Button(
            self,
            text="Medicines",
            font=("Verdana", 16),
            width=16,
            height=3,
            command=lambda: controller.show_frame("MedicinesPage")
        )
        medicines_button.place(x=280, y=220)
        
        orders_button = tk.Button(
            self,
            text="Orders",
            font=("Verdana", 16),
            width=16,
            height=3,
            command=lambda: controller.show_frame("OrdersPage")
        )
        orders_button.place(x=280, y=300)
        
        patients_button = tk.Button(
            self,
            text="Patients",
            font=("Verdana", 16),
            width=16,
            height=3,
            command=lambda: controller.show_frame("PatientsPage")
        )
        patients_button.place(x=500, y=220)
        
        technologies_button = tk.Button(
            self,
            text="Technologies",
            font=("Verdana", 16),
            width=16,
            height=3,
            command=lambda: controller.show_frame("TechnologiesPage")
        )
        technologies_button.place(x=500, y=300)
        
#Страница управления таблицей medicines
class MedicinesPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        database = Medicines()
        
        back_button = tk.Button(
            self,
            text="Back",
            command=lambda: controller.show_frame("MenuPage")
        )
        back_button.place(x=10, y=10)
        
        def get_selected_row(event):
            try:
                global selected_tuple
                
                selected_item = medicines_table.selection()
                selected_tuple = medicines_table.item(selected_item)
                selected_tuple = selected_tuple["values"]

                medicines_id_entry.delete(0, "end")
                medicines_id_entry.insert(0, selected_tuple[0])
                medicines_name_entry.delete(0, "end")
                medicines_name_entry.insert(0, selected_tuple[1])
                medicines_type_entry.delete(0, "end")
                medicines_type_entry.insert(0, selected_tuple[2])
                application_method_entry.delete(0, "end")
                application_method_entry.insert(0, selected_tuple[3])
                price_entry.delete(0, "end")
                price_entry.insert(0, selected_tuple[4])
                doctor_entry.delete(0, "end")
                doctor_entry.insert(0, selected_tuple[5])
                
            except Exception as error:
                print(Fore.RED + "[ERROR] Tech error." + Fore.RESET)
                print(error)
        
        def view_command():
            for i in medicines_table.get_children():
                medicines_table.delete(i)
                
            for row in database.view("medicines"):
                medicines_table.insert("", "end", values=row)
                
        def search_command():

            query = search_entry.get()
            selections = []
                    
            for child in medicines_table.get_children():
                if query in medicines_table.item(child)['values']:
                    selections.append(medicines_table.item(child)['values'])
                        
            for i in medicines_table.get_children():
                medicines_table.delete(i)
            
            for s in selections:
                medicines_table.insert("", "end", values=s)         
        
        def sort_command(event):
            
            for i in medicines_table.get_children():
                medicines_table.delete(i)
                
            if sort_combobox.get() == "По возрастанию цены":
                
                for row in database.sort_by_price():
                    medicines_table.insert("", "end", values=row)
                    
            elif sort_combobox.get() == "По убыванию цены":
                
                for row in database.sort_by_price_reverse():
                    medicines_table.insert("", "end", values=row)
            
        def filter_command(event):
                
            if filter_combobox.get() == "Готовые":
                select_ready = []
                
                for child in medicines_table.get_children():
                    if "Готовые" in medicines_table.item(child)['values']:
                        select_ready.append(medicines_table.item(child)['values'])
                        
                for i in medicines_table.get_children():
                    medicines_table.delete(i)
                        
                for i in select_ready:
                    medicines_table.insert("", "end", values=i)
                    
                        
            elif filter_combobox.get() == "Изготовляемые":
                select_manufactured = []
                
                for child in medicines_table.get_children():
                    if "Изготовляемые" in medicines_table.item(child)['values']:
                        select_manufactured.append(medicines_table.item(child)['values'])
                        
                for i in medicines_table.get_children():
                    medicines_table.delete(i)
                        
                for i in select_manufactured:
                    medicines_table.insert("", "end", values=i)
                        
            elif filter_combobox.get() == "Нужен рецепт":
                select_recipe = []
                
                for child in medicines_table.get_children():
                    if "Y" in medicines_table.item(child)['values']:
                        select_recipe.append(medicines_table.item(child)['values'])
                        
                for i in medicines_table.get_children():
                    medicines_table.delete(i)
                        
                for i in select_recipe:
                    medicines_table.insert("", "end", values=i)
                
            elif filter_combobox.get() == "Рецепт не нужен":
                select_norecipe = []
                
                for child in medicines_table.get_children():
                    if "N" in medicines_table.item(child)['values']:
                        select_norecipe.append(medicines_table.item(child)['values'])
                        
                for i in medicines_table.get_children():
                    medicines_table.delete(i)
                        
                for i in select_norecipe:
                    medicines_table.insert("", "end", values=i)
        
        def add_command():
            for i in medicines_table.get_children():
                medicines_table.delete(i)
            
            database.insert(
                medicines_id.get(),
                medicines_name.get(),
                medicines_type.get(),
                application_method.get(),
                price.get(),
                doctor.get()
            )
            
            medicines_table.insert("", "end",
                (
                    medicines_id.get(),
                    medicines_name.get(),
                    medicines_type.get(),
                    application_method.get(),
                    price.get(),
                    doctor.get()
                )
            )
            
        def update_command(): 
            database.update(
                selected_tuple[0],
                medicines_name.get(),
                medicines_type.get(),
                application_method.get(),
                price.get(),
                doctor.get()
            )
                
        def delete_command():
            database.delete(selected_tuple[0])
        
        medicines_label = tk.Label(
            self,
            text="Таблица 'ЛЕКАРСТВА' (medicines)",
            font=("Verdana", 18)
        )
        medicines_label.pack(pady=10)
        
        search_entry = tk.Entry(
            self,
            width=16
        )
        search_entry.place(x=80, y=50)
        
        search_button = tk.Button(
            self,
            text="Search",
            width=4,
            command=search_command
        )
        search_button.place(x=240, y=48)
        
        sort_label = tk.Label(
            self,
            text="Sort",
            font=("Verdana", 14)
        )
        sort_label.place(x=480, y=50)
        
        sort_combobox = ttk.Combobox(
            self,
            width=16,
            values=["По возрастанию цены", "По убыванию цены"]
        )
        sort_combobox.place(x=525, y=48)
        
        sort_combobox.bind("<<ComboboxSelected>>", sort_command)
        
        filter_label = tk.Label(
            self,
            text="Filter",
            font=("Verdana", 14)
        )
        filter_label.place(x=710, y=50)
        
        filter_combobox = ttk.Combobox(
            self,
            width=16,
            values=["Готовые", "Изготовляемые", "Нужен рецепт", "Рецепт не нужен"]
        )
        filter_combobox.place(x=760, y=48)
        
        filter_combobox.bind("<<ComboboxSelected>>", filter_command)
        
        medicines_id_label = tk.Label(
            self,
            text="ID",
            font=("Verdana", 14)
        )
        medicines_id_label.place(x=80, y=480)
        
        medicines_id = tk.StringVar()
        medicines_id_entry = tk.Entry(
            self,
            width=16,
            textvariable=medicines_id
        )
        medicines_id_entry.place(x=160, y=480)
        
        medicines_name_label = tk.Label(
            self,
            text="Название",
            font=("Verdana", 14)
        )
        medicines_name_label.place(x=80, y=520)
        
        medicines_name = tk.StringVar()
        medicines_name_entry = tk.Entry(
            self,
            width=16,
            textvariable=medicines_name
        )
        medicines_name_entry.place(x=160, y=520)
        
        medicines_type_label = tk.Label(
            self,
            text="Тип",
            font=("Verdana", 14)
        )
        medicines_type_label.place(x=370, y=480)
        
        medicines_type = tk.StringVar()
        medicines_type_entry = tk.Entry(
            self,
            width=16,
            textvariable=medicines_type
        )
        medicines_type_entry.place(x=440, y=480)
        
        application_method_label = tk.Label(
            self,
            text="Способ",
            font=("Verdana", 14)
        )
        application_method_label.place(x=370, y=520)
        
        application_method = tk.StringVar()
        application_method_entry = tk.Entry(
            self,
            width=16,
            textvariable=application_method
        )
        application_method_entry.place(x=440, y=520)
        
        price_label = tk.Label(
            self,
            text="Цена",
            font=("Verdana", 14)
        )
        price_label.place(x=660, y=480)
        
        price = tk.StringVar()
        price_entry = tk.Entry(
            self,
            width=16,
            textvariable=price
        )
        price_entry.place(x=780, y=480)
        
        doctor_label = tk.Label(
            self,
            text="Рецепт(Y/N)",
            font=("Verdana", 14)
        )
        doctor_label.place(x=660, y=520)
        
        doctor = tk.StringVar()
        doctor_entry = tk.Entry(
            self,
            width=16,
            textvariable=doctor
        )
        doctor_entry.place(x=780, y=520)
        
        medicines_table = ttk.Treeview(
            self,
            columns=("medicines_id", "medicines_name", "medicines_type", 
                    "application_method", "price", "doctor"),
            show="headings",
            height=20
        )
        medicines_table.place(x=80, y=80)
        
        medicines_table.heading("medicines_id", text="ID")
        medicines_table.heading("medicines_name", text="Название лекарства")
        medicines_table.heading("medicines_type", text="Тип лекарства")
        medicines_table.heading("application_method", text="Способ применения")
        medicines_table.heading("price", text="Цена")
        medicines_table.heading("doctor", text="Рецепт")
        
        medicines_table.column("#1", width=50)
        medicines_table.column("#5", width=100)
        medicines_table.column("#6", width=100)
        
        medicines_sb = tk.Scrollbar(
            self,
            orient="vertical",
            command=medicines_table.yview
        )
        medicines_sb.place(x=950, y=165)
        
        medicines_table.configure(yscrollcommand=medicines_sb.set)
        medicines_sb.configure(command=medicines_table.yview)

        medicines_table.bind("<<TreeviewSelect>>", get_selected_row)
        
        view_button = tk.Button(
            self,
            text="View",
            width=12,
            command=view_command
        )
        view_button.place(x=140, y=560)
        
        add_button = tk.Button(
            self,
            text="Add",
            width=12,
            command=add_command
        )
        add_button.place(x=340, y=560)
        
        update_button = tk.Button(
            self,
            text="Update",
            width=12,
            command=update_command
        )
        update_button.place(x=540, y=560)
        
        delete_button = tk.Button(
            self,
            text="Delete",
            width=12,
            command=delete_command
        )
        delete_button.place(x=740, y=560)
      
#Страница управления таблицей orders
class OrdersPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        database = Orders()
        
        def get_selected_row(event):
            try:
                global selected_tuple
                
                selected_item = orders_table.selection()
                selected_tuple = orders_table.item(selected_item)
                selected_tuple = selected_tuple["values"]

                order_id_entry.delete(0, "end")
                order_id_entry.insert(0, selected_tuple[0])
                patient_id_entry.delete(0, "end")
                patient_id_entry.insert(0, selected_tuple[1])
                medicines_id_entry.delete(0, "end")
                medicines_id_entry.insert(0, selected_tuple[2])
                medicines_quantity_entry.delete(0, "end")
                medicines_quantity_entry.insert(0, selected_tuple[3])
                order_date_entry.delete(0, "end")
                order_date_entry.insert(0, selected_tuple[4])
                order_status_entry.delete(0, "end")
                order_status_entry.insert(0, selected_tuple[5])
                
            except Exception as error:
                print(Fore.RED + "[ERROR] Tech error." + Fore.RESET)
                print(error)
        
        def view_command():
            for i in orders_table.get_children():
                orders_table.delete(i)
                
            for row in database.view("orders"):
                orders_table.insert("", "end", values=row)
        
        def add_command():
            for i in orders_table.get_children():
                orders_table.delete(i)
            
            database.insert(
                order_id.get(),
                patient_id.get(),
                medicines_id.get(),
                medicines_quantity.get(),
                order_date.get(),
                order_status.get()
            )
            
            orders_table.insert("", "end",
                (
                    order_id.get(),
                    patient_id.get(),
                    medicines_id.get(),
                    medicines_quantity.get(),
                    order_date.get(),
                    order_status.get()
                )
            )        
        
        def update_command(): 
            database.update(
                selected_tuple[0],
                patient_id.get(),
                medicines_id.get(),
                medicines_quantity.get(),
                order_date.get(),
                order_status.get()
            )
        
        def delete_command():
            database.delete(selected_tuple[0])
        
        def make_report():
            df = pd.DataFrame({"Общее количество заказов": [int(database.report()[0][0])],
                               "Среднее количество лекарств в заказе": [int(database.report()[0][1])]
                            })
            df.to_excel("reports/report1.xlsx", sheet_name="orders_report", index=False)
                
        back_button = tk.Button(
            self,
            text="Back",
            command=lambda: controller.show_frame("MenuPage")
        )
        back_button.place(x=10, y=10)
        
        report_button = tk.Button(
            self,
            text="Report",
            command=make_report
        )
        report_button.place(x=900, y=10)
        
        orders_label = tk.Label(
            self,
            text="Таблица 'ЗАКАЗЫ' (orders)",
            font=("Verdana", 18)
        )
        orders_label.pack(pady=10)
        
        order_id_label = tk.Label(
            self,
            text="ID",
            font=("Verdana", 14)
        )
        order_id_label.place(x=80, y=480)
        
        order_id = tk.StringVar()
        order_id_entry = tk.Entry(
            self,
            width=16,
            textvariable=order_id
        )
        order_id_entry.place(x=180, y=480)
        
        patient_id_label = tk.Label(
            self,
            text="ID Пациента",
            font=("Verdana", 14)
        )
        patient_id_label.place(x=80, y=520)
        
        patient_id = tk.StringVar()
        patient_id_entry = tk.Entry(
            self,
            width=16,
            textvariable=patient_id
        )
        patient_id_entry.place(x=180, y=520)
        
        medicines_id_label = tk.Label(
            self,
            text="ID Лекарства",
            font=("Verdana", 14)
        )
        medicines_id_label.place(x=390, y=480)
        
        medicines_id = tk.StringVar()
        medicines_id_entry = tk.Entry(
            self,
            width=16,
            textvariable=medicines_id
        )
        medicines_id_entry.place(x=500, y=480)
        
        medicines_quantity_label = tk.Label(
            self,
            text="Количество",
            font=("Verdana", 14)
        )
        medicines_quantity_label.place(x=390, y=520)
        
        medicines_quantity = tk.StringVar()
        medicines_quantity_entry = tk.Entry(
            self,
            width=16,
            textvariable=medicines_quantity
        )
        medicines_quantity_entry.place(x=500, y=520)
        
        order_date_label = tk.Label(
            self,
            text="Дата",
            font=("Verdana", 14)
        )
        order_date_label.place(x=720, y=480)
        
        order_date = tk.StringVar()
        order_date_entry = tk.Entry(
            self,
            width=16,
            textvariable=order_date
        )
        order_date_entry.place(x=780, y=480)
        
        order_status_label = tk.Label(
            self,
            text="Статус",
            font=("Verdana", 14)
        )
        order_status_label.place(x=720, y=520)
        
        order_status = tk.StringVar()
        order_status_entry = tk.Entry(
            self,
            width=16,
            textvariable=order_status
        )
        order_status_entry.place(x=780, y=520)
        
        orders_table = ttk.Treeview(
            self,
            columns=("order_id", "patient_id", "medicines_id", 
                    "medicines_quantity", "order_date", "order_status"),
            show="headings",
            height=20
        )
        orders_table.place(x=80, y=80)
        
        orders_table.heading("order_id", text="ID")
        orders_table.heading("patient_id", text="ID Пациента")
        orders_table.heading("medicines_id", text="ID Лекарства")
        orders_table.heading("medicines_quantity", text="Количество")
        orders_table.heading("order_date", text="Дата заказа")
        orders_table.heading("order_status", text="Статус заказа")
        
        orders_table.column("#1", width=50)
        orders_table.column("#2", width=100)
        orders_table.column("#3", width=100)
        
        orders_sb = tk.Scrollbar(
            self,
            orient="vertical",
            command=orders_table.yview
        )
        orders_sb.place(x=950, y=165)
        
        orders_table.configure(yscrollcommand=orders_sb.set)
        orders_sb.configure(command=orders_table.yview)

        orders_table.bind("<<TreeviewSelect>>", get_selected_row)
        
        view_button = tk.Button(
            self,
            text="View",
            width=12,
            command=view_command
        )
        view_button.place(x=140, y=560)
        
        add_button = tk.Button(
            self,
            text="Add",
            width=12,
            command=add_command
        )
        add_button.place(x=340, y=560)
        
        update_button = tk.Button(
            self,
            text="Update",
            width=12,
            command=update_command
        )
        update_button.place(x=540, y=560)
        
        delete_button = tk.Button(
            self,
            text="Delete",
            width=12,
            command=delete_command
        )
        delete_button.place(x=740, y=560)
        
#Страница управления таблицей patients
class PatientsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        database = Patients()
        
        def get_selected_row(event):
            try:
                global selected_tuple
                
                selected_item = patient_table.selection()
                selected_tuple = patient_table.item(selected_item)
                selected_tuple = selected_tuple["values"]

                patient_id_entry.delete(0, "end")
                patient_id_entry.insert(0, selected_tuple[0])
                order_id_entry.delete(0, "end")
                order_id_entry.insert(0, selected_tuple[1])
                fullname_entry.delete(0, "end")
                fullname_entry.insert(0, selected_tuple[2])
                age_entry.delete(0, "end")
                age_entry.insert(0, selected_tuple[3])
                diagnosis_entry.delete(0, "end")
                diagnosis_entry.insert(0, selected_tuple[4])
                doctor_entry.delete(0, "end")
                doctor_entry.insert(0, selected_tuple[5])
                
            except Exception as error:
                print(Fore.RED + "[ERROR] Tech error." + Fore.RESET)
                print(error)
        
        def view_command():
            for i in patient_table.get_children():
                patient_table.delete(i)
                
            for row in database.view("patients"):
                patient_table.insert("", "end", values=row)
        
        def add_command():
            for i in patient_table.get_children():
                patient_table.delete(i)
            
            database.insert(
                patient_id.get(),
                order_id.get(),
                fullname.get(),
                age.get(),
                diagnosis.get(),
                doctor.get()
            )
            
            patient_table.insert("", "end",
                (
                    patient_id.get(),
                    order_id.get(),
                    fullname.get(),
                    age.get(),
                    diagnosis.get(),
                    doctor.get()
                )
            )       
        
        def update_command(): 
            database.update(
                selected_tuple[0],
                order_id.get(),
                fullname.get(),
                age.get(),
                diagnosis.get(),
                doctor.get()
            )
        
        def delete_command():
            database.delete(selected_tuple[0])
        
        def make_report():
            df = pd.DataFrame({"Общее количество пациентов": [int(database.report()[0][0])],
                               "Средний возраст пациентов": [int(database.report()[0][1])]
                            })
            df.to_excel("reports/report2.xlsx", sheet_name="patients_report", index=False)
        
        back_button = tk.Button(
            self,
            text="Back",
            command=lambda: controller.show_frame("MenuPage")
        )
        back_button.place(x=10, y=10)
        
        report_button = tk.Button(
            self,
            text="Report",
            command=make_report
        )
        report_button.place(x=900, y=10)
        
        patients_label = tk.Label(
            self,
            text="Таблица 'ПАЦИЕНТЫ' (patients)",
            font=("Verdana", 18)
        )
        patients_label.pack(pady=10)
        
        patient_id_label = tk.Label(
            self,
            text="ID",
            font=("Verdana", 14)
        )
        patient_id_label.place(x=80, y=480)
        
        patient_id = tk.StringVar()
        patient_id_entry = tk.Entry(
            self,
            width=16,
            textvariable=patient_id
        )
        patient_id_entry.place(x=160, y=480)
        
        order_id_label = tk.Label(
            self,
            text="ID Заказа",
            font=("Verdana", 14)
        )
        order_id_label.place(x=80, y=520)
        
        order_id = tk.StringVar()
        order_id_entry = tk.Entry(
            self,
            width=16,
            textvariable=patient_id
        )
        order_id_entry.place(x=160, y=520)
        
        fullname_label = tk.Label(
            self,
            text="Полное имя",
            font=("Verdana", 14)
        )
        fullname_label.place(x=370, y=480)
        
        fullname = tk.StringVar()
        fullname_entry = tk.Entry(
            self,
            width=16,
            textvariable=fullname
        )
        fullname_entry.place(x=470, y=480)
        
        age_label = tk.Label(
            self,
            text="Возраст",
            font=("Verdana", 14)
        )
        age_label.place(x=370, y=520)
        
        age = tk.StringVar()
        age_entry = tk.Entry(
            self,
            width=16,
            textvariable=age
        )
        age_entry.place(x=470, y=520)
        
        diagnosis_label = tk.Label(
            self,
            text="Диагноз",
            font=("Verdana", 14)
        )
        diagnosis_label.place(x=670, y=480)
        
        diagnosis = tk.StringVar()
        diagnosis_entry = tk.Entry(
            self,
            width=16,
            textvariable=diagnosis
        )
        diagnosis_entry.place(x=740, y=480)
        
        doctor_label = tk.Label(
            self,
            text="Рецепт",
            font=("Verdana", 14)
        )
        doctor_label.place(x=670, y=520)
        
        doctor = tk.StringVar()
        doctor_entry = tk.Entry(
            self,
            width=16,
            textvariable=doctor
        )
        doctor_entry.place(x=740, y=520)
        
        patient_table = ttk.Treeview(
            self,
            columns=("patient_id", "order_id", "fullname", 
                    "age", "diagnosis", "doctor_prescription"),
            show="headings",
            height=20
        )
        patient_table.place(x=80, y=80)
        
        patient_table.heading("patient_id", text="ID")
        patient_table.heading("order_id", text="ID Заказа")
        patient_table.heading("fullname", text="Полное имя")
        patient_table.heading("age", text="Возраст")
        patient_table.heading("diagnosis", text="Диагноз")
        patient_table.heading("doctor_prescription", text="Рецепт(Y/N)")
        
        patient_table.column("#1", width=50)
        patient_table.column("#2", width=80)
        patient_table.column("#4", width=80)
        
        patient_sb = tk.Scrollbar(
            self,
            orient="vertical",
            command=patient_table.yview
        )
        patient_sb.place(x=950, y=165)
        
        patient_table.configure(yscrollcommand=patient_sb.set)
        patient_sb.configure(command=patient_table.yview)

        patient_table.bind("<<TreeviewSelect>>", get_selected_row)
        
        
        view_button = tk.Button(
            self,
            text="View",
            width=12,
            command=view_command
        )
        view_button.place(x=120, y=560)
        
        add_button = tk.Button(
            self,
            text="Add",
            width=12,
            command=add_command
        )
        add_button.place(x=320, y=560)
        
        update_button = tk.Button(
            self,
            text="Update",
            width=12,
            command=update_command
        )
        update_button.place(x=520, y=560)
        
        delete_button = tk.Button(
            self,
            text="Delete",
            width=12,
            command=delete_command
        )
        delete_button.place(x=720, y=560)
        
#Страница управления таблицей technology_reference       
class TechnologiesPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        database = Technologies()
        
        def get_selected_row(event):
            try:
                global selected_tuple
                
                selected_item = technologies_table.selection()
                selected_tuple = technologies_table.item(selected_item)
                selected_tuple = selected_tuple["values"]

                technology_id_entry.delete(0, "end")
                technology_id_entry.insert(0, selected_tuple[0])
                medicines_id_entry.delete(0, "end")
                medicines_id_entry.insert(0, selected_tuple[1])
                medicines_name_entry.delete(0, "end")
                medicines_name_entry.insert(0, selected_tuple[2])
                preparation_method_entry.delete(0, "end")
                preparation_method_entry.insert(0, selected_tuple[3])
                preparation_time_entry.delete(0, "end")
                preparation_time_entry.insert(0, selected_tuple[4])
                required_entry.delete(0, "end")
                required_entry.insert(0, selected_tuple[5])
                
            except Exception as error:
                print(Fore.RED + "[ERROR] Tech error." + Fore.RESET)
                print(error)
        
        def view_command():
            for i in technologies_table.get_children():
                technologies_table.delete(i)
                
            for row in database.view("technology_reference"):
                technologies_table.insert("", "end", values=row)        
        
        def add_command():
            for i in technologies_table.get_children():
                technologies_table.delete(i)
            
            database.insert(
                technology_id.get(),
                medicines_id.get(),
                medicines_name.get(),
                preparation_method.get(),
                preparation_time.get(),
                required.get()
            )
            
            technologies_table.insert("", "end",
                (
                    technology_id.get(),
                    medicines_id.get(),
                    medicines_name.get(),
                    preparation_method.get(),
                    preparation_time.get(),
                    required.get()
                )
            )
        
        def update_command(): 
            database.update(
                selected_tuple[0],
                medicines_id.get(),
                medicines_name.get(),
                preparation_method.get(),
                preparation_time.get(),
                required.get()
            )        
        
        def delete_command():
            database.delete(selected_tuple[0])
        
        back_button = tk.Button(
            self,
            text="Back",
            command=lambda: controller.show_frame("MenuPage")
        )
        back_button.place(x=10, y=10)
        
        technologies_label = tk.Label(
            self,
            text="Таблица 'ТЕХНОЛОГИИ' (technology_reference)",
            font=("Verdana", 18)
        )
        technologies_label.pack(pady=10)
        
        technology_id_label = tk.Label(
            self,
            text="ID",
            font=("Verdana", 14)
        )
        technology_id_label.place(x=80, y=480)
        
        technology_id = tk.StringVar()
        technology_id_entry = tk.Entry(
            self,
            width=16,
            textvariable=technology_id
        )
        technology_id_entry.place(x=200, y=480)
        
        medicines_id_label = tk.Label(
            self,
            text="ID Лекарства",
            font=("Verdana", 14)
        )
        medicines_id_label.place(x=80, y=520)
        
        medicines_id = tk.StringVar()
        medicines_id_entry = tk.Entry(
            self,
            width=16,
            textvariable=medicines_id
        )
        medicines_id_entry.place(x=200, y=520)
        
        medicines_name_label = tk.Label(
            self,
            text="Название",
            font=("Verdana", 14)
        )
        medicines_name_label.place(x=390, y=480)
        
        medicines_name = tk.StringVar()
        medicines_name_entry = tk.Entry(
            self,
            width=16,
            textvariable=medicines_name
        )
        medicines_name_entry.place(x=470, y=480)
        
        preparation_method_label = tk.Label(
            self,
            text="Способ",
            font=("Verdana", 14)
        )
        preparation_method_label.place(x=390, y=520)
        
        preparation_method = tk.StringVar()
        preparation_method_entry = tk.Entry(
            self,
            width=16,
            textvariable=preparation_method
        )
        preparation_method_entry.place(x=470, y=520)
        
        preparation_time_label = tk.Label(
            self,
            text="Время",
            font=("Verdana", 14)
        )
        preparation_time_label.place(x=660, y=480)
        
        preparation_time = tk.StringVar()
        preparation_time_entry = tk.Entry(
            self,
            width=16,
            textvariable=preparation_time
        )
        preparation_time_entry.place(x=760, y=480)
        
        required_label = tk.Label(
            self,
            text="Необходимо",
            font=("Verdana", 14)
        )
        required_label.place(x=660, y=520)
        
        required = tk.StringVar()
        required_entry = tk.Entry(
            self,
            width=16,
            textvariable=required
        )
        required_entry.place(x=760, y=520)
        
        technologies_table = ttk.Treeview(
            self,
            columns=("technology_id", "medicines_id", "medicines_name", 
                    "preparation_method", "preparation_time", "required_components"),
            show="headings",
            height=20
        )
        technologies_table.place(x=80, y=80)
        
        technologies_table.heading("technology_id", text="ID")
        technologies_table.heading("medicines_id", text="ID Лекарства")
        technologies_table.heading("medicines_name", text="Название")
        technologies_table.heading("preparation_method", text="Способ")
        technologies_table.heading("preparation_time", text="Время")
        technologies_table.heading("required_components", text="Необходимо")
        
        technologies_table.column("#1", width=50)
        technologies_table.column("#2", width=100)
        technologies_table.column("#5", width=80)
        
        technologies_sb = tk.Scrollbar(
            self,
            orient="vertical",
            command=technologies_table.yview
        )
        technologies_sb.place(x=950, y=165)
        
        technologies_table.configure(yscrollcommand=technologies_sb.set)
        technologies_sb.configure(command=technologies_table.yview)

        technologies_table.bind("<<TreeviewSelect>>", get_selected_row)
        
        view_button = tk.Button(
            self,
            text="View",
            width=12,
            command=view_command
        )
        view_button.place(x=120, y=560)
        
        add_button = tk.Button(
            self,
            text="Add",
            width=12,
            command=add_command
        )
        add_button.place(x=320, y=560)
        
        update_button = tk.Button(
            self,
            text="Update",
            width=12,
            command=update_command
        )
        update_button.place(x=520, y=560)
        
        delete_button = tk.Button(
            self,
            text="Delete",
            width=12,
            command=delete_command
        )
        delete_button.place(x=720, y=560)
        
#Страница о программе
class AboutProgramPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        about_label = tk.Label(
            self,
            text="О программе",
            font=("Verdana", 36)
        )
        about_label.pack(pady=40)
        
        about_sublabel = tk.Label(
            self,
            text="Программа разработана для управления информационной системой аптеки.",
            font=("Verdana", 16)
        )
        about_sublabel.pack()
        
        rights_label = tk.Label(
            self,
            font=("Verdana", 14),
            text="Все права защищены"
        )
        rights_label.pack(side="bottom", pady=40)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
