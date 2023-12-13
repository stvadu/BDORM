import psycopg2
import sqlalchemy
from sqlalchemy.orm import sessionmaker, declarative_base, relationship


with open('DSN.txt', 'r') as file_object:
    DSN = file_object.read().strip()

engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


def create_table(engine1):
    Base.metadata.create_all(engine1)


def drop_table(engine2):
    Base.metadata.drop_all(engine2)


class Publisher(Base):
    __tablename__ = 'publisher'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(length=100), unique=True)


create_table(engine)

publisher_1 = Publisher(name='Пушкин')
publisher_2 = Publisher(name='Лермонтов')
publisher_3 = Publisher(name='Замятин')
publisher_4 = Publisher(name='Усачёв')


class Book(Base):
    __tablename__ = 'book'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String(length=100), unique=True)
    id_publisher = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('publisher.id'), nullable=False)

    publisher = relationship(Publisher, backref='book')


create_table(engine)

book_1 = Book(title='Капитанская Дочка', id_publisher=1)
book_2 = Book(title='Мцыри', id_publisher=2)
book_3 = Book(title='Мы', id_publisher=3)
book_4 = Book(title='Собачка Соня', id_publisher=4)
book_5 = Book(title='Руслан и Людмила', id_publisher=1)
book_6 = Book(title='Евгений Онегин', id_publisher=1)


class Shop(Base):
    __tablename__ = 'shop'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(length=100), unique=True)


create_table(engine)

shop_1 = Shop(name='Буквоед')
shop_2 = Shop(name='Лабиринт')
shop_3 = Shop(name='Книжный Дом')


class Stock(Base):
    __tablename__ = 'stock'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    id_book = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('book.id'), nullable=False)
    id_shop = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('shop.id'), nullable=False)
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    book = relationship(Book, backref='book')
    shop = relationship(Shop, backref='book')


create_table(engine)

stock_1 = Stock(id_book=1, id_shop=1, count=18)
stock_2 = Stock(id_book=2, id_shop=1, count=20)
stock_3 = Stock(id_book=2, id_shop=2, count=14)
stock_4 = Stock(id_book=3, id_shop=3, count=17)
stock_5 = Stock(id_book=4, id_shop=1, count=14)
stock_6 = Stock(id_book=6, id_shop=2, count=18)
stock_7 = Stock(id_book=3, id_shop=3, count=26)
stock_8 = Stock(id_book=1, id_shop=3, count=15)


class Sale(Base):
    __tablename__ = 'sale'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    price = sqlalchemy.Column(sqlalchemy.Numeric(5, 2))
    date_sale = sqlalchemy.Column(sqlalchemy.Date, nullable=False)
    id_stock = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('stock.id'), nullable=False)
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    stock = relationship(Stock, backref='stock')


create_table(engine)

sale_1 = Sale(price=505, date_sale='01-11-2023', id_stock=1, count=5)
sale_2 = Sale(price=510, date_sale='02-11-2023', id_stock=2, count=2)
sale_3 = Sale(price=500, date_sale='03-11-2023', id_stock=3, count=6)
sale_4 = Sale(price=515, date_sale='04-11-2023', id_stock=4, count=3)
sale_5 = Sale(price=525, date_sale='08-11-2023', id_stock=5, count=4)
sale_6 = Sale(price=530, date_sale='09-11-2023', id_stock=6, count=3)
sale_7 = Sale(price=545, date_sale='15-11-2023', id_stock=7, count=6)
sale_8 = Sale(price=540, date_sale='16-11-2023', id_stock=8, count=3)
sale_9 = Sale(price=500, date_sale='18-11-2023', id_stock=3, count=4)
sale_10 = Sale(price=500, date_sale='19-11-2023', id_stock=3, count=1)

session.add_all([publisher_1, publisher_2, publisher_3, publisher_4])
session.add_all([book_1, book_2, book_3, book_4, book_5, book_6])
session.add_all([shop_1, shop_2, shop_3])
session.add_all([stock_1, stock_2, stock_3, stock_4, stock_5, stock_6, stock_7, stock_8])
session.add_all([sale_1, sale_2, sale_3, sale_4, sale_5, sale_6, sale_7, sale_8, sale_9, sale_10])

writer = input('Введите writer_id или writer_name: ')
query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher).join(Stock).join(Shop).join(
    Sale)

if writer.isnumeric():
    query = query.filter(Publisher.id == writer).all()
else:
    query = query.filter(Publisher.name == writer).all()

for title, name, price, date_sale in query:
    print(f'{title:<20} | {name:<10} | {price:<10} | {date_sale}')

session.close()
