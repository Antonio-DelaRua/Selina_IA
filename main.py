
import os
from openrouter_exception_handler.exception_handler import exception_handler, class_exception_handler
from gui import setup_gui

# help(exception_handler)


# @class_exception_handler
# class MyClass:
#     def instance_method(self, x):
#         return 10 / x  # Si x es 0, provocará ZeroDivisionError

#     @staticmethod
#     def static_method(x):
#         return 10 / x  # Igualmente provoca ZeroDivisionError si x es 0

#     @classmethod
#     def class_method(cls, x):
#         return 10 / x  # Este método ahora también provoca ZeroDivisionError si x es 0


# obj = MyClass()
# obj.instance_method(0)   # Exception will be caught and sent to OpenRouter
# MyClass.static_method(0) # Same behavior
# MyClass.class_method(0)  # Same behavior

@exception_handler
def main():
   # print("Hello", os.environ.get('APIKEY_OPENROUTER'))
   # a = []
   # print(a[1])
   setup_gui()
if __name__ == "__main__":
    main()
