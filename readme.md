# Inventory Management System

## Overview

This Inventory Management System is a backend API that allows businesses to manage their stock of products efficiently. The system supports CRUD (Create, Read, Update, Delete) operations on inventory items. It leverages FastAPI for the API framework, PostgreSQL or MySQL for the database, Redis for caching, and includes unit tests to ensure functionality. Proper error handling is implemented with appropriate error codes, and logging is integrated for debugging and monitoring.

## Features

- **Create**: Add new items to the inventory.
- **Read**: Retrieve details of items from the inventory, with caching for frequently accessed items using Redis.
- **Update**: Modify details of existing items in the inventory.
- **Delete**: Remove items from the inventory.
- **Error Handling**: Provides meaningful error messages and appropriate HTTP status codes.
- **Logging**: Integrated logging for monitoring and debugging.

## Technologies Used

- **FastAPI**: API framework for building the backend.
- **PostgreSQL/MySQL**: Relational database for storing inventory data.
- **Redis**: In-memory data store used for caching.
- **SQLAlchemy**: ORM for database interactions.
- **Pytest**: Framework for unit testing.

## Prerequisites

- Docker and Docker Compose
- Python 3.8+
- PostgreSQL or MySQL
- Redis

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/kartikpatil2200/inventory-management-system.git
cd inventory-management-system
```

### Setup Environment Variables

Create a `.env` file and add the following variables:

```dotenv
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
POSTGRES_SERVER=postgres
POSTGRES_PORT=5432
POSTGRES_DB=mydatabase
REDIS_URL=redis://localhost:6379/0
Setup Environment Variables
Create a .env file and add the following variables:
```

### Setup Environment Variables

Update the `DockerCompose\docker-compose.yml` file if necessary and start the services:

```docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:latest
    environment:
      POSTGRES_DB: mydatabase
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:latest
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### Start the services:

open up new terminal and run below command to start the mysql/postgres and redis services:

```bash
docker-compose up -d
```

### Create Virtual Environment:

Create a virtual environment to isolate your project dependencies in new terminal:

```bash
python -m venv venv
```

 - Activate the virtual environment:
   - On Windows:
     ```
      venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
      source venv/bin/activate
     ```

### Install Dependencies
Install Python dependencies using pip:

```bash
pip install -r requirements.txt
```

### Run the Application
Start the FastAPI application in new terminal:

```bash
uvicorn main:app --reload
```

### Running Tests
Run the tests using pytest in new terminal:

```bash
pytest
```

### API Endpoints
#### Create Item
 - URL: /items/
 - Method: POST
 - Request Body:
    ```
    {
        "itemname": "pen",
        "itemdesc": "blue pen"
    }
    ```
 - Response:

   - 201 Created:
    ```
    {
        "item_name": "pen",
        "item_desc": "blue pen"
    }
    ```
   - 400 Bad Request:
    ```
    {
        "error": "Item already exists."
    }
    ```
   
#### Get Item
 - URL: /items/{item_id}
 - Method: GET
 - Response:
   - 200 OK:
   ```
    {
        "item_name": "pen",
        "item_desc": "blue pen"
    }
   ```
   - 404 Not Found:
    ```
    {
        "error": "Item not found"
    }
   ```

#### Update Item
 - URL: /items/{item_id}
 - Method: PUT
 - Request Body:
   ```
    {
        "itemname": "marker",
        "itemdesc": "black marker pen"
    }
   ```
 - Response:
   - 200 OK:
   ```
    {
        "item_name": "marker",
        "item_desc": "black marker pen"
    }
   ```
   - 404 Not Found:
    ```
    {
        "error": "Item not found"
    }
   ```

#### Delete Item
 - URL: /items/{item_id}
 - Method: DELETE
 - Response:

   - 200 OK:
   ```
    {
        "message": "Item Deleted Successfully"
    }
   ```
   - 404 Not Found:
    ```
    {
        "error": "Item not found"
    }
    ```

### Logging
Logs are configured to capture request and response details, along with any errors encountered. The log messages provide context for debugging and monitoring.