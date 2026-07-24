# Urja Meter Ops Portal Protocol Notes

## Overview

This document describes how the Urja Meter Ops portal works based on the investigation performed during development.

The goal was to understand how the existing portal provides meter information and build an API service on top of it.

The portal is a web-based internal application used by utility operations teams to view smart meter information.

The portal provides:

- Meter details
- Meter network hierarchy information
- Meter geographical location
- Recent energy consumption data


---

# Portal Access

Portal URL:

```
https://urja-ops.flockenergy.tech
```

Authentication credentials are provided through environment variables:

```
USERNAME
PASSWORD
```


The portal does not expose a documented public API. Therefore, the service interacts with the portal through browser automation.


---

# Authentication Flow

## Login Process

The authentication flow works as follows:

1. Open the login page.

```
/login
```

2. Enter:

```
email
password
```

3. Submit the login form.

4. The portal creates an authenticated browser session.

5. The authenticated session is maintained using cookies.


Example session cookie observed:

```
__Secure-better-auth.session_token
```


The cookie is required to access authenticated pages such as:

```
/meters
/meters/{meter_id}
```


---

# Browser Automation

Playwright is used to automate the portal interaction.

The flow:

```
FastAPI Request

        |
        v

UrjaClient

        |
        v

Playwright Browser Session

        |
        v

Login Portal

        |
        v

Authenticated Meter Pages
```


The browser session is kept active during API requests to maintain authentication.


---

# Available Data


## Meter Information

Meter pages provide:

- Meter ID
- Serial number
- Manufacturer
- Phase type
- Installation status
- Installation type


Example:

```
Meter ID:
J100000

Serial:
SE33962

Make:
HPL
```


---

## Geographic Information

The meter page contains location information.

Extracted fields:

```
latitude
longitude
```


Example:

```json
{
  "latitude": "26.938961002479868",
  "longitude": "75.83095696146852"
}
```


---

## Energy Consumption Data

The portal provides recent consumption information.

Extracted values include:

- Timestamp
- KWH
- KVAH
- Voltage values


Example:

```json
{
  "timestamp": "23/06/2026 23:30",
  "kwh": 48438.74,
  "kvah": 52313.84,
  "voltage": 226
}
```


---

# Data Retrieval Process


## Meter Request Flow

When the API receives:

```
GET /api/v1/meters/{meter_id}
```


The process is:

```
API Request

    |
    v

Authenticate Portal

    |
    v

Open Meter Page

    |
    v

Extract Location

    |
    v

Capture Energy Data

    |
    v

Return Structured JSON
```


---

# Portal Observations


## Dynamic Frontend

The portal is a JavaScript-based web application.

The data is rendered dynamically after page loading.

Because of this:

- Simple HTML requests are insufficient.
- Browser execution is required.


---

## No Public API

During investigation:

- No documented API endpoint was available.
- Data was accessed through the authenticated portal interface.


Therefore browser automation was selected as the integration approach.


---

# Design Decisions


## Why Playwright?

Playwright was chosen because:

- It supports JavaScript-heavy applications.
- It handles authentication flows.
- It maintains browser sessions.
- It behaves similarly to a real user.


## Why not scrape raw HTML?

The portal content is dynamically generated.

Raw HTTP scraping would not reliably provide:

- Session handling
- Rendered data
- Client-side loaded information


---

# Limitations


Current implementation depends on:

- Portal availability.
- Existing login flow.
- Existing page structure.

Changes in the portal frontend may require updates to extraction logic.


---

# Future Improvements

Possible improvements:

1. Persistent browser session storage.

2. Automated retry handling.

3. Better monitoring and logging.

4. Background synchronization.

5. Local caching layer.

6. Bulk meter extraction support.


---

# Summary

The Urja Meter API acts as an abstraction layer over the existing portal.

It allows external applications to retrieve meter information through a clean REST API without directly interacting with the original portal interface.