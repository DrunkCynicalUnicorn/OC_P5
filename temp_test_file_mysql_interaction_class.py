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



"""
def load_data(data):
    try:
        with connection.cursor() as cursor:
            for category_data in data:
                for product_data in category_data:
                    cursor.execute(
                    
                    INSERT INTO category(name) 
                    VALUES(product_data['category']),
                    
                    INSERT INTO product(name, url, nutriscore, 
                    description) VALUES (product_data['product_name_fr'], 
                    product_data['url'], product_data['nutrition_grade_fr'], 
                    product_data['description']),             
                    
                    INSERT INTO product(category_id) VALUES ((SELECT id FROM
                    category WHERE category.name = product_data['category']))
                    
                    
                    stores_list = product_data['stores'].split(',')
                    for store_data in stores_list:
                        store_data = store_data.strip()
                        cursor.execute(
                        INSERT INTO store(name) VALUES (product_data['stores'])
                        
                        INSERT INTO 
                        product_store_association(product_id, store_id)
                        VALUES (
                        (SELECT id FROM product WHERE store.name = product_data['store']),
                        (SELECT id FROM store WHERE store.name = product_data['store'])
                        )

"""


if __name__ == "__main__":
	create_tables(tables_creation_cmds) # is ok