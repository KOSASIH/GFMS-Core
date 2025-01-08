# API Reference

## Overview

The GFMS API provides endpoints for managing users, transactions, notifications, and more. All endpoints are secured and require authentication.

## Authentication

- **Endpoint**: `/api/token`
- **Method**: POST
- **Description**: Obtain a JWT token for authentication.

## User Endpoints

- **Create User**
  - **Endpoint**: `/api/users/`
  - **Method**: POST
  - **Request Body**: `{ "username": "string", "email": "string", "password": "string" }`
  - **Response**: User object with ID.

- **Get User**
  - **Endpoint**: `/api/users/{user_id}`
  - **Method**: GET
  - **Response**: User object.

## Transaction Endpoints

- **Create Transaction**
  - **Endpoint**: `/api/transactions/`
  - **Method**: POST
  - **Request Body**: `{ "sender_id": "int", "receiver_id": "int", "amount": "float" }`
  - **Response**: Transaction object.

- **Get Transaction**
  - **Endpoint**: `/api/transactions/{transaction_id}`
  - **Method**: GET
  - **Response**: Transaction object.

## Notifications

- **Get User Notifications**
  - **Endpoint**: `/api/notifications/{user_id}`
  - **Method**: GET
  - **Response**: List of notifications.
