# Event Booking System (EBS) Project

The Event Booking System (EBS) is a Dockerized Django-based web application that allows users to book tickets for events and manage event-related operations. This project includes features such as booking management, event creation, and ticket management.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Running Tests](#running-tests)
- [API Documentation](#api-documentation)
- [Superuser Access](#superuser-access)

## Features

- User authentication.
- Booking creation and management.
- Event creation and management.
- Ticket creation and management.
- Role-based access control for customers and event organizers.
- Asynchronous email notifications for booking confirmation and event updates using Celery.
- RESTful API for interacting with the system.
- Dockerized deployment environment.

## Requirements

- Docker
- Docker Compose

## Installation

1. Clone this repository to your local machine.
2. Navigate to the project directory.

## Usage

1. Make sure Docker and Docker Compose are installed on your machine.
2. Build and start the Docker containers: `docker-compose up --build -d`.

Visit `http://localhost:8000` in your web browser to access the Dockerized application.

## Running Tests

To ensure the quality and reliability of the Event Booking System (EBS) project, test cases are included to test all the business logic for ticket booking process. Follow the steps below to run the test cases using pytest:

1. Enable your virtual environment and install all the dependencies

2. Navigate to project root directory.

3. To run all the test cases run `pytest` in the project root directory.

## API Documentation

You can access the API documentation using the following Swagger endpoints:

- JSON format: `/swagger.json`
- YAML format: `/swagger.yaml`
- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`

Visit these endpoints in your web browser to view and interact with the API documentation.


## Superuser Access

You can access the admin panel using the following superuser credentials:
- Username: admin
- Password: 1234

---