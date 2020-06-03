SET client_encoding = 'UTF-8';

CREATE EXTENSION pgcrypto;

DROP TABLE IF EXISTS Swap;
DROP TABLE IF EXISTS AppUser;
DROP TABLE IF EXISTS Aliment;
DROP TABLE IF EXISTS Category;

CREATE TABLE Category(
    id SERIAL PRIMARY KEY,
    category_name varchar(100) NOT NULL UNIQUE,
    category_url text NOT NULL
);

CREATE TABLE Aliment (
    id SERIAL PRIMARY KEY,
    product_name varchar(100) NOT NULL UNIQUE,
    product_description text,
    barcode varchar(20) NOT NULL,
    nutritional_score char(1) NOT NULL,
    stores varchar(200),
    product_category varchar(100) NOT NULL,
    picture text NOT NULL,
    CONSTRAINT fk_product_category FOREIGN KEY (product_category) REFERENCES Category(category_name)
);

CREATE TABLE AppUser(
    id SERIAL PRIMARY KEY,
    user_name varchar(100) NOT NULL UNIQUE,
    user_mail text NOT NULL UNIQUE,
    user_password text NOT NULL
);

CREATE TABLE Swap(
    id SERIAL PRIMARY KEY,
    user_id integer NOT NULL,
    aliment_id integer NOT NULL,
    substitute_id integer NOT NULL,
    CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES AppUser(id),
    CONSTRAINT fk_aliment_id FOREIGN KEY (aliment_id) REFERENCES Aliment(id),
    CONSTRAINT fk_substitute_id FOREIGN KEY (substitute_id) REFERENCES Aliment(id)
);

INSERT INTO Category(category_name, category_url) VALUES
('Compotes', 'https://fr.openfoodfacts.org/categorie/compotes'),
('Bonbons de chocolat', 'https://fr.openfoodfacts.org/categorie/bonbons-de-chocolat'),
('Sodas', 'https://fr.openfoodfacts.org/categorie/sodas'),
('Barres', 'https://fr.openfoodfacts.org/categorie/barres'),
('Yaourts aux fruits', 'https://fr.openfoodfacts.org/categorie/yaourts-aux-fruits'),
('Produits de la mer', 'https://fr.openfoodfacts.org/categorie/produits-de-la-mer'),
('Produits a la viande', 'https://fr.openfoodfacts.org/categorie/produits-a-la-viande'),
('Produits deshydrates', 'https://fr.openfoodfacts.org/categorie/produits-deshydrates'),
('Jambons', 'https://fr.openfoodfacts.org/categorie/jambons'),
('Cereales pour petit-dejeuner', 'https://fr.openfoodfacts.org/categorie/cereales-pour-petit-dejeuner');

INSERT INTO AppUser(user_name, user_mail, user_password) VALUES
('Kirby-54', 'charlesrouge@gmail.com', crypt('12345', gen_salt('bf', 8))),
('GT Gaby', 'ledon@brocantegame.com', crypt('g4m3g34rF0R3V4R', gen_salt('bf', 8))),
('Mr Quarate', 'philippe@gwak.fr', crypt('shalomsalamsalut', gen_salt('bf', 8))),
('Zoulman', 'zoulman@caramail.fr', crypt('chouette', gen_salt('bf', 8))),
('Payou', 'papayou@lele.fr', crypt('bonjour123', gen_salt('bf', 8)));