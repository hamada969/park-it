from datetime import datetime
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Text, Optional


class VehicleType(Enum):
    MOTORCYCLE = "Motorcycle"
    SCOOTER = "Scooter"
    CAR = "Car"
    SUV = "SUV"
    BUS = "Bus"
    TRUCK = "Truck"


@dataclass
class FeeInterval:
    start_time: int
    end_time: int
    fee: int


@dataclass
class FeeModel:
    vehicle_type: VehicleType
    fee_intervals: List[FeeInterval]


@dataclass
class ParkingSpot:
    spot_number: int
    size: VehicleType
    is_available: bool


@dataclass
class Vehicle:
    vehicle_type: VehicleType
    license_plate: Text
    owner_details: Optional[Text] = None


@dataclass
class Ticket:
    ticket_number: int
    spot_number: int
    entry_datetime: datetime
    vehicle: Vehicle


@dataclass
class Receipt:
    receipt_number: int
    entry_datetime: datetime
    exit_datetime: datetime
    fees_paid: int


@dataclass
class ParkingLot:
    spots: Dict[VehicleType, int]
    fee_model: List[FeeModel]
