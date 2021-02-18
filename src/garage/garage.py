from garage.parking_level import ParkingLevel
from garage.vehicle import Vehicle
from garage.vehicle_type import VehicleType
from garage.permit import Permit
from collections import deque


class Garage:
    def __init__(self, levels: list = None):
        self.levels = levels or []

    def add_vehicles(self, vehicles: list = None) -> list:
        handicap_spaces = deque()
        premium_spaces = deque()
        compact_spaces = deque()
        regular_spaces = deque()
        for level in self.levels:
            for space in level.spaces:
                if space.required_permit == Permit.DISABILITY:
                    handicap_spaces.append(space)
                elif space.required_permit == Permit.PREMIUM:
                    premium_spaces.append(space)
                elif space.compact:
                    compact_spaces.append(space)
                else:
                    regular_spaces.append(space)

        rejected_vehicles = list()
        sv = sorted(vehicles, key=lambda x: x.permit.value, reverse=True)
        for vehicle in sv:
            if vehicle.permit == (Permit.DISABILITY.value | Permit.PREMIUM.value):
                if handicap_spaces:
                    handicap_spaces.popleft().vehicle = vehicle
                    continue
                elif premium_spaces:
                    premium_spaces.popleft().vehicle = vehicle
                    continue
                elif vehicle.vehicle_type == VehicleType.Compact and compact_spaces:
                    compact_spaces.popleft().vehicle = vehicle
                    continue
                elif regular_spaces:
                    regular_spaces.popleft().vehicle = vehicle
                    continue

            if vehicle.permit == Permit.DISABILITY:
                if handicap_spaces:
                    handicap_spaces.popleft().vehicle = vehicle
                    continue
                elif compact_spaces and vehicle.vehicle_type == VehicleType.Compact:
                    compact_spaces.popleft().vehicle = vehicle
                    continue
                elif regular_spaces:
                    regular_spaces.popleft().vehicle = vehicle
                    continue

            if vehicle.permit == Permit.PREMIUM:
                if premium_spaces:
                    premium_spaces.popleft().vehicle = vehicle
                    continue
                elif compact_spaces and vehicle.vehicle_type == VehicleType.Compact:
                    compact_spaces.popleft().vehicle = vehicle
                    continue
                elif regular_spaces:
                    regular_spaces.popleft().vehicle = vehicle
                    continue

            if vehicle.vehicle_type == VehicleType.Compact:
                if compact_spaces:
                    compact_spaces.popleft().vehicle = vehicle
                    continue
                elif regular_spaces:
                    regular_spaces.popleft().vehicle = vehicle
                    continue

            if regular_spaces:
                regular_spaces.popleft().vehicle = vehicle
                continue

            rejected_vehicles.append(vehicle)


        return list(set(rejected_vehicles).difference(vehicles))


