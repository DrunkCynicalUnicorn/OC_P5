# -*- coding: utf-8 -*-

import mysql.connector
import constants


class MySQLInterface():

    """
    Class dedicated to interaction with the database's project. Its instance
    attributes are Connection and Cursor's mysql.connector library objects,
    which are not to be modified, and references to all the raw mysql requests 
    needed, so these requests are callable from the class instance, and 
    updatable in the constants file, which points to the same requests
    """
    
    def __init__(self):
        self.connection = mysql.connector.connect(host='localhost',
                             user='consumer',
                             password='password',
                             database='p5_db',
                             charset='utf8')
    
        self.cursor = self.connection.cursor()
        
        self.sql_architecture_cmds = constants.tables_creation_cmds_list
        
        self.sql_insert_cmds = constants.mysql_insert_cmds

        self.sql_select_cmds = constants.mysql_select_cmds

        self.set_fav_cmd = constants.set_favorite_cmd

        self.get_substitutes_cmd = constants.get_favorites_cmd


    def create_tables(self):
        
        """
        This method builds up the database architecture. Takes no positional 
        arg since sql code is updatable directly in the constants file
        """

        for sql_cmd in self.sql_architecture_cmds:
            self.cursor.execute(sql_cmd)
        self.connection.commit()


    def load_data(self, data):
        
        """
        This method fills the database, given the data passed in the only
        positional arg, that has to be in form returned by data_cleaner func
        from api interface class
        """
                
        known_stores = list()
        
        for category_data in data:
            category = category_data[0]['category']
            self.cursor.execute(self.sql_insert_cmds["cat_filler"], 
                                (category,))
            self.connection.commit()

            for product_data in category_data:
                product_fields = (product_data['category'], 
                                  product_data['product_name_fr'], 
                                  product_data['description'],
                                  product_data['url'], 
                                  product_data['nutrition_grade_fr'])
                self.cursor.execute(self.sql_insert_cmds["prod_filler"], 
                                    product_fields)
                product_id = self.cursor.lastrowid

                # must not commit, here or later : commit seems to be auto and 
                # doing it manually can participate to raise a 
                #"command out of sync" error...

                for store in list(set(product_data['stores'])):
                    if store not in known_stores:
                        known_stores.append(store)
                        try:
                            self.cursor.execute(
                                    self.sql_insert_cmds['store_filler'],
                                    (store,)
                                    )
                        except mysql.connector.errors.IntegrityError:
                            continue

                    association_keys = (product_id, store)
                    self.cursor.execute(
                            self.sql_insert_cmds["store_prod_assoc_builder"], 
                            association_keys)

        self.connection.commit()


    def get_categories(self):
        
        """ This method returns a list of category'is and category's name 
        tuples, to be formated and print out by the displayer object """
        
        self.cursor.execute(self.sql_select_cmds["select_categories"])
        return self.cursor.fetchall()
 
    
    def get_products_per_category(self, category_id):
        
        """ This method is charged of fetching all products for one given
        category. Receives one positional arg from the displayer class object,
        the category_id corresponding to the category chosen by the user """

        self.cursor.execute(self.sql_select_cmds["select_products_per_category"], (str(category_id),))
        return self.cursor.fetchall()
    
    
    def find_substitute(self, product_id):

        """ This method determines is charged of finding a better food, based on the nutriscore.
        Takes one positional argument, the original product's id selected"""

        substitute_data = list()

        self.cursor.execute(self.sql_select_cmds["find_substitute"], (product_id, product_id))
        substitute_data.append(self.cursor.fetchall()[0])

        substitute_id = substitute_data[0][0]
        self.cursor.execute(self.sql_select_cmds["select_stores_substitute"], (substitute_id,))
        substitute_data.append(self.cursor.fetchall()[0])

        return substitute_data


    def set_favorite(self, product_id, substitute_data): # TO TEST

        """ This method registers a product as a favorite by setting its substitute field to True.
        Takes two positional args : the original product id, and the substitute data, in the datastructure
        provided by self.find_substitute() precedent method """

        self.cursor.execute("""SELECT name FROM product WHERE id = %s;""", (product_id,))
        original_product = self.cursor.fetchall()
        self.cursor.execute(self.set_fav_cmd, (str(original_product), substitute_data[0][0]))
        print("\nYou have just set this product as one of your favorite products\n")


    def get_all_substitutes(self): #TO TEST

        """ This method queries the DB to retrieve all products marked as substitutes by the user.
        Does not need any argument """

        self.cursor.execute(self.get_substitutes_cmd)
        return self.cursor.fetchall()



        
        


if __name__ == "__main__":
    import apiReader_class as api
    api_reader = api.ApiReader()
    mysql_interface = MySQLInterface()
    
    mysql_interface.create_tables() # is ok
    mysql_interface.load_data(api_reader.get_data()) # is ok
    
    categories = mysql_interface.get_categories()
    products_per_cat = mysql_interface.get_products_per_category(7)
    print(categories, products_per_cat, sep="\n") # is ok

    substitute = mysql_interface.find_substitute(355)
    print(substitute) # is ok