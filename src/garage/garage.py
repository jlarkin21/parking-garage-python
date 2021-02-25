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

        premium_reservation_vehicles = deque()
        special_premium = deque()
        compact_parking = deque()
        premium_parking = deque()
        general_parking = deque()
        rejected_vehicles = vehicles.copy()
        for vehicle in vehicles:
            dual = (vehicle.permit == (Permit.DISABILITY.value | Permit.PREMIUM.value))
            if dual:
                if handicap_spaces:
                    handicap_spaces.popleft().vehicle = vehicle
                    rejected_vehicles.remove(vehicle)
                    continue
                elif premium_spaces:
                    special_premium.append(vehicle)
                    # premium_spaces.popleft().vehicle = vehicle
                    # rejected_vehicles.remove(vehicle)
                    continue
                elif (vehicle.vehicle_type == VehicleType.Compact) and compact_spaces:
                    compact_spaces.popleft().vehicle = vehicle
                    rejected_vehicles.remove(vehicle)
                    continue
                else:
                    premium_reservation_vehicles.append(vehicle)

            if vehicle.permit == Permit.DISABILITY:
                if handicap_spaces:
                    handicap_spaces.popleft().vehicle = vehicle
                    rejected_vehicles.remove(vehicle)
                    continue
                elif regular_spaces:
                    general_parking.append(vehicle)
                    continue

            if vehicle.permit == Permit.PREMIUM:
                if premium_spaces:
                    premium_parking.append(vehicle)

                if regular_spaces:
                    premium_reservation_vehicles.append(vehicle)

            if (vehicle.vehicle_type == VehicleType.Compact):
                if compact_spaces:
                    compact_parking.append(vehicle)
                if regular_spaces:
                    general_parking.append(vehicle)
                continue

            if regular_spaces and (vehicle.permit != Permit.PREMIUM):
                general_parking.append(vehicle)


        premium_parking = special_premium + premium_parking
        while premium_parking and premium_spaces:
            v = premium_parking.popleft()
            premium_spaces.popleft().vehicle = v
            rejected_vehicles.remove(v)
            try:
                premium_reservation_vehicles.remove(v)
            except ValueError:
                pass
            try:
                compact_parking.remove(v)
            except ValueError:
                pass
            try:
                general_parking.remove(v)
            except ValueError:
                pass

        while compact_parking and compact_spaces:
            v = compact_parking.popleft()
            compact_spaces.popleft().vehicle = v
            rejected_vehicles.remove(v)
            try:
                premium_reservation_vehicles.remove(v)
            except ValueError:
                pass
            try:
                general_parking.remove(v)
            except ValueError:
                pass


        general_parking = premium_reservation_vehicles + general_parking
        while general_parking and regular_spaces:
            v = general_parking.popleft()
            regular_spaces.popleft().vehicle = v
            rejected_vehicles.remove(v)

        # dual_permit_vehicles = deque()
        # disability_vehicles = deque()
        # premium_vehicles = deque()
        # compact_vehicles = deque()
        # regular_vehicles = deque()
        # for vehicle in vehicles:
        #     dual = (vehicle.permit == (Permit.DISABILITY.value | Permit.PREMIUM.value))
        #     if dual:
        #         dual_permit_vehicles.append(vehicle)
        #
        #     if vehicle.permit == Permit.DISABILITY:
        #         disability_vehicles.append(vehicle)
        #
        #     if vehicle.permit == Permit.PREMIUM:
        #         premium_vehicles.append(vehicle)
        #
        #     if vehicle.vehicle_type == VehicleType.Compact:
        #         compact_vehicles.append(vehicle)
        #
        #     if vehicle.permit == Permit.NONE and vehicle.vehicle_type != VehicleType.Compact:
        #         regular_vehicles.append(vehicle)
        #
        # for level in self.levels:
        #     for space in level.spaces:
        #         selected_vehicle = Vehicle()
        #
        #         if space.required_permit == Permit.DISABILITY:
        #             if dual_permit_vehicles:
        #                 selected_vehicle = dual_permit_vehicles.popleft()
        #                 space.vehicle = selected_vehicle
        #                 vehicles.remove(selected_vehicle)
        #                 try:
        #                     compact_vehicles.remove(selected_vehicle)
        #                 except ValueError:
        #                     pass
        #
        #             elif disability_vehicles:
        #                 selected_vehicle = disability_vehicles.popleft()
        #                 space.vehicle = selected_vehicle
        #                 vehicles.remove(selected_vehicle)
        #                 try:
        #                     compact_vehicles.remove(selected_vehicle)
        #                 except ValueError:
        #                     pass
        #
        #         elif space.required_permit == Permit.PREMIUM:
        #             if dual_permit_vehicles and premium_vehicles:
        #                 if vehicles.index(dual_permit_vehicles[0]) < vehicles.index(premium_vehicles[0]):
        #                     selected_vehicle = dual_permit_vehicles.popleft()
        #                     space.vehicle = selected_vehicle
        #                     vehicles.remove(selected_vehicle)
        #                     try:
        #                         compact_vehicles.remove(selected_vehicle)
        #                     except ValueError:
        #                         pass
        #                 else:
        #                     selected_vehicle = premium_vehicles.popleft()
        #                     space.vehicle = selected_vehicle
        #                     vehicles.remove(selected_vehicle)
        #                     try:
        #                         compact_vehicles.remove(selected_vehicle)
        #                     except ValueError:
        #                         pass
        #
        #             elif dual_permit_vehicles:
        #                 selected_vehicle = dual_permit_vehicles.popleft()
        #                 space.vehicle = selected_vehicle
        #                 vehicles.remove(selected_vehicle)
        #                 try:
        #                     compact_vehicles.remove(selected_vehicle)
        #                 except ValueError:
        #                     pass
        #
        #             elif premium_vehicles:
        #                 selected_vehicle = premium_vehicles.popleft()
        #                 space.vehicle = selected_vehicle
        #                 vehicles.remove(selected_vehicle)
        #                 try:
        #                     compact_vehicles.remove(selected_vehicle)
        #                 except ValueError:
        #                     pass
        #
        #
        #
        #         elif space.compact:
        #             if compact_vehicles:
        #                 selected_vehicle = compact_vehicles.popleft()
        #                 space.vehicle = selected_vehicle
        #                 vehicles.remove(selected_vehicle)
        #
        #                 try:
        #                     dual_permit_vehicles.remove(selected_vehicle)
        #                 except ValueError:
        #                     pass
        #                 try:
        #                     premium_vehicles.remove(selected_vehicle)
        #                 except ValueError:
        #                     pass
        #                 try:
        #                     disability_vehicles.remove(selected_vehicle)
        #                 except ValueError:
        #                     pass
        #
        #         else:
        #             regular_spaces.append(space)
        #
        # while regular_spaces and vehicles:
        #     regular_spaces.popleft().vehicle = vehicles.pop(0)

        return rejected_vehicles
