from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional, Union, Text

from parking.models.fees import FeeModel
from parking.models.slips import Ticket, Receipt
from parking.models.vehicle import VehicleType, Vehicle

SEC_PER_HR: int = 3600
Error = Text


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
        self, vehicle: Vehicle, fake_entry_time: Optional[datetime] = None
    ) -> Union[Ticket, Error]:
        if self.occupied_spots[vehicle.type] < self.spots[vehicle.type]:
            self.occupied_spots[vehicle.type] += 1
            spot_number = self.occupied_spots[vehicle.type]
            ticket = Ticket(
                self.ticket_counter, vehicle.type, fake_entry_time or datetime.now(), spot_number
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
