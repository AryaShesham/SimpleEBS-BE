# Event Booking System (EBS) Project

The Event Booking System (EBS) is a Dockerized Django-based web application that allows users to book tickets for events and manage event-related operations. This project includes features such as booking management, event creation, and ticket management.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
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

## Superuser Access

You can access the admin panel using the following superuser credentials:
- Username: admin
- Password: 1234

---