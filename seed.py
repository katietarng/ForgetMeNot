"""Seed database with static ingredient measurements that can convert weight to volume."""

from model import *
from server import app


def load_measurements():
    """Load measurements from seed file into database."""

    seed = open("data/seed_data.txt")

    for row in seed:
        row = row.rstrip()
        name, volume, vol_unit, ounce, gram = row.split("|")

        if ounce == "":
            ounce = None

        ing_measurement = IngMeasurement(name=name,
                                         volume=volume,
                                         vol_unit=vol_unit,
                                         ounce=ounce,
                                         gram=gram
                                         )

        db.session.add(ing_measurement)

    db.session.commit()

    seed.close()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_measurements()
