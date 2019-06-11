import unittest
import random
import uuid
import logging
from testfixtures import LogCapture
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

class GarageTestCase(unittest.TestCase):

    def test_equal(self):
        garage1 = data_init_garage()
        garage2 = Garage(garage1.town, garage1.cars, garage1.places, garage1.owner)
        self.assertEqual(garage1, garage2)

    def test_not_equal(self):
        garage1 = data_init_garage()
        garage2 = data_init_garage()
        self.assertNotEqual(garage1, garage2)

    def test_serialization(self):
        garage = data_init_garage()
        Serialization.json_to_file(garage, "fixtures/garage1.json")
        Serialization.pickle_to_file(garage, "fixtures/garage1.pickle")
        Serialization.yaml_to_file(garage, "fixtures/garage1.yaml")
        garage_json = Serialization.instance_from_json_file(Garage, "fixtures/garage1.json")
        garage_pickle = Serialization.instance_from_pickle_file("fixtures/garage1.pickle")
        garage_yaml = Serialization.instance_from_yaml_file(Garage, "fixtures/garage1.yaml")
        self.assertEqual(garage, garage_json)
        self.assertEqual(garage, garage_pickle)
        self.assertEqual(garage, garage_yaml)

    def test_deserialization(self):
        car_data = [
        "{\"car_type\": \"Coupe\", \"producer\": \"Chevrolet\", \"price\": 43976.5, \"number\": \"db85d5f2-5cf0-40b3-b7c4-26bd9b2df68e\", \"mileage\": 64728.51}",
        "{\"car_type\": \"Crossover\", \"producer\": \"BENTLEY\", \"price\": 22809.77, \"number\": \"1154dd04-fca2-4947-8e51-13de5901467d\", \"mileage\": 24325.23}",
        "{\"car_type\": \"Diesel\", \"producer\": \"Buick\", \"price\": 56415.45, \"number\": \"6d7f767b-109d-4c29-b41c-74ef51903f08\", \"mileage\": 3885.34}"
        ]
        car_list = [Serialization.instance_from_json_string(Car, c) for c in car_data]
        garage = Garage("Rome", car_list, 5, "f2b521c8-6d5d-460f-8101-2603a1e7d316")
        garage_json = Serialization.instance_from_json_file(Garage, "fixtures/garage.json")
        garage_pickle = Serialization.instance_from_pickle_file("fixtures/garage.pickle")
        garage_yaml = Serialization.instance_from_yaml_file(Garage, "fixtures/garage.yaml")
        self.assertEqual(garage, garage_json)
        self.assertEqual(garage, garage_pickle)
        self.assertEqual(garage, garage_yaml)

    def test_hit_hat(self):
        garage = Serialization.instance_from_json_file(Garage, "fixtures/garage.json")
        self.assertEqual(garage.hit_hat(), 123201.72)
        self.assertNotEqual(garage.hit_hat(), 123687768)

    def test_add_car_to_garage(self):
        garage = Serialization.instance_from_json_file(Garage, "fixtures/garage.json")
        garage.places = len(garage.cars)
        car = data_init_car()
        with self.assertRaises(Exception, msg="Should raise: No place available error") as context:
            garage.add(car)
            self.assertTrue("No place available in" in context.exception.args)
        garage.places += 1
        garage.add(car)
        self.assertIn(car, garage.cars)

    def test_remove_car_from_garage(self):
        garage = Serialization.instance_from_json_file(Garage, "fixtures/garage.json")
        car_raise = data_init_car()
        car_valid = garage.cars[1]
        with self.assertRaises(Exception, msg="Should raise: No car in garage error") as context:
            garage.remove(car_raise)
            self.assertTrue(f"Car: '{car_raise}' removed from garage" in context.exception.args)
        garage.remove(car_valid)
        self.assertNotIn(car_valid, garage.cars)


class CesarTestCase(unittest.TestCase):
    def test_equal(self):
        cesar1 = date_init_cesar()
        cesar2 = Cesar(cesar1.name, cesar1.garages, cesar1.register_id)
        self.assertTrue(cesar1.equal(cesar2))

    def test_not_equal(self):
        cesar1 = date_init_cesar()
        cesar2 = date_init_cesar()
        self.assertFalse(cesar1.equal(cesar2))

    def test_serialization(self):
        cesar = date_init_cesar()
        Serialization.json_to_file(cesar, "fixtures/cesar1.json")
        Serialization.pickle_to_file(cesar, "fixtures/cesar1.pickle")
        Serialization.yaml_to_file(cesar, "fixtures/cesar1.yaml")
        cesar_json = Serialization.instance_from_json_file(Cesar, "fixtures/cesar1.json")
        cesar_pickle = Serialization.instance_from_pickle_file("fixtures/cesar1.pickle")
        cesar_yaml = Serialization.instance_from_yaml_file(Cesar, "fixtures/cesar1.yaml")
        self.assertTrue(cesar.equal(cesar_json))
        self.assertTrue(cesar.equal(cesar_pickle))
        self.assertTrue(cesar.equal(cesar_yaml))

    def test_deserialization(self):
        garage_data = [
        "{\"cars\": [\"{\\\"car_type\\\": \\\"Luxury Car\\\", \\\"producer\\\": \\\"BMW\\\", \\\"price\\\": 78038.71, \\\"number\\\": \\\"254b106d-452b-4e4d-989f-9434a69890b7\\\", \\\"mileage\\\": 72005.86}\", \"{\\\"car_type\\\": \\\"Crossover\\\", \\\"producer\\\": \\\"Chevrolet\\\", \\\"price\\\": 71032.82, \\\"number\\\": \\\"43228351-71cf-48c2-88e3-b5d0509fd462\\\", \\\"mileage\\\": 40815.66}\", \"{\\\"car_type\\\": \\\"Luxury Car\\\", \\\"producer\\\": \\\"Chery\\\", \\\"price\\\": 27577.73, \\\"number\\\": \\\"42beba8b-e1e4-4d4c-bb88-46f0ef50bf03\\\", \\\"mileage\\\": 84138.02}\"], \"places\": 5, \"owner\": \"428cd5f1-7646-4016-8e2d-ec26d151fe9b\", \"town\": \"Kiev\"}",
        "{\"cars\": [\"{\\\"car_type\\\": \\\"Coupe\\\", \\\"producer\\\": \\\"Buick\\\", \\\"price\\\": 38621.58, \\\"number\\\": \\\"e359ed2d-60dd-42c4-a761-8d5634da60ed\\\", \\\"mileage\\\": 7703.62}\", \"{\\\"car_type\\\": \\\"Sports Car\\\", \\\"producer\\\": \\\"Ford\\\", \\\"price\\\": 4948.44, \\\"number\\\": \\\"cab8988e-d033-4b43-966b-e3af6a6b75e6\\\", \\\"mileage\\\": 58175.29}\", \"{\\\"car_type\\\": \\\"SUV\\\", \\\"producer\\\": \\\"Ford\\\", \\\"price\\\": 32144.82, \\\"number\\\": \\\"f11a06f6-912c-4adc-99a3-16f3883d1f4c\\\", \\\"mileage\\\": 27458.44}\"], \"places\": 5, \"owner\": \"98462db8-87c8-4d5a-9f2a-f879187f0e79\", \"town\": \"Berlin\"}",
        "{\"cars\": [\"{\\\"car_type\\\": \\\"Luxury Car\\\", \\\"producer\\\": \\\"Dodge\\\", \\\"price\\\": 14991.98, \\\"number\\\": \\\"5c9c7c32-3b41-42e0-9a21-103a1d72730f\\\", \\\"mileage\\\": 67796.76}\", \"{\\\"car_type\\\": \\\"Diesel\\\", \\\"producer\\\": \\\"Chery\\\", \\\"price\\\": 80906.93, \\\"number\\\": \\\"9cb7fef1-9873-4dbc-8984-4db02011d97b\\\", \\\"mileage\\\": 25090.87}\", \"{\\\"car_type\\\": \\\"Coupe\\\", \\\"producer\\\": \\\"Lamborghini\\\", \\\"price\\\": 78447.6, \\\"number\\\": \\\"5add9532-516a-4d97-a381-dddc16259954\\\", \\\"mileage\\\": 76750.82}\"], \"places\": 5, \"owner\": \"39dd22de-5a0c-462f-a13e-24aef4e447f0\", \"town\": \"Rome\"}"
    ]
        garage_list = [Serialization.instance_from_json_string(Garage, c) for c in garage_data]
        cesar = Cesar("Benia", garage_list, "199e4987-9428-4bc4-a26b-1645c7c81cf8")
        cesar_json = Serialization.instance_from_json_file(Cesar, "fixtures/cesar.json")
        cesar_pickle = Serialization.instance_from_pickle_file("fixtures/cesar.pickle")
        cesar_yaml = Serialization.instance_from_yaml_file(Cesar, "fixtures/cesar.yaml")
        self.assertTrue(cesar.equal(cesar_json))
        self.assertTrue(cesar.equal(cesar_pickle))
        self.assertTrue(cesar.equal(cesar_yaml))

    def test_hit_hat(self):
        cesar = Serialization.instance_from_json_file(Cesar, "fixtures/cesar.json")
        self.assertEqual(cesar.hit_hat(), 426710.61000000004)
        self.assertNotEqual(cesar.hit_hat(), 123687768)

    def test_garage_count(self):
        cesar = Serialization.instance_from_json_file(Cesar, "fixtures/cesar.json")
        self.assertEqual(cesar.garage_count(), 3)
        self.assertNotEqual(cesar.garage_count(), 18)

    def test_cars_count(self):
        cesar = Serialization.instance_from_json_file(Cesar, "fixtures/cesar.json")
        self.assertEqual(cesar.cars_count(), 9)
        self.assertNotEqual(cesar.cars_count(), 12)

    def test_add_car(self):
        exp_msg_no_place = "No place available"
        exp_msg_exist = "The car is already in the garage"
        exp_msg_someone_else_car = "You can not add a car to someone else's garage"
        cesar = Serialization.instance_from_json_file(Cesar, "fixtures/cesar.json")
        car_exist = cesar.garages[0].cars[0]
        car_someone_else = data_init_car()
        garage_someone_else = data_init_garage()
        car = data_init_car()

        cesar.add_car(car)
        self.assertIn(car, [car for garage in [garage.cars for garage in cesar.garages]])

        with LogCapture(level=logging.WARNING) as logs:
            cesar.add_car(car_exist, cesar.garages[0])
            [record] = logs.records
            self.assertEqual(record.msg, exp_msg_exist)

        with LogCapture(level=logging.WARNING) as logs:
            cesar.add_car(car_someone_else, garage_someone_else)
            [record] = logs.records
            self.assertEqual(record.msg, exp_msg_someone_else_car)

        for garage in cesar.garages:
            garage.places = len(garage.cars)

        with LogCapture(level=logging.WARNING) as logs:
            cesar.add_car(car_someone_else)
            [record] = logs.records
            self.assertEqual(record.msg, exp_msg_no_place)


if __name__ == '__main__':
    unittest.main()
