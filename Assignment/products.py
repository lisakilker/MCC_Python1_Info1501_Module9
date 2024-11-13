#This is the getter/setter file class for storing/editing the products within the database

class Product:
    def __init__(self, id, name, price, quantity, quality):
        self.__id = id
        self.__name = name
        #Ensures the price is stored as a float
        self.__price = float(price)
        self.__quantity = quantity
        self.__quality = quality

    #Stringifies the return
    def __str__(self):
        return f"ID: {self.__id}, Name: {self.__name}, Price: {self.__price:.2f}, Quantity: {self.__quantity}, Quality: {self.__quality}"

    def to_dict(self):
        return {
            "ID": self.__id,
            "name": self.__name,
            "price": self.__price,
            "quantity": self.__quantity,
            "quality": self.__quality
        }
    
    #This is to ensure that the price displays as a float.  I was having trouble with this, so I added this just in case.
    @property
    def price(self):
        return f"{self.__price:.2f}"