import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

class Interface(tk.Tk):
    def __init__(self):
        super().__init__()

        self.init_gui()

    def init_gui(self):
        self.title("SQL injection")
        self.geometry("800x600")
        self.resizable(False, False)

        self.create_mysql_login_widgets()
        self.create_mongo_db_login_widgets()

        self.create_mysql_data_panel()
        self.create_mysql_insert_widgets_for_manufacturer()
        self.create_mysql_insert_widgets_for_product()
        self.create_mysql_manufacturer_and_product_view_widgets()

        self.create_mongodb_scrollable_widgets()

    def create_mysql_login_widgets(self):
        # login frame for other widgets
        self.mysql_login_frame = ttk.LabelFrame(self, text="MySQL", borderwidth=5, relief="groove")
        self.mysql_login_frame.place(relx=0.01, rely=0.01, relwidth=0.48, relheight=0.3)

        # server label and entry
        self.server_label = ttk.Label(self.mysql_login_frame, text="Server:")
        self.server_label.place(relx=0.01, rely=0.01)
        self.server_entry = ttk.Entry(self.mysql_login_frame)
        self.server_entry.insert(0, "localhost")
        self.server_entry.place(relx=0.11, rely=0.01)
        
        # host label and entry
        self.host_label = ttk.Label(self.mysql_login_frame, text="Host:")
        self.host_label.place(relx=0.52, rely=0.01)
        self.host_entry = ttk.Entry(self.mysql_login_frame)
        self.host_entry.insert(0, "root")
        self.host_entry.place(relx=0.61, rely=0.01)

        # password label and entry
        self.password_label = ttk.Label(self.mysql_login_frame, text="PWD:")
        self.password_label.place(relx=0.01, rely=0.3)
        self.password_entry = ttk.Entry(self.mysql_login_frame, show="*")
        self.password_entry.place(relx=0.11, rely=0.3)

        # database label and entry
        self.database_label = ttk.Label(self.mysql_login_frame, text="DB:")
        self.database_label.place(relx=0.52, rely=0.3)
        self.database_entry = ttk.Entry(self.mysql_login_frame)
        self.database_entry.insert(0, "adatbazis_projekt")
        self.database_entry.place(relx=0.61, rely=0.3)

        # login button
        self.login_button = ttk.Button(self.mysql_login_frame, text="Login")
        self.login_button.place(relx=0.14, rely=0.55, relwidth=0.70, relheight=0.25)
        self.login_button.bind("<Button-1>", lambda event: self.get_mysql_login_data())

        # login status label
        self.mysql_login_status = ttk.Label(self.mysql_login_frame, text="There is no connection to the MySQL database!")
        self.mysql_login_status.place(relx=0.17, rely=0.85)
        self.mysql_login_status.configure(foreground="red")

    def create_mongo_db_login_widgets(self):
        # login frame for other widgets
        self.mongo_login_frame = ttk.LabelFrame(self, text="MongoDB", borderwidth=5, relief="groove")
        self.mongo_login_frame.place(relx=0.51, rely=0.01, relwidth=0.48, relheight=0.3)

        # ip label and entry
        self.ip_label = ttk.Label(self.mongo_login_frame, text="IP address:")
        self.ip_label.place(relx=0.01, rely=0.01)
        self.ip_entry = ttk.Entry(self.mongo_login_frame)
        self.ip_entry.insert(0, "localhost")
        self.ip_entry.place(relx=0.18, rely=0.01)

        # port label and entry
        self.port_label = ttk.Label(self.mongo_login_frame, text="Port:")
        self.port_label.place(relx=0.55, rely=0.01)
        self.port_entry = ttk.Entry(self.mongo_login_frame)
        self.port_entry.insert(0, "27017")
        self.port_entry.place(relx=0.64, rely=0.01)

        # database name label and entry
        self.database_name_label = ttk.Label(self.mongo_login_frame, text="DB:")
        self.database_name_label.place(relx=0.01, rely=0.3)
        self.database_name_entry = ttk.Entry(self.mongo_login_frame)
        self.database_name_entry.insert(0, "bakcsitamas")
        self.database_name_entry.place(relx=0.11, rely=0.3)

        # collection name label and entry
        self.collection_label = ttk.Label(self.mongo_login_frame, text="Collection:")
        self.collection_label.place(relx=0.47, rely=0.3)
        self.collection_entry = ttk.Entry(self.mongo_login_frame)
        self.collection_entry.insert(0, "products")
        self.collection_entry.place(relx=0.64, rely=0.3)

        # login button
        self.login_button = ttk.Button(self.mongo_login_frame, text="Login")
        self.login_button.place(relx=0.14, rely=0.55, relwidth=0.70, relheight=0.25)
        self.login_button.bind("<Button-1>", lambda event: self.get_mongo_login_data())

        # login status label
        self.mongo_login_status = ttk.Label(self.mongo_login_frame, text="There is no connection to the MongoDB database!")
        self.mongo_login_status.place(relx=0.17, rely=0.85)
        self.mongo_login_status.configure(foreground="red")

    def create_mysql_data_panel(self):
        self.data_panel = ttk.LabelFrame(self, text="Data", borderwidth=5, relief="groove")
        self.data_panel.place(relx=0.01, rely=0.31, relwidth=0.48, relheight=0.10)

    def create_mysql_insert_widgets_for_manufacturer(self):
        self.insert_panel_for_manufacturer = ttk.LabelFrame(self, text="Insert into manufacturer", borderwidth=5, relief="groove")
        self.insert_panel_for_manufacturer.place(relx=0.01, rely=0.41, relwidth=0.48, relheight=0.15)
    
    def create_mysql_insert_widgets_for_product(self):
        self.insert_panel_for_product = ttk.LabelFrame(self, text="Insert into product", borderwidth=5, relief="groove")
        self.insert_panel_for_product.place(relx=0.01, rely=0.56, relwidth=0.48, relheight=0.25)

    def create_mysql_manufacturer_and_product_view_widgets(self):
        self.manufacturer_view = ttk.LabelFrame(self, text="Manufacturer table", borderwidth=5, relief="groove")
        self.manufacturer_view.place(relx=0.01, rely=0.81, relwidth=0.48, relheight=0.18)

        self.product_view = ttk.LabelFrame(self, text="Product table", borderwidth=5, relief="groove")
        self.product_view.place(relx=0.51, rely=0.81, relwidth=0.48, relheight=0.18)

    def create_mongodb_scrollable_widgets(self):
        self.scrollable_frame = ttk.LabelFrame(self, text="MongoDB", borderwidth=5, relief="groove")
        self.scrollable_frame.place(relx=0.51, rely=0.31, relwidth=0.48, relheight=0.50)

        self.scrollable_text = ScrolledText(self.scrollable_frame, width=50, height=10)
        self.scrollable_text.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)

    def get_mysql_login_data(self):
        server = self.server_entry.get()
        host = self.host_entry.get()
        password = self.password_entry.get()
        database = self.database_entry.get()

        return server, host, password, database

    def get_mongo_login_data(self):
        ip = self.ip_entry.get()
        port = self.port_entry.get()
        database_name = self.database_name_entry.get()
        collection_name = self.collection_entry.get()

        return ip, port, database_name, collection_name