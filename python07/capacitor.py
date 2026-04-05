#!/usr/bin/env python3

from ex1 import HealingCreatureFactory, TransformCreatureFactory


def test_healing_creature(factory):
    """Test healing creature factory"""
    base = factory.create_base()
    evolved = factory.create_evolved()

    print(f"{base.describe()}")
    print(f"{base.attack()}")
    if hasattr(base, 'heal'):
        print(base.heal())

    print("evolved:")
    print(f"{evolved.describe()}")
    print(f"{evolved.attack()}")
    if hasattr(evolved, 'heal'):
        print(evolved.heal())


def test_transform_creature(factory):
    """Test transform creature factory"""
    base = factory.create_base()
    evolved = factory.create_evolved()

    print(f"{base.describe()}")
    print(f"{base.attack()}")
    if hasattr(base, 'transform'):
        print(base.transform())
        print(f"{base.attack()}")
        print(base.revert())

    print("evolved:")
    print(f"{evolved.describe()}")
    print(f"{evolved.attack()}")
    if hasattr(evolved, 'transform'):
        print(evolved.transform())
        print(f"{evolved.attack()}")
        print(evolved.revert())


if __name__ == "__main__":
    print("Testing Creature with healing capability")
    print("base:")
    healing_factory = HealingCreatureFactory()
    test_healing_creature(healing_factory)

    print("\nTesting Creature with transform capability")
    print("base:")
    transform_factory = TransformCreatureFactory()
    test_transform_creature(transform_factory)
