# Flock Energy - Urja Meter API

## Overview

This project builds a clean REST API service over the Urja Meter Ops portal.

The original portal is designed for human users to access smart meter information through a web interface. Since the portal does not provide a public API, this service acts as an integration layer that authenticates with the portal, retrieves meter information, and exposes the data through a structured API.

The API provides:

- Meter identification details
- Meter geographical location
- Recent energy consumption data


## Architecture

```
Client Application
        |
        |
        v
    FastAPI Service
        |
        |
        v
    UrjaClient
        |
        |
        v
 Playwright Browser Automation
        |
        |
        v
 Urja Meter Ops Portal
```


## Project Structure

```
flock-energy-api/

├── app/
│   │
│   ├── main.py
│   │   FastAPI application entry point
│   │
│   ├── config.py
│   │   Environment configuration handling
│   │
│   ├── client/
│   │   │
│   │   ├── browser.py
│   │   │   Playwright browser session manager
│   │   │
│   │   └── urja_client.py
│   │       Portal authentication and data extraction
│   │
│   └── routes/
│       API route handlers
│
├── requirements.txt
├── .env
├── README.md
├── PROTOCOL.md
├── REFLECTION.md
└── openapi.json
```


# Technology Stack

- Python
- FastAPI
- Playwright
- Uvicorn
- python-dotenv


# Features Implemented

## Authentication

The Urja portal uses browser-based authentication.

The service:

1. Opens the portal login page.
2. Enters user credentials.
3. Waits for successful authentication.
4. Maintains the authenticated browser session using cookies.


## Meter Data Extraction

The API extracts:

- Meter ID
- Latitude
- Longitude
- Energy consumption records


# Installation


## Clone Repository

```bash
git clone <repository-url>

cd flock-energy-api
```


## Create Virtual Environment

Linux:

```bash
python -m venv venv

source venv/bin/activate
```


Windows:

```bash
python -m venv venv

venv\Scripts\activate
```


## Install Dependencies

```bash
pip install -r requirements.txt
```


## Environment Configuration

Create a `.env` file in the project root.

Example:

```env
URJA_URL=https://urja-ops.flockenergy.tech
USERNAME=operator@urja.local
PASSWORD=urja-ops-2026
```


# Running the Application

Start the FastAPI server:

```bash
python -m uvicorn app.main:app --reload
```


The API will be available at:

```
http://127.0.0.1:8000
```


Swagger documentation:

```
http://127.0.0.1:8000/docs
```


# API Documentation


## Get Meter Details

### Endpoint

```
GET /api/v1/meters/{meter_id}
```


### Example Request

```
GET http://127.0.0.1:8000/api/v1/meters/J100000
```


### Example Response

```json
{
  "meter": {
    "meterId": "J100000"
  },
  "geo": {
    "latitude": "26.938961002479868",
    "longitude": "75.83095696146852"
  },
  "energy": {
    "data": [
      {
        "timestamp": "23/06/2026 23:30",
        "kwh": 48438.74,
        "kvah": 52313.84,
        "voltage": 226
      }
    ]
  }
}
```


# Design Decisions


## Browser Automation Approach

The portal does not expose a documented public API.

Playwright was selected because it allows the service to interact with the portal in the same way as a normal user:

- Handles JavaScript-rendered pages.
- Supports browser-based authentication.
- Maintains session cookies.
- Avoids dependency on undocumented internal APIs.


## Why FastAPI?

FastAPI was selected because:

- Simple REST API development.
- Automatic OpenAPI generation.
- Strong validation support.
- Good performance for lightweight services.


# Assumptions

- The provided portal credentials remain valid.
- The portal URL structure remains unchanged.
- Meter pages continue to expose required information.
- The portal is treated as read-only.
- The extracted data format remains consistent.


# Trade-offs


## Playwright vs Direct HTTP Requests

A direct HTTP integration would be faster and require fewer resources.

However, the portal authentication flow is browser-based and dynamically rendered. Browser automation provides better compatibility with the existing system.

Trade-offs:

Advantages:

- Reliable authentication.
- Works with dynamic frontend applications.
- Matches normal user behaviour.

Limitations:

- Slower than direct API calls.
- Depends on frontend behaviour.


# What Was Intentionally Skipped

The following features were not implemented because they were outside the core requirement:

- Database storage
- Background data synchronization
- Meter history database
- User management
- Caching system
- Bulk data processing


# Future Improvements

With additional time, the following improvements could be added:

- Persistent browser session storage.
- Automated test suite.
- Retry handling for portal failures.
- Data caching layer.
- Bulk meter extraction.
- Monitoring and logging improvements.
- Local indexing and search support.


# Additional Documentation

## Portal Investigation

See:

```
PROTOCOL.md
```

This document explains:

- Portal behaviour
- Authentication flow
- Data extraction process
- Observations and limitations


## API Specification

See:

```
openapi.json
```

Contains the OpenAPI 3.x specification for this API.


## Reflection

See:

```
REFLECTION.md
```

Contains:

- Assumptions made
- Challenges faced
- Improvements considered
- Self-review


# Conclusion

This project provides a clean API layer over the Urja Meter Ops portal, allowing applications to retrieve smart meter information without directly interacting with the original portal interface.