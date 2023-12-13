from tkinter import messagebox
import mysql.connector

def get_table_names_and_columns(host, user, password, database):
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    try:
        cursor = connection.cursor()

        cursor.execute("SHOW TABLES")
        table_names = [table[0] for table in cursor.fetchall()]

        table_columns = {}
        for table_name in table_names:
            cursor.execute(f"DESCRIBE {table_name}")
            columns = [column[0] for column in cursor.fetchall()]
            table_columns[table_name] = columns

    finally:
        cursor.close()
        connection.close()

    return table_names, table_columns

def fetch_data_from_manufacturer(host, user, password, database):
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    try:
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM manufacturer")
        data = cursor.fetchall()

    finally:
        cursor.close()
        connection.close()

    return data

def fetch_data_from_product(host, user, password, database):
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    try:
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM product")
        data = cursor.fetchall()

    finally:
        cursor.close()
        connection.close()

    return data

def insert_into_manufacturer(id, manufacturer_name, host, user, password, database):
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    try:
        cursor = connection.cursor()

        insert_query = "INSERT INTO manufacturer (id, manufacturer_name) VALUES (%s, %s)"
        values = (id, manufacturer_name,)
        cursor.execute(insert_query, values)

        connection.commit()
        messagebox.showinfo("Success", "Record inserted successfully!")

    except mysql.connector.Error as error:
        messagebox.showerror("Error", str(error))

def insert_into_product(name, category, price, manufacturer_id, host, user, password, database):
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    try:
        cursor = connection.cursor()

        insert_query = "INSERT INTO product (name, category, price, manufacturer_id) VALUES (%s, %s, %s, %s)"
        values = (name, category, price, manufacturer_id,)
        cursor.execute(insert_query, values)

        connection.commit()
        messagebox.showinfo("Success", "Record inserted successfully!")

    except mysql.connector.Error as error:
        messagebox.showerror("Error", str(error))