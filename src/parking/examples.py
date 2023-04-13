from datetime import datetime

from parking.models.parking_lot import ParkingLot
from parking.models.vehicle import VehicleType
from parking.models.fees import MallFeeModel, StadiumFeeModel, AirportFeeModel


def run_example_one() -> None:
    spots = {VehicleType.MOTORCYCLE_SCOOTER: 2}

    fee_models = {VehicleType.MOTORCYCLE_SCOOTER: MallFeeModel()}
    scooter_parking_lot = ParkingLot("Motorcycle/Scooter Parking Lot", spots, fee_models)
    print(scooter_parking_lot.name)

    # Action 1
    ticket_one = scooter_parking_lot.park_vehicle(
        vehicle_type=VehicleType.MOTORCYCLE_SCOOTER,
        fake_entry_time=datetime(2022, 5, 29, 14, 4, 7),
    )
    print(ticket_one)

    # Action 2
    ticket_two = scooter_parking_lot.park_vehicle(
        vehicle_type=VehicleType.MOTORCYCLE_SCOOTER,
        fake_entry_time=datetime(2022, 5, 29, 14, 44, 7),
    )
    print(ticket_two)

    # Action 3
    ticket_three = scooter_parking_lot.park_vehicle(vehicle_type=VehicleType.MOTORCYCLE_SCOOTER)
    print(ticket_three)

    # Action 4
    receipt_one = scooter_parking_lot.unpark_vehicle(
        ticket_number=ticket_two.ticket_number, fake_duration=3360  # 56 min
    )
    print(receipt_one)

    # Action 5
    ticket_four = scooter_parking_lot.park_vehicle(
        vehicle_type=VehicleType.MOTORCYCLE_SCOOTER,
        fake_entry_time=datetime(2022, 5, 29, 15, 59, 7),
    )
    print(ticket_four)

    # Action 6
    receipt_two = scooter_parking_lot.unpark_vehicle(
        ticket_number=ticket_one.ticket_number, fake_duration=13200
    )
    print(receipt_two)


def run_example_two() -> None:
    spots = {
        VehicleType.MOTORCYCLE_SCOOTER: 100,
        VehicleType.CAR_SUV: 80,
        VehicleType.BUS_TRUCK: 10,
    }

    mall = MallFeeModel()
    fee_models = {
        VehicleType.MOTORCYCLE_SCOOTER: mall,
        VehicleType.CAR_SUV: mall,
        VehicleType.BUS_TRUCK: mall,
    }
    mall_parking_lot = ParkingLot("Mall parking lot", spots, fee_models)
    print(mall_parking_lot.name)

    # Action 1
    ticket_one = mall_parking_lot.park_vehicle(vehicle_type=VehicleType.MOTORCYCLE_SCOOTER)
    receipt_one = mall_parking_lot.unpark_vehicle(
        ticket_number=ticket_one.ticket_number, fake_duration=12600
    )
    print(ticket_one)
    print(receipt_one)

    # Action 2
    ticket_two = mall_parking_lot.park_vehicle(vehicle_type=VehicleType.CAR_SUV)
    receipt_two = mall_parking_lot.unpark_vehicle(
        ticket_number=ticket_two.ticket_number, fake_duration=21660
    )
    print(ticket_two)
    print(receipt_two)

    # Action 3
    ticket_three = mall_parking_lot.park_vehicle(vehicle_type=VehicleType.BUS_TRUCK)
    receipt_three = mall_parking_lot.unpark_vehicle(
        ticket_number=ticket_three.ticket_number, fake_duration=7140
    )
    print(ticket_three)
    print(receipt_three)


def run_example_three() -> None:
    spots = {VehicleType.MOTORCYCLE_SCOOTER: 1000, VehicleType.CAR_SUV: 1500}

    motorcycle_fee_model = StadiumFeeModel()
    car_fee_model = StadiumFeeModel()
    fee_models = {
        VehicleType.MOTORCYCLE_SCOOTER: motorcycle_fee_model,
        VehicleType.CAR_SUV: car_fee_model,
    }
    stadium_parking_lot = ParkingLot("Stadium Parking Lot", spots, fee_models)
    print(stadium_parking_lot.name)

    # Action 1
    ticket_one = stadium_parking_lot.park_vehicle(vehicle_type=VehicleType.MOTORCYCLE_SCOOTER)
    receipt_one = stadium_parking_lot.unpark_vehicle(
        ticket_number=ticket_one.ticket_number, fake_duration=13200  # 3 hour 40 min
    )
    print(ticket_one)
    print(receipt_one)

    # Action 2
    ticket_two = stadium_parking_lot.park_vehicle(vehicle_type=VehicleType.MOTORCYCLE_SCOOTER)
    receipt_two = stadium_parking_lot.unpark_vehicle(
        ticket_number=ticket_two.ticket_number, fake_duration=53940  # 14 hour 59 min
    )
    print(ticket_two)
    print(receipt_two)

    # Action 3
    ticket_three = stadium_parking_lot.park_vehicle(vehicle_type=VehicleType.CAR_SUV)
    receipt_three = stadium_parking_lot.unpark_vehicle(
        ticket_number=ticket_three.ticket_number, fake_duration=41400  # 11 hour 30 min
    )
    print(ticket_three)
    print(receipt_three)

    # Action 4
    ticket_four = stadium_parking_lot.park_vehicle(vehicle_type=VehicleType.CAR_SUV)
    receipt_four = stadium_parking_lot.unpark_vehicle(
        ticket_number=ticket_four.ticket_number, fake_duration=47100  # 13 hour 5 min
    )
    print(ticket_four)
    print(receipt_four)


def run_example_four() -> None:
    spots = {
        VehicleType.MOTORCYCLE_SCOOTER: 200,
        VehicleType.CAR_SUV: 500,
        VehicleType.BUS_TRUCK: 100,
    }

    motorcycle_fee_model = AirportFeeModel()
    car_fee_model = AirportFeeModel()

    fee_models = {
        VehicleType.MOTORCYCLE_SCOOTER: motorcycle_fee_model,
        VehicleType.CAR_SUV: car_fee_model,
    }

    airport_parking_lot = ParkingLot("Airport Parking Lot", spots, fee_models)
    print(airport_parking_lot.name)

    # Action 1
    ticket_one = airport_parking_lot.park_vehicle(vehicle_type=VehicleType.MOTORCYCLE_SCOOTER)
    receipt_one = airport_parking_lot.unpark_vehicle(
        ticket_number=ticket_one.ticket_number, fake_duration=3300  # 55 min
    )
    print(ticket_one)
    print(receipt_one)

    # Action 2
    ticket_two = airport_parking_lot.park_vehicle(vehicle_type=VehicleType.MOTORCYCLE_SCOOTER)
    receipt_two = airport_parking_lot.unpark_vehicle(
        ticket_number=ticket_two.ticket_number, fake_duration=53940  # 14 hour 59 min
    )
    print(ticket_two)
    print(receipt_two)

    # Action 3
    ticket_three = airport_parking_lot.park_vehicle(vehicle_type=VehicleType.MOTORCYCLE_SCOOTER)
    receipt_three = airport_parking_lot.unpark_vehicle(
        ticket_number=ticket_three.ticket_number, fake_duration=129600  # 1 day 12 hours
    )
    print(ticket_three)
    print(receipt_three)

    # Action 4
    ticket_four = airport_parking_lot.park_vehicle(vehicle_type=VehicleType.CAR_SUV)
    receipt_four = airport_parking_lot.unpark_vehicle(
        ticket_number=ticket_four.ticket_number, fake_duration=3000  # 50 min
    )
    print(ticket_four)
    print(receipt_four)

    # Action 5
    ticket_five = airport_parking_lot.park_vehicle(vehicle_type=VehicleType.CAR_SUV)
    receipt_five = airport_parking_lot.unpark_vehicle(
        ticket_number=ticket_five.ticket_number, fake_duration=86340  # 23 hours 59 min
    )
    print(ticket_five)
    print(receipt_five)

    # Action 6
    ticket_six = airport_parking_lot.park_vehicle(vehicle_type=VehicleType.CAR_SUV)
    receipt_six = airport_parking_lot.unpark_vehicle(
        ticket_number=ticket_six.ticket_number, fake_duration=262800  # 3 days 1 hour
    )
    print(ticket_six)
    print(receipt_six)
