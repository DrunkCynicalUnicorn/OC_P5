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
		url VARCHAR(200) NOT NULL,
        description VARCHAR(200) NOT NULL,
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



cat_filler = """INSERT IGNORE INTO category(name) VALUES(%s);"""
   
prod_filler = """INSERT INTO product(category_id, name, description, url, nutriscore) 
        VALUES ((SELECT id FROM category WHERE category.name = %s), %s,  %s,  %s, %s );"""
    
store_filler = """INSERT IGNORE INTO store(name) VALUES (%s);"""

store_prod_association_builder = """INSERT INTO product_store_association(product_id)
        VALUES ((SELECT id FROM product WHERE product.name = %s));"""


sql_cmd2 = """INSERT INTO product_store_association(store_id) VALUES (SELECT id FROM store WHERE store.name = %s);"""



# alternate prod_filler func using dict syntax to fill variable fields
#"""INSERT INTO product(name, description, url, nutriscore, category_id)
#        VALUES (%('product_name_fr')s,  %('description')s,  %('url')s, %('nutrition_grade_fr')s,
#        (SELECT id FROM category WHERE category.name = %s));"""