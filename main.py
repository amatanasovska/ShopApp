import tkinter as Tkinter
import sqlite3
import datetime
import tkinter.messagebox

def create_tables(cursor, conn):
    """
    Function which is called once just to create tables.

    :param cursor: cursor
    :param conn: conn
    :return: None
    """

    query1 = "CREATE TABLE products(id TEXT, name TEXT, type TEXT, price INTEGER, quantity_available INTEGER)"
    query2 = "CREATE TABLE customers(id TEXT, name TEXT, address TEXT, phone_number TEXT)"
    query3 = "CREATE TABLE orders(id INTEGER, product_id TEXT,customer_id  TEXT, quantity_bought TEXT, full_price INTEGER,date TEXT) "

    cursor.execute(query1)
    conn.commit()
    cursor.execute(query2)
    conn.commit()
    cursor.execute(query3)
    conn.commit()


def search_for_the_product(p_id_entry, cursor, conn, p_name, p_type, p_price, p_quantity):
    """
    Activates when you click the "Search for the product" button. Uses the argument p_id_entry to get the text out of the
    product id entry and find its details.


    :param p_id_entry: The product id entry
    :param cursor: Cursor for the sqlite file.
    :param conn: Connection for the sqlite file.
    :param p_name: Label to set the product name.
    :param p_type: Label to set the product type.
    :param p_price: Label to set the product price.
    :param p_quantity: Label to set the product's available quantity.
    :return: None. Just finds the product and changes the labels.
    """
    if len(p_id_entry.get()) == 0:
        tkinter.messagebox.showinfo("Error", "Empty field")

    else:
        data = cursor.execute(f"SELECT * FROM products WHERE id='{str(p_id_entry.get())}'").fetchall()
        conn.commit()

        if len(data) != 0:
            p_name['text'] = str(data[0][1])
            p_type['text'] = str(data[0][2])
            p_price['text'] = str(data[0][3])
            p_quantity['text'] = str(data[0][4])

        else:
            tkinter.messagebox.showinfo("Error", "Product not found")
            p_name['text'] = ""
            p_type['text'] = ""
            p_price['text'] = ""
            p_quantity['text'] = ""


def search_for_the_customer(c_id_entry, cursor, conn, c_name, c_address, c_phone):
    """
    Activated when you press "Search for the customer" button. Uses the argument c_id_entry to get the text out of the
    customer id entry and find its details.

    :param c_id_entry:The customer id entry
    :param cursor: Cursor for the sqlite file
    :param conn: Connection for the sqlite file
    :param c_name: Label for the customer name
    :param c_address: Label for the customer address
    :param c_phone: Label for the customer phone
    :return: None. Just finds the customers and fills the labels with the customer's details.
    """

    if len(c_id_entry.get()) == 0:
        tkinter.messagebox.showinfo("Error", "Empty field")

    else:
        data = cursor.execute(f"SELECT * FROM customers WHERE id='{str(c_id_entry.get())}'").fetchall()
        conn.commit()

        if len(data) != 0:
            c_name['text'] = str(data[0][1])
            c_address['text'] = str(data[0][2])
            c_phone['text'] = str(data[0][3])
        else:
            tkinter.messagebox.showinfo("Error", "Customer not found")
            c_name['text'] = ""
            c_address['text'] = ""
            c_phone['text'] = ""


def add_customer():
    """
    Called from the "Add customer" button. Used to add a new customer.

    :return: None.
    """
    conn = sqlite3.connect("data.sqlite")
    cursor = conn.cursor()

    add_customer_root = Tkinter.Tk()
    add_customer_root.title("Add customer")

    Tkinter.Label(add_customer_root, text="Set the new customer id:", font="Arial 10 bold").grid(row=0, column=0,
                                                                                                 padx=10,
                                                                                                 pady=10)
    id_new_customer_entry = Tkinter.Entry(add_customer_root, font="Arial 10", width=40)
    id_new_customer_entry.grid(row=0, column=1, padx=10, pady=10, columnspan=2)

    Tkinter.Label(add_customer_root, text="Set the new customer name:", font="Arial 10 bold").grid(row=1, column=0,
                                                                                                   padx=10,
                                                                                                   pady=10)
    name_new_customer_entry = Tkinter.Entry(add_customer_root, font="Arial 10", width=40)
    name_new_customer_entry.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

    Tkinter.Label(add_customer_root, text="Set the new customer address:", font="Arial 10 bold").grid(row=2, column=0,
                                                                                                      padx=10,
                                                                                                      pady=10)
    address_new_customer_entry = Tkinter.Entry(add_customer_root, font="Arial 10", width=40)
    address_new_customer_entry.grid(row=2, column=1, padx=10, pady=10, columnspan=2)

    Tkinter.Label(add_customer_root, text="Set the new customer phone number:", font="Arial 10 bold").grid(row=3,
                                                                                                           column=0,
                                                                                                           padx=10,
                                                                                                           pady=10)
    phone_new_customer_entry = Tkinter.Entry(add_customer_root, font="Arial 10", width=40)
    phone_new_customer_entry.grid(row=3, column=1, padx=10, pady=10, columnspan=2)

    Tkinter.Button(add_customer_root, text="Add a new customer", height=3, width=20, bg="white",
                   command=lambda: add_customer_btn(cursor, conn, id_new_customer_entry, name_new_customer_entry,
                                                    address_new_customer_entry, phone_new_customer_entry,
                                                    new_customer_status)).grid(row=5, column=0, padx=10, pady=10)
    new_customer_status = Tkinter.Label(add_customer_root, text="", font="Arial 10 italic")
    new_customer_status.grid(row=6, column=0, padx=10, pady=10)

    add_customer_root.mainloop()


def add_customer_btn(cursor, conn, entry_new_customer_id, entry_new_customer_name, entry_new_customer_address,
                     entry_new_customer_phone, label_customer_status):
    """
    Used to extract the information entered in the entries and create the new customer.


    :param cursor: Cursor for the sqlite file
    :param conn: Connection for the sqlite file
    :param entry_new_customer_id: Entry to get the new customer's id
    :param entry_new_customer_name: Entry to get the new customer's name
    :param entry_new_customer_address: Entry to get the new customer's address
    :param entry_new_customer_phone: Entry to get the new customer's phone number
    :param label_customer_status: Label used to indicate if the new customer was created or not (reasons: invalid input,
    empty fields...)
    :return: None
    """
    label_customer_status['text'] = ""
    try:
        listValues = [str(entry_new_customer_id.get()), str(entry_new_customer_name.get()),
                      str(entry_new_customer_address.get()), str(entry_new_customer_phone.get())]

        if len(listValues[0]) == 0 or len(listValues[1]) == 0 or len(listValues[2]) == 0 or len(listValues[3]) == 0:
            label_customer_status['text'] = "Do not leave empty fields please."
            raise Exception

        var = str(listValues[0])

        same_id = cursor.execute(f"SELECT * FROM customers WHERE id={var}").fetchall()
        if len(same_id) != 0:
            label_customer_status['text'] = "ID already taken"
            raise Exception

        query = f"INSERT INTO customers(id, name, address, phone_number) VALUES (?, ?, ?, ?)"

        cursor.execute(query, listValues)
        conn.commit()
        label_customer_status['fg'] = "green"
        label_customer_status['text'] = "Success!"
    except Exception:
        label_customer_status['fg'] = "red"
        if label_customer_status['text'] == "":
            label_customer_status['text'] = "Invalid input"


def make_order(cursor, conn, label_order_id, entry_product_id, entry_customer_id, entry_quantity_bought,
               label_full_price, label_product_quantity, tk_to_cancel):
    """
    Function called by the Make Order button. Gets the product and customer ID from the entry,
    so if we must SEARCH FOR THE PRODUCT AND CUSTOMER before we check out, same goes for quantity if you enter 10 and
    still not click Calculate the price, an order will be made using the value in the entry, even though it was not
    calculated that way. If the id is not found when we review the orders it shows as DELETED product Also the full price
    has to be using the button for that purpose. //Should search for a solution.

    :param cursor: Cursor for the sqlite file
    :param conn: Connection for the sqlite file
    :param label_order_id: Label for the order id
    :param entry_product_id: Entry for the product id
    :param entry_customer_id: Entry for the customer id
    :param entry_quantity_bought: Entry for the quantity bought
    :param label_full_price: Label for the full price
    :param label_product_quantity: Label to check the product quantity and take out of it since some of it is bought and
    We check if the quantity written is compatible using the button for that purpose.
    :param tk_to_cancel: The main tk(). Used to destroy it, so we can restart the problem //Should search for a  better
    solution
    :return: None
    """
    if len(label_full_price['text']):
        query = f"INSERT INTO orders(id, product_id, customer_id, quantity_bought, full_price, date) VALUES ({label_order_id['text']}, {entry_product_id.get()}, {entry_customer_id.get()}, {entry_quantity_bought.get()}, {int(label_full_price['text'])}, date('now'))"
        cursor.execute(query)
        conn.commit()

        var = int(label_product_quantity['text']) - int(entry_quantity_bought.get())

        query1 = f"UPDATE products SET quantity_available={var} WHERE id={entry_product_id.get()}"
        cursor.execute(query1)
        conn.commit()

        tk_to_cancel.destroy()
        main()
    else:
        Tkinter.messagebox.showinfo("Error", "Full price NOT calculated")


def list_of_orders():
    """
    Function to show the list of orders in a scrollbar. //Should find a way to edit them with a double click not using
    the button Find an order by ID


    :return: None.
    """
    conn = sqlite3.connect("data.sqlite")
    cursor = conn.cursor()

    list_of_orders_root = Tkinter.Tk()
    list_of_orders_root.title("List of orders")

    scrollbar = Tkinter.Scrollbar(list_of_orders_root)
    scrollbar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)

    list_orders = Tkinter.Listbox(list_of_orders_root, yscrollcommand=scrollbar.set, width=90)
    list_orders.pack()
    orders = cursor.execute("SELECT * FROM orders ORDER BY date DESC").fetchall()
    conn.commit()
    var = 1
    for order in orders:
        x = "ID: {}, product ID: {}, customer ID: {}, quantity bought {}, total price {}, date {} ".format(order[0],
                                                                                                           order[1],
                                                                                                           order[2],
                                                                                                           order[3],
                                                                                                           order[4],
                                                                                                           order[5])
        list_orders.insert(Tkinter.END, f"Order {var}: {x} ")
        var = var + 1

    order_found_label = Tkinter.Label(list_of_orders_root, text="", font="Arial 10 italic bold underline")
    order_found_label.pack()
    find_order_by_id = Tkinter.Entry(list_of_orders_root, width=15)
    find_order_by_id.pack(padx=10, pady=10)
    Tkinter.Button(list_of_orders_root, text="Find an order by id",
                   command=lambda: find_order(cursor, conn, find_order_by_id, order_found_label)).pack(padx=5, pady=5)
    list_of_orders_root.mainloop()


def find_order(cursor, conn, entry_find_order_by_id, label_order_found):
    """
    Function used to find the order using the given id in the Entry in the List of orders screen.

    :param cursor: Cursor to the sqlite file
    :param conn: Connection to the sqlite file
    :param entry_find_order_by_id:  Entry where you enter the ID of the product you want to find
    :param label_order_found: Label that shows if your order is found.
    :return: None
    """
    try:
        query = f"SELECT * FROM orders WHERE id = {entry_find_order_by_id.get()}"
        data = cursor.execute(query).fetchall()
        conn.commit()

        if len(data):
            label_order_found['text'] = ""
            review_order(data, cursor, conn)
        else:
            label_order_found['text'] = "Order not found."
    except sqlite3.OperationalError:
        label_order_found['text'] = "Invalid input"


def review_order(data, cursor, conn):
    """
    Function to see what the order consists of. Does not have any additional buttons. //Might consider adding a delete
    order button so it will give the subtracted quantity back to the returned product


    :param data: Product details. List of Tuples.
    :param cursor: Cursor for the sqlite file.
    :param conn: Connection for the sqlite file.
    :return: None.
    """
    review_order_root = Tkinter.Tk()
    review_order_root.title("Information for order")
    Tkinter.Label(review_order_root, text=f"Information for order with ID {data[0][0]}:",
                  font="Arial 10 underline").grid(row=1, column=0, columnspan=2)

    Tkinter.Label(review_order_root, text=f"Product ID: {data[0][1]}", font="Arial 10 bold").grid(row=2, column=0,
                                                                                                  columnspan=2)
    query = f"SELECT * FROM products WHERE id = {data[0][1]}"
    prod_info = cursor.execute(query).fetchall()
    conn.commit()

    pn_var = "Deleted"
    pt_var = "Deleted"
    pp_var = "Deleted"
    pqa_var = "Deleted"

    if len(prod_info):
        pn_var = prod_info[0][1]
        pt_var = prod_info[0][2]
        pp_var = prod_info[0][3]
        pqa_var = prod_info[0][4]

    Tkinter.Label(review_order_root, text=f"Product Name: {pn_var}", font="Arial 10 italic").grid(row=3,
                                                                                                  column=0,
                                                                                                  columnspan=2)
    Tkinter.Label(review_order_root, text=f"Product Type: {pt_var}", font="Arial 10 italic").grid(row=3,
                                                                                                  column=2,
                                                                                                  columnspan=2)
    Tkinter.Label(review_order_root, text=f"Product Price: {pp_var}", font="Arial 10 italic").grid(row=3,
                                                                                                   column=4,
                                                                                                   columnspan=2)
    Tkinter.Label(review_order_root, text=f"Product Quantity Available: {pqa_var}",
                  font="Arial 10 italic").grid(row=3, column=6, columnspan=2)

    Tkinter.Label(review_order_root, text=f"Customer ID: {data[0][2]}", font="Arial 10 bold").grid(row=4, column=0,
                                                                                                   columnspan=2)
    query1 = f"SELECT * FROM customers WHERE id = {data[0][2]}"
    cust_info = cursor.execute(query1).fetchall()
    conn.commit()

    ocn_var = "Deleted."
    oca_var = "Deleted."
    ocpn_var = "Deleted."

    if len(cust_info):
        ocn_var = cust_info[0][1]
        oca_var = cust_info[0][2]
        ocpn_var = cust_info[0][3]

    order_customer_name = Tkinter.Label(review_order_root, text=f"Customer Name: {ocn_var}", font="Arial 10 italic")
    order_customer_name.grid(row=5,
                             column=0,
                             columnspan=2)
    order_customer_address = Tkinter.Label(review_order_root, text=f"Customer Address: {oca_var}",
                                           font="Arial 10 italic")
    order_customer_address.grid(row=5,
                                column=2,
                                columnspan=2)
    order_customer_phone_number = Tkinter.Label(review_order_root, text=f"Customer Phone Number: {ocpn_var}", width=50,
                                                font="Arial 10 italic")
    order_customer_phone_number.grid(
        row=5, column=5, columnspan=2)

    order_customer_quantity_bought = Tkinter.Label(review_order_root, text=f"Quantity bought: {data[0][3]}",
                                                   font="Arial 10 underline")
    order_customer_quantity_bought.grid(row=6,
                                        column=0,
                                        columnspan=2)

    Tkinter.Label(review_order_root, text=f"Total price: {data[0][4]}", font="Arial 10 underline").grid(row=7,
                                                                                                        column=0,
                                                                                                        columnspan=2)
    Tkinter.Label(review_order_root, text=f"Date: {data[0][5]}", font="Arial 10 underline").grid(row=8, column=0,
                                                                                                 columnspan=2)


def list_of_products():
    """
    Shows a list of product in a scrollbar. // Notes are the same as the ones for the list_of_orders()


    :return: None.
    """
    conn = sqlite3.connect("data.sqlite")
    cursor = conn.cursor()

    list_of_products_root = Tkinter.Tk()
    list_of_products_root.title("List of products")

    scrollbar = Tkinter.Scrollbar(list_of_products_root)
    scrollbar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)

    list_products = Tkinter.Listbox(list_of_products_root, yscrollcommand=scrollbar.set, width=90)
    list_products.pack()

    products = cursor.execute("SELECT * FROM products ORDER BY id").fetchall()
    conn.commit()
    var = 1
    for product in products:
        x = "ID: {}, Name: {}, Type: {}, Price {}, Quantity {}".format(product[0], product[1], product[2], product[3],
                                                                       product[4])
        list_products.insert(Tkinter.END, f"Product {var}: {x} ")
        var = var + 1

    product_found_label = Tkinter.Label(list_of_products_root, text="", font="Arial 10 italic bold underline")
    product_found_label.pack()
    find_product_id_entry = Tkinter.Entry(list_of_products_root, width=15)
    find_product_id_entry.pack(padx=10, pady=10)
    Tkinter.Button(list_of_products_root, text="Find a product by id",
                   command=lambda: find_product(cursor, conn, find_product_id_entry, product_found_label)).pack(padx=5,
                                                                                                                pady=5)
    list_of_products_root.mainloop()


def find_product(cursor, conn, entry_find_product_id, label_product_found):
    """
    Finds the product using the given id in the entry.

    :param cursor: Cursor for the sqlite file
    :param conn: Connection for the sqlite file
    :param entry_find_product_id: Entry to extract the product id from
    :param label_product_found: Label to show if the product was found
    :return: None
    """
    try:
        query = f"SELECT * FROM products WHERE id = {entry_find_product_id.get()}"
        data = cursor.execute(query).fetchall()
        conn.commit()

        if len(data):
            label_product_found['text'] = ""
            review_product(data, cursor, conn)
        else:
            label_product_found['text'] = "Product not found."
    except sqlite3.OperationalError:
        label_product_found['text'] = "Invalid input"


def review_product(data, cursor, conn):
    """
    Shows product information. If everything is okay in find_product() you get redirected to this function.

    :param data: Data for the product. List of tuples.
    :param cursor: Cursor for the sqlite file
    :param conn: Connection for the sqlite file
    :return:None.
    """
    review_product_root = Tkinter.Tk()
    review_product_root.title("Information for product")
    Tkinter.Label(review_product_root, text=f"Information for product with ID {data[0][0]}:",
                  font="Arial 10 underline").grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    Tkinter.Label(review_product_root, text="Update the product:", font="Arial 10 underline").grid(row=1, column=2,
                                                                                                   columnspan=2,
                                                                                                   padx=10, pady=10)
    Tkinter.Label(review_product_root, text=f"Product Name: {data[0][1]}", font="Arial 10 bold").grid(row=2, column=0,
                                                                                                      columnspan=2,
                                                                                                      padx=10, pady=10)

    new_product_name = Tkinter.Entry(review_product_root, font="Arial 10 bold")
    new_product_name.grid(row=2, column=2, columnspan=2, padx=10, pady=10)

    Tkinter.Label(review_product_root, text=f"Product type: {data[0][2]}", font="Arial 10 bold").grid(row=3, column=0,
                                                                                                      columnspan=2,
                                                                                                      padx=10, pady=10)

    new_product_type = Tkinter.Entry(review_product_root, font="Arial 10 bold")
    new_product_type.grid(row=3, column=2, columnspan=2, padx=10, pady=10)

    Tkinter.Label(review_product_root, text=f"Price of the product: {data[0][3]}", font="Arial 10 underline").grid(
        row=4, column=0, columnspan=2, padx=10, pady=10)

    new_product_price = Tkinter.Entry(review_product_root, font="Arial 10 bold")
    new_product_price.grid(row=4, column=2, columnspan=2, padx=10, pady=10)

    Tkinter.Label(review_product_root, text=f"Quantity available {data[0][4]}", font="Arial 10 underline").grid(row=5,
                                                                                                                column=0,
                                                                                                                columnspan=2,
                                                                                                                padx=10,
                                                                                                                pady=10)
    new_product_quantity = Tkinter.Entry(review_product_root, font="Arial 10 bold")
    new_product_quantity.grid(row=5, column=2, columnspan=2, padx=10, pady=10)

    status_label = Tkinter.Label(review_product_root, text="", fg="red", font="Arial 10 bold")
    status_label.grid(row=7, column=2, columnspan=2, padx=10, pady=10)
    Tkinter.Button(review_product_root, height=3, width=15, text="Update the product",
                   command=lambda: update_product(cursor, conn, data[0][0], new_product_name, new_product_type,
                                                  new_product_price, new_product_quantity, status_label)).grid(row=6,
                                                                                                               column=0,
                                                                                                               columnspan=2,
                                                                                                               padx=10,
                                                                                                               pady=10)
    Tkinter.Button(review_product_root, height=3, width=15, text="Cancel", command=review_product_root.destroy).grid(
        row=6, column=2, columnspan=2, padx=10, pady=10)
    Tkinter.Button(review_product_root, height=3, width=15, text="Delete the product",
                   command=lambda: delete_product(cursor, conn, review_product_root, data[0][0])).grid(row=6, column=4,
                                                                                                       columnspan=2,
                                                                                                       padx=10, pady=10)

    review_product_root.mainloop()


def update_product(cursor, conn, p_id, entry_new_name, entry_new_type, entry_new_price, entry_new_quantity,
                   label_status):
    """
    Activated when you click the Update product button in Review Product screen //Should try to put the already existing
    text in the entries, so if a person would like to change only one thing in the product he would just change the thing
    and not rewrite the rest.


    :param cursor: Cursor for the sqlite file
    :param conn: Connection for the sqlite
    :param p_id: ID for the product which needs to be updated
    :param entry_new_name: Entry for the new name of the product
    :param entry_new_type: Entry for the new type of the product
    :param entry_new_price: Entry for the new price of the product
    :param entry_new_quantity: Entry for the new quantity of the product
    :param label_status: Label that shows if the product was updated or not
    :return: None.
    """
    try:

        query = f"UPDATE products SET name='{entry_new_name.get()}', type='{entry_new_type.get()}', price='{int(entry_new_price.get())}', quantity_available={int(entry_new_quantity.get())} WHERE id={p_id}"

        cursor.execute(query)
        conn.commit()

        label_status['fg'] = "green"
        label_status['text'] = "Success."

    except ValueError:
        label_status['fg'] = "red"
        label_status['text'] = "Error. Invalid input."


def delete_product(cursor, conn, tk, p_id):
    """
    Deletes the product and destroys the tk()

    :param cursor:Cursor for the sqlite file.
    :param conn: Connection for the sqlite file.
    :param tk: The window.
    :param p_id: ID of the product that should be deleted.
    :return: None.
    """
    query = f"DELETE FROM products WHERE id={p_id}"
    cursor.execute(query)
    conn.commit()

    tk.destroy()


def list_of_customers():
    """
    Shows the list of customers in a scroll bar // For notes see in list_of_orders()


    :return: None.
    """
    conn = sqlite3.connect("data.sqlite")
    cursor = conn.cursor()

    list_of_customers_root = Tkinter.Tk()
    list_of_customers_root.title("List of customers")

    scrollbar = Tkinter.Scrollbar(list_of_customers_root)
    scrollbar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)

    list_customers = Tkinter.Listbox(list_of_customers_root, yscrollcommand=scrollbar.set, width=90)
    list_customers.pack()

    customers = cursor.execute("SELECT * FROM customers ORDER BY id").fetchall()
    var = 1
    for customer in customers:
        x = "ID: {}, Name: {}, Address: {}, Phone Number {}".format(customer[0],
                                                                    customer[1],
                                                                    customer[2],
                                                                    customer[3])
        list_customers.insert(Tkinter.END, f"Customer {var}: {x} ")
        var = var + 1

    customer_found_label = Tkinter.Label(list_of_customers_root, text="", font="Arial 10 italic bold underline")
    customer_found_label.pack()
    find_customer_id_entry = Tkinter.Entry(list_of_customers_root, width=15)
    find_customer_id_entry.pack(padx=10, pady=10)
    Tkinter.Button(list_of_customers_root, text="Find a customer by id",
                   command=lambda: find_customer(cursor, conn, find_customer_id_entry, customer_found_label)).pack(
        padx=5, pady=5)
    list_of_customers_root.mainloop()


def find_customer(cursor, conn, entry_find_customer_id, label_customer_found):
    """
    Find customer using the given ID in the entry in the List of Customers screen.

    :param cursor: Cursor for the sqlite file
    :param conn: Connection for the sqlite file
    :param entry_find_customer_id: Entry for the desired customer's ID
    :param label_customer_found: Label to show if the customer is found
    :return: None.
    """
    try:
        query = f"SELECT * FROM customers WHERE id = {entry_find_customer_id.get()}"
        data = cursor.execute(query).fetchall()
        conn.commit()
        if len(data):
            label_customer_found['text'] = ""
            review_customer(cursor, conn, data)
        else:
            label_customer_found['text'] = "Customer not found"
    except:
        label_customer_found['text'] = "Invalid input"


def review_customer(cursor, conn, data):
    """
    Reviews the customer's data. Activates if the customer ID in find_customer()'s entry_find_customer_id was valid

    :param cursor: Cursor for the sqlite file
    :param conn: Cursor for the sqlite file
    :param data: Customer's details
    :return:
    """
    review_customer_root = Tkinter.Tk()
    review_customer_root.title("Information for customer")
    Tkinter.Label(review_customer_root, text=f"Information for customer with ID {data[0][0]}:",
                  font="Arial 10 underline").grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    Tkinter.Label(review_customer_root, text="Update the customer:", font="Arial 10 underline").grid(row=1, column=2,
                                                                                                     columnspan=2,
                                                                                                     padx=10, pady=10)
    Tkinter.Label(review_customer_root, text=f"Customer Name: {data[0][1]}", font="Arial 10 bold").grid(row=2, column=0,
                                                                                                        columnspan=2,
                                                                                                        padx=10,
                                                                                                        pady=10)

    new_customer_name = Tkinter.Entry(review_customer_root, font="Arial 10 bold")
    new_customer_name.grid(row=2, column=2, columnspan=2, padx=10, pady=10)

    Tkinter.Label(review_customer_root, text=f"Customer address: {data[0][2]}", font="Arial 10 bold").grid(row=3,
                                                                                                           column=0,
                                                                                                           columnspan=2,
                                                                                                           padx=10,
                                                                                                           pady=10)

    new_customer_address = Tkinter.Entry(review_customer_root, font="Arial 10 bold")
    new_customer_address.grid(row=3, column=2, columnspan=2, padx=10, pady=10)

    Tkinter.Label(review_customer_root, text=f"Customer phone number: {data[0][3]}", font="Arial 10 underline").grid(
        row=4, column=0, columnspan=2, padx=10, pady=10)

    new_customer_phone_number = Tkinter.Entry(review_customer_root, font="Arial 10 bold")
    new_customer_phone_number.grid(row=4, column=2, columnspan=2, padx=10, pady=10)

    status_label = Tkinter.Label(review_customer_root, text="", fg="red", font="Arial 10 bold")
    status_label.grid(row=6, column=2, columnspan=2, padx=10, pady=10)
    Tkinter.Button(review_customer_root, height=3, width=15, text="Update the customer",
                   command=lambda: update_customer(cursor, conn, data[0][0], new_customer_name, new_customer_address,
                                                   new_customer_phone_number, status_label)).grid(row=5,
                                                                                                  column=0,
                                                                                                  columnspan=2,
                                                                                                  padx=10,
                                                                                                  pady=10)
    Tkinter.Button(review_customer_root, height=3, width=15, text="Cancel", command=review_customer_root.destroy).grid(
        row=5, column=2, columnspan=2, padx=10, pady=10)
    Tkinter.Button(review_customer_root, height=3, width=15, text="Delete the product",
                   command=lambda: delete_customer(cursor, conn, review_customer_root, data[0][0])).grid(row=5,
                                                                                                         column=4,
                                                                                                         columnspan=2,
                                                                                                         padx=10,
                                                                                                         pady=10)

    review_customer_root.mainloop()


def update_customer(cursor, conn, c_id, new_customer_name, new_customer_address, new_customer_phone_number,
                    status_label):
    """
    Activated by the Update customer button. Updates the customer using the information given in the entries. //For Notes
    see the update_product function

    :param cursor:Cursor for the sqlite file
    :param conn:Connection for the sqlite file
    :param c_id:Customer id NOT an entry
    :param new_customer_name: Entry for the customer name
    :param new_customer_address: Entry for the customer address
    :param new_customer_phone_number: Entry for the customer phone_number
    :param status_label: Label to show if the customer was updated or not
    :return:None.
    """

    try:

        query = f"UPDATE customers SET name='{new_customer_name.get()}', address='{new_customer_address.get()}', phone_number='{new_customer_phone_number.get()}' WHERE id={c_id}"

        cursor.execute(query)
        conn.commit()

        status_label['fg'] = "green"
        status_label['text'] = "Success."

    except ValueError:
        status_label['fg'] = "red"
        status_label['text'] = "Error. Invalid input."


def delete_customer(cursor, conn, tk, c_id):
    """
    Used to delete customer.

    :param cursor: Cursor for the sqlite file
    :param conn: Connection for the sqlite file
    :param tk: Screen for the sqlite file
    :param c_id: Customer ID
    :return: None.
    """
    query = f"DELETE FROM customers WHERE id={c_id}"
    cursor.execute(query)
    conn.commit()

    tk.destroy()


def calculate_the_price(label_product_price, entry_quantity_bought, label_product_quantity, label_total_price):
    """
    Used to calculate the price using the quantity written AND VALIDATED USING THE BUTTON for that purpose //Should find
    a way to automatically update it

    :param label_product_price: Label where is shown the product price( UPDATED ONLY AFTER THE PRODUCT ID IS VALIDATED
    USING THE BUTTON //should fix)
    :param entry_quantity_bought: Entry where the quantity bought is shown
    :param label_product_quantity: Label where is shown the product quantity( UPDATED ONLY AFTER THE PRODUCT ID IS VALIDATED
    USING THE BUTTON //should fix)
    :param label_total_price: Label where the total price is written
    :return: None.
    """

    try:
        if int(entry_quantity_bought.get()) <= int(label_product_quantity['text']):
            totalPrice = int(label_product_price['text']) * int(entry_quantity_bought.get())
            label_total_price.config(text=str(totalPrice))
        else:
            tkinter.messagebox.showinfo("Error", "We do not have that much in stock.")
    except ValueError:
        tkinter.messagebox.showinfo("Error", "Please enter valid input.")


def add_product():
    """
    Used to open a screen when you click the button Add Product


    :return: None
    """
    conn = sqlite3.connect("data.sqlite")
    cursor = conn.cursor()

    add_product_root = Tkinter.Tk()
    add_product_root.title("Add product")

    Tkinter.Label(add_product_root, text="Set the new product id:", font="Arial 10 bold").grid(row=0, column=0, padx=10,
                                                                                               pady=10)
    id_new_product_entry = Tkinter.Entry(add_product_root, font="Arial 10", width=40)
    id_new_product_entry.grid(row=0, column=1, padx=10, pady=10, columnspan=2)

    Tkinter.Label(add_product_root, text="Set the new product name:", font="Arial 10 bold").grid(row=1, column=0,
                                                                                                 padx=10,
                                                                                                 pady=10)
    name_new_product_entry = Tkinter.Entry(add_product_root, font="Arial 10", width=40)
    name_new_product_entry.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

    Tkinter.Label(add_product_root, text="Set the new product type:", font="Arial 10 bold").grid(row=2, column=0,
                                                                                                 padx=10,
                                                                                                 pady=10)
    type_new_product_entry = Tkinter.Entry(add_product_root, font="Arial 10", width=40)
    type_new_product_entry.grid(row=2, column=1, padx=10, pady=10, columnspan=2)

    Tkinter.Label(add_product_root, text="Set the new product price:", font="Arial 10 bold").grid(row=3, column=0,
                                                                                                  padx=10,
                                                                                                  pady=10)
    price_new_product_entry = Tkinter.Entry(add_product_root, font="Arial 10", width=40)
    price_new_product_entry.grid(row=3, column=1, padx=10, pady=10, columnspan=2)

    Tkinter.Label(add_product_root, text="Set the new quantity available of the product:", font="Arial 10 bold").grid(
        row=4, column=0,
        padx=10,
        pady=10)
    quantity_new_product_entry = Tkinter.Entry(add_product_root, font="Arial 10", width=40)
    quantity_new_product_entry.grid(row=4, column=1, padx=10, pady=10, columnspan=2)

    invalid_product_input_label = Tkinter.Label(add_product_root, text="", font="Arial 10 italic", fg="red")
    invalid_product_input_label.grid(row=6, column=0, padx=10, pady=10)
    Tkinter.Button(add_product_root, text="Add a new product", height=3, width=20, bg="white",
                   command=lambda: add_product_btn_command(cursor, conn, id_new_product_entry, name_new_product_entry,
                                                           type_new_product_entry, price_new_product_entry,
                                                           quantity_new_product_entry,
                                                           invalid_product_input_label)).grid(row=5, column=0, padx=10,
                                                                                              pady=10)

    add_product_root.mainloop()


def add_product_btn_command(cursor, conn, entry_id, entry_name, entry_type, entry_price, entry_quantity,
                            label_invalid_product):
    """
    Used after the screen Add Product for the button "Add Product" to create new product using the data given in the
    entries on the Add Product screen and given as arguments to this function.

    :param cursor: Cursor for the sqlite function
    :param conn: Connection for the sqlite function
    :param entry_id: Entry for the new product ID
    :param entry_name: Entry for the new product Name
    :param entry_type: Entry for the new product Type
    :param entry_price: Entry for the new product Price
    :param entry_quantity: Entry for the new product Quantity Available
    :param label_invalid_product: Shows if any of the entries is invalid
    :return: None
    """
    label_invalid_product['text'] = ""
    try:
        listValues = [str(entry_id.get()), str(entry_name.get()), str(entry_type.get()), int(entry_price.get()),
                      int(entry_quantity.get())]

        if len(listValues[0]) == 0 or len(listValues[1]) == 0 or len(listValues[2]) == 0:
            label_invalid_product['text'] = "Do not leave empty fields please."
            raise Exception

        var = str(listValues[0])

        same_id = cursor.execute(f"SELECT * FROM products WHERE id={var}").fetchall()
        if len(same_id) != 0:
            label_invalid_product['text'] = "ID already taken"
            raise Exception

        query = f"INSERT INTO products(id, name, type, price, quantity_available) VALUES (?, ?, ?, ?, ?)"

        cursor.execute(query, listValues)
        conn.commit()
        label_invalid_product['fg'] = "green"
        label_invalid_product['text'] = "Success!"
    except Exception:
        label_invalid_product['fg'] = "red"
        if label_invalid_product['text'] == "":
            label_invalid_product['text'] = "Invalid input"


def main():
    """
    The main screen that shows immediately after you Run this program.

    :return: None.
    """
    conn = sqlite3.connect("data.sqlite")
    cursor = conn.cursor()
    # create_tables(cursor,conn)

    root = Tkinter.Tk()
    root.title("ShopApp")
    Tkinter.Label(root, text="Make an order", height=3, font='Arial 15 bold underline').grid(row=0, column=1)

    #####################
    # product row
    var_p_id = Tkinter.StringVar(root)
    Tkinter.Label(root, text="product ID", font=10).grid(row=1, column=0)
    p_id_entry = Tkinter.Entry(root, borderwidth=3, width=50, font=10, textvariable=var_p_id)
    p_id_entry.grid(row=1, column=1)

    Tkinter.Label(root, text="Name:", font=10, borderwidth=10).grid(row=2, column=0)
    p_name = Tkinter.Label(root, text="", font='Ariel 10 bold', borderwidth=10, fg="blue")
    p_name.grid(row=2, column=1)

    Tkinter.Label(root, text="Type:", font=10, borderwidth=10).grid(row=2, column=2)
    p_type = Tkinter.Label(root, text="", font='Ariel 10 bold', borderwidth=10, fg="blue")
    p_type.grid(row=2, column=3)

    Tkinter.Label(root, text="Price:", font=10, borderwidth=10).grid(row=2, column=4)
    p_price = Tkinter.Label(root, font='Ariel 10 bold', borderwidth=10, fg="blue")
    p_price.grid(row=2, column=5)

    Tkinter.Label(root, text="Quantity Available:", font=10, borderwidth=10).grid(row=2, column=6)
    p_quantity = Tkinter.Label(root, text="", font='Ariel 10 bold', borderwidth=10, fg="blue")
    p_quantity.grid(row=2, column=7)

    Tkinter.Button(root, text="Search for the product", font=20, pady=10,
                   command=lambda: search_for_the_product(p_id_entry, cursor, conn, p_name, p_type, p_price,
                                                          p_quantity)).grid(row=1, column=2)
    Tkinter.Button(root, text="Add product", font=20, pady=10, command=add_product).grid(row=1, column=3)
    #####################

    ######################
    # customer row
    Tkinter.Label(root, text="customer ID", font=10).grid(row=3, column=0)
    c_id = Tkinter.Entry(root, borderwidth=3, width=50, font=10)
    c_id.grid(row=3, column=1)

    Tkinter.Label(root, text="Name:", font=10, borderwidth=10).grid(row=4, column=0)
    c_name = Tkinter.Label(root, text="", font=10, borderwidth=10, fg="red")
    c_name.grid(row=4, column=1)

    Tkinter.Label(root, text="Address:", font=10, borderwidth=10).grid(row=4, column=2)
    c_address = Tkinter.Label(root, text="", font=10, borderwidth=10, fg="red")
    c_address.grid(row=4, column=3)

    Tkinter.Label(root, text="Phone number:", font=10, borderwidth=10).grid(row=4, column=4)
    c_phone = Tkinter.Label(root, text="", font=10, borderwidth=10, fg="red")
    c_phone.grid(row=4, column=5)

    Tkinter.Button(root, text="Search for the customer", font=20, pady=10,
                   command=lambda: search_for_the_customer(c_id, cursor, conn, c_name, c_address, c_phone)).grid(row=3,
                                                                                                                 column=2)
    Tkinter.Button(root, text="Add Customer", font=20, pady=10, command=add_customer).grid(row=3, column=3)
    ##########################

    ###########################
    # order unique
    Tkinter.Label(root, text="Quantity bought", font=10).grid(row=5, column=0)

    # quantity_okay = Tkinter.Label(root, text = "",font = 'Arial 10 italic', fg="red")
    # quantity_okay.grid(row=5,column=2)
    quantity_entry = Tkinter.Entry(root, borderwidth=3, width=50,
                                   font=10)
    quantity_entry.grid(row=5, column=1)

    Tkinter.Label(root, text="Total price:", font=("Arial 20 bold underline")).grid(row=6, column=0, columnspan=2,
                                                                                    rowspan=4,
                                                                                    padx=10, pady=20)
    total_price = Tkinter.Label(root, text="", font=("Arial 20 bold underline"))
    total_price.grid(row=6, column=2, columnspan=2, rowspan=4, padx=10, pady=20)
    Tkinter.Button(root, text="Calculate the price", font=20, pady=10,
                   command=lambda: calculate_the_price(p_price, quantity_entry, p_quantity, total_price)).grid(row=5,
                                                                                                               column=2)

    Tkinter.Label(root, text="Order id:", pady=20).grid(row=10, column=0)
    order_id = Tkinter.Label(root, text="", pady=20)
    order_id.grid(row=10, column=1)

    queryGETORDERID = f"SELECT max(id) FROM orders"

    query_done_orders = cursor.execute(queryGETORDERID).fetchall()
    conn.commit()

    oid = 1
    if (query_done_orders == [(None,)]):
        order_id['text'] = 9 * '0' + f"{oid}"
    else:
        oid = int(query_done_orders[0][0]) + 1
        v = (10 - len(str(oid)))
        order_id['text'] = v * '0' + f"{oid}"

    Tkinter.Label(root, text="Date:", pady=20).grid(row=10, column=2)
    order_date = Tkinter.Label(root, text=datetime.datetime.today(), pady=20)
    order_date.grid(row=10, column=3)
    ##########################

    #########################
    # last buttons
    Tkinter.Button(root, text="Make Order", font=20, pady=10,
                   command=lambda: make_order(cursor, conn, order_id, p_id_entry, c_id, quantity_entry, total_price,
                                              p_quantity, root)).grid(row=11, column=3, padx=20, pady=20)

    Tkinter.Button(root, text="List of Orders", font=20, pady=10, command=list_of_orders).grid(row=12, column=2,
                                                                                               padx=20, pady=20)
    Tkinter.Button(root, text="List of Products", font=20, pady=10, command=list_of_products).grid(row=12, column=3,
                                                                                                   padx=20, pady=20)
    Tkinter.Button(root, text="List of Customers", font=20, pady=10, command=list_of_customers).grid(row=12, column=4,
                                                                                                     padx=20, pady=20)
    #########################

    Tkinter.Button(root, text="EXIT", bg="red", fg="white", font=30, command=root.destroy).grid(row=15, column=4,
                                                                                                padx=20, pady=20)

    root.mainloop()


main()
