# README #

This repository contains the outlines of a web API. Review the problem statement below. When you arrive at Kyruus, you will design and implement a solution which satisfies the design criteria.

### Problem statement ###

We would like to build a simple service for managing doctors and their schedules. 
Requirements:

* For each doctor we would initially like to store the following:
    * id
	* name
	* locations - represented as a collection of address strings
	* schedule - weekly schedule indicating the hours they are available each day of the week
* CRUD operations for doctors
* Ability to book an appointment with a doctor (a tuple of (doctor, location, time)) 
* Ability to cancel an appointment with a doctor
* Ability to get all appointments for a doctor

Expectations/assumptions:

* The API will be internally-facing and used by other applications/services that we trust
* The API will be single-tenant (it only contains data for a single customer)
* A doctor is available at any of his locations for any of his available times
* A doctor can only have one appointment at a time
* A doctor can travel instantaneously between locations
* No UI/front-end is expected   

### Getting started ###

#### Prerequisites

* [Python 2.7](https://www.python.org/downloads/)
* [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
* [git](https://git-scm.com/downloads)
* [flask](http://flask.pocoo.org/)

If you did not receive this question as a zipfile, first [fork the repository](https://confluence.atlassian.com/bitbucket/forking-a-repository-221449527.html).
Then, check out your repository:

    $ git clone git@bitbucket.org:<your_user>/<your_repo>.git

Create a branch for your work

    $ git checkout -b'<your_branch_name>' origin/master
	
When you've unzipped the zipfile or forked the repository, familiarize yourself with the project structure and the code we've provided as a starting point.   
The `example` package shows the syntax of Flask routes.

To install requirements in a virtual environment begin by running

    $ virtualenv doctor_service

Followed by installing requirements:

    $ pip install -r requirements.txt

This is a Flask application which comes with some built-in commands.   
To start your application, run 

    $ python manage.py runserver

To execute unit tests, run

    $ python manage.py test

#### Extra questions ####

Below are a few questions which expand the scope of the service. Please pick one and describe your approach.

* What are some real-world constraints to booking appointments that would add complexity to this API and how would they impact the design.
* How would our design change if this API was opened up to external users?
* What concerns are there with multi-tenant data management and how could we modify the design to increase data security?

#### Suggestions ####

* Start simple 
* Document your assumptions and their impact on the design
* Stub out areas that are not related to core functionality and describe their expected behavior
* You may choose any means of persistence (ex: database, third-party service, etc.) or choose to exclude it (e.g. in-memory only). We recognize that integrating with a persistence layer may be time-consuming and by omitting it, more time can be allocated to service development.
* You may use any third-party libraries you feel are appropriate

### Who do I talk to? ###
* If you have any questions prior to your interview, please reach out to your designated Kyruus recruiting contact and he/she will get back to you as soon as possible.
* If you have any feedback on the interview question after you're done, let us know, we're always looking into improving the interview process. Thanks!
