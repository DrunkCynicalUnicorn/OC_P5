import pymysql

connection = pymysql.connect(host='localhost',
                             user='consumer',
                             password='password',
                             database='p5_db',
                             charset='utf8')



category_table_code = """ CREATE TABLE IF NOT EXISTS category
	(
		id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
		name VARCHAR(40) NOT NULL,
		
		PRIMARY KEY (id)
	)
	ENGINE = INNODB; """




product_table_code = """ CREATE TABLE IF NOT EXISTS product
	(
		id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,   
		name VARCHAR(40) NOT NULL,
		nutriscore CHAR(1) NOT NULL,
		url VARCHAR(70) NOT NULL,
		category_id SMALLINT UNSIGNED NOT NULL,
		
		PRIMARY KEY (id),
		FOREIGN KEY (category_id) REFERENCES category(id)
	)
	ENGINE = INNODB; """



store_table_code = """ CREATE TABLE IF NOT EXISTS store
	(
		id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
		name VARCHAR(40) NOT NULL,
		
		PRIMARY KEY (id)
	)
	ENGINE = INNODB; """


association_table_code = """ CREATE TABLE IF NOT EXISTS product_store_association 
	(
		product_id SMALLINT UNSIGNED NOT NULL,
		store_id SMALLINT UNSIGNED NOT NULL,

		PRIMARY KEY (product_id, store_id),
		FOREIGN KEY (product_id) REFERENCES product(id),
		FOREIGN KEY (store_id) REFERENCES store(id)
	) 
	ENGINE = INNODB; """


tables_creation_cmds = [category_table_code, product_table_code,
                       store_table_code, association_table_code]



def create_tables(sql_cmd_list):
    try:
        with connection.cursor() as cursor:
            for sql_cmd in sql_cmd_list:
                cursor.execute(sql_cmd)
        connection.commit()
    finally:
        connection.close()





# TO DO before going on :
# !!! find a reference field for description column !!!
# !!! need to look in detail how to fill fk fields !!!
        # first idea : 
            # => compare data['category'] and category.name : if it matches,
            # set product.category_id to category.id 
"""
def load_data(data):
    try:
        with connection.cursor() as cursor:
            for category in data:
                for product in category:
                    cursor.execute(
                    INSERT INTO 'category'('name') VALUES(product['category']),
                    
                    INSERT INTO 'product'('name', 'url', 'nutriscore', 
                    'description') VALUES (product['product_name_fr'], product['url'],
                    product['nutrition_grade_fr'], product['description']),
                    
                    INSERT INTO 'store'('name') VALUES ('product'['stores'])
                    )

"""


if __name__ == "__main__":
	create_tables(tables_creation_cmds) # is ok