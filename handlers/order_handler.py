from objects.order_object import *
from utility.utility import *


def new_order(cid, pid, file='data/orders.txt'):
    """ Creates a new order object with the customer ID and payment
        passed in
        Method arguments
        ================
        cid - the unique customer ID
        pid - the unique payment ID
    """
    new_order_obj = Order(cid, pid)
    new_id = add_to_file(file, new_order_obj)
    return new_id


def build_order_dict(cid=None, file='data/orders.txt'):
    """ Returns a dictionary of orders matching the arguments passed in
      Method arguments
      ================
      file - the file to read from; default is the standard orders file,
             but in testing, the test file is passed in
      cid -  the customer ID to match; default is none, which will return
             all customers
    """
    order_lib = deserialize(file)
    temp_order_lib = dict()
    index = 1

    if cid == None:
        for uid, item in order_lib.items():
            temp_order_lib[index] = uid
            index += 1
    else:
        for uid, item in order_lib.items():
            if item.customer_id == cid:
                temp_order_lib[index] = uid
                index += 1

    return temp_order_lib
