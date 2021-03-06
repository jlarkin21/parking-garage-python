from typing import List

from garage.parking_space import ParkingSpace


class ParkingLevel:
    spaces: List[ParkingSpace]

    def __init__(
        self,
        spaces: List[ParkingSpace] = None,
    ):
        self.spaces = spaces or []
