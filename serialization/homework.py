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
import pickle
import codecs
from ruamel.yaml import YAML
from serialization.constants import TOWNS, CARS_TYPES, CARS_PRODUCER


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

    def json_to_string(self):
        try:
            return json.dumps(self, default=Car.to_json)
        except TypeError as e:
            print(e)

    @staticmethod
    def сar_from_json_string(json_string: str):
        try:
            return json.loads(json_string, object_hook=Car.from_json)

        except TypeError as e:
            print(e)

    def json_to_file(self, file_name: str):
        with open(file_name, 'w') as file:
            json.dump(self.to_json(self), file, indent=4)

    @staticmethod
    def instance_from_json_file(file_name: str):
        with open(file_name, 'r') as file:
            return json.load(file, object_hook=Car.from_json)

    def __setstate__(self, state):
        self.__dict__ = state

    def __getstate__(self):
        return self.__dict__

    def pickle_to_string(self):
        return codecs.encode(pickle.dumps(self), "base64").decode()

    @staticmethod
    def car_instance_from_string(pickle_str: str):
        return pickle.loads(codecs.decode(pickle_str.encode(), "base64"))

    def pickle_to_file(self, file_name: str):
        with open(file_name, 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def car_from_pickle_file(file_name: str):
        with open(file_name, 'rb') as file:
            return pickle.load(file)

    def to_yaml(self):
        data = {self.__class__.__name__ : {"car_type": self.car_type, "producer": self.producer, "price": self.price, "number": str(self.number),
                "mileage": self.mileage}}
        return data

    def yaml_to_string(self):
        yaml = YAML()
        return str(self.to_yaml())

    @staticmethod
    def instance_from_yaml_string(yaml_string: str):
        yaml = YAML()
        return yaml.load(yaml_string)

    def yaml_to_file(self, file_name: str):
        yaml = YAML()
        with open(file_name, 'w') as file:
            return yaml.dump(self.to_yaml(), file)

    @staticmethod
    def instance_from_yaml_file(file_name: str):
        yaml = YAML()
        with open(file_name, 'r') as file:
            return yaml.load(file)

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

    print()
    print(type(car.yaml_to_string()), car.yaml_to_string())
    st=car.yaml_to_string()
    print(type(car.instance_from_yaml_string(st)),car.instance_from_yaml_string(st))
    print()
    print(type(car.instance_from_json_file("car.json")), car.instance_from_json_file("car.json"))
    print("pickle  ", type(car.car_from_pickle_file("pickle.txt")), car.car_from_pickle_file("pickle.txt"))
    print(type(car.instance_from_yaml_file("car.yaml")), car.instance_from_yaml_file("car.yaml"))
    car.json_to_file("car.json")
    car.pickle_to_file("pickle.txt")
    car.yaml_to_file("car.yaml")
    print("JSON -->", type(car.instance_from_json_file("car.json")), car.instance_from_json_file("car.json"))
    print("Pickle -->", type(car.car_from_pickle_file("pickle.txt")), car.car_from_pickle_file("pickle.txt"))
    print("Yaml -->",type(car.instance_from_yaml_file("car.yaml")), car.instance_from_yaml_file("car.yaml"))
