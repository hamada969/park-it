import math
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple, Text


class VehicleType(Enum):
    MOTORCYCLE_SCOOTER = "Motorcycle/Scooter"
    CAR_SUV = "Car/SUV"
    BUS_TRUCK = "Bus/Truck"


@dataclass
class FeeInterval:
    start_time: int
    end_time: int
    fee: int


@dataclass
class Vehicle:
    type: VehicleType


@dataclass
class Ticket:
    ticket_number: int
    vehicle_type: VehicleType
    entry_datetime: datetime


@dataclass
class Receipt:
    receipt_number: int
    ticket: Ticket
    exit_datetime: datetime
    fees_paid: float

    def __str__(self) -> Text:
        return (
            f"ParkingReceipt(receipt_number={self.receipt_number}, "
            f"ticket={self.ticket}, exit_datetime={self.exit_datetime}, "
            f"fees_paid={self.fees_paid})"
        )


class FeeModel(ABC):
    @abstractmethod
    def calculate_fee(self, vehicle_type: VehicleType, duration: int) -> int:
        pass


class MallFeeModel(FeeModel):
    def calculate_fee(self, vehicle_type: VehicleType, duration: int) -> int:
        fees = {"motorcycle": 10, "car": 20, "bus": 50}
        return fees[vehicle_type.name] * duration


class CustomFeeModel(FeeModel):
    def __init__(self, fee_intervals: List[Tuple[Optional[int], int]]):
        self.fee_intervals = fee_intervals

    def calculate_fee(self, vehicle_type: VehicleType, duration: int) -> int:
        total_fee = 0
        for interval_end, fee in self.fee_intervals:
            if interval_end is None or duration < interval_end:
                total_fee += fee * duration
                break
            else:
                total_fee += fee * (
                    interval_end  # type: ignore
                    - (0 if interval_end == self.fee_intervals[0][0] else self.fee_intervals[0][0])
                )
                duration -= interval_end
        return total_fee


class StadiumFeeModel(CustomFeeModel):
    def __init__(self, vehicle_type: VehicleType):
        if vehicle_type == VehicleType.MOTORCYCLE_SCOOTER:
            fee_intervals = [(4, 30), (12, 60), (None, 100)]  # None indicates infinity
        elif vehicle_type == VehicleType.CAR_SUV:
            fee_intervals = [(4, 60), (12, 120), (None, 200)]  # None indicates infinity
        else:
            raise ValueError("Invalid vehicle type for StadiumFeeModel")

        super().__init__(fee_intervals)


class AirportFeeModel(CustomFeeModel):
    def __init__(self, vehicle_type: VehicleType) -> None:
        if vehicle_type == VehicleType.MOTORCYCLE_SCOOTER:
            fee_intervals = [
                (1, 0),
                (8, 40),
                (24, 60),
                (None, 80),  # None indicates per day after 24 hours
            ]
        elif vehicle_type == VehicleType.CAR_SUV:
            fee_intervals = [
                (12, 60),
                (24, 80),
                (None, 100),  # None indicates per day after 24 hours
            ]
        else:
            raise ValueError("Invalid vehicle type for AirportFeeModel")

        super().__init__(fee_intervals)


class ParkingLot:
    def __init__(
        self, name: str, spots: Dict[VehicleType, int], fee_models: Dict[VehicleType, FeeModel]
    ):
        self.name = name
        self.spots = spots
        self.occupied_spots = {vehicle_type: 0 for vehicle_type in spots.keys()}
        self.vehicle_records: Dict[int, Tuple[Vehicle, Ticket]] = {}
        self.fee_models = fee_models
        self.ticket_counter = 1
        self.receipt_counter = 1

    def park_vehicle(self, vehicle: Vehicle) -> Optional[Ticket]:
        if self.occupied_spots[vehicle.type] < self.spots[vehicle.type]:
            self.occupied_spots[vehicle.type] += 1
            ticket = Ticket(self.ticket_counter, vehicle.type, datetime.now())
            self.vehicle_records[self.ticket_counter] = (vehicle, ticket)
            self.ticket_counter += 1
            return ticket
        else:
            return None

    def unpark_vehicle(self, ticket_number: int) -> Optional[Receipt]:
        if ticket_number not in self.vehicle_records:
            return None

        vehicle, ticket = self.vehicle_records[ticket_number]
        del self.vehicle_records[ticket_number]

        self.occupied_spots[vehicle.type] -= 1

        duration = int((datetime.now() - ticket.entry_datetime).total_seconds() / 3600)
        fees_paid = self.fee_models[vehicle.type].calculate_fee(vehicle.type, math.ceil(duration))

        receipt = Receipt(self.receipt_counter, ticket, datetime.now(), fees_paid)
        self.receipt_counter += 1
        return receipt
