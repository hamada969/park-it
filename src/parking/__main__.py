from datetime import datetime, timedelta
from typing import Dict, List

from parking.domain_types import (
    VehicleType,
    FeeInterval,
    Vehicle,
    ParkingLot,
)


def create_fee_models() -> Dict[VehicleType, List[FeeInterval]]:
    mall_fee_intervals = {
        VehicleType.MOTORCYCLE_SCOOTER: [FeeInterval(0, 1, 10), FeeInterval(1, 24, 10)],
        VehicleType.CAR_SUV: [FeeInterval(0, 1, 20), FeeInterval(1, 24, 20)],
        VehicleType.BUS_TRUCK: [FeeInterval(0, 1, 50), FeeInterval(1, 24, 50)],
    }
    return mall_fee_intervals


def main() -> None:
    # Create parking lot
    spots = {
        VehicleType.MOTORCYCLE_SCOOTER: 100,
        VehicleType.CAR_SUV: 80,
        VehicleType.BUS_TRUCK: 10,
    }
    fee_model = create_fee_models()
    parking_lot = ParkingLot(spots, fee_model)

    # Park vehicles
    motorcycle = Vehicle(VehicleType.MOTORCYCLE_SCOOTER, "ABC123")
    car = Vehicle(VehicleType.CAR_SUV, "XYZ789")
    truck = Vehicle(VehicleType.BUS_TRUCK, "JKL456")

    motorcycle_ticket = parking_lot.park_vehicle(motorcycle, datetime.now())
    car_ticket = parking_lot.park_vehicle(car, datetime.now())
    truck_ticket = parking_lot.park_vehicle(truck, datetime.now())

    if motorcycle_ticket:
        print(
            f"Motorcycle ticket: {motorcycle_ticket.ticket_number}, "
            f"spot: {motorcycle_ticket.spot_number}"
        )
        motorcycle_receipt = parking_lot.unpark_vehicle(
            motorcycle_ticket.ticket_number, datetime.now() + timedelta(hours=3, minutes=30)
        )
        print(f"Motorcycle fees: {motorcycle_receipt.fees_paid}")

    if car_ticket:
        print(f"Car ticket: {car_ticket.ticket_number}, spot: {car_ticket.spot_number}")
        car_receipt = parking_lot.unpark_vehicle(
            car_ticket.ticket_number, datetime.now() + timedelta(hours=6, minutes=1)
        )
        print(f"Car fees: {car_receipt.fees_paid}")

    if truck_ticket:
        print(f"Truck ticket: {truck_ticket.ticket_number}, spot: {truck_ticket.spot_number}")
        truck_receipt = parking_lot.unpark_vehicle(
            truck_ticket.ticket_number, datetime.now() + timedelta(hours=1, minutes=59)
        )
        print(f"Truck fees: {truck_receipt.fees_paid}")


if __name__ == "__main__":
    main()
