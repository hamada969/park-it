from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional, Union, Text

from parking.models.fees import FeeModel
from parking.models.slips import Ticket, Receipt
from parking.models.vehicle import VehicleType

SEC_PER_HR: int = 3600
ERROR_MSG = Text


class ParkingLot:
    """
    The Parking Lot service, parks and unparks vehicles
    """

    def __init__(
        self, name: str, spots: Dict[VehicleType, int], fee_models: Dict[VehicleType, FeeModel]
    ):
        """
        Parking Lot constructor, that initialises service state

        :param name: name of the parking lot, just descriptive
        :param spots: how many spots are assigned for each vehicle type
        :param fee_models: fee models assigned by vehicle type, see fees.py
        """
        self.name = name
        self.spots = spots
        self.occupied_spots = {vehicle_type: 0 for vehicle_type in spots.keys()}
        self.vehicle_records: Dict[int, Tuple[VehicleType, Ticket]] = {}
        self.fee_models = fee_models
        self.ticket_counter = 1
        self.receipt_counter = 1

    def park_vehicle(
        self, vehicle_type: VehicleType, fake_entry_time: Optional[datetime] = None
    ) -> Union[Ticket, ERROR_MSG]:
        """
        When called, parks a vehicle by editing service state:
            * increments occupied_spots of vehicle type by 1
            * assigns a spot number
            * creates a ticket
            * updates vehicle records
            * increments tickets handed out by 1

        :param vehicle_type: vehicle type being parked, see VehicleType enum
        :param fake_entry_time:
                if assigned, uses that as a parking entry time instead of current time
        :return: a parking lot ticket or an error message
        """
        if not isinstance(vehicle_type, VehicleType):
            raise ValueError(f"Vehicle type passed is not recognised: {type(vehicle_type)}")
        elif fake_entry_time and not isinstance(fake_entry_time, datetime):
            raise ValueError(
                "Vehicle entry time to the parking needs to be a valid Date time instance"
            )

        if self.occupied_spots[vehicle_type] < self.spots[vehicle_type]:
            self.occupied_spots[vehicle_type] += 1
            spot_number = self.occupied_spots[vehicle_type]
            ticket = Ticket(self.ticket_counter, spot_number, fake_entry_time or datetime.now())
            self.vehicle_records[self.ticket_counter] = (vehicle_type, ticket)
            self.ticket_counter += 1
            return ticket
        else:
            return "No space available"

    def unpark_vehicle(self, ticket_number: int, fake_duration: Optional[int] = None) -> Receipt:
        """
        When called, unparks a vehicle by editing service state:
            * retrieves vehicle info from vehicle records
            * calculates fees to be paid based on vehicle type and total duration spent in parking
            * creates a receipt to be returned
            * decrements parking lot occupied spots by 1
            * increments released receipts by 1

        :param ticket_number: vehicle type being parked, see VehicleType enum
        :param fake_duration:
                if assigned, uses that as total time spent inside a parking lot, in seconds
        :return: a parking lot receipt
        """
        if ticket_number not in self.vehicle_records:
            raise ValueError(
                f"Ticket {ticket_number} has not been commissioned by this parking lot"
            )
        elif fake_duration and fake_duration <= 0:
            raise ValueError("Vehicle parking duration should be positive")

        vehicle_type, ticket = self.vehicle_records[ticket_number]

        duration_in_hours = (
            fake_duration or (datetime.now() - ticket.entry_datetime).total_seconds()
        ) / SEC_PER_HR

        fees_paid = self.fee_models[vehicle_type].calculate_fees(vehicle_type, duration_in_hours)

        receipt = Receipt(
            receipt_number=self.receipt_counter,
            entry_datetime=ticket.entry_datetime,
            exit_datetime=ticket.entry_datetime + timedelta(seconds=fake_duration)
            if fake_duration
            else datetime.now(),
            fees_paid=fees_paid,
        )

        self.occupied_spots[vehicle_type] -= 1
        self.receipt_counter += 1

        return receipt
