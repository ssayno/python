#!/usr/bin/env python3
from abc import ABC, abstractmethod
from collections import namedtuple


Customer = namedtuple('Customer', ['name', 'fidelity'])


class LineItem:

    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity


class Order:

    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion

    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum([item.total() for item in self.cart])
        return self.__total

    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion.discount(self)
        return self.total() - discount

    def __repr__(self):
        return f"<Order total: {self.total()} due: {self.due()}>"


class Promotion(ABC):

    @abstractmethod
    def discount(self):
        pass


class FidelityPromo(Promotion):

    def discount(self, order):
        return order.total() * 0.05 if order.customer.fidelity >= 1000 else 0


class BulkItemPromotion(Promotion):

    def discount(self, order):
        discount = 0
        for item in order.cart:
            if item.quantity > 20:
                discount += item.total() * 0.1
        return discount


class LargeOrderPromotion(Promotion):

    def discount(self, order):
        distinct_item = [item.product for item in order.cart]
        if len(distinct_item) >= 10:
            return order.total() * 0.07
        return 0


if __name__ == '__main__':
    A = Customer('joe', 88)
    B = Customer('John', 1000)
    cart = [LineItem('banana', 4, 0.5),
            LineItem('apple', 10, 1.5),
            LineItem('watermellon', 5, 5)]
    print(Order(A, cart, FidelityPromo()))
    print(Order(B, cart, FidelityPromo()))
