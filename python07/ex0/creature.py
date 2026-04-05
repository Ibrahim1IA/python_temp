from abc import ABC, abstractmethod


class Creature(ABC):
    name: str = "Unknown"
    type: str = "Creature"

    @abstractmethod
    def attack(self) -> str:
        pass

    def describe(self) -> str:
        return f"{self.name} is a {self.type} type Creature"


class Flameling(Creature):
    name: str = "Flameling"
    type: str = "Fire"

    def attack(self):
        return f"{self.name} uses Ember!"


class Aquabub(Creature):
    name: str = "Aquabub"
    type: str = "Water"

    def attack(self):
        return f"{self.name} uses water gun!"


class Torragon(Creature):
    name: str = "Torragon"
    type: str = "Water"

    def attack(self):
        return f"{self.name} uses Hydro Pump!"


class Pyrodon(Creature):
    name: str = "Pyrodon"
    type: str = "Fire/Flying"

    def attack(self):
        return f"{self.name} uses Flamethrower!"
