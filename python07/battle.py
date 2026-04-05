#! /usr/bin/env python3
from typing import Any
from ex0 import CreatureFactory, Creature, FlameFactory, AquaFactory


def process_factory(creature_factory: Any):
    if not isinstance(creature_factory, CreatureFactory):
        raise TypeError("Invalid factory type")
    base_creature = creature_factory.create_base()
    evolved_creature = creature_factory.create_evolved()
    print(base_creature.describe())
    print(base_creature.attack())
    print(evolved_creature.describe())
    print(evolved_creature.attack())


def battle(creature1: Creature, creature2: Creature):
    print(f"{creature1.describe()}\n vs\n{creature2.describe()}")
    print(" fight!")
    print(creature1.attack())
    print(creature2.attack())


if __name__ == "__main__":

    flame_factory = FlameFactory()
    aqua_factory = AquaFactory()
    print("Testing factory")
    process_factory(flame_factory)
    print("\nTesting factory")
    process_factory(aqua_factory)
    print("\nTesting battle")
    flame_creature = flame_factory.create_base()
    aqua_creature = aqua_factory.create_base()
    battle(flame_creature, aqua_creature)
