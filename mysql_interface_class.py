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


if __name__ == "__main__":
    import apiReader_class as api
    api_reader = api.ApiReader()
    mysql_interface = MySQLInterface()
    mysql_interface.create_tables() # is ok
    mysql_interface.load_data(api_reader.get_data()) # is ok