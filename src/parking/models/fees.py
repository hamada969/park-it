import math
from abc import ABC, abstractmethod

from parking.models.vehicle import VehicleType


class FeeModel(ABC):
    """
    An abstract representation of a Fee Model.
    Any class implementing this parent class should define its own way of calculating fees
    """

    @abstractmethod
    def calculate_fees(self, vehicle_type: VehicleType, duration_in_hours: float) -> int:
        """
        calculate_fee needs to be implemented if this class is used as a base class

        :param vehicle_type: the vehicle type dictates how much is charged in a given period
        :param duration_in_hours: the entire duration of the booking from parking to unparking
        :return: Total fees to be paid on exit
        """
        pass


class MallFeeModel(FeeModel):
    def calculate_fees(self, vehicle_type: VehicleType, duration_in_hours: float) -> int:
        fees = {
            VehicleType.MOTORCYCLE_SCOOTER: 10,
            VehicleType.CAR_SUV: 20,
            VehicleType.BUS_TRUCK: 50,
        }
        return fees[vehicle_type] * math.ceil(duration_in_hours)


class StadiumFeeModel(FeeModel):
    def calculate_fees(self, vehicle_type: VehicleType, duration_in_hours: float) -> int:
        if vehicle_type == VehicleType.MOTORCYCLE_SCOOTER:
            fee_intervals = [(0, 4, 30), (4, 12, 60)]
            per_hour_fee = 100
        elif vehicle_type == VehicleType.CAR_SUV:
            fee_intervals = [(0, 4, 60), (4, 12, 120)]
            per_hour_fee = 200
        else:
            raise ValueError("Unsupported vehicle type for StadiumFeeModel")

        total_fee = 0
        hours_passed = 0
        for start, end, fee in fee_intervals:
            if start <= hours_passed < end and hours_passed <= duration_in_hours:
                total_fee += fee
            hours_passed += end - start

        charges_past_twelve = 0
        if duration_in_hours - hours_passed > 0:
            charges_past_twelve = (math.ceil(duration_in_hours) - hours_passed) * per_hour_fee

        return total_fee + charges_past_twelve


class AirportFeeModel(FeeModel):
    def calculate_fees(self, vehicle_type: VehicleType, duration_in_hours: float) -> int:
        if vehicle_type == VehicleType.MOTORCYCLE_SCOOTER:
            fee_intervals = [(0, 1, 0), (1, 8, 40), (8, 24, 60)]
            per_day_fee = 80
        elif vehicle_type == VehicleType.CAR_SUV:
            fee_intervals = [(0, 12, 60), (12, 24, 80)]
            per_day_fee = 100
        else:
            raise ValueError("Unsupported vehicle type for AirportFeeModel")

        if duration_in_hours < 24:
            for start, end, fee in fee_intervals:
                if start <= duration_in_hours < end:
                    return fee

        total_days = math.ceil(duration_in_hours / 24)
        return total_days * per_day_fee
