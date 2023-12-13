import threading
from tkinter import messagebox, ttk
from src.gui.interface import Interface
from src.mysql_conn.establish_connection import establish_database_connection
from src.mysql_conn.mysql_utils import fetch_data_from_manufacturer, fetch_data_from_product, get_table_names_and_columns, insert_into_manufacturer, insert_into_product
from src.mongo_conn.establish_mongo_connection import establish_mongo_database_connection, get_collection_contents, insert_into_manufacturer_mongo, update_manufacturer_mongo

class MainApp:
    def __init__(self):
        self.server = None
        self.host = None
        self.password = None
        self.database = None

        self.ip = None
        self.port = None
        self.database_name = None
        self.collection_name = None
        self.client = None

        self.table_name = None
        self.table_columns = None
        self.insert_entries = {}

        self.interface = Interface()
        self.interface.login_button.bind("<Button-1>", lambda event: self.handle_login_button_click())

    def handle_login_button_click(self):
        login_data = self.interface.get_mysql_login_data()
        mongo_login_data = self.interface.get_mongo_login_data()
        
        self.server = login_data[0]
        self.host = login_data[1]
        self.password = login_data[2]
        self.database = login_data[3]

        self.ip = mongo_login_data[0]
        self.port = mongo_login_data[1]
        self.database_name = mongo_login_data[2]
        self.collection_name = mongo_login_data[3]

        mysql_conn = establish_database_connection(self.server, self.host, self.password, self.database)
        self.client = mongo_conn = establish_mongo_database_connection(self.ip, self.port)
        if mysql_conn and mongo_conn:
            messagebox.showinfo("Login Successful!", "Login Successful!")
            self.interface.mysql_login_status.configure(text="Connection made to the MySQL server!", foreground="green")
            self.interface.mongo_login_status.configure(text="Connection made to the MongoDB server!", foreground="green")
            self.display_tables_and_columns()
            self.display_insert_options_for_manufacturer()
            self.display_insert_options_for_product()
            self.insert_data_in_manufacturer_view()
            self.insert_data_in_product_view()
            self.get_data()
        else: 
            messagebox.showerror("Error", "Login Failed!")

    def display_tables_and_columns(self):
        self.table_name, self.table_columns = get_table_names_and_columns(self.server, self.host, self.password, self.database)

        if self.table_columns:
            for i, table in enumerate(self.table_name):
                ttk.Label(self.interface.data_panel, text=f"Table: {table}").grid(row=i, column=0, sticky="w")

                columns = self.table_columns.get(table, [])
                columns_label = ttk.Label(self.interface.data_panel, text=f"Columns: {', '.join(columns)}")
                columns_label.grid(row=i, column=1, sticky="w")
        else:
            print("Table columns is empty or invalid.")

    def display_insert_options_for_manufacturer(self):
        if self.table_name and self.table_columns:
            if "manufacturer" in self.table_name:
                for i, column in enumerate(self.table_columns.get("manufacturer", [])):
                    insert_label = ttk.Label(self.interface.insert_panel_for_manufacturer, text=f"Insert {column}:")
                    insert_label.grid(row=i, column=2, sticky="w")
                    insert_entry = ttk.Entry(self.interface.insert_panel_for_manufacturer)
                    insert_entry.grid(row=i, column=3, sticky="w")
                    self.insert_entries[column] = insert_entry
                insert_button = ttk.Button(self.interface.insert_panel_for_manufacturer, text="Insert", command=self.handle_insert_button_click_for_manufacturer, style="TButton")
                insert_button.grid(row=1+i, column=2, sticky="w")
        else:
            print("Table columns is empty or invalid.")

    def display_insert_options_for_product(self):
        if self.table_name and self.table_columns:
            if "product" in self.table_name:
                for i, column in enumerate(self.table_columns.get("product", [])):
                    insert_label = ttk.Label(self.interface.insert_panel_for_product, text=f"Insert {column}:")
                    insert_label.grid(row=i, column=2, sticky="w")
                    insert_entry = ttk.Entry(self.interface.insert_panel_for_product)
                    insert_entry.grid(row=i, column=3, sticky="w")
                    self.insert_entries[column] = insert_entry
                insert_button = ttk.Button(self.interface.insert_panel_for_product, text="Insert", command=self.handle_insert_button_click_for_product, style="TButton")
                insert_button.grid(row=1+i, column=2, sticky="w")
        else:
            print("Table columns is empty or invalid.")

    def handle_insert_button_click_for_manufacturer(self):
        threading.Thread(target=self.insert_manufacturer_in_thread).start()

    def handle_insert_button_click_for_product(self):
        threading.Thread(target=self.insert_product_in_thread).start()

    def insert_manufacturer_in_thread(self):
        values = {}
        for column, entry in self.insert_entries.items():
            value = entry.get()
            values[column] = value
        insert_into_manufacturer(values.get("id"), values.get("manufacturer_name"), self.server, self.host, self.password, self.database)
        insert_into_manufacturer_mongo(values.get("id"), values.get("manufacturer_name"), self.ip, self.port, self.database_name, self.collection_name)

        self.insert_data_in_manufacturer_view()
        self.get_data()
    
    def insert_product_in_thread(self):
        values = {}
        for column, entry in self.insert_entries.items():
            value = entry.get()
            values[column] = value
        insert_into_product(values.get("name"), values.get("category"), int(values.get("price")), int(values.get("manufacturer_id")), self.server, self.host, self.password, self.database) 

        update_manufacturer_mongo(
            values.get("manufacturer_id"),
            values.get("manufacturer_name"),
            values.get("name"),
            values.get("category"),
            values.get("price"),
            self.ip,
            self.port,
            self.database_name,
            self.collection_name
        )
        
        self.insert_data_in_product_view()
        self.get_data()

    def insert_data_in_manufacturer_view(self):
        data  = fetch_data_from_manufacturer(self.server, self.host, self.password, self.database)
        if data:
            for i, row in enumerate(data):
                for j, value in enumerate(row):
                    label = ttk.Label(self.interface.manufacturer_view, text=value)
                    label.grid(row=i, column=j, sticky="w")
        else:
            print("Data is empty or invalid.")

    def insert_data_in_product_view(self):
        data  = fetch_data_from_product(self.server, self.host, self.password, self.database)
        if data:
            for i, row in enumerate(data):
                for j, value in enumerate(row):
                    label = ttk.Label(self.interface.product_view, text=value)
                    label.grid(row=i, column=j, sticky="w")
        else:
            print("Data is empty or invalid.")

    def get_data(self):
        documents = get_collection_contents(self.client, self.database_name, self.collection_name)
        for index, document in enumerate(documents, start=1):
            document.pop('_id', None)
            
            formatted_text = f"Index: {index}\n"
            for key, value in document.items():
                formatted_text += f"{key}: {value}\n"

            self.interface.scrollable_text.insert("end", formatted_text + "\n")

if __name__ == "__main__":
    app = MainApp()
    app.interface.mainloop()
