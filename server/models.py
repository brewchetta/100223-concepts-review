from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Gift(db.Model, SerializerMixin):

    __tablename__ = "gifts_table"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("receivers_table.id"))
    giver_id = db.Column(db.Integer, db.ForeignKey("givers_table.id"))

    def pretty_print(self):
        return f"{self.name} costing ${self.price}"

    receiver = db.relationship("Receiver", back_populates="gifts")

    giver = db.relationship("Giver", back_populates="gifts")

    serialize_rules = ("-receiver.gifts", "-receiver_id", "pretty_print", "-giver.gifts",)


class Receiver(db.Model, SerializerMixin):

    __tablename__ = "receivers_table"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    @validates("name")
    def validate_name(self, key, val):
        if 3 <= len(val) <= 40:
            return val
        else:
            raise ValueError(f"{key} must be between 3 and 40 characters long")

    gifts = db.relationship("Gift", back_populates="receiver", cascade="all, delete-orphan")
    givers = association_proxy("gifts", "giver")

    serialize_rules = ("-gifts.receiver",)


class Giver(db.Model, SerializerMixin):

    __tablename__ = "givers_table"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    gifts = db.relationship("Gift", back_populates="giver", cascade="all, delete-orphan")
    receivers = association_proxy("gifts", "receiver")

    serialize_rules = ("-gifts.giver",)