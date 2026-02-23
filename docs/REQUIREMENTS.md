# Mercial Requirements

This document defines the functional and non-functional requirements for a microservices-based system composed of User, Inventory, Order, Payment, and Notification services.

Each service owns its data, exposes a clear contract, and communicates through synchronous APIs and asynchronous events.

---

## **1. System Scope & Principles**
### *1.1 Overall Goals*
- Provide a ***scalable, modular backend*** suitable for real-world system design practice
- Enforce clear service ***boundaries*** and database ownership
- Support ***independent deployment and scaling***

### *1.2 Architectural Constraints*
- Each service SHALL own its database
- Services SHALL communicate via well-defined APIs
- Cross-service data access is NOT permitted

## **2. Common Non-Functional Requirements**
### *2.1 Performance*
- All services SHALL respond to read requests with low latency under normal load
- Write operations SHALL be atomic within a service boundary
### *2.2 Reliability*
- Services SHALL tolerate partial system failures
- Data integrity SHALL be preserved under concurrent access
### *2.3 Security*
- External-facing APIs SHALL require authentication
- Internal service-to-service communication SHALL be authenticated
### *2.4 Observability*
- Services SHALL emit logs for key operations
- Errors SHALL be traceable across service boundaries

## **3. Service Requirements**
### *3.1 User Service*
**Responsibilities:**
- Manage user identities and profiles
- Act as the source of truth for user-related data

**Functional Requirements:**
- SHALL create and manage user accounts
- SHALL expose user data to other services via APIs
- SHALL NOT handle authentication tokens beyond validation

### *3.2 Inventory Service*
**Responsibilities:**
- Manage product catalog and stock levels
- Act as the source of truth for inventory data

**Functional Requirements:**
- SHALL create and manage products identified by SKU
- SHALL track stock quantities per product
- SHALL prevent stock from going below zero
- SHALL store product image references, not binary data

### *3.3 Order Service*
**Responsibilities:**
- Manage order lifecycle from creation to completion
- Coordinate with inventory and payment services

**Functional Requirements:**
- SHALL create orders associated with users
- SHALL reserve inventory during order creation
- SHALL track order state transitions

### *3.4 Payment Service*
Responsibilities:
- Process and track payments
- Integrate with external payment providers (mocked)

Functional Requirements:
- SHALL initiate and record payment attempts
- SHALL expose payment status to the order service
- SHALL NOT store sensitive payment details

### *3.5 Notification Service*
**Responsibilities:**
- Deliver user notifications triggered by system events

**Functional Requirements:**
- SHALL consume events from other services
- SHALL send notifications via configured channels (e.g. email mock)
- SHALL operate asynchronously

## **4. Data Ownership & Integration**
### *4.1 Data Ownership*
- Each service SHALL exclusively own its database schema
- Shared schemas are NOT permitted

### *4.2 Integration Patterns*
- Synchronous APIs for queries
- Asynchronous events for state changes


## **5. Assumptions & Future Extensions**
### *5.1 Assumptions*
- All services are deployed in a containerized environment
- Databases are relational by default

### *5.2 Future Extensions*
- API Gateway introduction
- Advanced observability
- Event sourcing for order lifecycle
