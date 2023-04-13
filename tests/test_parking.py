from datetime import datetime

import pytest

from parking.examples import run_example_one, run_example_two, run_example_three, run_example_four
from parking.models.fees import MallFeeModel, StadiumFeeModel, AirportFeeModel
from parking.models.parking_lot import ParkingLot
from parking.models.slips import Ticket, Receipt
from parking.models.vehicle import VehicleType


def test_base_case_example_one(capsys):
    """
    Example 1: Small motorcycle/scooter parking lot
    Spots:
        ● Motorcycles/scooters: 2 spots
        ● Cars/SUVs/Buses/Trucks: NA
    Fee Model: Please refer to the Mall fee model, mentioned in the ‘Fee Models’ section
    Scenarios:

    Action: Park motorcycle
        Result:
        Parking Ticket: Ticket Number: 001,
        Spot Number: 1
        Entry Date-time: 29-May-2022 14:04:07

    Action: Park scooter
        Result:
        Parking Ticket: Ticket Number: 002
        Spot Number: 2
        Entry Date-time: 29-May-2022 14:44:07

    Action: Park scooter:
        Result:
        No space available

    Action: Unpark scooter, ticket number 002
        Result:
        Parking Receipt: Receipt Number: R-001
        Entry Date-time: 29-May-2022 14:44:07
        Exit Date-time: 29-May-2022 15:40:07
        Fees: 10

    Action: Park motorcycle
        Result:
        Parking Ticket: Ticket Number: 003
        Spot Number: 2
        Entry Date-time: 29-May-2022 15:59:07

    Action: Unpark motorcycle, Ticket number 001
        Result:
        Parking Receipt: Receipt Number: R-002
        Entry Date-time: 29-May-2022 14:04:07
        Exit Date-time: 29-May-2022 17:44:07
        Fees: 40
    """
    run_example_one()
    captured = capsys.readouterr()
    assert (
        f"Parking Ticket:\n\tTicket Number: 001\n"
        f"\tSpot Number: 1\n"
        f"\tEntry Date-time: 29-May-2022 14:04:07"
    ) in captured.out
    assert (
        f"Parking Ticket:\n\tTicket Number: 002\n"
        f"\tSpot Number: 2\n"
        f"\tEntry Date-time: 29-May-2022 14:44:07"
    ) in captured.out
    assert "No space available" in captured.out
    assert (
        f"Parking Receipt:\n\tReceipt Number: R-001\n"
        f"\tEntry Date-time: 29-May-2022 14:44:07\n"
        f"\tExit Date-time: 29-May-2022 15:40:07\n"
        f"\tFees: 10"
    ) in captured.out
    assert (
        f"Parking Ticket:\n\tTicket Number: 003\n"
        f"\tSpot Number: 2\n"
        f"\tEntry Date-time: 29-May-2022 15:59:07"
    ) in captured.out
    assert (
        f"Parking Receipt:\n\tReceipt Number: R-002\n"
        f"\tEntry Date-time: 29-May-2022 14:04:07\n"
        f"\tExit Date-time: 29-May-2022 17:44:07\n"
        f"\tFees: 40"
    ) in captured.out


def test_base_case_example_two(capsys):
    """
    Example 2: Mall parking lot
    Spots:
        ● Motorcycles/scooters: 100 spots
        ● Cars/SUVs: 80 spots
        ● Buses/Trucks: 10 spots
    Fee Model: Please refer to the Mall fee model and its examples, mentioned in the ‘Fee
    Models’ section
    Scenarios: The park and unpark steps shown in the previous example have been skipped to
    reduce the text in the problem statement.
        ● Motorcycle parked for 3 hours and 30 mins. Fees: 40
        ● Car parked for 6 hours and 1 min. Fees: 140
        ● Truck parked for 1 hour and 59 mins. Fees: 100
    """
    run_example_two()
    captured = capsys.readouterr()
    assert "Fees: 40" in captured.out
    assert "Fees: 140" in captured.out
    assert "Fees: 100" in captured.out


def test_base_case_example_three(capsys):
    """
    Example 3: Stadium Parking Lot
    Spots:
        ● Motorcycles/scooters: 1000 spots
        ● Cars/SUVs: 1500 spots
    Fee Model: Please refer to the Stadium fee model mentioned in the ‘Fee Models’ section
    Scenarios: The park and unpark steps shown in the previous example have been skipped to
    reduce the text in the problem statement.
        ● Motorcycle parked for 3 hours and 40 mins. Fees: 30
        ● Motorcycle parked for 14 hours and 59 mins. Fees: 390.
            ○ 30 for the first 4 hours. 60 for the next 8 hours. And then 300 for the
            remaining duration.
        ● Electric SUV parked for 11 hours and 30 mins. Fees: 180.
            ○ 60 for the first 4 hours and then 120 for the remaining duration.
        ● SUV parked for 13 hours and 5 mins. Fees: 580.
            ○ 60 for the first 4 hours and then 120 for the next 8 hours. 400 for the
            remaining duration.
    """
    run_example_three()
    captured = capsys.readouterr()
    assert "Fees: 30" in captured.out
    assert "Fees: 390" in captured.out
    assert "Fees: 180" in captured.out
    assert "Fees: 580" in captured.out


def test_base_case_example_four(capsys):
    """
    Example 4: Airport Parking Lot
    Spots:
        ● Motorcycles/scooters: 200 spots
        ● Cars/SUVs: 500 spots
        ● Buses/Trucks: 100 spots
    Fee Model: Please refer to the Airport fee model mentioned in the ‘Fee Models’ section
    Scenarios: The park and unpark steps shown in the previous example have been skipped to
    reduce the text in the problem statement.
        ● Motorcycle parked for 55 mins. Fees: 0
        ● Motorcycle parked for 14 hours and 59 mins. Fees: 60
        ● Motorcycle parked for 1 day and 12 hours. Fees: 160
        ● Car parked for 50 mins. Fees: 60
        ● SUV parked for 23 hours and 59 mins. Fees: 80
        ● Car parked for 3 days and 1 hour. Fees: 400
    """
    run_example_four()
    captured = capsys.readouterr()
    assert "Fees: 0" in captured.out
    assert "Fees: 60" in captured.out
    assert "Fees: 160" in captured.out
    assert "Fees: 60" in captured.out
    assert "Fees: 80" in captured.out
    assert "Fees: 400" in captured.out


def test_assigning_ticket_attributes_prints_as_expected():
    t = Ticket(ticket_number=1, spot_number=1, entry_datetime=datetime(2022, 5, 29, 14, 4, 7))
    assert str(t) == (
        f"Parking Ticket:\n\tTicket Number: 001\n"
        f"\tSpot Number: 1\n"
        f"\tEntry Date-time: 29-May-2022 14:04:07"
    )


def test_assigning_receipt_attributes_prints_as_expected():
    r = Receipt(
        receipt_number=2,
        entry_datetime=datetime(2022, 5, 29, 14, 4, 7),
        exit_datetime=datetime(2022, 5, 29, 16, 4, 7),
        fees_paid=5,
    )
    assert str(r) == (
        f"Parking Receipt:\n\tReceipt Number: R-002\n"
        f"\tEntry Date-time: 29-May-2022 14:04:07\n"
        f"\tExit Date-time: 29-May-2022 16:04:07\n"
        f"\tFees: 5"
    )


mall_test_data = [(1, 20), (2, 40), (3, 60), (4, 80)]


@pytest.mark.parametrize("duration, expected_fees", mall_test_data)
def test_mall_fee_model_returns_flat_fee(duration, expected_fees):
    mall_fee_model = MallFeeModel()
    fees_paid = mall_fee_model.calculate_fees(
        vehicle_type=VehicleType.CAR_SUV, duration_in_hours=duration
    )
    assert fees_paid == expected_fees


stadium_test_data = [
    (3, 60),
    (4, 180),
    # 60 for 4 hours, 120 for next 8, then 3 * 200
    (15, 780),
]


@pytest.mark.parametrize("duration, expected_fees", stadium_test_data)
def test_stadium_fee_model_returns_flat_fee_then_per_hour(duration, expected_fees):
    stadium_fee_model = StadiumFeeModel()
    fees_paid = stadium_fee_model.calculate_fees(
        vehicle_type=VehicleType.CAR_SUV, duration_in_hours=duration
    )
    assert fees_paid == expected_fees


airport_test_data = [
    (7, 60),
    (18, 80),
    # 38 hours, calculated at a ceiling of 2 days, so 100*2
    (38, 200),
]


@pytest.mark.parametrize("duration, expected_fees", airport_test_data)
def test_airport_fee_model_returns_flat_fee_one_day_then_per_day(duration, expected_fees):
    airport_fee_model = AirportFeeModel()
    fees_paid = airport_fee_model.calculate_fees(
        vehicle_type=VehicleType.CAR_SUV, duration_in_hours=duration
    )
    assert fees_paid == expected_fees


def test_parking_lot_park_a_bus_inside_airport_returns_a_valid_ticket():
    parking_lot = ParkingLot(
        name="Airport Parking Lot",
        spots={VehicleType.BUS_TRUCK: 4},
        fee_models={VehicleType.BUS_TRUCK: AirportFeeModel()},
    )
    ticket = parking_lot.park_vehicle(
        vehicle_type=VehicleType.BUS_TRUCK, fake_entry_time=datetime(2022, 5, 29, 14, 4, 7)
    )
    assert str(ticket) == (
        f"Parking Ticket:\n\tTicket Number: 001\n"
        f"\tSpot Number: 1\n"
        f"\tEntry Date-time: 29-May-2022 14:04:07"
    )


def test_parking_lot_unpark_a_car_from_mall_returns_a_valid_receipt():
    parking_lot = ParkingLot(
        name="Mall Parking Lot",
        spots={VehicleType.CAR_SUV: 1},
        fee_models={VehicleType.CAR_SUV: MallFeeModel()},
    )
    ticket = parking_lot.park_vehicle(
        vehicle_type=VehicleType.CAR_SUV, fake_entry_time=datetime(2022, 5, 29, 14, 4, 7)
    )

    receipt = parking_lot.unpark_vehicle(ticket.ticket_number, fake_duration=3600)

    assert str(receipt) == (
        f"Parking Receipt:\n\tReceipt Number: R-001\n"
        f"\tEntry Date-time: 29-May-2022 14:04:07\n"
        f"\tExit Date-time: 29-May-2022 15:04:07\n"
        f"\tFees: 20"
    )


def test_parking_lot_parking_with_invalid_vehicle_type_fails():
    parking_lot = ParkingLot(
        name="Sample Parking Lot",
        spots={VehicleType.CAR_SUV: 1},
        fee_models={VehicleType.CAR_SUV: MallFeeModel()},
    )
    with pytest.raises(ValueError, match="Vehicle type passed is not recognised"):
        parking_lot.park_vehicle(vehicle_type=1)


def test_parking_lot_unparking_with_invalid_ticket_number_fails():
    parking_lot = ParkingLot(
        name="Another Sample Parking Lot",
        spots={VehicleType.CAR_SUV: 1},
        fee_models={VehicleType.CAR_SUV: MallFeeModel()},
    )
    with pytest.raises(
        ValueError, match="Ticket 15 has not been commissioned by this parking lot"
    ):
        parking_lot.unpark_vehicle(ticket_number=15)
