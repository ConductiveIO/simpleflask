# Design decisions #

:: Technologies
  - SQLAlchemy
    - Lightweight, quick to setup database. 
  - autoenv
  


:: Database Architecture

Tables:(see doctor_service_data_architecture.jpg)
  - doctor:
    - Set of atomic data representing an Doctor in our system
  - appointment:
    - Transactional data representing a scheduled (past or future) appointment.
  - location:
    - Atomic dataset representing locations related to the doctors in our system.
  - doctorLocationAssociation:
    - Join table mapping doctors to the locations where they are available for apointment.

:: Endpoint List

/doctor/
  - GET /<id>
    - If no ID provided, return list of all doctors. If ID provided, only provide details for that doctor.

  - POST /
    - Create a doctor with the given data.
    - Params: name, list of locations.

  - PATCH /<id>
    - Update a doctor's information, including name, location affiliations, and isActive status. 

  - DELETE /<id>
    - Sets a doctor's entry to inactive. Rather than delete the doctor and lose valuable analytics insights, we mark the doctor as inactive, preventing appointments to be scheduled with them (but not canceling their standing appointments). In future iterations, should add change tracking table to track when doctors statuses change. 


/appointment/
  - GET /<doctorId>
    - Returns a list of all appointments for this doctor.

  - POST /
    - Attempts to create an appointment for a given doctor at a given location and time.
      - Returns an error and fails to create appointment if doctor is not in our system, doctor is not affiliated with given location, doctor is unavailable at this time.
  - DELETE /<id>
    - Sets appointment status to canceled. 

# Extra question #
Pick one extra question from the readme and write a few sentences on how your would alter your design to accommodate it.