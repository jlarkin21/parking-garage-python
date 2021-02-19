from garage.parking_level import ParkingLevel
from garage.vehicle import Vehicle
from garage.vehicle_type import VehicleType
from garage.permit import Permit
from collections import deque


class Garage:
    def __init__(self, levels: list = None):
        self.levels = levels or []

    def add_vehicles(self, vehicle_queue: list = None) -> list:
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
        vehicles_sorted_by_permit = sorted(vehicle_queue, key=lambda x: x.permit.value, reverse=True)

        while vehicle_queue:
            vehicle = vehicle_queue.pop()
            premium_reservation_vehicles = list()
            general_parking = list()

            dual = (vehicle.permit == (Permit.DISABILITY.value | Permit.PREMIUM.value))
            if not (handicap_spaces or premium_spaces or compact_spaces) and regular_spaces and vehicle.permit != Permit.PREMIUM and vehicle.permit != dual:
                general_parking.append(vehicle)
                continue

            if vehicle.permit == dual or Permit.DISABILITY and handicap_spaces:
                handicap_spaces.popleft().vehicle = vehicle
                continue

            if vehicle.permit == dual or Permit.PREMIUM:
                if premium_spaces:
                    premium_spaces.popleft().vehicle = vehicle
                    continue
                elif regular_spaces:
                    premium_reservation_vehicles.append(vehicle)
                    continue

            if vehicle.vehicle_type == VehicleType.Compact and compact_spaces:
                    compact_spaces.popleft().vehicle = vehicle
                    vehicle_queue.remove(vehicle)
                    continue

            rejected_vehicles.append(vehicle)


        premium_reservation_vehicles.append(general_parking)


        return vehicles


