from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    reviews = db.relationship('Review', back_populates='customer')

    # Association proxy to get the items the customer has reviewed
    items = association_proxy('reviews', 'item')

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'

    def to_dict(self):
        # Serialize basic customer data
        result = {
            'id': self.id,
            'name': self.name,
            'reviews': [{'id': review.id, 'comment': review.comment} for review in self.reviews]
        }
        return result


class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    reviews = db.relationship('Review', back_populates='item')

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

    def to_dict(self):
        # Serialize basic item data
        result = {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'reviews': [{'id': review.id, 'comment': review.comment} for review in self.reviews]
        }
        return result


class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')

    def __repr__(self):
        return f'<Review {self.id}, {self.comment}>'

    def to_dict(self):
        # Avoid serializing nested relationships that cause recursion
        result = {
            'id': self.id,
            'comment': self.comment,
            'customer': {'id': self.customer.id, 'name': self.customer.name} if self.customer else None,
            'item': {'id': self.item.id, 'name': self.item.name, 'price': self.item.price} if self.item else None,
        }
        return result
