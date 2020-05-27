"""
Following the pony docs and tutorial
"""
from pony import orm
from typing import Callable

def main() -> None:
    db = orm.Database()

    class Person(db.Entity):
        name = orm.Required(str)
        age = orm.Required(int)
        cars = orm.Set("Car")

    class Car(db.Entity):
        make = orm.Required(str)
        model = orm.Required(str)
        owner = orm.Required(Person)

    orm.show(Person)

    db.bind(provider="sqlite", filename=":memory:")

    orm.set_sql_debug(True)

    db.generate_mapping(create_tables=True)

    space: Callable[[], None] = lambda:print("\n...\n")
    space()

    with orm.db_session():
        p1 = Person(name="John", age=20)
        p2 = Person(name="Mary", age=22)
        p3 = Person(name="Bob", age=30)
        c1 = Car(make="Toyota", model="Prius", owner=p2)
        c2 = Car(make="Ford", model="Explorer", owner=p3)

        db.commit()

    with orm.db_session():
        query = orm.select(p for p in Person if p.age > 21)
        breakpoint()
        print(*query)

if __name__ == "__main__":
    main()
