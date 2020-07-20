"""
Following the pony docs and tutorial
It uses Python 2.x print statements
"""
from typing import Callable

from pony import orm


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

    space: Callable[[], None] = lambda: print("\n...\n")
    space()

    with orm.db_session():
        p1 = Person(name="John", age=20)
        p2 = Person(name="Mary", age=22)
        p3 = Person(name="Bob", age=30)
        c1 = Car(make="Toyota", model="Prius", owner=p2)
        c2 = Car(make="Ford", model="Explorer", owner=p3)

        db.commit()

    space()

    with orm.db_session():
        query = orm.select(p for p in Person if p.age > 21)

    space()

    with orm.db_session():
        try:
            for p in query.order_by(Person.name):
                orm.show(p)
        except AttributeError as err:
            print(
                f"Can't use orm.show() on arbitrary objects, and the error messages are obtuse:\n{err}"
            )
        query.order_by(Person.name).show()

    space()

    with orm.db_session():
        # Why does show() not return a string? Why does it print?
        # Why don't the objects all have __repr__ methods that have
        # similar information as show()
        Car.select().show()

    space()

    with orm.db_session():
        try:
            Person.select(p for p in Person).show()
        except TypeError as err:
            print(
                f"different select()s in different places have same semantic meaning, but different parameter types:\n{err}"
            )

    space()

    with orm.db_session():
        Person.select(lambda x: x.id + 1).show()
        # Did not do what I expected
        # Don't know what I expected,
        # but not that

    space()

    with orm.db_session():
        # This works
        orm.select(c.id + 1 for c in Car).show()

        # And this
        orm.select(str(c.id) + "1" for c in Car).show()

        try:
            orm.select(str(lambda: c) for c in Car).show()
        except NotImplementedError as err:
            print(
                f"Complex expressions should probably be iterated over though:\n{err}"
            )

    space()

    # Better to iterate over it; e.g.
    with orm.db_session():
        query = orm.select(c for c in Car)

        print(*(lambda: item for item in query), sep=", ")

    space()

    with orm.db_session():
        # This is fine
        Car.select()[:]

        try:
            print(Car.select()[1].owner)
        except TypeError as err:
            print(f"This doesn't work:\n{err}")

        # This does work, though
        print(Car.select()[:][1].owner)

    space()

    with orm.db_session():
        # The cache is per-session, not shared
        print(f"Car 1's owner: {Car[1].owner}")

    space()

    with orm.db_session():
        mary = Person.select(lambda x: x.name == "Mary")[:][0]

        try:
            mary.age += 0.0
        except TypeError as err:
            print(f"This is a runtime type error that mypy can't catch:\n{err}")

        orm.commit()

    def broken() -> None:
        """
        This is on the last page of the Connecting to the Database page,
        and I really have no idea where options is defined
        I'd also love to see a quick and general example on checking Database object statistics
        """

        @db.on_connect(provider="sqlite")
        def sqlite_case_sensitivity(db, connection):
            cursor = connection.cursor()
            cursor.execute("PRAGMA case_sensitive_like = OFF")

        db.bind(**options)
        db.generate_mapping(create_tables=True)

    # "The composite index can include a discriminator attribute used for inheritance"
    # Example?


if __name__ == "__main__":
    main()
