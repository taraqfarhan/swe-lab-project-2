# FoodFlow - Food Delivery Application
## Project Design & Requirement Report (Lab 2 Milestone)

**Course:** CSE 3206 – Software Engineering Sessional  
**Department:** Computer Science & Engineering  
**Institution:** Rajshahi University of Engineering & Technology (RUET)  
**Group:** 11 (Section A)  
**Assigned Project:** Food Delivery Application  
**Assigned Process Model:** Kanban  

---

## 1. Project Overview & Problem Statement

### 1.1 Project Overview
**FoodFlow** is an on-demand multi-tenant food ordering and delivery management system designed for the university campus and surrounding urban areas. The platform connects customers, partner restaurants, delivery riders, and administrators through a responsive web application and a unified visual Kanban workflow.

### 1.2 Problem Statement
Traditional food ordering processes in university ecosystems suffer from:
- Lack of live transparency regarding order preparation and delivery milestones.
- Severe kitchen bottlenecks during peak hours due to lack of Work-In-Progress (WIP) controls.
- Disjointed communication between kitchen staff and delivery couriers.
- Delayed deliveries and poor customer satisfaction.

FoodFlow addresses these issues by modeling both the software development lifecycle and order fulfillment pipeline using **Kanban** principles with explicit WIP limits.

---

## 2. Stakeholder Analysis

| Stakeholder | Role & Responsibilities | Key Expectations & Goals |
| :--- | :--- | :--- |
| **Customer / Foodie** | Searches menus, places food orders, tracks deliveries | Fast search, easy cart management, live tracking, coupon discounts, receipt breakdown |
| **Restaurant Owner** | Manages dish catalog, accepts orders, cooks food | Real-time incoming orders, menu item CRUD, toggle availability, kitchen WIP limit controls |
| **Delivery Rider** | Picks up packaged meals from kitchens, delivers to customers | Available delivery alerts, delivery addresses, navigation directions, earnings tracking |
| **System Admin** | Oversees entire platform operations and governance | Platform revenue stats, order volume, lead time / cycle time monitoring, user management |

---

## 3. Requirement Analysis

### 3.1 Functional Requirements (FR)
- **FR1 (Authentication & RBAC):** Secure user registration and login with bcrypt password hashing and Role-Based Access Control (`customer`, `restaurant_owner`, `rider`, `admin`).
- **FR2 (Restaurant Catalog & Search):** Search and filter restaurants by cuisine (Italian, Japanese, American Fast Food) and keyword search.
- **FR3 (Menu Management):** Restaurant owners can perform full CRUD operations on dishes (name, description, category, price, image, availability).
- **FR4 (Cart & Checkout):** Interactive shopping cart supporting item increment/decrement, special instructions, promo codes (`RUET10`, `KANBAN5`), and payment method selection.
- **FR5 (Order Fulfillment Pipeline):** Sequential status transition through Kanban stages: `placed` -> `preparing` -> `ready` -> `in_transit` -> `delivered`.
- **FR6 (Delivery Dispatch):** Riders can view ready orders, claim delivery tasks, and complete deliveries.
- **FR7 (Payment Simulation):** Support Cash on Delivery (COD), Credit Card mock gateway, and Digital Wallet (bKash/Nagad mock).
- **FR8 (Customer Order Tracking):** Real-time visual progress step tracker showing current stage and timestamps.
- **FR9 (Reviews & Ratings):** Customers can review delivered orders (1 to 5 stars) and leave comments, dynamically updating restaurant ratings.
- **FR10 (Interactive Kanban Board):** Full visual Kanban board with drag/one-click transitions, WIP limit monitoring, and overflow alerts.
- **FR11 (Admin Analytics):** System dashboards tracking total orders, revenue, active WIP count, and lead times.
- **FR12 (REST API):** Standardized JSON endpoints for restaurants, menus, orders, and Kanban metrics.

### 3.2 Non-Functional Requirements (NFR)
- **NFR1 (Performance):** Page rendering under 1.2s; API response time < 150ms.
- **NFR2 (Reliability & ACID):** Transactional SQLite3 database with foreign key constraints and indexed queries.
- **NFR3 (Security):** Passwords hashed with salted bcrypt/Werkzeug; role-protected endpoints using decorators.
- **NFR4 (Usability):** Responsive modern UI built with Tailwind CSS and FontAwesome icons.
- **NFR5 (Maintainability):** Layered MVC architecture separating models, services, routes, and views.
- **NFR6 (Testability):** 100% test pass rate across 20 pytest unit and integration tests.
- **NFR7 (Availability):** Graceful error handling and flash message feedback.
- **NFR8 (Extensibility):** Modular service structure ready for future payment gateways and map APIs.

---

## 4. User Stories & Acceptance Criteria

### User Story 1: Customer Ordering
> **As a** Customer,  
> **I want to** browse dishes, add them to my cart, and place an order with my campus delivery address,  
> **So that** I can get hot meals delivered directly to my dorm.  
> 
> **Acceptance Criteria:**
> - Cart calculates subtotals, discounts, and delivery fee.
> - Order is assigned an order number and placed into the 'Placed' status.

### User Story 2: Kitchen Order Preparation
> **As a** Restaurant Owner,  
> **I want to** receive incoming orders and transition them to 'Preparing' and 'Ready for Pickup',  
> **So that** my kitchen cooks dishes in order without getting overwhelmed.  
> 
> **Acceptance Criteria:**
> - Order appears in Kitchen Orders dashboard with customer notes.
> - Clicking 'Start Cooking' updates status to 'preparing'.

### User Story 3: Rider Order Dispatch
> **As a** Delivery Rider,  
> **I want to** see orders that are ready for pickup, accept jobs, and mark them delivered,  
> **So that** I can transport meals quickly and track my earnings.  
> 
> **Acceptance Criteria:**
> - Available jobs list shows restaurant pickup and customer drop-off.
> - Completing delivery increments rider total earnings.

### User Story 4: Kanban WIP Limit Enforcement
> **As a** Kitchen / Logistics Manager,  
> **I want to** enforce Work-In-Progress (WIP) limits on active cooking and transit stages,  
> **So that** we prevent bottlenecks and maintain low lead times.  
> 
> **Acceptance Criteria:**
> - Column highlights with a warning banner when current orders exceed the WIP limit.

### User Story 5: Platform Analytics & Governance
> **As a** System Admin,  
> **I want to** view system-wide revenue, active WIP orders, and lead time metrics,  
> **So that** I can monitor platform health and operational efficiency.  
> 
> **Acceptance Criteria:**
> - Admin dashboard aggregates gross revenue, orders count, and average lead time.

---

## 5. Software Process Model Justification: Kanban

### 5.1 Why Kanban Fits FoodFlow
1. **Continuous Flow:** Unlike batch-based models, food delivery operates continuously 24/7 where each order is an independent work item flowing through stages.
2. **Work-In-Progress (WIP) Limits:** Enforces capacity limits on kitchen preparation (e.g. max 5 concurrent cooking orders) and delivery queues, preventing system saturation and cold food deliveries.
3. **Pull System:** Kitchens pull orders from the backlog as capacity frees up; riders pull ready orders as they complete existing deliveries.
4. **Lead Time & Cycle Time Focus:** Kanban focuses heavily on reducing Lead Time (time from order placed to delivered) and Cycle Time (active cooking/transit time).

### 5.2 Comparative Analysis against Alternative Models

| Model | Workflow Mechanism | Suitability for Food Delivery | Key Drawbacks |
| :--- | :--- | :--- | :--- |
| **Kanban (Selected)** | Continuous pull flow with WIP limits | **Optimal (100% Fit)** | Requires discipline in adhering to WIP limits |
| **Waterfall** | Linear sequential phases | **Unsuitable** | Cannot adapt to changing requirements; testing occurs too late |
| **Agile Scrum** | Fixed time-boxed sprints (1-4 weeks) | **Suboptimal** | Fixed sprint backlogs cannot accommodate real-time operational flow and continuous order dispatching |
| **Spiral Model** | Heavy risk analysis & prototype cycles | **Unsuitable** | Excessive overhead and delays for a web/mobile MVP |
| **Prototype Model** | Quick throwaway prototype | **Suboptimal** | Lacks formal process discipline for production maintainability |

---

## 6. MVP Architecture & Technical Implementation

```
food-delivery-app/
├── src/
│   ├── app.py               # Flask Application Factory
│   ├── config.py            # Global & Kanban Configuration
│   ├── database/
│   │   ├── db.py            # SQLite Connection & Query Helpers
│   │   ├── schema.sql       # Relational Schema Definition
│   │   └── seeder.py        # Realistic Seed Data
│   ├── models/              # Domain Models (User, Restaurant, Order, Kanban)
│   ├── services/            # Business Logic (Auth, Restaurant, Order, Kanban)
│   ├── routes/              # Blueprints (Auth, Customer, Restaurant, Rider, Admin, Kanban, API)
│   ├── templates/           # Jinja2 HTML5 Responsive Views
│   └── static/              # Tailwind CSS & Client JavaScript
├── tests/                   # 20 Automated Pytest Suite
├── docs/                    # Requirement_Report.pdf & Project Design
├── requirements.txt         # Dependencies
├── run.py                   # Server Entry Point
└── README.md                # Documentation & Setup Guide
```

---

## 7. Verification & Test Summary
The project contains 20 automated tests verifying:
- User authentication and role redirection.
- Restaurant filtering, search, and menu item CRUD.
- Shopping cart totals, discounts, and checkout.
- Kanban state transitions and WIP limit enforcement.
- REST API endpoints.

**Test Result:** `20 passed in 2.25s (100% Pass Rate)`
