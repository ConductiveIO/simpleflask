from dictalchemy import make_class_dictable
from extensions import db
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

import time

DATETIME_FORMAT = "%D %I:%M"

make_class_dictable(db.Model)

doctor_location_association_table = Table(
        "doctorLocationAssociation", 
        db.Model.metadata,
        Column("doctor_id", Integer, ForeignKey("doctor.id")),
        Column("location_id", Integer, ForeignKey("location.id"))
)


class Doctor(db.Model):
    __tablename__ = "doctor"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    isActive = db.Column(db.Boolean())
    locations = relationship(
            "Location",
            secondary=doctor_location_association_table
    )
    appointments = db.relationship("Appointment", backref="doctor", lazy=True)

    def __init__(self, name, isActive, locations):
        self.name = name
        self.isActive = isActive
        self.locations = locations

    @property
    def as_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data["locations"] = [location.as_dict for location in self.locations]
        data["appointments"] = [appointment.as_dict for appointment in self.appointments]
        return data


class Location(db.Model):
    __tablename__ = "location"

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(String(), nullable=False)

    def __init__(self, address):
        self.address = address

    @property
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Appointment(db.Model):
    __tablename__ = "appointment"
    
    id = db.Column(db.Integer, primary_key=True)
    doctorId = db.Column(db.Integer, ForeignKey("doctor.id"), nullable=False)
    locationId = db.Column(db.Integer, ForeignKey("location.id"), nullable=False)
    startTime = db.Column(db.DateTime, nullable=False)
    endTime = db.Column(db.DateTime, nullable=False)
    isCanceled = db.Column(db.Boolean, default=False)

    def __init__(self, doctorId, locationId, startTime, endTime):
        self.doctorId = doctorId
        self.locationId = locationId
        self.startTime = startTime
        self.endTime = endTime

    @property
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
