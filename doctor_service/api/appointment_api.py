# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

from flask import Blueprint, jsonify, request
from version import VERSION
from datetime import datetime

from ..extensions import db
from ..models import Appointment, Doctor, Location

appointment_api = Blueprint("appointment_api", __name__, url_prefix="/appointment")

DATETIME_FORMAT = "%m/%d/%Y %H:%M"


@appointment_api.route("/", methods=["POST"])
def schedule_appointment():
    data = request.json
    
    # Format datetime for database
    data["startTime"] = datetime.strptime(data.get("startTime"), DATETIME_FORMAT)
    data["endTime"] = datetime.strptime(data.get("endTime"), DATETIME_FORMAT)

    # Make sure the doctor exists and is active
    doctor = Doctor.query.get_or_404(data.get("doctorId"))
    if not doctor.isActive:
        return "%s is not currently accepting appointments" % doctor.name, 403
    location = Location.query.get_or_404(data.get("locationId"))
   
    # Make sure doctor is available at this time
    if does_time_conflict_exist(doctor.id, data.get("startTime"), data.get("endTime")):
        return "%s is unavailable at this time" % doctor.name, 403

    # Make sure doctor is available in this location
    if not location in doctor.locations:
        return "%s is not available in %s" % (doctor.name, location.address), 403

    # Schedule the appointment
    instance = Appointment(doctor.id, location.id, data.get("startTime"), data.get("endTime"))
    db.session.add(instance)
    db.session.commit()
    return jsonify(instance), 200

@appointment_api.route("/<appointment_id>", methods=["DELETE"])
def delete_appointment(appointment_id):
    instance = Appointment.query.get_or_404(appointment_id)
    instance.isCanceled = True
    db.session.commit()
    return "success", 200

@appointment_api.route("/<doctor_id>", methods=["GET"])
def get_appointments(doctor_id):
    appointments = Appointment.query.filter_by(doctorId=doctor_id).all()
    return jsonify({"appointments": [appointment.as_dict for appointment in appointments]}), 200

def does_time_conflict_exist(doctorId, requestStartTime, requestEndTime):
    # https://nedbatchelder.com/blog/201310/range_overlap_in_two_compares.html
    return Appointment.query.filter_by(doctorId=doctorId, isCanceled=False).filter(
                requestEndTime >= Appointment.startTime, 
                Appointment.endTime >= requestStartTime
    ).count() > 0 
