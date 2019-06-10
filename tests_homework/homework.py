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
import logging
import json
import pickle
import codecs
from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO
from constants import TOWNS, CARS_TYPES, CARS_PRODUCER, CESAR_NAME


class MyYAML(YAML):
    def dump(self, data, stream=None, **kw):
        inefficient = False
        if stream is None:
            inefficient = True
            stream = StringIO()
        YAML.dump(self, data, stream, **kw)
        if inefficient:
            return stream.getvalue()


yaml = YAML()
my_yaml = MyYAML()


class Serialization:
    # JSON
    @staticmethod
    def json_to_string(obj):
        try:
            return json.dumps(obj, default=obj.to_json)
        except TypeError as e:
            print(e)

    @staticmethod
    def instance_from_json_string(obj, json_string: str):
        try:
            return json.loads(json_string, object_hook=obj.from_json)

        except TypeError as e:
            print(e)

    @staticmethod
    def json_to_file(obj, file_name: str):
        with open(file_name, 'w') as f:
            json.dump(obj.to_json(obj), f, indent=4)

    @staticmethod
    def instance_from_json_file(obj, file_name: str):
        with open(file_name, 'r') as f:
            return json.load(f, object_hook=obj.from_json)

    # Pickle
    @staticmethod
    def pickle_to_string(obj):
        return codecs.encode(pickle.dumps(obj), "base64").decode()

    @staticmethod
    def instance_from_pickle_string(pickle_str: str):
        return pickle.loads(codecs.decode(pickle_str.encode(), "base64"))

    @staticmethod
    def pickle_to_file(obj, file_name: str):
        with open(file_name, 'wb') as f:
            pickle.dump(obj, f)

    @staticmethod
    def instance_from_pickle_file(file_name: str):
        with open(file_name, 'rb') as f:
            return pickle.load(f)
    # Yaml
    @staticmethod
    def yaml_to_string(obj):
        return my_yaml.dump(obj.to_yaml())

    @staticmethod
    def instance_from_yaml_string(obj, yaml_string: str):
        return obj.from_yaml(yaml.load(yaml_string))

    @staticmethod
    def yaml_to_file(obj, file_name: str):
        with open(file_name, 'w') as f:
            return yaml.dump(obj.to_yaml(), f)

    @staticmethod
    def instance_from_yaml_file(obj, file_name: str):
        with open(file_name, 'r') as f:
            return obj.from_yaml(yaml.load(f))


# _le_ and other comparison operators are defined by
# @functools.total_ordering using provided _lt_ and _eq_
@functools.total_ordering
class Car:
    def __init__(self, price: float, car_type: CARS_TYPES, producer: CARS_PRODUCER, mileage: float, number=None):
        self.price = price
        self.number = number if number else str(uuid.uuid4())
        self.mileage = mileage
        if producer in CARS_PRODUCER:
            self.producer = producer
        else:
            raise Exception("Bad Producer value, producer value must be: ", CARS_PRODUCER)
        if car_type in CARS_TYPES:
            self.car_type = car_type
        else:
            raise Exception("Bad car type, car type must be: ", CARS_TYPES)

    @staticmethod
    def to_json(obj: Car):
        data = {"car_type": obj.car_type, "producer": obj.producer, "price": obj.price, "number": obj.number,
                "mileage": obj.mileage}
        return data

    @staticmethod
    def from_json(data):
        car_type = data['car_type']
        producer = data['producer']
        price = data['price']
        number = data['number']
        mileage = data['mileage']
        return Car(car_type=car_type, producer=producer, price=price, number=number, mileage=mileage)

    def __setstate__(self, state):
        self.__dict__ = state

    def __getstate__(self):
        return self.__dict__

    def to_yaml(self):
        data = {"Car": {"car_type": self.car_type, "producer": self.producer, "price": self.price,
                        "number": str(self.number), "mileage": self.mileage}}
        return data

    @staticmethod
    def from_yaml(data):
        car_type = data['Car']['car_type']
        producer = data['Car']['producer']
        price = data['Car']['price']
        number = data['Car']['number']
        mileage = data['Car']['mileage']
        return Car(car_type=car_type, producer=producer, price=price, number=number, mileage=mileage)

    def __repr__(self):
        return f"Car(car_type='{self.car_type}', producer='{self.producer}', price='{self.price}'," \
            f" number='{self.number}', mileage='{self.mileage}')"

    def change_number(self):
        self.number = str(uuid.uuid4())

    def __lt__(self, other: Car):
        self_param_list = [self.price, self.number, self.mileage, self.producer, self.car_type]
        other_param_list = [other.price, other.number, other.mileage, other.producer, other.car_type]
        return self_param_list < other_param_list

    def __eq__(self, other: Car):
        self_param_list = [self.price, self.number, self.mileage, self.producer, self.car_type]
        other_param_list = [other.price, other.number, other.mileage, other.producer, other.car_type]
        return self_param_list == other_param_list


@functools.total_ordering
class Garage:
    def __init__(self, town: TOWNS, cars: [], places: int, owner=None):
        self.cars = cars if cars else []
        self.places = places
        self.owner = str(owner) if owner else None
        if town in TOWNS:
            self.town = town
        else:
            raise Exception("Bad Town name, available town: ", TOWNS)

    @staticmethod
    def to_json(obj: Garage):
        data = {"cars": [Serialization.json_to_string(c) for c in obj.cars],
                "places": obj.places,
                "owner": obj.owner,
                "town": obj.town
                }
        return data

    @staticmethod
    def from_json(data):
        cars = [Serialization.instance_from_json_string(Car, c) for c in data['cars']]
        places = data['places']
        owner = data['owner']
        town = data['town']
        return Garage(town=town, cars=cars, places=places, owner=owner)

    def __setstate__(self, state):
        self.__dict__ = state

    def __getstate__(self):
        return self.__dict__

    def to_yaml(self):
        data = {"Garage": {"cars": [Serialization.yaml_to_string(c) for c in self.cars],
                           "places": self.places,
                           "owner": str(self.owner),
                           "town": self.town}
                }
        return data

    @classmethod
    def from_yaml(cls, data):
        cars = [Serialization.instance_from_yaml_string(Car, c) for c in data['Garage']['cars']]
        places = data['Garage']['places']
        owner = data['Garage']['owner']
        town = data['Garage']['town']
        return Garage(cars=cars, places=places, owner=owner, town=town)

    def __repr__(self):
        return f"Garage(town='{self.town}', places='{self.places}', owner='{self.owner}', cars='{self.cars}')"

    def add(self, c):
        if len(self.cars) < self.places:
            self.cars.append(c)
        else:
            raise Exception("No place available in ", self)

    def remove(self, c):
        if c in self.cars:
            self.cars.remove(c)
            print(f"Car: '{c}' removed from garage")
        else:
            raise Exception(f"There is no '{c}' in this garage")

    def hit_hat(self):
        return sum(c.price for c in self.cars)

    def __lt__(self, other: Garage):
        self_param_list = [self.town, self.cars, self.places, self.owner]
        other_param_list = [other.town, other.cars, other.places, other.owner]
        return self_param_list < other_param_list

    def __eq__(self, other: Garage):
        self_param_list = [self.town, self.cars, self.places, self.owner]
        other_param_list = [other.town, other.cars, other.places, other.owner]
        return self_param_list == other_param_list

# _le_ and other comparison operators are defined by
# @functools.total_ordering using provided _lt_ and _eq_
@functools.total_ordering
class Cesar:
    def __init__(self, name: str, garages=None, register_id=None):
        self.name = name
        self.garages = garages if garages else []
        self.register_id = register_id if register_id else str(uuid.uuid4())

    @staticmethod
    def to_json(obj: Cesar):
        data = {"name": obj.name,
                "register_id": obj.register_id,
                "garages": [Serialization.json_to_string(g) for g in obj.garages],
                }
        return data

    @staticmethod
    def from_json(data):
        name = data['name']
        register_id = data['register_id']
        garages = [Serialization.instance_from_json_string(Garage, g) for g in data['garages']]
        return Cesar(name=name, register_id=register_id, garages=garages)

    def __setstate__(self, state):
        self.__dict__ = state

    def __getstate__(self):
        return self.__dict__

    def to_yaml(self):
        data = {"Cesar": {"name": self.name,
                          "register_id": self.register_id,
                          "garages": [Serialization.yaml_to_string(g) for g in self.garages]
                          }
                }
        return data

    @classmethod
    def from_yaml(cls, data):
        name = data['Cesar']['name']
        register_id = data['Cesar']['register_id']
        garages = [Serialization.instance_from_yaml_string(Garage, g) for g in data['Cesar']['garages']]
        return Cesar(name=name, register_id=register_id, garages=garages)

    def __repr__(self):
        return f"Cesar(name='{self.name}', registerID='{self.register_id}' garages='{self.garages}')"

    def hit_hat(self):
        return sum(g.hit_hat() for g in self.garages)

    def garage_count(self):
        return len(self.garages)

    def cars_count(self):
        return sum(len(g.cars) for g in self.garages)

    def place_available(self):
        for i in self.garages:
            if (i.places - len(i.cars)) > 0:
                return True
        return False

    def add_car(self, c: Car, g=None):
        if g is None:
            max(self.garages, key=lambda x: (x.places - len(x.cars))).add(c) if self.place_available() else \
                logging.warning("No place available")
        elif g in self.garages:
            g.add(c) if c not in g.cars else logging.warning("The car is already in the garage")
        elif g not in self.garages:
            logging.warning("You can not add a car to someone else's garage")

    def __eq__(self, other: Cesar):
        return self.hit_hat() == other.hit_hat()

    def equal(self, other: Cesar):
        self_list = [self.name, self.garages, self.register_id]
        other_list = [other.name, self.garages, self.register_id]
        return self_list == other_list

    def __lt__(self, other: Cesar):
        return self.hit_hat() < other.hit_hat()

