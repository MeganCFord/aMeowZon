
from handlers.customer_handler import *
from handlers.line_item_handler import *
from handlers.order_handler import *
from handlers.payment_handler import *
from handlers.product_handler import *
from handlers.cart_handler import *

from objects.customer_object import *
from objects.line_item_object import *
from objects.order_object import *
from objects.payment_object import *

import curses

try:
    class Meow():
        def __init__(self):
            # init curses
            self.screen = curses.initscr()
            self.current_user = None
            self.unlogged_in_menu()

        def unlogged_in_menu(self):

            # 1. log in to a user (user_menu)
            # 2. create a new user (create_new_user)
            # 3. view available products (shop_menu)
            # 4. generate report (generate_popularity_report)
            # 5. exit.
            self.screen.clear()
            self.screen.border(0)
            self.screen.addstr(12, 40, "1. Log in to a user")
            self.screen.addstr(13, 40, "2. Create a new user")
            self.screen.addstr(14, 40, "3. View available products")
            self.screen.addstr(15, 40, "4. Generate report")
            self.screen.addstr(16, 40, "5. Exit")
            self.screen.refresh()

            try:
                choice = int(chr(self.screen.getch()))

                if (choice == 1):  # Log in
                    self.user_menu()

                elif (choice == 2):  # Create a new user
                    self.create_new_user()

                elif (choice == 3):  # View available products
                    self.shop_menu()

                elif (choice == 4):  # Generate report
                    self.generate_popularity_report()

                elif (choice == 5):  # Exit
                    curses.endwin()
                    exit()
                else:
                    self.unlogged_in_menu()

            except ValueError:
                self.unlogged_in_menu()

        def logged_in_menu(self):
            # print the logged-in menu options.
            # request input.
            # based on input, do:
            # 1. log out (reset_user)
            # 2. shop(shop_menu)
            # 3. payment options(payment_menu)
            # 4. product report (generate_popularity_report)
            # 5. view orders
            # 6. exit.
            pass

        def user_menu(self):
            # generate the user index. (generate_customer )
            # for each index, use get_value to print the name value.
            # request input for which user.
            pass

        def create_new_user(self):
            # request input for all the things.
            # pass all the input into the create_new_user.
            # set the current user to the UID that returns,
            # then print the logged in menu.
            pass

        def set_user(user_id):
            # set user ID to current user.
            pass

        def reset_user(self):
            # set current user to none. that's it.
            pass

        def shop_menu(self):
            """
            Prints a list of products and prices from products.txt, saved as a index-uid dictionary in a scoped product_menu variable.  Then it requests next_step input from the user. If the user is not logged in, the only subsequent options are to go back or exit. If the user is logged in, they have the option of adding an item to their cart (via product_menu) or completing their order via payment_options_menu.
            ==========
            Method Arguments: none.
            """
            # load_product_library and for each available product index, get_value to print the name and price.
            product_menu = generate_product_list("data/products.txt")
            for index, UID in product_menu.items():
                info = get_value("data/products.txt", UID)
                print("{0}. {1}-- ${2}".format(index, info["name"], info["price"]))
            # are you logged in or not?
            if self.current_user is not None:
                # view your cart or note that it's empty.
                self.view_cart()
                print("press the number of the item you'd like to add to your cart,\nOr press'c' to check out, 'b' to go back, 'x' to exit.")
                next_step = input("\n>>")
                if next_step == "x":  # Exit.
                    print("goodbye.")
                    exit()
                elif next_step == "b":  # Go back.
                    self.logged_in_menu()
                elif next_step == "c":  # Check Out.
                    self.payment_options_menu(True)
                else:
                    print(next_step)
                    try:  # Add a product to your cart.
                        next_step = int(next_step)
                    except ValueError:
                        print("command not recognized.")
                        self.shop_menu()
                    finally:
                        if next_step in product_menu.keys():
                            self.add_to_cart_menu(product_menu[next_step])
                        else:
                            print("command not recognized.")
                            self.shop_menu()
            else:
                # if you're not logged in you can view products, but you can't do anything with a cart.
                print("You are not logged in.\nPress 'b' to go back and choose a login option, or x to exit.")
                next_step = input("\n>> ")
                if next_step == "b":
                    self.unlogged_in_menu()
                elif next_step == "x":
                    self.quit_menu()
                else:
                    print("command_not_recognized.")
                    self.shop_menu()

        def add_to_cart_menu(self, prod_ID):
            """
            Receives a unique id for a product to add to the current user's 'cart' property. To separate concerns from shop_menu, this function requests the quantity to add, and adds the item to the cart.
            ==========
            Arguments: the string unique ID of one of the products in products.txt.
            """
            item_to_add = get_value("data/products.txt", prod_id)
            print("how many" + prod_id["name"] + "s would you like to add?")
            print("'b' to go back, 'x' to exit.")
            quantity = input(">> ")

            if next_step == "b":  # go back.
                self.shop_menu()
            elif next_step == "x":  # exit.
                self.quit_menu()
            else:
                try:  # add a qty of items to cart property on the current user object.
                    quantity = int(quantity)
                except ValueError:
                    print("command not recognized.")
                    self.add_to_cart_menu(prod_ID)
                finally:
                    add_item_to_cart("data/customers.txt", self.current_user, prod_ID, quantity)
                    print(quantity + item_to_add["name"] + " added to cart.")
                    self.shop_menu()

        def convert_to_completed(payment_uid):
            # grab user name top-level variable.
            # generate a new order uid with that user name and the UID argument.
            # for each cart item, for qty number of times, generate a line item with the product number and order number.
            # return the order number.
            pass

        def payment_options_menu(completing=False):
            # pass user name top-level variable to generate_payment_list.
            # for each payment id in payment_list, use get_value to print the name or something.
            # if completing == false
            # request input to either add a new payment or go back.
            # if they'd like to add a new payment, request input for all the data,
            # then pass it to generate_new_payment and restart the function.
            # if completing == true
            # request input to either add a new payment or select a current payment.
            # if they'd like to add a new payment, request input for all the data,
            # then pass it to generate_new_payment and restart the function to print the updated list of payments.
            # if they select a current payment:
            # pass the payment uid to convert to completed.
            # print the order number, and print the top level logged-in menu.
            pass

        def generate_popularity_report(self):
            pass

    if __name__ == '__main__':
        # Meow().print_hey()
        # print_hello()
        # Meow().unlogged_in_menu()
        Meow()

except KeyboardInterrupt:
    curses.endwin()
