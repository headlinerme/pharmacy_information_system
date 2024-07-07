import psycopg2 as pg
from colorama import Fore


#Класс - база данных
class Database:
    def __init__(self):
        try:
            self.con = pg.connect(
                host="localhost", 
                database="pharmacy_db", 
                port=5432, 
                user="postgres", 
                password="123"
            )
            
            self.cur = self.con.cursor()
            print(Fore.GREEN + "[SUCCESS] Connection successful." + Fore.RESET)
            
        except Exception as error:
            print(Fore.RED + "[ERROR] Connection error." + Fore.RESET)
            print(error)
            
    def view(self, table_name):
        try:
            self.cur.execute(
                f"""
                SELECT *
                FROM {table_name}
                """
            )
            rows = self.cur.fetchall()
            return rows 
        
        except Exception as error:
            print(Fore.RED + "[ERROR] View command error." + Fore.RESET) 
            print(error)
            
    def __del__(self):
        self.con.close()

#Класс - таблица medicines
class Medicines(Database):
            
    def insert(self, medicines_id, medicines_name, medicines_type, application_method, price, doctor_prescription):
        try:
            self.cur.execute(
                f"""
                INSERT INTO medicines VALUES ({medicines_id}, '{medicines_name}', '{medicines_type}', '{application_method}', {price}, '{doctor_prescription}')
                """
            )
            self.con.commit()
        except Exception as error:
            print(Fore.RED + "[ERROR] Insert error." + Fore.RESET)
            print(error)
    
    def update(self, medicines_id, medicines_name, medicines_type, application_method, price, doctor_prescription): 
        try:
            self.cur.execute(
                f"""
                UPDATE medicines SET
                medicines_id = {medicines_id},
                medicines_name = '{medicines_name}',
                medicines_type = '{medicines_type}',
                application_method = '{application_method}',
                price = {price},
                doctor_prescription = '{doctor_prescription}'
                WHERE medicines_id = '{medicines_id}'
                """
            )
            self.con.commit()
            
        except Exception as error:
            print(Fore.RED + "[ERROR] Update error." + Fore.RESET)
            print(error)
    
    def delete(self, medicines_id):
        try:
            self.cur.execute(
                f"""
                DELETE FROM medicines
                WHERE medicines_id = {medicines_id}
                """
            )
            self.con.commit()
            
        except Exception as error:
            print(Fore.RED + "[ERROR] Delete error." + Fore.RESET)
            print(error)
    
    def sort_by_price(self):
        try:
            self.cur.execute(
                f"""
                SELECT *
                FROM medicines
                ORDER BY price ASC
                """
            )
            rows = self.cur.fetchall()
            return rows    
            
        except Exception as error:
            print(Fore.RED + "[ERROR] Sort error." + Fore.RESET)
            print(error)
            
    def sort_by_price_reverse(self):
        try:
            self.cur.execute(
                f"""
                SELECT *
                FROM medicines
                ORDER BY price DESC
                """
            )
            rows = self.cur.fetchall()
            return rows
            
        except Exception as error:
            print(Fore.RED + "[ERROR] Sort error." + Fore.RESET)
            print(error)

#Класс - таблица orders
class Orders(Database):
    
    def insert(self, order_id, patient_id, medicines_id, medicines_quantity, order_date, order_status):
        try:
            self.cur.execute(
                f"""
                INSERT INTO orders VALUES ({order_id}, {patient_id}, {medicines_id}, {medicines_quantity}, '{order_date}', '{order_status}')
                """
            )
            self.con.commit()
        except Exception as error:
            print(Fore.RED + "[ERROR] Insert error." + Fore.RESET)
            print(error)   
    
    def update(self, order_id, patient_id, medicines_id, medicines_quantity, order_date, order_status): 
        try:
            self.cur.execute(
                f"""
                UPDATE orders SET
                order_id = {order_id},
                patient_id = {patient_id},
                medicines_id = {medicines_id},
                medicines_quantity = {medicines_quantity},
                order_date = '{order_date}',
                order_status = '{order_status}'
                WHERE order_id = '{order_id}'
                """
            )
            self.con.commit()
            
        except Exception as error:
            print(Fore.RED + "[ERROR] Update error." + Fore.RESET)
            print(error)

    def delete(self, order_id):
        try:
            self.cur.execute(
                f"""
                DELETE FROM orders
                WHERE order_id = {order_id}
                """
            )
            self.con.commit()
            
        except Exception as error:
            print(Fore.RED + "[ERROR] Delete error." + Fore.RESET)
            print(error)

    def report(self):
        try:
            self.cur.execute(
                """
                SELECT COUNT (*) AS total_orders,
                AVG(medicines_quantity) AS average_quantity
                FROM orders
                """
            )
            rows = self.cur.fetchall()
            return rows
        
        except Exception as error:
            print("[ERROR] Report error.")
            print(error)

#Класс - таблица patients
class Patients(Database):

    def insert(self, patient_id, order_id, fullname, age, diagnosis, doctor_prescription):
        try:
            self.cur.execute(
                f"""
                INSERT INTO patients VALUES ({patient_id}, {order_id}, '{fullname}', {age}, '{diagnosis}', '{doctor_prescription}')
                """
            )
            self.con.commit()
        except Exception as error:
            print(Fore.RED + "[ERROR] Insert error." + Fore.RESET)
            print(error)

    def update(self, patient_id, order_id, fullname, age, diagnosis, doctor_prescription): 
        try:
            self.cur.execute(
                f"""
                UPDATE patients SET
                patient_id = {patient_id},
                order_id = {order_id},
                fullname = '{fullname}',
                age = {age},
                diagnosis = '{diagnosis}',
                doctor_prescription = '{doctor_prescription}'
                WHERE patient_id = '{patient_id}'
                """
            )
            self.con.commit()
            
        except Exception as error:
            print(Fore.RED + "[ERROR] Update error." + Fore.RESET)
            print(error)

    def delete(self, patient_id):
        try:
            self.cur.execute(
                f"""
                DELETE FROM patients
                WHERE patient_id = {patient_id}
                """
            )
            self.con.commit()
            
        except Exception as error:
            print(Fore.RED + "[ERROR] Delete error." + Fore.RESET)
            print(error)

    def report(self):
        try:
            self.cur.execute(
                """
                SELECT COUNT (*) AS total_patients,
                AVG(age) AS average_age
                FROM patients
                """
            )
            rows = self.cur.fetchall()
            return rows
        
        except Exception as error:
            print("[ERROR] Report error.")
            print(error)

#Класс - таблица technology_reference
class Technologies(Database):
    
    def insert(self, technology_id, medicines_id, medicines_name, preparation_method, preparation_time, required_components):
        try:
            self.cur.execute(
                f"""
                INSERT INTO technology_reference VALUES ({technology_id}, {medicines_id}, '{medicines_name}', '{preparation_method}', {preparation_time}, '{required_components}')
                """
            )
            self.con.commit()
        except Exception as error:
            print(Fore.RED + "[ERROR] Insert error." + Fore.RESET)
            print(error)
            
    def update(self, technology_id, medicines_id, medicines_name, preparation_method, preparation_time, required_components): 
        try:
            self.cur.execute(
                f"""
                UPDATE technology_reference SET
                technology_id = {technology_id},
                medicines_id = {medicines_id},
                medicines_name = '{medicines_name}',
                preparation_method = '{preparation_method}',
                preparation_time = '{preparation_time}',
                required_components = '{required_components}'
                WHERE technology_id = '{technology_id}'
                """
            )
            self.con.commit()
            
        except Exception as error:
            print(Fore.RED + "[ERROR] Update error." + Fore.RESET)
            print(error)  
    
    def delete(self, technology_id):
        try:
            self.cur.execute(
                f"""
                DELETE FROM technology_reference
                WHERE technology_id = {technology_id}
                """
            )
            self.con.commit()
            
        except Exception as error:
            print(Fore.RED + "[ERROR] Delete error." + Fore.RESET)
            print(error) 
