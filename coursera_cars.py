import os
import csv

"""reading  a data from table about different types of cars, an example table coursera_week3_cars.csv"""


class CarBase:  # base car class
    def __init__(self, brand, photo_file_name, carrying):
        self.carrying = float(carrying)
        self.photo_file_name = photo_file_name
        self.brand = brand

    def get_photo_file_ext(self):  # getting name of photo file without .png and so on
        return os.path.splitext(self.photo_file_name)[1]


class Car(CarBase):  # passenger car
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)
        self.car_type = "car"


class Truck(CarBase):  # truck
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = "truck"
        try:
            self.body_length, self.body_width, self.body_height = body_whl.split("x")
            self.body_height = float(self.body_height)
            self.body_length = float(self.body_length)
            self.body_width = float(self.body_width)
        except ValueError:
            self.body_width, self.body_height, self.body_length = 0.0, 0.0, 0.0

    def get_body_volume(self):
        return self.body_length * self.body_height * self.body_width


class SpecMachine(CarBase):  # special machines
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra
        self.car_type = "spec_machine"


def get_car_list(csv_filename):  # checking if in the table right data and adding it to the list if they are ok
    car_list = []
    try:
        with open(csv_filename) as file:
            reader = csv.reader(file, delimiter=";")  # reading a file through a separator
            next(reader)
            for row in reader:
                if row[0] == "car" and row[1] != '' and row[2] != '' and row[3] != '' and row[5] != '':
                    car = Car(row[1], row[3], row[5], row[2])
                    if car.get_photo_file_ext() not in (".png", ".jpeg", ".jpg", ".gif"):
                        continue
                    car_list.append(car)
                if row[0] == "truck" and row[1] != '' and row[3] != '' and row[5] != '':
                    truck = Truck(row[1], row[3], row[5], row[4])
                    if truck.get_photo_file_ext() not in (".png", ".jpeg", ".jpg", ".gif"):
                        continue
                    car_list.append(truck)
                if row[0] == "spec_machine" and row[1] != '' and row[3] != '' and row[5] != '' and row[6] != '':
                    spec_macine = SpecMachine(row[1], row[3], row[5], row[6])
                    print(spec_macine.get_photo_file_ext())
                    if spec_macine.get_photo_file_ext() not in (".png", ".jpeg", ".jpg", ".gif"):
                        continue
                    car_list.append(spec_macine)
        return car_list
    except ValueError:
        return car_list
