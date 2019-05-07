"""
Для попереднього домашнього завдання.
Для класу Колекціонер Машина і Гараж написати методи, які створюють інстанс обєкту
з (yaml, json, pickle) файлу відповідно
Для класів Колекціонер Машина і Гараж написати методи, які зберігають стан обєкту в файли формату
yaml, json, pickle відповідно.
Для класів Колекціонер Машина і Гараж написати методи, які конвертують обєкт в строку формату
yaml, json, pickle відповідно.
Для класу Колекціонер Машина і Гараж написати методи, які створюють інстанс обєкту
з (yaml, json, pickle) строки відповідно
Advanced
Добавити опрацьовку формату ini

"""

from __future__ import annotations
import uuid
import functools
import random
import json
from constants import TOWNS, CARS_TYPES, CARS_PRODUCER


# _le_ and other comparison operators are defined by
# @functools.total_ordering using provided _lt_ and _eq_
@functools.total_ordering
class Car:
    def __init__(self, price: float, car_type: CARS_TYPES, producer: CARS_PRODUCER, mileage: float, number=None):
        self.price = price
        self.number = number if number else uuid.uuid4()
        self.mileage = mileage
        if producer in CARS_PRODUCER:
            self.producer = producer
        else:
            raise Exception("Bad Producer value, producer value must be: ", CARS_PRODUCER)
        if car_type in CARS_TYPES:
            self.car_type = car_type
        else:
            raise Exception("Bad car type, car type must be: ", CARS_TYPES)

    def __str__(self):
        return f"Car. Car_type: {self.car_type}; Producer: {self.producer}; Price: {self.price}; " \
            f"Number: {self.number}; Mileage: {self.mileage}"

    @staticmethod
    def to_json(obj: Car):
        data = {"car_type": obj.car_type, "producer": obj.producer, "price": obj.price, "number": str(obj.number),
                "mileage": obj.mileage}
        return data

    @classmethod
    def from_json(cls, data):
        car_type = data['car_type']
        producer = data['producer']
        price = data['price']
        number = data['number']
        mileage = data['mileage']
        cr = Car(car_type=car_type, producer=producer, price=price, number=number, mileage=mileage)
        return cr

    @staticmethod
    def json_to_file(self):
        with open("car.json", 'w') as file:
            json.dump(self.to_json(self), file, indent=4)

    def __repr__(self):
        return f"Car(car_type='{self.car_type}', producer='{self.producer}', price='{self.price}'," \
            f" number='{self.number}', mileage='{self.mileage}')"

    def change_number(self):
        self.number = uuid.uuid4()

    def __lt__(self, other: Car):
        return self.price < other.price

    def __eq__(self, other: Car):
        return self.price == other.price


class Garage:
    def __init__(self, town: TOWNS, cars: [], places: int, owner=None):
        self.cars = cars if cars else []
        self.places = places
        self.owner = owner if owner else None
        if town in TOWNS:
            self.town = town
        else:
            raise Exception("Bad Town name, available town: ", TOWNS)

    def __str__(self):
        return f"Garage(town='{self.town}', places='{self.places}', owner='{self.owner}', cars='{self.cars}')"

    def __repr__(self):
        return f"Garage(town='{self.town}', places='{self.places}', owner='{self.owner}', cars='{self.cars}')"

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


# _le_ and other comparison operators are defined by
# @functools.total_ordering using provided _lt_ and _eq_
@functools.total_ordering
class Cesar:
    def __init__(self, name: str, garages=None):
        self.name = name
        self.garages = garages if garages else []
        self.register_id = uuid.uuid4()

    def __str__(self):
        return f"Cesar(name='{self.name}', registerID='{self.register_id}' garages='{self.garages}')"

    def __repr__(self):
        return f"Cesar(name='{self.name}', registerID='{self.register_id}' garages='{self.garages}')"

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

    def __lt__(self, other: Cesar):
        return self.hit_hat() < other.hit_hat()


if __name__ == "__main__":

    car = Car(
        car_type=random.choice(CARS_TYPES),
        producer=random.choice(CARS_PRODUCER),
        price=round(random.uniform(1, 100000), 2),
        mileage=round(random.uniform(1, 100000), 2)
    )

    print(car)
    ser_pr = ''
    # Should raise TypeError. Json does not know how to work with custom objects
    try:
        ser_pr = json.dumps(car)
        print(ser_pr)
    except TypeError as e:
        print(e)

    # Should work fine. Use custom json decoder
    try:
        ser_pr = json.dumps(car, default=Car.to_json)
        print(type(ser_pr), ser_pr)
    except TypeError as e:
        print(e)

    # Should not fault. But we will get dict instead of object
    try:
        load_pr = json.loads(ser_pr)
        print(type(load_pr), load_pr)
    except TypeError as e:
        print(e)

    # Should works fine. Use custom hook
    try:
        load_pr = json.loads(ser_pr, object_hook=Car.from_json)
        print(type(load_pr), load_pr)
    except TypeError as e:
        print(e)

    car.json_to_file(car)