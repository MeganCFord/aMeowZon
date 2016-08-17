from objects.customer_object import *
from utility.utility import *
import sqlite3


def generate_new_customer(name="", address="", city="", state="", zipcode="", phone=""):
    """
    
    ===========
    Method Arguments: strings. 1. file_name of txt file to add to, 2. name, 3. address, 4. city, 5. state, 6. zipcode, 7. phone. Note that these are keyed arguments so can be passed in any order if specified with the appropriate key.
    """
    with sqlite3.connect("bangazon.db") as database:
        db = database.cursor()

        db.execute("insert into Customer (FullName, StreetAddress, City, StateOfResidence, ZipCode, PhoneNumber) values (?,?,?,?,?,?)", (name, address, city, state, zipcode, phone))
        database.commit()
        db.execute("select c.CustomerId from Customer c where c.FullName = ?", (name,))
        print(db.fetchone())


def generate_customer_menu():
    """
    Queries bangazon.db's customer table and returns a list of tuples for each active customer. The first item in each tuple is the unique customer ID, the second is the customer's full name. This list will be printed in utility.py.
    ============
    Method Arguments: None.
    """

    with sqlite3.connect("bangazon.db") as database:
        db = database.cursor()

        db.execute("""select c.CustomerId, c.FullName
                        from Customer as c""")
        return db.fetchall()
