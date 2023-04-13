from dataclasses import dataclass
from enum import Enum
from typing import Text


class VehicleType(Enum):
    MOTORCYCLE_SCOOTER = "Motorcycle/Scooter"
    CAR_SUV = "Car/SUV"
    BUS_TRUCK = "Bus/Truck"


@dataclass
class Vehicle:
    model: Text
    type: VehicleType
