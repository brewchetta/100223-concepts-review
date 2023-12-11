#!/usr/bin/env python3

from app import app
from models import db, Gift
from faker import Faker
from random import randint

faker = Faker()

if __name__ == '__main__':
    with app.app_context():
        print("Seeding database...")

        Gift.query.delete()

        for _ in range(0,6):
            new_gift = Gift(name=faker.commerce.product(), price=faker.commerce.price() )
            db.session.add(new_gift)

        db.session.commit()

        print("Seeding complete!")
