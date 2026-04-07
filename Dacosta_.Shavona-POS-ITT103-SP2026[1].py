# CODE COBRAS!
# Best Buy Retail Store
# ITT103 - Programming Techniques
#------------------------------------------------------------------------

#Product Management
"""
The three lists act as parallel arrays to store our inventory.
Each list corresponds by index, meaning store_item[0] is linked to
item_price[0] and item_quantity[0]. This structure allows for synchronized
data management across different product attributes.
The catalog includes a minimum of 10 predefined items.
"""

store_item = [
    "2L Wata Wata Water", "2LB Jasmine Rice", "Grace Tin Mackerel", "Corn Beef", "2L Bigga Soda",
    "1LB Flour", "1LB Refine Cornmeal", "Red & White Cornflakes", "Frosted Flakes", "1LB Brown Sugar"
]
item_price = [200, 500, 150, 300, 180, 120, 80, 600, 740, 120]
item_quantity = [20, 3, 30, 40, 12, 12, 4, 20, 30, 40]

"""
This function handles the visual presentation of the store's inventory.
I've used a for loop to iterate through the lists to format the text 
into a clean, easy to read layout.
"""
def display_inventory(items, prices, stock):
    print("-------------------------------------")
    print("  WELCOME TO BEST BUY RETAIL STORE")
    print("--------------------------------------")
    for i in range(len(items)):
        print(f"\n{i + 1}. Item - {items[i]} \n\tPrice - ${prices[i]} \n\tQuantity - {stock[i]}")
    print("------------------------------------------------------------------")
#-----------------------------------------------------------------------------------------------------

# Calculation 5% Discount

"""
This Function handles the store's promotional logics. It calculates a 5% 
reduction if the total exceeds a $5000 threshold.
"""
def calculate_discount(bill_total): #initialize the discount value to zero as the default state
    discount_val = 0
    if bill_total > 5000:
        discount_val = bill_total * 0.05 #calculating 5% reduction for qualifying transactions
        print(f"\n (5% Discount Applied ${discount_val} for spending $5000 and more)")
    return discount_val

#Checkout and Payment Processing

"""
This function handles payment validation. It ensures the cashier cannot 
proceed until the amount received is greater than or equal to the total 
due and calculates the change.
"""
def process_payment(total_due):
    while True:
        try:
            # capture the payment amount provided by customer
            amount_received = float(input(f"\nEnter amount received from customer: $"))

            if amount_received >= total_due: #calculates remnaining balance to returnto custome
                customer_change = amount_received - total_due
                print(f"Change Due: ${customer_change:.2f}")
                print("\nTransaction Completed!")
                return amount_received, customer_change
            else:
                print(f"ERROR: Not enough funds. Amount Due: ${total_due - amount_received}")
        except ValueError:
            print("Error: Please enter a numerical value for payment.")

# Main program loop

while True:
    # Reset variables for each NEW customer session
    """
        The total variable is initialized at zero to serve as a running balance.
        As items are added to or removed from the cart, this variable is updated 
        to reflect the final amount the customer owes at the end of the transaction.
        The cart_items list was also created to store sub lisyts of the item name, quantity etc
        for the cart to show detail information. 
        """
    cart_items = []
    total = 0

    payment_info = None # This is used to predefine the variable for the Recept final bill

    # calling the function so that they could be recognized in the strings
    display_inventory(store_item, item_price, item_quantity)

    # Shopping Cart Operations
    """
    The following inner loop manages the persistent flow for the POS system, 
    allowing the cashier to add, remove, or view items without 
    closing the program.
    """
    while True:
        print("\n\t\t=========Point of Sale=========")

        """
            The action variable captures the user's primary menu choice.
            By using 'if and elif branches, the system can isolate specific logic 
            paths, ensuring that Selling code does not interfere with Removal code.
            """

        action = input("\nPlease Select: (1) Add Item, (2) Remove Item, (3) View Cart, (4) Checkout: ")

        if action == "1":

            """
            In the Selling path, the system first verifies if the item name exists.
            If found, it converts the name into its index position (idx). This index 
            is then used to look up values in the parallel price and quantity lists.
            """

            item_name = input("\nEnter Item Name EXACTLY as Shown in List: ")
            if item_name in store_item:
                idx = store_item.index(item_name)

                """
                The try except block is a crash prevention measure. It ensures 
                that if a user types text instead of a number for quantity, 
                the program handles the valueerror gracefully instead of crashing.
                """

                try:
                    qty = int(input(f"Enter quantity for {item_name}: "))
                except ValueError:
                    print("Error: Invalid number.")
                    continue

                """
                Before modifying any data, its good to compare the requested amount against 
                the available stock. This prevents negative inventory scenarios.
                """

                if qty <= item_quantity[idx]:
                    sub = item_price[idx] * qty

                    """
                    Displaying the subtotal before committing the sale allows the 
                    cashier to double check with the customer before the balance 
                    is added to the grand total. For this i've use strings and lists
                    to store the variables. Also, .lower was adding to prevent code from crashing despite
                    entering the information whether upper case or lower case, it would
                    still accept it.
                    """

                    confirm = input(f"Add to cart for ${sub}? (yes/no): ").lower()
                    if confirm == "yes" or confirm == "y":
                        item_quantity[idx] -= qty #Deduct the purchase quantity from the inventory list
                        total += sub #increement customers running total with the item's subtotal
                        cart_items.append([item_name, qty, sub]) #record item as sub list in cart for final receipt
                        print(f"Success! {item_name} is added.")

                        """
                        Immediately after the inventory is updated, the system 
                        checks if the stock has dropped to 5 or fewer units to 
                        warn the cashier that a restock is needed. Thats when you see the 
                        LOW STOCK ALERT message and it tells you how many units are available.
                        """

                        if item_quantity[idx] <=5:
                            print(f" Low Stock Alert: Only {item_quantity[idx]} Now Remaining.")
                else:
                    print("Error: Insufficient stock.")
            else:
                print("Item not found Please check spelling or capitalization.")

        elif action == "2":
            """
            Allows the cashier to remove items and automatically returns 
            the stock to the inventory. This path performs reverse math. It adds the quantity back 
            into the inventory list and subtracts the corresponding cost from 
            the grand total, canceling a specific part of a sale and putting 
            back the unit in its inventory.
            """
            item_to_remove = input("Enter item name to REMOVE: ")

            # Verify if the entered item exists within the inventory
            if item_to_remove in store_item:
                idx = store_item.index(item_to_remove)
                try:
                    qty_back = int(input(f"Quantity to remove: "))
                except ValueError:
                    print("Error: Invalid number.")
                    continue
                refund = item_price[idx] * qty_back

                """
                This prevents the total from becoming negative if a cashier tries 
                to remove more items than were originally added to the cart.
                item_quantity[idx] += qty_back is used to update the inventory database
                based on the fcat that the customer is returning the item hence using addition
                which is the += to but the units back into item_quantity list
                so that it can be sold to someone else.
                """

                """
                total -= refund is used to update the customer's bill hence using
                subtraction to remove the cost of the items from the total so that
                the customer doesnt get charged for items they no longer have.
                """

                """
                if refund_amount <= total was used for validation to prevent cashoer from 
                accidentally refunding more money than what the customer paid.
                """
                if refund <= total:
                    item_quantity[idx] += qty_back
                    total -= refund
                    print(f"Removed. New Total: ${total}")
            else:
                print("Item not found.")

        elif action == "3":
            """
            Provides an option to view the cart with a list of items, 
            their quantities, and their total price. This section checks
            if the cart is empty. If not, it iterates through the cart_items list to
            display each individual purchase and the total.
            """
            print("\n--- Current Cart ---")
            # Checking the shopping cart if its empty
            if not cart_items:
                print("Cart is Empty")
            else:
                # Iterate through cart entries to display itemized details
                for item in cart_items:
                    #This prints the information that are in the string per line
                    print(f"{item[0]} | Quantity: {item[1]} | Subtotal: ${item[2]}")

                #Show the current running total for the transaction
                print(f"Running Total: ${total}")

        elif action == "4":
            """
            This Calculates the subtotal, applies a 10% sales tax, and displays 
            the final amount due before processing payment. At this stage, I am calling 
            the variable since i used a function for the 5% discount earlier.
            """
            discount = calculate_discount(total) #detremining if the transaction qualifies for 5% discount
            bill = total - discount #subtracting applied discounts from the original subtotal
            tax = bill * 0.10 #calculating 10% tax based on the new subtotal
            final = bill + tax #formulating the grand total by adding the tax to the bill

            # Checkout generation

            print(f"\n========= CHECKOUT ==========")
            print(f"Subtotal:   ${total:.2f}")
            if discount > 0:
                print(f"Discount (5%): -${discount:.2f}") #Apply and show 5% discount if applicable
                print(f"New Subtotal:  ${bill:.2f}")

            print(f"Sales Tax (10%): ${tax:.2f}") #Calculates and display 10% sale
            print(f"Grand Total: ${final:.2f}") # Print Final amount due
            print("=============================")

            payment_info = process_payment(final)
            if payment_info: #Trigger payment validation
                received, change = payment_info
                print(f"\n{'OFFICIAL RECEIPT':^45}")
                print(f"{'Best Buy Retail Store':^45}")
                print(f"{f'=' * 45}")

                # itemized List Headers
                # These formatting codes (<20, <5) ensure columns stay aligned
                print(f"{'Item':<20} {'Qty':<5} {'Unit $':<10} {'Total $':<10}")
                print("-" * 45)

                # Itemized List Loop
                # Iterates through each sublist in cart_items
                for item in cart_items:
                    # Look up the unit price from the master list using the item name
                    idx = store_item.index(item[0])
                    unit_p = item_price[idx]

                    # Prints Item Name | Quantity | Unit Price | Item Subtotal
                    print(f"{item[0]:<20} {item[1]:<5} ${unit_p:<9.2f} ${item[2]:<9.2f}")

                print("-" * 45)

                #Financial Summary
                print(f"Subtotal:           ${total:>10.2f}")
                if discount > 0:
                    print(f"Discount (5%):     -${discount:>10.2f}")
                    print(f"Sales Tax (10%):    ${tax:>10.2f}")
                    print(f"===============================")
                    print(f"GRAND TOTAL:        ${final:>10.2f}")
                    print(f"===============================")
                    print(f"Amount Paid:       ${received:>10.2f}")
                    print(f"Change Due:        ${change:>10.2f}")
                    print(f"{'Thank You for choosing Best Buy!':^45}\n")
                break  # Ends shopping for this customer

    #Store Control

    """
    This section is for the final control for the store's daily operations.
    after a customer completes their transaction and a receipt is generated, the system asks
    the cashier they they are ready for another customer, if no is selected,
    the loop is broken.  
    """
    next_customer = input("\nOpen register for next customer? (yes/no): ").lower()
    if next_customer == "no" or next_customer == "n":
        print("Closing Register. Goodbye!")
        break

input("\nProgram Finish, Press Enter to Exit...")