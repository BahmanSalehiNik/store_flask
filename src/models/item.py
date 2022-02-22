from query_decorator import query_method_decorator


class ItemModel:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price':self.price}

    @classmethod
    @query_method_decorator
    def find_item_by_name(cls, name, cursor=None):
        update_item_by_name_query = "SELECT * FROM items WHERE name=?"
        items_qs = cursor.execute(update_item_by_name_query, (name,))
        row = items_qs.fetchone()
        if not row:
            return None
        else:
            return cls(name=row[1], price=row[2])

    @query_method_decorator
    def insert(self, cursor=None):

        create_item_query = "INSERT INTO items VALUES (NULL , ?, ?)"
        cursor.execute(create_item_query, (self.name, self.price))

    @query_method_decorator
    def update(self, price, cursor=None):
        self.price = price
        update_query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(update_query, (price, self.name))
