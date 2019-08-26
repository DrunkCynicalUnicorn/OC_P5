# -*- coding: utf-8 -*-


class Displayer():
    
    """ Instance of this class is assigned to display data and to interact
    with the user. It consults mysql_interface class to get data to display,
    and sends back to this same instance class user choices. Instances do not
    have any attributes """
    
    def print_startpoint(self):

        """ This method prints the start interactive menu """

        print("\n1. Go to food categories", "2. Go to your favorite substitutes", sep="\n")
        valid_choice = False
        while not valid_choice:
            user_input = input("\nSelect the number corresponding to your choice then hit 'Enter' : ")
            if user_input not in "12":
                print("\nPlease enter a valid choice by hitting the number corresponding to your choice")
                continue
            else :
                valid_choice = True
        return user_input


    def print_categories(self, categories):

        """ This method prints out the list of the predefined categories and engage the user to choose one.
         Takes no positional arg and returns the chosen category' id"""

        for category in categories:
            print(f"\n{category[0]}. {category[1]}")
        valid_choice = False
        while not valid_choice:
            try:
                category_id = int(input("\nSelect the number corresponding to your choice then hit Enter : "))
            except:
                print("Please enter a valid ENTIRE NUMBER !")
                continue
            if category_id not in range(1, len(categories)+1):
                print("\nYour choice does not correspond to any category... Please enter a valid number : ")
                continue
            else :
                valid_choice = True

        return category_id


    def print_products_per_category(self, products_per_cat):

        """ This method prints all products belonging to the category chosen by the user.
        Takes one positional arg : the chosen category' id ; returns the id of the product chosen"""

        
        correspondance_dict = dict()
        for nb, product in enumerate(products_per_cat):
            correspondance_dict[nb+1] = product[0]
            print(f"{nb+1}. {product[1]}")
        valid_choice = False
        while not valid_choice:
            try:
                product_choice = int(input("\nSelect the number corresponding to your choice then hit Enter : "))
            except:
                print("\nPlease enter a valid ENTIRE NUMBER !")
                continue
            if product_choice not in correspondance_dict.keys():
                print("\nYour choice does not correspond to any product... Please enter a valid number : ")
                continue
            else:
                valid_choice=True

        return correspondance_dict[int(product_choice)]


    def print_substitute_data(self, data, product_id):

        """ This method prints out a substitute dataset and asks the user for selecting this substitute
        as a favorite substitute for this product.
        Takes one positional arg : the product id to replace by a substitute """
        stores_list = [store[0] for store in data[1]]
        print(data)
        print(stores_list)
        stores = ", ".join(stores_list)
        print(f"\nProduct name : {data[0][1]}\nDescription : {data[0][2]}\nURL : {data[0][3]}\nStores to buy this"
              f" product : {stores}\n")

        user_choice = input("Would you like to tag this product as a favorite substitute ? Enter 'y' to do "
                            "so, anything else to leave : ")
        return user_choice
        



    def print_all_favorites(self, favorites):

        """ This method prints out all the substitute previously set as favorites by the user.
        Does not need any arg to work out """

        for fav in favorites:
            print(f"\nProduct : {fav[0]}\nDescription : {fav[1]}\nURL : {fav[2]}\nIs your substitute for {eval(fav[3])[0][0]}\n\n\n")







