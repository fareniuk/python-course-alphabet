"""
Вам небхідно написати 3 класи. Колекціонери Гаражі та Автомобілі.
Звязкок наступний один колекціонер може мати багато гаражів.
В одному гаражі може знаходитися багато автомобілів.

"""
from __future__ import annotations
import uuid
from constants import TOWNS
from constants import CARS_TYPES
from constants import CARS_PRODUCER

print(TOWNS)


class Car:
    """
    Автомобіль має наступні характеристики:
    price - значення типу float. Всі ціни за дефолтом в одній валюті.
    type - одне з перечисленних значеннь з CARS_TYPES в docs.
    producer - одне з перечисленних значеннь в CARS_PRODUCER.
    number - значення типу UUID. Присвоюється автоматично при створенні автомобілю.
    mileage - значення типу float. Пробіг автомобіля в кілометрах.


    Автомобілі можна перівнювати між собою за ціною.
    При виводі(logs, print) автомобілю повинні зазначатися всі його атрибути.

    Автомобіль має метод заміни номеру.
    номер повинен відповідати UUID
    """
    def __init__(self, price: float, car_type: CARS_TYPES, producer: CARS_PRODUCER, mileage: float):
        self.price = price
        self.number = uuid.uuid4()
        self.mileage = mileage
        if producer in CARS_PRODUCER:
            self.producer = producer
        else:
            raise Exception("Bad Producer value")
        if car_type in CARS_TYPES:
            self.car_type = car_type
        else:
            raise Exception("Bad car type")
    pass

    def __str__(self):
        return f"Car(car_type='{self.car_type}', producer='{self.producer}', price='{self.price}'," \
            f" number='{self.number}', mileage='{self.mileage}')"

    def __repr__(self):
        return self.__str__()

    def change_number(self):
        self.number = uuid.uuid4()

    def __le__(self, other: Car):
        return self.price <= other.price

    def __lt__(self, other: Car):
        return self.price < other.price

    def __eq__(self, other: Car):
        return self.price == other.price

    def __ne__(self, other: Car):
        return self.price != other.price

    def __ge__(self, other: Car):
        return self.price >= other.price

    def __gt__(self, other: Car):
        return self.price > other.price


class Garage:
    """
    Гараж має наступні характеристики:

    town - одне з перечислениз значеннь в TOWNS
    cars - список з усіх автомобілів які знаходяться в гаражі
    places - значення типу int. Максимально допустима кількість автомобілів в гаражі
    owner - значення типу UUID. За дефолтом None.

    Повинен мати реалізованими наступні методи

    add(car) -> Добавляє машину в гараж, якщо є вільні місця
    remove(cat) -> Забирає машину з гаражу.
    hit_hat() -> Вертає сумарну вартість всіх машин в гаражі
    """
    def __init__(self, town: TOWNS, cars: [], places: int, owner=None):
        self.cars = cars
        self.places = places
        self.owner = owner if owner else None
        if town in TOWNS:
            self.town = town
        else:
            raise Exception("Bad Town")

    def __str__(self):
        return f"Garage(town='{self.town}', places='{self.places}', owner='{self.owner}', cars='{self.cars}')"

    def __repr__(self):
        return self.__str__()

    def add(self, car):
        if len(self.cars) < self.places:
            self.cars.append(car)
        else:
            raise Exception('No place available in ', self)

    def remove(self, car):
        if car in self.cars:
            self.cars.remove(car)
            print(f"Car: '{car}' removed from garage")
        else:
            raise Exception(f"There is no '{car}' in this garage")

    def hit_hat(self):
        return sum(car.price for car in self.cars)


class Cesar:
    """
    name - значення типу str. Його ім'я
    garages - список з усіх гаражів які належать цьому Колекціонеру. Кількість гаражів за замовчуванням - 0
    register_id - UUID; Унікальна айдішка Колекціонера.

    Повинні бути реалізовані наступні методи:
    hit_hat() - повертає ціну всіх його автомобілів.
    garages_count() - вертає кількість гаріжів.
    сars_count() - вертає кількість машиню
    add_car() - додає машину у вибраний гараж. Якщо гараж не вказаний, то додає в гараж, де найбільше вільних місць.
    Якщо вільних місць немає повинне вивести повідомлення про це.

    Колекціонерів можна порівнювати за ціною всіх їх автомобілів.
    """
    def __init__(self, name: str, garages=[]):
        self.name = name
        self.garages = garages
        self.register_id = uuid.uuid4()

    def __str__(self):
        return f"Cesar(name='{self.name}', registerID='{self.register_id}' garages='{self.garages}')"

    def __repr__(self):
        return self.__str__()

    def hit_hat(self):
        return sum(garage.hit_hat() for garage in self.garages)

    def garage_count(self):
        return len(self.garages)

    def cars_count(self):
        return sum(len(garage.cars) for garage in self.garages)

    def place_available(self):
        for i in self.garages:
            if (i.places - len(i.cars)) > 0:
                return True
        return False

    def add_car(self, car: Car, garage=None):
        if garage is None:
            max(self.garages, key=lambda x: (x.places - len(x.cars))).add(car) if self.place_available() else print('if self.place_available():')
        elif garage in self.garages:
            garage.add(car) if car not in garage.cars else print("The car is already in the garage")
        elif garage not in self.garages:
            print("You can not add a car to someone else's garage")

    def __eq__(self, other: Cesar):
        return self.hit_hat() == other.hit_hat()

    def __le__(self, other: Cesar):
        return self.hit_hat() <= other.hit_hat()

    def __lt__(self, other: Cesar):
        return self.hit_hat() < other.hit_hat()

    def __ne__(self, other: Cesar):
        return self.hit_hat() != other.hit_hat()

    def __ge__(self, other: Cesar):
        return self.hit_hat() >= other.hit_hat()

    def __gt__(self, other: Cesar):
        return self.hit_hat() > other.hit_hat()
