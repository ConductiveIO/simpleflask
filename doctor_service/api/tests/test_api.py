# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function


from doctor_service.core.tests import BaseTestCase
from doctor_service.extensions import db
from doctor_service.models import Doctor
from version import VERSION


class AppointmentApiTestCase(BaseTestCase):
    def setUp(self):
        super(AppointmentApiTestCase, self).setUp()
        doctor = Doctor('Seuss', True, ['Whoville', 'BWH', 'MGH'])
        db.session.add(doctor)
        db.session.commit()

    def test_schedule_appointment_success(self):
        response = self.client.get('/doctor/1/')
        import pdb; pdb.set_trace()
        
