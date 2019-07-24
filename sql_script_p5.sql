CREATE DATABASE IF NOT EXISTS p5 CHARACTER SET 'utf8';

USE p5;

CREATE TABLE IF NOT EXISTS category
	(
		id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
		name VARCHAR(40) NOT NULL,
		
		PRIMARY KEY (id)
	)
	ENGINE = INNODB;


CREATE TABLE IF NOT EXISTS product
	(
		id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,   
		name VARCHAR(40) NOT NULL,
		nutriscore CHAR(1) NOT NULL,
		url VARCHAR(50) NOT NULL
		category_id SMALLINT UNSIGNED NOT NULL,
		# !!! add a column for product description !!!
		
		PRIMARY KEY (id),
		ADD CONSTRAINT fk_category_id
			FOREIGN KEY (category_id)
			REFERENCES category(id)
	)
	ENGINE = INNODB;


CREATE TABLE IF NOT EXISTS store
	(
		id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
		name VARCHAR(40) NOT NULL,
		
		PRIMARY KEY (id)
	)
	ENGINE = INNODB;



CREATE TABLE IF NOT EXISTS product_store_association
	(
		product_id SMALLINT UNSIGNED NOT NULL,
		store_id SMALLINT UNSIGNED NOT NULL

		PRIMARY KEY (product_id, store_id),
		ADD CONSTRAINT fk_product_id
			FOREIGN KEY (product_id)
			REFERENCES product(id),
		ADD CONSTRAINT fk_store_id
			FOREIGN KEY (store_id);
			REFERENCES store(id)
	)
	ENGINE = INNODB;
