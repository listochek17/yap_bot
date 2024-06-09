import sqlite3
import json

# with open('category.json', mode='r', encoding='utf-8') as f:
#     content_categories = json.load(f)
#
# with open('products.json', mode='r', encoding='utf-8') as f:
#     content_product = json.load(f)


connection = sqlite3.connect('yap2.db', check_same_thread=False)
cursor = connection.cursor()


def create_table1():
    cursor.executescript("""
        DROP TABLE IF EXISTS category;
        CREATE TABLE IF NOT EXISTS category(
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            cat_title1 TEXT
        );
     """)
    connection.commit()


def create_table2():
    cursor.executescript("""
    DROP TABLE IF EXISTS product;
    CREATE TABLE IF NOT EXISTS product(
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        coast INTEGER,
        cat_id INTEGER REFERENCES category(cat_id) 
    );
    """)
    connection.commit()


# create_table1()
# create_table2()


def cat_get_base(obj):
    for i in obj:
        cursor.execute('''
        INSERT INTO category(cat_title1) VALUES (?)
        ''', (i['name'], ))
        connection.commit()


# cat_get_base(content_categories)


def prod_get_base(obj):
    for i in obj:
        cursor.execute('''
        INSERT INTO product(title, coast, cat_id) VALUES (?, ?, ?)
        ''', (i['title'], i['coast'], i['cat_id'] ))
        connection.commit()


# prod_get_base(content_product)


def categories_list():
    sql1 = 'SELECT cat_title1 FROM category'
    cursor.execute(sql1)
    return [item[0] for item in cursor.fetchall()]


def show_cat_id(cat_name):
    sql1 = 'SELECT category_id FROM category WHERE cat_title1 = ?'
    cursor.execute(sql1, (cat_name, ))
    return cursor.fetchone()[0]


def prod_list(cat_id):
    sql1 = 'SELECT title FROM product WHERE cat_id = ?'
    cursor.execute(sql1, (cat_id, ))
    return [item[0] for item in cursor.fetchall()]


def show_detail(name_product):
    sql1 = 'SELECT coast FROM product WHERE title = ?'
    cursor.execute(sql1, (name_product, ))
    return cursor.fetchone()[0]

