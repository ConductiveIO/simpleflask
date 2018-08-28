# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

from flask import Blueprint, jsonify, request
from version import VERSION

from ..extensions import db
from ..models import Doctor, Location

doctor_api = Blueprint("doctor_api", __name__, url_prefix="/doctor")


@doctor_api.route("/", methods=["GET"])
def get_all_doctors():
    return jsonify({"doctors": [doctor.as_dict for doctor in db.session.query(Doctor).all()]}), 202

@doctor_api.route("/<doctor_id>", methods=["GET"])
def get_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    return jsonify(doctor.as_dict), 202

@doctor_api.route("/", methods=["POST"])
def create_doctor():
    data = request.json
    locations = ingest_locations(data.get("locations"))
    instance = Doctor(name=data.get("name"), isActive=True, locations=locations)
    db.session.add(instance)
    db.session.commit()
    return jsonify(instance.as_dict), 202

@doctor_api.route("/<doctor_id>", methods=["PATCH"])
def update_doctor(doctor_id):
    instance = Doctor.query.get_or_404(doctor_id)
    data = request.json
    instance.name = data.get("name", instance.name)
    instance.isActive = data.get("isActive", instance.isActive)
    if data.get("locations"):
        locations = ingest_locations(data.get("locations"))
        instance.locations = locations
    db.session.commit()
    return jsonify(instance.as_dict), 202

@doctor_api.route("/<doctor_id>", methods=["DELETE"])
def delete_doctor(doctor_id):
    instance = Doctor.query.get_or_404(doctor_id)
    instance.isActive = False
    db.session.commit()
    return "success", 202

def ingest_locations(addresses):
    locations = []
    for address in addresses:
        entry = db.session.query(Location).filter_by(address=address).first()
        if entry:
            locations.append(entry)
        else:
            location = Location(address)
            db.session.add(location)
            db.session.commit()
            locations.append(location)
    return locations
