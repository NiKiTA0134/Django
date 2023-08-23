# #Розробити систему керування бібліотекою.
# #Створіть клас бібліотеки та об'єкт цього класу.
# #Створіть класи для представлення книг, авторів, користувачів.
# #Додайте методи до бібліотеки для додавання нових книг, видачі книг користувачам та повернення книг у бібліотеку.
#
# class Book:
#     def __init__(self, title, author):
#         self.title = title
#         self.author = author
#         self.is_available = True
#
#     def borrow(self):
#         if self.is_available:
#             self.is_available = False
#             print(f"The book has been borrowed.")
#         else:
#             print(f"The book is currently unavailable.")
#
#     def return_book(self):
#         self.is_available = True
#         print(f"The book has been returned to the library.")
#
#
# class Author:
#     def __init__(self, name):
#         self.name = name
#
#
# class User:
#     def __init__(self, name):
#         self.name = name
#
#
# class Library:
#     def __init__(self):
#         self.books = []
#
#     def add_book(self, book):
#         self.books.append(book)
#         print('Book added')
#
#     def borrow_book(self, book_title):
#         for book in self.books:
#             if book.title == book_title:
#                 book.borrow()
#                 return
#         print("Book borrowed")
#
#     def return_book(self, book_title):
#         for book in self.books:
#             if book.title == book_title:
#                 book.return_book()
#                 return
#         print(f"The book does not return to this library")
#
#
# book = Book("Warriors", Author("Erin Hunter"))
#
# library = Library()
#
# library.add_book(book)
# library.borrow_book("Warriors")
# library.return_book("Warriors")
#
#
# class ShoppingCart:
#     def __init__(self):
#         self.product = []
#
#     def add_product(self, name):
#         self.product.append(name)
#
#     def calculate_price(self):
#         sum(c.product for c in self.price)
#
#
# class Product:
#     def __init__(self, price, name):
#         self.price = price
#         self.name = name
#         self.is_added = False
#
# apple = Product('Apple', 10)
# tomato = Product('Tomato', 15)
#
# cart = ShoppingCart()
#
# cart.add_product(apple)
# cart.add_product(tomato)
#
# print(cart.calculate_price())
#
# print(cart.product)

import unittest


def add(a,b):
    return a + b


class Test(unittest.TestCase):
    def test_check_add(self):
        result = add(10, 20)
        self.assertEqual(result, 30)