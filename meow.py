
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
            self.screen.addstr(18, 40, '')
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
                    self.quit_menu(self.unlogged_in_menu)
                else:
                    self.unlogged_in_menu()

            except ValueError:
                self.unlogged_in_menu()

        def logged_in_menu(self):
            # print the logged-in menu options.
            # request input.
            # based on input, do:
            self.screen.clear()
            self.screen.border(0)
            self.screen.addstr(12, 40, '1. Log out')
            self.screen.addstr(13, 40, '2. Shop')
            self.screen.addstr(14, 40, '3. Payment options')
            self.screen.addstr(15, 40, '4. Product report')
            self.screen.addstr(16, 40, '5. Exit')
            self.screen.addstr(18, 40, '')
            self.screen.refresh()

            try:
                choice = int(chr(self.screen.getch()))

                if choice == 1:
                    self.reset_user()
                    self.unlogged_in_menu()

                elif choice == 2:
                    self.shop_menu()

                elif choice == 3:
                    self.payment_options_menu()

                elif choice == 4:
                    self.generate_popularity_report()

                elif choice == 5:
                    self.quit_menu(self.logged_in_menu)

            except ValueError:
                self.logged_in_menu()

        def quit_menu(self, back_to_menu):
            self.screen.clear()
            self.screen.border(0)
            self.screen.addstr(12, 40, 'Are you sure you want to exit? [ y / n ]')
            self.screen.addstr(14, 40, '')
            self.screen.refresh()

            try:
                choice = chr(self.screen.getch())

                if choice.lower() == 'y':
                    curses.endwin()
                    quit()
                else:
                    if self.current_user == None:
                        self.unlogged_in_menu()
                    else:
                        back_to_menu()

            except ValueError:
                back_to_menu()

        def user_menu(self):
            # generate the customer menu.
            # for each customer item, use get_value to print the name value.
            # request input for which user.
            user_lib = generate_customer_menu('data/customers.txt')

            self.screen.clear()
            self.screen.border(0)

            row = 12
            for index, user_id in user_lib.items():
                user = get_value('data/customers.txt', user_id)
                self.screen.addstr(row, 40, '{0}. {1}'.format(index, user.name))
                row += 1
            self.screen.addstr((row + 1), 40, '')
            self.screen.refresh()

            try:
                choice = int(chr(self.screen.getch()))
                self.set_user(user_lib[choice])
                self.logged_in_menu()

            except ValueError:
                self.user_menu()

            except IndexError:
                self.user_menu()

        def create_new_user(self):
            # request input for all the things.
            # pass all the input into the create_new_user.
            # set the current user to the UID that returns,
            # then print the logged in menu.
            name = get_param('What is your name?', self.screen)
            address = get_param('What is your street address?', self.screen)
            city = get_param('What city do you live in?', self.screen)
            state = get_param('What state do you live in?', self.screen)
            zipcode = get_param('What is your zipcode?', self.screen)
            phone = get_param('What is your phone number?', self.screen)

            try:
                new_uid = generate_new_customer('data/customers.txt', name, address, city, state, zipcode, phone)
                self.set_user(new_uid)
                self.logged_in_menu()
            except:
                self.unlogged_in_menu()

        def set_user(self, user_id):
            # set user ID to current user.
            self.current_user = user_id

        def reset_user(self):
            # set current user to none. that's it.
            self.current_user = None

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
                    self.quit_menu(self.shop_menu)
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
            quantity = get_param(">> ", self.screen)

            if quantity == "b":  # go back.
                self.shop_menu()
            elif quantity == "x":  # exit.
                self.quit_menu(self.shop_menu)
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

        def view_cart(self):
            """
            Displays the content of the currently logged in user

            Args- None
            """
            # get the user object of the currently logged in user
            current_user_obj = get_value("data/users.txt", self.current_user)
            # get that users cart
            cart = current_user_obj.cart
            # check if cart is not empty
            if cart == {}:
                print("Your cart is empty. Start shopping!")
            else:
                print("Your cart:")
                print("*" * 44)
                # format for columns
                row_string = "{0:<18}{1:<11}${2:<14}"
                total_string = "{0:<29}${1:<14}"
                total_list = []
                # loop over cart items and calculate total (grab price from 'products.txt')
                for prod_id, qty in cart.items():
                    product_obj = get_value("data/products.txt", prod_id)
                    total = qty * product_obj["price"]
                    # append total to list of totals (for amount due calculation)
                    total_list.append(total)
                    # limit product name
                    product_name = product_obj.name
                    product_name = (product_name if len(product_name) <= 17 else product_name[:14] + "...") + " "
                    print(row_string.format(product_name, qty, total))
                print("*" * 44)
                # print out total amount due
                print(total_string.format("Total:", sum(total_list)))

        def convert_to_completed(payment_uid):
            # grab user name top-level variable.
            # generate a new order uid with that user name and the UID argument.
            # for each cart item, for qty number of times, generate a line item with the product number and order number.
            # return the order number.
            pass

        def payment_options_menu(self, completing=False):
            self.screen.clear()
            self.screen.border(0)
            how_far_down = 12
            # pass user name top-level variable to generate_payment_list.
            payment_options = generate_payments_menu("data/payments.txt", self.current_user)
            # for each payment id in payment_list, use get_value to print the name or something.
            for index, uid in payment_options:
                payment = get_value("data/payments.txt", uid)
                self.screen.addstr(how_far_down, 40, index + ". " + payment["name"])
                how_far_down += 1

            self.screen.addstr(how_far_down, 40, '')
            how_far_down += 1
            self.screen.refresh()

            if completing is False:
                self.screen.addstr(how_far_down, 40, "n for new payment. b to go back. x to exit.")
                next_step = get_param(">> ", self.screen)
                if next_step == "n":
                    self.new_payment()
                    self.payment_options_menu(completing)
                elif next_step == "b":
                    self.logged_in_menu()
                elif next_step == "x":
                    self.quit_menu(self.payment_options_menu)
                else:
                    self.payment_options_menu()
            elif completing is True:
                self.screen.addstr(how_far_down, 40, "press the number of the payment to use for this order. n to make a new payment. b to go back. x to exit.")
                next_step = get_param(">>", self.screen)
                if next_step == "n":
                    self.payment_options_menu(False)
                elif next_step == "b":
                    self.shop_menu()
                elif next_step == "x":
                    self.quit_menu(self.shop_menu)
                else:
                    try:
                        next_step = int(next_step)
                    except ValueError:
                        self.payment_options_menu(True)
                    finally:
                        if next_step in payment_options.keys():
                            self.convert_to_completed(payment_options[next_step])
                        else:
                            self.payment_options_menu(True)

        def new_payment(self):
            account_num = input("enter the account number.\n>> ")
            account_name = input("enter a nickname for this account.\n>> ")
            generate_new_payment("data/payments.txt", account_name, account_num, self.current_user)

        def generate_popularity_report(self):
            pass

    if __name__ == '__main__':
        # Meow().print_hey()
        # print_hello()
        # Meow().unlogged_in_menu()
        Meow()

except KeyboardInterrupt:
    curses.endwin()
