import pytest

from parking.examples import run_example_one, run_example_two, run_example_three, run_example_four


# This is the base case for the Thought Machine test


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
