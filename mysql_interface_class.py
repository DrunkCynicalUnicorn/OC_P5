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



    def load_data(self, data, sql_cmd_dict):
        
        
        known_stores = list()
        
        for category_data in data:
            category_filler =  """INSERT IGNORE INTO category(name) 
            VALUES(%(category)s);"""
            self.cursor.execute(sql_cmd_dict["category_filler"], category_data[0])


            for product_data in category_data:
                self.cursor.execute(sql_cmd_dict["product_filler"], product_data)
                self.connection.commit()
            

                for store_name in product_data['stores']:
                    store_name = store_name.strip().lower().capitalize()
                    if store_name not in known_stores:
                        known_stores.append(store_name)
                        try:
                            self.cursor.execute(
                                    sql_cmd_dict["store_name_filler"],
                                    (store_name,)) # param must be in tuple for mysql.connector module
                                                                      # to accept it
                        except mysql.connector.errors.IntegrityError:
                            continue
                    
                        #finally:
                         #   association_dict = {"product_name" : product_data["product_name_fr"], "store_name" : store_name}
                          #  test_tuple = (product_data["product_name_fr"], store_name)
                           # cursor.execute(store_product_association_cmd, test_tuple)






            #for store_data in stores_list:
             #   store_name = store_data.strip()
              #  cursor.execute(store_name_cmd, store_name)

            #cursor.execute(store_product_association_cmd, (store_name,))
            self.connection.commit()
        
        self.connection.close()



if __name__ == "__main__":
    api_reader = api.ApiReader()
    interface = MySQLInterface()
    #clean_data = list(api_reader.get_data())
    interface.create_tables(constants.tables_creation_cmds_list)
    interface.load_data(api_reader.get_data(), constants.table_filling_cmds_dict)