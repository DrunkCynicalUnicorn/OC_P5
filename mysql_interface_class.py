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
        
            self.cursor.execute(sql_cmd_dict["category_filler"], category_data[0])

            """
            = > this first execute() func raises following error : 
            Traceback(most
            recent
            call
            last):                                                                                        File
            "mysql_interface_class.py", line
            85, in < module > interface.load_data(api_reader.get_data(), constants.table_filling_cmds_dict)
            File
            "mysql_interface_class.py", line
            39, in load_data
            self.cursor.execute(sql_cmd_dict["category_filler"], category_data[0])
            File
            "C:\Users\pc_portable\AppData\Local\Programs\Python\Python37\lib\site-packages\mysql\connector\cursor_cext.py", line
            248, in execute
            prepared = self._cnx.prepare_for_mysql(params)
            File
            "C:\Users\pc_portable\AppData\Local\Programs\Python\Python37\lib\site-packages\mysql\connector\connection_cext.py", line
            613, in prepare_for_mysql
            result[key] = self._cmysql.convert_to_mysql(value)[0]
            _mysql_connector.MySQLInterfaceError: Python
            type
            list
            cannot
            be
            converted
            !!! what list ??? => repl might be referring to api data, whom 2 first levels are nested lists... ???
                -> but the func was perfectly working in this form during non-object oriented test (= without sql_class)
                -> + a new test whithout a python sql class raises exactly the same error...
                -> + changing the first execute func param (= the sql request), by putting it in a dedicated classic var 
                    or in raw form does not change anything...
            """

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
                                    (store_name,)) # param must be in tuple for mysql.connector module to accept it
                        except mysql.connector.errors.IntegrityError:
                            continue
                    
                    # following code, whose purpose is to fill the association table, did not even work in draft-test
                    # phase : it always raised a sql syntax error : too much or not enough params, whatever data
                    # type used (dict or tuple) was, or sometimes, in alternative tests, syntax problems with %s syntax
                    # ??? it might be because the 2 values researched are calculated by SELECT sub-requests... ???
                    association_dict = {"product_name" : product_data["product_name_fr"], "store_name" : store_name}
                    test_tuple = (product_data["product_name_fr"], store_name)
                    self.cursor.execute(sql_cmd_dict, test_tuple)


            self.connection.commit()
        
        self.connection.close()



if __name__ == "__main__":
    api_reader = api.ApiReader()
    interface = MySQLInterface()
    interface.create_tables(constants.tables_creation_cmds_list) # is ok
    interface.load_data(api_reader.get_data(), constants.table_filling_cmds_dict) # not ok, cf supra func body