# -*- coding: utf-8 -*-

import mysql.connector
import apiReader_class as api
import constants


class MySQLInterface():
    
    def __init__(self):
        self.connection = mysql.connector.connect(host='localhost',
                             user='consumer',
                             password='password',
                             database='p5_db',
                             charset='utf8')
    
        self.cursor = self.connection.cursor()
    
    




    def create_tables(self, sql_cmd_list):

        for sql_cmd in sql_cmd_list:
            self.cursor.execute(sql_cmd)
        self.connection.commit()



    def load_data(self, data, sql_cat, sql_prod, sql_store, sql_assoc):
        
        
        known_stores = list()
        
        for category_data in data:
            category = category_data[0]['category']
        
            self.cursor.execute(sql_cat, (category,))
            self.connection.commit()


            for product_data in category_data:
                product_fields = (product_data['category'], product_data['product_name_fr'], product_data['description'],
                           product_data['url'], product_data['nutrition_grade_fr'])
                self.cursor.execute(sql_prod, product_fields)

                # must not commit, here or later : commit seems to be auto and doing it manually can participate to
                # raise a "command out of sync" error...




                for store_name in product_data['stores']:
                    store_name = store_name.strip().lower().capitalize()
                    if store_name not in known_stores:
                        known_stores.append(store_name)
                        try:
                            self.cursor.execute(sql_store, (store_name,)) # param must be in tuple for mysql.connector module to accept it
                        except mysql.connector.errors.IntegrityError:
                            continue
                    
                    # following code, whose purpose is to fill the association table, did not even work in draft-test
                    # phase : it always raised a sql syntax error or "could not process parameters" error : too much or not enough params, whatever data
                    # type used (dict or tuple) was, or sometimes, in alternative tests, syntax problems with %s syntax
                    # ??? it might be because the 2 values researched are calculated by SELECT sub-requests... ???

                    #association_dict = {"product_name": product_data["product_name_fr"], "store_name": store_name}
                    #association_tuple = (product_data["product_name_fr"], store_name)  # = exactly the same syntax than
                    #self.cursor.execute(sql_assoc, association_tuple)                  # in product_filler, which works
                                                                                       # perfectly... error must be
                                                                                       # raised because of the 2 subrequests
                                                                                       # of the mysql request
                                                                                       # + some errors let us understand
                                                                                       # that select subrequests work fine

                    self.association_table_builder(sql_assoc, product_data, store_name)


        self.connection.commit()


    def association_table_builder(self,sql_cmd, data, store):
        association_tuple = (data["product_name_fr"], store)
        product_name = data["product_name_fr"]
        self.cursor.execute(sql_cmd, (product_name,))
        #self.cursor.execute(sql_cmd2, (store,))
        self.connection.commit()


if __name__ == "__main__":
    api_reader = api.ApiReader()
    interface = MySQLInterface()
    interface.create_tables(constants.tables_creation_cmds_list) # is ok
    interface.load_data(api_reader.get_data(), constants.cat_filler, constants.prod_filler, constants.store_filler,
                        constants.store_prod_association_builder) # not ok, cf supra func body