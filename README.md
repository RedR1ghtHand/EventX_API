# EventX API

EventX API is a Django REST Framework application for managing events. It includes features such as user authentication, event registration, and event filtering. The application is containerized using Docker for easy setup and deployment.

## Features

- User Registration and Authentication
- Event Management (Create, Read, Update, Delete events)
- Event Registration by users
- Event filtering and search
- API secured using Token-based Authentication
- generated API documentation via drf-yasg [here](#api)

## Requirements

- Python 3.11+
- Poetry for dependency management
- Docker (if running via containers)

## Getting Started

### 1. Clone the Repository

`git clone https://github.com/RedR1ghtHand/EventX_API.git`

### 2. No Docker:
 1. Have the following prerequisites: python 3.11+, poetry(`pip install poetry`)
 2. `cd event_management`
 3. `poetry install`
 4. `poetry shell`
 5. `python manage.py migrate`
 6. (optional) `python manage.py createsuperuser`
 7. `python manage.py runserver`
 8. (tests)`pytest`

 - The application will be available at http://127.0.0.1:8000/.

### 3. Docker:
- Build and Run the Docker Container:
  1. `docker build -t eventx-api .`
  2. `docker run -p 8000:8000 eventx-api`

- Running with Docker Compose:
  1. `docker-compose up --build`
  2. `docker exec -it <container_name> bash`
  3. `python manage.py migrate`
  4. `python manage.py createsuperuser`
  5. (tests)`docker exec -it <container_name> pytest`

- The application will be available at http://localhost:8000/.

### API
- documentation will be available at http://localhost:8000/swagger/ | http://localhost:8000/redoc/