# -*- coding: utf-8 -*-

import apiReader_class as api
import mysql_interface_class as sql
import displayer_class as display


api_reader = api.ApiReader()
sql_interface = sql.MySQLInterface()
displayer = display.Displayer()


sql_interface.create_tables() 
sql_interface.load_data(api_reader.get_data())


use_it = True
while use_it : 
    user_choice = displayer.print_startpoint()
    
    
    if int(user_choice) == 1:
        categories = sql_interface.get_categories()
        cat_id = displayer.print_categories(categories)
        
        products_per_cat = sql_interface.get_products_per_category(int(cat_id))
        prod_id = displayer.print_products_per_category(products_per_cat)
        
        substitute_data = sql_interface.find_substitute(int(prod_id))
        tag_prod = displayer.print_substitute_data(substitute_data, int(prod_id))
        if tag_prod.lower() == "y":
            sql_interface.set_favorite(int(prod_id), substitute_data)
    else:
        favorites = sql_interface.get_all_substitutes()
        displayer.print_all_favorites(favorites)
    
    restart_or_leave = input("\nTape 'y' to go back to start selection page, anything else to leave the program : ")
    if restart_or_leave.lower() == "y":
        continue
    else:
        use_it = False