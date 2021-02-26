from garage.parking_level import ParkingLevel
from garage.vehicle import Vehicle
from garage.vehicle_type import VehicleType
from garage.permit import Permit
from collections import deque


class Garage:
    def __init__(self, levels: list = None):
        self.levels = levels or []

    def add_vehicles(self, vehicles: list = None) -> list:
        # Load parking spaces into queues by type
        disability_spaces = deque()
        premium_spaces = deque()
        compact_spaces = deque()
        general_spaces = deque()
        for level in self.levels:
            for space in level.spaces:
                # Disability Permit
                if space.required_permit == Permit.DISABILITY:
                    disability_spaces.append(space)
                # Premium Permit
                elif space.required_permit == Permit.PREMIUM:
                    premium_spaces.append(space)
                # Compact 
                elif space.compact:
                    compact_spaces.append(space)
                # General
                else:
                    general_spaces.append(space)

        # Load vehicles into queues by type
        priority_general_parking = deque()
        priority_premium_parking = deque()
        compact_parking = deque()
        premium_parking = deque()
        general_parking = deque()

        rejected_vehicles = vehicles.copy()

        for vehicle in vehicles:

            # Disability and Premium Permit
            dual = (vehicle.permit == (Permit.DISABILITY.value | Permit.PREMIUM.value))
            if dual:
                if disability_spaces:
                    # Place vehicle into first available disability space
                    disability_spaces.popleft().vehicle = vehicle
                    rejected_vehicles.remove(vehicle)
                    continue
                elif premium_spaces:
                    # Add vehicle to priority premium queue
                    priority_premium_parking.append(vehicle)
                    continue
                elif (vehicle.vehicle_type == VehicleType.Compact) and compact_spaces:
                    # Place vehicle in first available compact space
                    compact_spaces.popleft().vehicle = vehicle
                    rejected_vehicles.remove(vehicle)
                    continue
                else:
                    # Add vehicle to priority general queue
                    priority_general_parking.append(vehicle)

            # Disability Permit
            if vehicle.permit == Permit.DISABILITY:
                if disability_spaces:
                    # Place vehicle in first available disability space
                    disability_spaces.popleft().vehicle = vehicle
                    rejected_vehicles.remove(vehicle)
                    continue
                elif general_spaces:
                    # Place vehicle in first available general space
                    general_parking.append(vehicle)
                    continue
            
            # Premium Permit
            if vehicle.permit == Permit.PREMIUM:
                if premium_spaces:
                    # Add vehicle to premium parking queue
                    premium_parking.append(vehicle)

                if general_spaces:
                    # Add vehicle to premium general queue
                    priority_general_parking.append(vehicle)

            # Compact
            if (vehicle.vehicle_type == VehicleType.Compact):
                if compact_spaces:
                    # Add vehicle to compact queue
                    compact_parking.append(vehicle)
                if general_spaces:
                    # Add vehicle to general queue
                    general_parking.append(vehicle)
                continue
            # Standard Vehicle
            if general_spaces and (vehicle.permit != Permit.PREMIUM):
                # Add vehicle to general queue
                general_parking.append(vehicle)

        # Prioritize dual disability and premium permit vehicles
        premium_parking = priority_premium_parking + premium_parking
        while premium_parking and premium_spaces:
            # Place vehicles in first available premium spaces
            v = premium_parking.popleft()
            premium_spaces.popleft().vehicle = v
            rejected_vehicles.remove(v)

            # Remove from any other queues
            try:
                priority_general_parking.remove(v)
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
            # Place vehicles in first available compact spaces
            v = compact_parking.popleft()
            compact_spaces.popleft().vehicle = v
            rejected_vehicles.remove(v)

            # Remove from any other queues
            try:
                priority_general_parking.remove(v)
            except ValueError:
                pass
            try:
                general_parking.remove(v)
            except ValueError:
                pass

        # Prioritize premium permit vehicles in general parking
        general_parking = priority_general_parking + general_parking
        while general_parking and general_spaces:
            # Place vehicles in first available general space
            v = general_parking.popleft()
            general_spaces.popleft().vehicle = v
            rejected_vehicles.remove(v)

        return rejected_vehicles
