from typing import Optional
from abc import ABC, abstractmethod
from ex1.capabilities import HealCapability, TransformCapability


class Creature(ABC):
    name: str = "Unknown"
    type: str = "Creature"

    @abstractmethod
    def attack(self) -> str:
        pass

    def describe(self) -> str:
        return f"{self.name} is a {self.type} type Creature"


class Sproutling(Creature, HealCapability):
    name: str = "Sproutling"
    type: str = "Grass"

    def attack(self) -> str:
        return f"{self.name} uses Vine Whip!"

    def heal(self, target: Optional[str] = "itself") -> str:
        return f"{self.name} heals {target} for a small amount"


class Bloomelle(Creature, HealCapability):
    name: str = "Bloomelle"
    type: str = "Grass/Fairy"

    def attack(self) -> str:
        return f"{self.name} uses Petal Dance!"

    def heal(self, target: Optional[str] = "itself and others") -> str:
        return f"{self.name} heals {target} for a large amount"


class Shiftling(Creature, TransformCapability):
    name: str = "Shiftling"
    type: str = "Normal"
    _is_transformed: bool = False

    def attack(self) -> str:
        if self._is_transformed:
            return f"{self.name} performs a boosted strike!"
        return f"{self.name} attacks normally."

    def transform(self) -> str:
        self._is_transformed = True
        return f"{self.name} shifts into a sharper form!"

    def revert(self) -> str:
        self._is_transformed = False
        return f"{self.name} returns to normal."


class Morphagon(Creature, TransformCapability):
    name: str = "Morphagon"
    type: str = "Normal/Dragon"
    _is_transformed: bool = False

    def attack(self) -> str:
        if self._is_transformed:
            return f"{self.name} unleashes a devastating morph strike!"
        return f"{self.name} attacks normally."

    def transform(self) -> str:
        self._is_transformed = True
        return f"{self.name} morphs into a dragonic battle form!"

    def revert(self) -> str:
        self._is_transformed = False
        return f"{self.name} stabilizes its form."
