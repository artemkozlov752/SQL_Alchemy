import random

from sqlalchemy import BigInteger, Column, Integer, Unicode
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Order(Base):
    __tablename__ = 'orders'

    id = Column(BigInteger, nullable=False, primary_key=True, autoincrement=True)
    name = Column(Unicode(64), nullable=False)
    state = Column(Integer, nullable=False, index=True)  # accepted = 1, hold = 0

    def __init__(self, id, name, state):
        self.id = id
        self.name = name
        self.state = state


def mark_random_orders_accepted(orders: list, session):
    """Choose random orders from orders-list and change its state to 1.

    Args:
        orders (list).
        session (sqlalchemy session).

    """
    random_orders = random.sample(orders, random.randint(0, len(orders)))
    for random_order in random_orders:
        query = f"UPDATE orders SET orders.state=1 WHERE orders.id={random_order.id};"
        session.execute(query)
        session.commit()


def get_data_by_chunks(batch_size: int, session):
    """Get data from sql by batches.

    Args:
        batch_size (int).
        session (sqlalchemy session).

    """
    orders = [0]
    initial_index = 0
    while orders:
        orders = list(session.query(Order).slice(initial_index, initial_index + batch_size))
        mark_random_orders_accepted(orders, session)
        initial_index += batch_size


def fill_test_data(data_length: int, session):
    """Filling base with test data.

    Args:
        data_length (int).
        session (sqlalchemy session).

    """
    objects = [Order(id=id, name=f"A{id}", state=0) for id in range(1, data_length + 1)]
    session.add_all(objects)
    session.commit()
