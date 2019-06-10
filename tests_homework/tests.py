import unittest
import random
import uuid
from homework import Car, Cesar, Garage, Serialization
from constants import TOWNS, CARS_TYPES, CARS_PRODUCER, CESAR_NAME


def data_init_car():
    return Car(
        car_type=random.choice(CARS_TYPES),
        producer=random.choice(CARS_PRODUCER),
        price=round(random.uniform(1, 100000), 2),
        mileage=round(random.uniform(1, 100000), 2)
    )


def data_init_garage():
    cesar_id = uuid.uuid4()
    return Garage(
        cars=[data_init_car(), data_init_car(), data_init_car()],
        town=random.choice(TOWNS),
        places=5,
        owner=cesar_id
    )


def date_init_cesar():
    return Cesar(random.choice(CESAR_NAME), [data_init_garage(), data_init_garage(), data_init_garage()])


class CarTestCase(unittest.TestCase):

    def test_change_number(self):
        car = data_init_car()
        first_number = car.number
        car.change_number()
        second_number = car.number
        self.assertNotEqual(first_number, second_number)

    def test_equal(self):
        car1 = data_init_car()
        car2 = Car(car1.price, car1.car_type, car1.producer, car1.mileage, car1.number)
        self.assertEqual(car1, car2)

    def test_not_equal(self):
        car1 = data_init_car()
        car2 = data_init_car()
        self.assertNotEqual(car1, car2)

    def test_serialization(self):
        car = data_init_car()
        Serialization.json_to_file(car, "fixtures/car1.json")
        Serialization.pickle_to_file(car, "fixtures/car1.pickle")
        Serialization.yaml_to_file(car, "fixtures/car1.yaml")
        car_json = Serialization.instance_from_json_file(Car, "fixtures/car1.json")
        car_pickle = Serialization.instance_from_pickle_file("fixtures/car1.pickle")
        car_yaml = Serialization.instance_from_yaml_file(Car, "fixtures/car1.yaml")
        self.assertEqual(car, car_json)
        self.assertEqual(car, car_pickle)
        self.assertEqual(car, car_yaml)

    def test_deserialization(self):
        car = Car(55523.42, "Coupe", "Buick", 13897.37, "b50d37e5-6a89-45da-a565-0607f72c7e72")
        car_json = Serialization.instance_from_json_file(Car, "fixtures/car.json")
        car_pickle = Serialization.instance_from_pickle_file("fixtures/car.pickle")
        car_yaml = Serialization.instance_from_yaml_file(Car, "fixtures/car.yaml")
        self.assertEqual(car, car_json)
        self.assertEqual(car, car_pickle)
        self.assertEqual(car, car_yaml)


if __name__ == '__main__':
    unittest.main()
