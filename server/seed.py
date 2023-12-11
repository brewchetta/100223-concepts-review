#!/usr/bin/env python3

from app import app
from models import db, Gift, Receiver, Giver
from faker import Faker
from random import randint, choice

faker = Faker()

if __name__ == '__main__':
    with app.app_context():
        print("Seeding database...")

        Gift.query.delete()
        Receiver.query.delete()
        Giver.query.delete()

        print("Creating gift receivers...")

        receivers_list = []

        for _ in range(0,6):
            new_receiver = Receiver( name=faker.name() )
            receivers_list.append(new_receiver)
            db.session.add(new_receiver)

        db.session.commit()

        print("Creating gift givers...")

        givers_list = []

        for _ in range(0,6):
            new_giver = Giver( name=faker.name() )
            givers_list.append(new_giver)
            db.session.add(new_giver)

        db.session.commit()

        print("Creating gifts...")

        for _ in range(0,30):
            rand_receiver = choice( receivers_list )
            rand_giver = choice( givers_list )
            new_gift = Gift(
                name=faker.address(), 
                price=(randint(1,1000) / 100.0), 
                receiver=rand_receiver,
                giver=rand_giver
            )
            db.session.add(new_gift)

        db.session.commit()

        print("Seeding complete!")
