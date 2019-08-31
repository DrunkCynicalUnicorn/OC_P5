# -*- coding: utf-8 -*-


                                    ### API's CONSTANTS ###

url = "https://fr-en.openfoodfacts.org/cgi/search.pl"
    
categories = {
    "Barres_chocolatées" : "chocolate-bars",
    "Pâtes_à_tartiner_aux noisettes_et_au_cacao" : 
        "cocoa-and-hazelnuts-spreads",
    "Sodas_au_cola" : "colas",
    "Pizzas_surgelées" : "frozen-pizzas",
    "Barres_énergétiques" : "energy-bars",
    "Biscuits_au_chocolat" : "chocolate-biscuits",
    "Biscuits_fourrés" : "filled-biscuits",
    "Plats_au_boeuf" : "beef-dishes",
    "Plats_préparés_en_conserve" : "canned-meals",
    "Lasagnes_préparées" : "prepared-lasagne"
    }

product_nb_per_category = 70

                                    ### MySQL 's CONSTANTS ###

check_db_state = """SELECT name FROM product;"""

        ## Table creation commands :
        
tables_creation_cmds_list = [
    """ CREATE TABLE IF NOT EXISTS category
	(
		id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
		name VARCHAR(100) NOT NULL UNIQUE,
		
		PRIMARY KEY (id)
        
	)
	ENGINE = INNODB; """,


    """ CREATE TABLE IF NOT EXISTS product
	(
		id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,   
		name VARCHAR(100) NOT NULL,
		nutriscore CHAR(1) NOT NULL,
		url VARCHAR(200) NOT NULL,
        description VARCHAR(200) NOT NULL,
		category_id SMALLINT UNSIGNED NOT NULL,
		substitute BOOLEAN NOT NULL DEFAULT 0,
		origin_search SMALLINT UNSIGNED NULL DEFAULT NULL,
		
		PRIMARY KEY (id),
		FOREIGN KEY (category_id) REFERENCES category(id)
	)
	ENGINE = INNODB; """,


    """ CREATE TABLE IF NOT EXISTS store
	(
		id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
		name VARCHAR(60) NOT NULL UNIQUE,
		
		PRIMARY KEY (id)
        
	)
	ENGINE = INNODB; """,


    """ CREATE TABLE IF NOT EXISTS product_store_association 
	(
		product_id SMALLINT UNSIGNED NOT NULL,
		store_id SMALLINT UNSIGNED NOT NULL,

		PRIMARY KEY (product_id, store_id),
		FOREIGN KEY (product_id) REFERENCES product(id),
		FOREIGN KEY (store_id) REFERENCES store(id)
	) 
	ENGINE = INNODB; """]


        ## Table filling commands :

mysql_insert_cmds = {
        "cat_filler": """INSERT IGNORE INTO category(name) VALUES(%s);""",
        
        "prod_filler": """INSERT INTO product(category_id, name, description, 
            url, nutriscore) 
            VALUES ((SELECT id FROM category WHERE category.name = %s), 
            %s,  %s,  %s, %s );""",
                    
        "store_filler": """INSERT IGNORE INTO store(name) VALUES (%s);""",
        
        "store_prod_assoc_builder": """INSERT INTO 
            product_store_association (product_id, store_id) 
            VALUES (%s, (SELECT id FROM store WHERE store.name = %s));"""
        }


        ## SQL queries :

mysql_select_cmds = {
    "select_categories": """SELECT id, name FROM category ORDER BY id ASC;""",
    "select_prods_per_category": """SELECT product.id, product.name FROM 
        product INNER JOIN category ON product.category_id = category.id 
        WHERE category.id = %s ORDER BY product.id ASC ;""",
    "find_substitute": """ SELECT id, name, description, url FROM product
        WHERE nutriscore <= (SELECT nutriscore FROM product WHERE id = %s) 
        AND category_id = (SELECT category_id FROM product WHERE id = %s) 
        ORDER BY nutriscore ASC LIMIT 1;""",
    "select_stores_substitute": """SELECT name FROM store INNER JOIN 
        product_store_association 
        ON store.id = product_store_association.store_id 
        WHERE product_store_association.product_id = %s;"""
    }

set_favorite_cmd = """UPDATE product SET substitute=True, origin_search = %s
    WHERE id = %s;"""

get_favorites_cmd = """SELECT name, description, url, origin_search 
    FROM product WHERE substitute = True;"""
