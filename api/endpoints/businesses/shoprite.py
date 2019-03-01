from sqlalchemy import Table, MetaData
from sqlalchemy.sql import select, or_
from utility import shopriteDbEng, resultSetToJson, setPagination

# Function for GET /products/
def shopRiteGetProducts(data):

    # Setup database connection, table, and query
    con = shopriteDbEng.connect()
    products = Table('products', MetaData(shopriteDbEng), autoload=True)
    stm = select([products])

    # Handle optional filters
    if data.get('name'):
        stm = stm.where(products.c.name.like('%' + data['name'] + '%'))
    if data.get('item_code'):
        stm = stm.where(products.c.item_code == data['item_code'])
    if data.get('plu'):
        stm = stm.where(products.c.plu == data['plu'])
    if data.get('barcode'):
        stm = stm.where(products.c.barcode == data['barcode'])
    
     # Handle search_term
    if data.get('search_term'):
        search_term = '%' + data['search_term'] + '%'
        stm = stm.where(or_(
            products.c.name.like(search_term),
            products.c.item_code.like(search_term),
            products.c.plu.like(search_term)
        ))
    
    # Handle page_size and page
    stm = setPagination(stm, data)

    return {
        'items': resultSetToJson(con.execute(stm).fetchall(), ['password_hash'])
    }