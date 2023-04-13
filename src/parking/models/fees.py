import math
from abc import ABC, abstractmethod

from parking.models.vehicle import VehicleType


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
            fee_intervals = [(0, 1, 0), (1, 8, 40), (8, 24, 60)]
            per_day_fee = 80
        elif vehicle_type == VehicleType.CAR_SUV:
            fee_intervals = [(0, 12, 60), (12, 24, 80)]
            per_day_fee = 100
        else:
            raise ValueError("Unsupported vehicle type for AirportFeeModel")

        if duration < 24:
            for start, end, fee in fee_intervals:
                if start <= duration < end:
                    return fee

        total_days = math.ceil(duration / 24)
        return total_days * per_day_fee
