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
        car_data = [
            "{\"car_type\": \"Coupe\", \"producer\": \"Chevrolet\", \"price\": 43976.5, \"number\": \"db85d5f2-5cf0-40b3-b7c4-26bd9b2df68e\", \"mileage\": 64728.51}",
            "{\"car_type\": \"Crossover\", \"producer\": \"BENTLEY\", \"price\": 22809.77, \"number\": \"1154dd04-fca2-4947-8e51-13de5901467d\", \"mileage\": 24325.23}",
            "{\"car_type\": \"Diesel\", \"producer\": \"Buick\", \"price\": 56415.45, \"number\": \"6d7f767b-109d-4c29-b41c-74ef51903f08\", \"mileage\": 3885.34}"
        ]
        car_list = [Serialization.instance_from_json_string(Car, c) for c in car_data]
        garage = Garage("Rome", car_list, 5, "f2b521c8-6d5d-460f-8101-2603a1e7d316")
        self.assertEqual(garage.hit_hat(), 123201.72)
        self.assertNotEqual(garage.hit_hat(), 123687768)

    def test_add_car_to_garage(self):
        car_data = [
            "{\"car_type\": \"Coupe\", \"producer\": \"Chevrolet\", \"price\": 43976.5, \"number\": \"db85d5f2-5cf0-40b3-b7c4-26bd9b2df68e\", \"mileage\": 64728.51}",
            "{\"car_type\": \"Crossover\", \"producer\": \"BENTLEY\", \"price\": 22809.77, \"number\": \"1154dd04-fca2-4947-8e51-13de5901467d\", \"mileage\": 24325.23}",
            "{\"car_type\": \"Diesel\", \"producer\": \"Buick\", \"price\": 56415.45, \"number\": \"6d7f767b-109d-4c29-b41c-74ef51903f08\", \"mileage\": 3885.34}"
        ]
        car_list = [Serialization.instance_from_json_string(Car, c) for c in car_data]
        garage = Garage("Rome", car_list, 3, "f2b521c8-6d5d-460f-8101-2603a1e7d316")
        car = data_init_car()
        with self.assertRaises(Exception, msg="Should raise: No place available error") as context:
            garage.add(car)
            self.assertTrue("No place available in" in context.exception.args)
        garage.places += 1
        garage.add(car)
        self.assertIn(car, garage.cars)

    def test_remove_car_from_garage(self):
        car_data = [
            "{\"car_type\": \"Coupe\", \"producer\": \"Chevrolet\", \"price\": 43976.5, \"number\": \"db85d5f2-5cf0-40b3-b7c4-26bd9b2df68e\", \"mileage\": 64728.51}",
            "{\"car_type\": \"Crossover\", \"producer\": \"BENTLEY\", \"price\": 22809.77, \"number\": \"1154dd04-fca2-4947-8e51-13de5901467d\", \"mileage\": 24325.23}",
            "{\"car_type\": \"Diesel\", \"producer\": \"Buick\", \"price\": 56415.45, \"number\": \"6d7f767b-109d-4c29-b41c-74ef51903f08\", \"mileage\": 3885.34}"
        ]
        car_list = [Serialization.instance_from_json_string(Car, c) for c in car_data]
        garage = Garage("Rome", car_list, 5, "f2b521c8-6d5d-460f-8101-2603a1e7d316")
        car_raise = data_init_car()
        car_valid = car_list[1]
        with self.assertRaises(Exception, msg="Should raise: No car in garage error") as context:
            garage.remove(car_raise)
            self.assertTrue(f"Car: '{car}' removed from garage" in context.exception.args)
        garage.remove(car_valid)
        self.assertNotIn(car_valid, garage.cars)

if __name__ == '__main__':
    unittest.main()
