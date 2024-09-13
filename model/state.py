from dataclasses import dataclass


@dataclass
class State:
    id: str
    Name: str
    Capital: str
    Lat: float
    Lng: float
    Area: float
    Population: int
    Neighbors: []
    Nall: int
    Nshape: int

    def __str__(self):
        return self.Name

    def __hash__(self):
        return hash(self.id)