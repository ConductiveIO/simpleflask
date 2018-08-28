# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function


from doctor_service.core.tests import BaseTestCase
from doctor_service.extensions import db
from doctor_service.models import Appointment, Doctor, Location, DATETIME_FORMAT
from version import VERSION

from werkzeug.test import EnvironBuilder

import json
from datetime import datetime

class AppointmentApiTestCase(BaseTestCase):
    def setUp(self):
        super(AppointmentApiTestCase, self).setUp()

        # Add locations
        addresses = ["Whoville", "BWH", "MGH"]
        locations = [Location(address) for address in addresses]
        [db.session.add(location) for location in locations]

        # Add doctor
        doctor = Doctor("Seuss", True, locations)
        db.session.add(doctor)
        db.session.commit()

    def test_schedule_appointment_success(self):
        response = self.client.post(
                "/appointment/",
                data=json.dumps(dict(doctorId=1,
                    locationId= 1,
                    startTime="03/07/2019 13:00",
                    endTime="03/07/2019 14:00")),
                content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_schedule_appointment_inactive_doctor_fails(self):
        self.client.delete('/doctor/1')
        response = self.client.post(
            "/appointment/",
            data=json.dumps(dict(doctorId=1,
                locationId= 1,
                startTime="03/07/2019 12:30",
                endTime="03/07/2019 13:30")),
            content_type="application/json")

        self.assertEqual(response.status_code, 403)

    def test_schedule_appointment_overlap_fails(self):
        # First appt
        self.client.post(
            "/appointment/",
            data=json.dumps(dict(doctorId=1,
                locationId= 1,
                startTime="03/07/2019 13:00",
                endTime="03/07/2019 14:00")),
            content_type="application/json")

        # Overlapping appt
        response = self.client.post(
            "/appointment/",
            data=json.dumps(dict(doctorId=1,
                locationId= 1,
                startTime="03/07/2019 12:30",
                endTime="03/07/2019 13:30")),
            content_type="application/json")

        self.assertEqual(response.status_code, 403)
    
    def test_schedule_appointment_invalid_location_fails(self):
        location = Location("Boston Children's")
        db.session.add(location)
        db.session.commit()

        response = self.client.post(
            "/appointment/",
            data=json.dumps(dict(doctorId=1,
                locationId= 4,
                startTime="03/07/2019 12:30",
                endTime="03/07/2019 13:30")),
            content_type="application/json")

        self.assertEqual(response.status_code, 403)

    def test_delete_schedule_succeeds(self):
        appointment = Appointment(
                doctorId=1, 
                locationId=2, 
                startTime=datetime.strptime("03/07/2019 10:00", DATETIME_FORMAT),
                endTime=datetime.strptime("03/07/2019 11:00", DATETIME_FORMAT))
        db.session.add(appointment)
        db.session.commit()

        response = self.client.delete("/appointment/%s" % appointment.id)
        self.assertEqual(response.status_code, 200)

        instance = Appointment.query.filter_by(id=appointment.id).first()
        self.assertTrue(instance.isCanceled)
