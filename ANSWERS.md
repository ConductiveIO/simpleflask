# Additional Setup:
- In addition to creating a virtual environment and pip installing all the necessary packages as outlined in the requirements.txt file, you will need to set up the database as follows.
1. Ensure you have postgresql installed
2. Create the `doctor_service` database
3. Run all migrations with `python manage.py db migrate && python manage.py db upgrade`
4. Source the `.env` file (in root level) to load the database URL into environment variables.

# Design decisions #

:: Technologies
  - Postgresql / SQLAlchemy
    - Lightweight, quick to setup database.
    - For this applications, I chose to use the ORM. I cannot state how difficult of a decision that was. Knowing that this application would need to be installed by another user, and would never be meant to scale, I moved forward as it was the fastest way to created self-documenting code and the easiest way to replicate the database on another machine with minimal need for developer support. To read further about my feelings on ORM's, see this post: `http://robbygrodin.com/2017/04/18/wayfair-blog-post-orm-bankruptcy/`
  - autoenv
    - You can use this to automatically source the .env file every time you ssh into the app directory, otherwise you'll need to do this on your own.
  - 

:: Database Architecture

Tables:(**NOTE**: see doctor_service_data_architecture.png)
  - doctor:
    - Set of atomic data representing an Doctor in our system
  - appointment:
    - Transactional data representing a scheduled (past or future) appointment.
  - location:
    - Atomic dataset representing locations related to the doctors in our system.
  - doctorLocationAssociation:
    - Join table mapping doctors to the locations where they are available for apointment.

:: Endpoint List

**Design Note**: Rather than create CRUD endpoints for every resource, I opted to design an API that would optimize for frontend performance by requiring as few requests as possible to perform an operation. This is why a doctor can be added without having to first create the location records. This can be further optimized by allowing endpoints to reference resources by string attributes (i.e. location.address, doctor.name) rather than the primary key ID, however I felt that was out of
scope and would be better just mentioned here.

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
    - Sets appointment status to canceled. Does not remove from database for analytics purposes. 


# Tests #

I've provided a handful of tests for the Appointments API. Definitely didn't catch all edge cases or test for database data integrity. Didn't provide tests for the Doctor API because 1. it's a simple set of CRUD endpoints, therefore lower priority than the more business-logic heavy Appointments API, and 2. I ran out of the amount of time I decided to allocate to this exercise.

# Extra question #
Some real world constraints that impact appointment scheduling:

**Doctor's need to travel from point A to point B.** 
I had originally misread the prompt and starting looking at Google API's to calculate travel time. It's not the most straightforward integration, and can be costly. One design would be a graph database where we can pre-fetch distance/travel-time data and store that on our own servers, reducing the number of calls we would need to make to an external service. The downside to that approach is that it doesn't take into account temporally sensitive travel times.

Another approach would be building an integration with a Google Maps API or Waze client, which would provide traffic predictions. One interesting problem would be to automatically detect if an abnormal travel time is expected and pre-cancel/reschedule an appointment, increasing the odds that the patient will be seen in a timely manner.

**Some doctors share their workspaces.**
This current implementation is sensitive to not over-booking doctors, but what about the space? A more intelligent solution (that wouldn't result in patients being seen in the waiting room) would have a more fleshed out dataset modeling the physical constraints of the office spaces they work in, such as the number of rooms in a given clinic. When scheduling an appointment, we can assign the appointment to a given room in a given location, thus making sure that we don't overbook
spaces.

**Not all appointments are equal.**
Deeper knowledge about the type of appointment would help us make sure the patient is seeing the right doctor with the right specialty. It would also help make sure the doctor can expect to have the equipment they need at the location the appointment is being scheduled at. Adding information about specialties to doctors, a mapping of those specialties to special equipment that may be needed, and logging information about the equipment available at each location would provide
enough data for a more intelligent location scheduling algorithm.

