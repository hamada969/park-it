import math
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass
from typing import Dict, Optional, Tuple, Text, Union

SEC_PER_HR: int = 3600
DATE_FORMAT: Text = "%d-%b-%Y %H:%M:%S"
Error = Text


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
    model: Text
    type: VehicleType


@dataclass
class Ticket:
    ticket_number: int
    vehicle_type: VehicleType
    entry_datetime: datetime
    spot_number: int

    def __str__(self) -> Text:
        return (
            f"Parking Ticket:\n\tTicket Number: {'{0:03}'.format(self.ticket_number)}\n"
            f"\tSpot Number: {self.spot_number}\n"
            f"\tEntry Date-time: {self.entry_datetime.strftime(DATE_FORMAT)}"
        )


@dataclass
class Receipt:
    receipt_number: int
    ticket: Ticket
    entry_datetime: datetime
    exit_datetime: datetime
    fees_paid: float

    def __str__(self) -> Text:
        return (
            f"Parking Receipt:\n\tReceipt Number: R-{'{0:03}'.format(self.receipt_number)}\n"
            f"\tEntry Date-time: {self.entry_datetime.strftime(DATE_FORMAT)}\n"
            f"\tExit Date-time: {self.exit_datetime.strftime(DATE_FORMAT)}\n"
            f"\tFees: {self.fees_paid}"
        )


class FeeModel(ABC):
    @abstractmethod
    def calculate_fee(self, vehicle_type: VehicleType, duration: float) -> int:
        pass


class MallFeeModel(FeeModel):
    def calculate_fee(self, vehicle_type: VehicleType, duration: float) -> int:
        fees = {
            VehicleType.MOTORCYCLE_SCOOTER: 10,
            VehicleType.CAR_SUV: 20,
            VehicleType.BUS_TRUCK: 50,
        }
        return fees[vehicle_type] * math.ceil(duration)


class StadiumFeeModel(FeeModel):
    def calculate_fee(self, vehicle_type: VehicleType, duration: float) -> int:
        if vehicle_type == VehicleType.MOTORCYCLE_SCOOTER:
            intervals = [(0, 4, 30), (4, 12, 60)]
            per_hour_fee = 100
        elif vehicle_type == VehicleType.CAR_SUV:
            intervals = [(0, 4, 60), (4, 12, 120)]
            per_hour_fee = 200
        else:
            raise ValueError("Unsupported vehicle type for StadiumFeeModel")

        total_fee = 0
        hours_passed = 0
        for start, end, fee in intervals:
            if start <= hours_passed < end and hours_passed < duration:
                total_fee += fee
            hours_passed += end - start

        charge_past_twelve = 0
        if duration - hours_passed > 0:
            charge_past_twelve = (math.ceil(duration) - hours_passed) * per_hour_fee

        return total_fee + charge_past_twelve


class AirportFeeModel(FeeModel):
    def calculate_fee(self, vehicle_type: VehicleType, duration: float) -> int:
        if vehicle_type == VehicleType.MOTORCYCLE_SCOOTER:
            intervals = [(0, 1, 0), (1, 8, 40), (8, 24, 60)]
            per_day_fee = 80
        elif vehicle_type == VehicleType.CAR_SUV:
            intervals = [(0, 12, 60), (12, 24, 80)]
            per_day_fee = 100
        else:
            raise ValueError("Unsupported vehicle type for AirportFeeModel")

        if duration < 24:
            for start, end, fee in intervals:
                if start <= duration < end:
                    return fee

        total_days = math.ceil(duration / 24)
        return total_days * per_day_fee


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

    def park_vehicle(
        self, vehicle: Vehicle, entry_time: Optional[datetime] = None
    ) -> Union[Ticket, Error]:
        if self.occupied_spots[vehicle.type] < self.spots[vehicle.type]:
            self.occupied_spots[vehicle.type] += 1
            spot_number = self.occupied_spots[vehicle.type]
            ticket = Ticket(
                self.ticket_counter, vehicle.type, entry_time or datetime.now(), spot_number
            )
            self.vehicle_records[self.ticket_counter] = (vehicle, ticket)
            self.ticket_counter += 1
            return ticket
        else:
            return "No space available"

    def unpark_vehicle(
        self, ticket_number: int, fake_duration: Optional[int] = None
    ) -> Optional[Receipt]:
        if ticket_number not in self.vehicle_records:
            return None

        vehicle, ticket = self.vehicle_records[ticket_number]
        del self.vehicle_records[ticket_number]

        self.occupied_spots[vehicle.type] -= 1

        duration = (
            fake_duration or (datetime.now() - ticket.entry_datetime).total_seconds()
        ) / SEC_PER_HR

        fees_paid = self.fee_models[vehicle.type].calculate_fee(vehicle.type, duration)

        receipt = Receipt(
            receipt_number=self.receipt_counter,
            ticket=ticket,
            entry_datetime=ticket.entry_datetime,
            exit_datetime=ticket.entry_datetime + timedelta(seconds=fake_duration)
            if fake_duration
            else datetime.now(),
            fees_paid=fees_paid,
        )

        self.receipt_counter += 1
        return receipt
