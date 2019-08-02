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
		url VARCHAR(140) NOT NULL,
        description VARCHAR(200),
		category_id SMALLINT UNSIGNED NOT NULL,
		
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

table_filling_cmds_dict = {

        "category_filler": """INSERT IGNORE INTO category(name) 
            VALUES(%(category)s);""",
   
        "product_filler": """INSERT INTO product(name, url, nutriscore, 
                category_id) 
            VALUES (%(product_name_fr)s,  %(url)s,  %(nutrition_grade_fr)s, 
            (SELECT id FROM category 
            WHERE category.name = %(category)s));""",
    
        "store_name_filler" : """INSERT IGNORE INTO store(name) VALUES (%s);}""",

        "store_product_association_builder": """INSERT INTO product_store_association(product_id, store_id)
        VALUES (SELECT id FROM product WHERE product.name = %s, SELECT id FROM store 
        WHERE store.name = %s;"""
        }

