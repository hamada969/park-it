import math
from datetime import datetime
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Text, Optional


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


class ParkingLot:
    def __init__(
        self, spots: Dict[VehicleType, int], fee_model: Dict[VehicleType, List[FeeInterval]]
    ):
        self.spots = spots
        self.fee_model = fee_model
        self.parking_tickets: List[Ticket] = []
        self.available_spots = {vehicle_type: spots[vehicle_type] for vehicle_type in spots}

    def _get_next_available_spot(self, vehicle_type: VehicleType) -> Optional[int]:
        if self.available_spots[vehicle_type] > 0:
            self.available_spots[vehicle_type] -= 1
            return self.spots[vehicle_type] - self.available_spots[vehicle_type]
        else:
            return None

    def park_vehicle(self, vehicle: Vehicle, entry_datetime: datetime) -> Optional[Ticket]:
        spot_number = self._get_next_available_spot(vehicle.vehicle_type)
        if spot_number is None:
            return None

        ticket_number = len(self.parking_tickets) + 1
        parking_ticket = Ticket(ticket_number, spot_number, entry_datetime, vehicle)
        self.parking_tickets.append(parking_ticket)
        return parking_ticket

    def _calculate_fee(self, vehicle_type: VehicleType, duration: int) -> int:
        total_fee = 0
        remaining_duration = duration

        for interval in self.fee_model[vehicle_type]:
            if remaining_duration > 0:
                interval_duration = min(
                    interval.end_time - interval.start_time, remaining_duration
                )
                fee_for_interval = interval_duration * interval.fee
                total_fee += fee_for_interval
                remaining_duration -= interval_duration
            else:
                break

        return total_fee

    def unpark_vehicle(self, ticket_number: int, exit_datetime: datetime) -> Receipt:
        parking_ticket = self.parking_tickets[ticket_number - 1]
        entry_datetime = parking_ticket.entry_datetime
        duration = (exit_datetime - entry_datetime).total_seconds() / 3600
        vehicle_type = parking_ticket.vehicle.vehicle_type

        fees_paid = self._calculate_fee(vehicle_type, math.ceil(duration))
        receipt_number = ticket_number
        parking_receipt = Receipt(receipt_number, entry_datetime, exit_datetime, fees_paid)

        self.available_spots[vehicle_type] += 1
        return parking_receipt
