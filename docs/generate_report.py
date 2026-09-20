import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

def build_pdf_report(output_filename="docs/Requirement_Report.pdf"):
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=50,
        rightMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1A365D")
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#C53030")
    )

    meta_style = ParagraphStyle(
        'CoverMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#4A5568")
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor("#1A365D"),
        spaceBefore=12,
        spaceAfter=6
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#2B6CB0"),
        spaceBefore=8,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor("#2D3748")
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        leftIndent=15,
        textColor=colors.HexColor("#2D3748")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        alignment=TA_LEFT,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#1A202C")
    )

    story = []

    # ==================== COVER PAGE ====================
    story.append(Spacer(1, 40))
    story.append(Paragraph("RAJSHAHI UNIVERSITY OF ENGINEERING & TECHNOLOGY", meta_style))
    story.append(Paragraph("Department of Computer Science & Engineering", meta_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>Course:</b> CSE 3206 (Software Engineering Sessional)", meta_style))
    story.append(Paragraph("<b>Lab Milestone 2:</b> Software Process Models, Requirement Analysis & MVP Development", meta_style))
    story.append(Spacer(1, 35))
    
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1A365D"), spaceBefore=5, spaceAfter=20))
    story.append(Paragraph("PROJECT DESIGN & REQUIREMENT REPORT", title_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Food Delivery Application (FoodFlow)", subtitle_style))
    story.append(Paragraph("Process Model: Kanban (Continuous Workflow with WIP Limits)", meta_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1A365D"), spaceBefore=20, spaceAfter=30))
    
    story.append(Spacer(1, 40))
    team_table_data = [
        [Paragraph("<b>Project Group:</b>", table_cell_style), Paragraph("Group 11 (Section A)", table_cell_style)],
        [Paragraph("<b>Assigned Project:</b>", table_cell_style), Paragraph("Food Delivery Application", table_cell_style)],
        [Paragraph("<b>Process Model:</b>", table_cell_style), Paragraph("Kanban Agile Framework", table_cell_style)],
        [Paragraph("<b>Technology Stack:</b>", table_cell_style), Paragraph("Python 3.14, Flask, SQLite3, HTML5/Tailwind CSS", table_cell_style)],
        [Paragraph("<b>Target Platform:</b>", table_cell_style), Paragraph("Web & Mobile-Responsive Browser Application", table_cell_style)],
        [Paragraph("<b>Submission Date:</b>", table_cell_style), Paragraph("September 2026", table_cell_style)]
    ]
    team_table = Table(team_table_data, colWidths=[140, 360])
    team_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F7FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(team_table)
    
    story.append(PageBreak())

    # ==================== EXECUTIVE SUMMARY & OBJECTIVES ====================
    story.append(Paragraph("1. Project Title & Overview", h1_style))
    story.append(Paragraph(
        "<b>FoodFlow</b> is an on-demand multi-tenant food ordering and delivery management system developed for RUET campus and surrounding urban areas. "
        "The system seamlessly connects hungry customers, partner restaurant kitchens, delivery drivers, and platform administrators through a responsive web application and unified Kanban workflow pipeline.",
        body_style
    ))
    
    story.append(Paragraph("2. Problem Statement", h1_style))
    story.append(Paragraph(
        "Traditional food ordering systems in local university ecosystems suffer from fragmented telephone orders, lack of order progress transparency, kitchen overcrowding during peak dining hours, and inefficient dispatching of delivery couriers. "
        "Without strict Work-In-Progress (WIP) controls, restaurant kitchens experience severe preparation bottlenecks, resulting in delayed orders, cold food, and customer dissatisfaction.",
        body_style
    ))

    story.append(Paragraph("3. Project Objectives", h1_style))
    story.append(Paragraph("• Deliver a functional Minimum Viable Product (MVP) enabling customer ordering, restaurant menu management, and courier dispatching.", bullet_style))
    story.append(Paragraph("• Enforce Kanban process principles both in the software development lifecycle and the real-time order fulfillment workflow.", bullet_style))
    story.append(Paragraph("• Eliminate kitchen bottlenecks and decrease order fulfillment lead times through explicit Work-In-Progress (WIP) limits.", bullet_style))
    story.append(Paragraph("• Provide real-time transparency for customers to track order progress across every milestone from preparation to doorstep delivery.", bullet_style))

    story.append(Paragraph("4. Stakeholder Analysis", h1_style))
    stakeholders_data = [
        [Paragraph("<b>Stakeholder</b>", table_header_style), Paragraph("<b>Role Description</b>", table_header_style), Paragraph("<b>Key Needs & Expectations</b>", table_header_style)],
        [Paragraph("Customer / Foodie", table_cell_style), Paragraph("End-users ordering meals for personal consumption", table_cell_style), Paragraph("Fast menu search, seamless cart checkout, accurate ETA, live tracking, fair pricing", table_cell_style)],
        [Paragraph("Restaurant Owner", table_cell_style), Paragraph("Kitchen managers offering culinary dishes", table_cell_style), Paragraph("Instant order notifications, menu item CRUD, inventory availability toggle, kitchen WIP limit controls", table_cell_style)],
        [Paragraph("Delivery Rider", table_cell_style), Paragraph("Logistics personnel transporting meals", table_cell_style), Paragraph("Instant job pickup alerts, pickup/drop-off directions, delivery fee earnings summary", table_cell_style)],
        [Paragraph("System Admin", table_cell_style), Paragraph("Platform operations & regulatory manager", table_cell_style), Paragraph("System-wide analytics, revenue reporting, dispute resolution, user governance, service health", table_cell_style)]
    ]
    st_table = Table(stakeholders_data, colWidths=[100, 160, 240])
    st_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1A365D")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(st_table)

    story.append(PageBreak())

    # ==================== REQUIREMENTS ====================
    story.append(Paragraph("5. Functional Requirements (FR)", h1_style))
    fr_data = [
        [Paragraph("<b>ID</b>", table_header_style), Paragraph("<b>Requirement Name</b>", table_header_style), Paragraph("<b>Description & Acceptance Criteria</b>", table_header_style)],
        [Paragraph("FR1", table_cell_style), Paragraph("User Registration & Auth", table_cell_style), Paragraph("Support secure registration and login with bcrypt password hashing and Role-Based Access Control (Customer, Owner, Rider, Admin).", table_cell_style)],
        [Paragraph("FR2", table_cell_style), Paragraph("Restaurant & Menu Catalog", table_cell_style), Paragraph("Display active restaurants with cuisine filtering (Italian, Japanese, Fast Food) and live text search.", table_cell_style)],
        [Paragraph("FR3", table_cell_style), Paragraph("Menu Management (CRUD)", table_cell_style), Paragraph("Restaurant owners can add dishes, update prices/descriptions, upload image URLs, and toggle item availability.", table_cell_style)],
        [Paragraph("FR4", table_cell_style), Paragraph("Shopping Cart & Checkout", table_cell_style), Paragraph("Customers can add items, modify quantities, apply coupon discounts (e.g. RUET10), and select payment methods.", table_cell_style)],
        [Paragraph("FR5", table_cell_style), Paragraph("Order Lifecycle & State Transitions", table_cell_style), Paragraph("Order transitions sequentially through Kanban states: Placed -> Preparing -> Ready -> In Transit -> Delivered.", table_cell_style)],
        [Paragraph("FR6", table_cell_style), Paragraph("Delivery Job Dispatch & Assignment", table_cell_style), Paragraph("Riders can view ready orders, accept delivery tasks, and mark orders picked up and delivered.", table_cell_style)],
        [Paragraph("FR7", table_cell_style), Paragraph("Payment Simulation", table_cell_style), Paragraph("Support Cash on Delivery (COD), Credit Card mock gateway, and Digital Wallet (bKash/Nagad simulation).", table_cell_style)],
        [Paragraph("FR8", table_cell_style), Paragraph("Ratings & Reviews", table_cell_style), Paragraph("Customers can rate delivered orders (1-5 stars) and provide feedback to update restaurant ratings dynamically.", table_cell_style)],
        [Paragraph("FR9", table_cell_style), Paragraph("Interactive Kanban Board", table_cell_style), Paragraph("Real-time visual board displaying order cards across 5 columns with configurable WIP limits and overflow alerts.", table_cell_style)],
        [Paragraph("FR10", table_cell_style), Paragraph("Customer Order History", table_cell_style), Paragraph("Customers can review past orders with item breakdown, receipts, and live delivery timeline tracker.", table_cell_style)],
        [Paragraph("FR11", table_cell_style), Paragraph("Admin Analytics & Governance", table_cell_style), Paragraph("Administrators can monitor total gross revenue, active WIP count, lead times, and manage all accounts.", table_cell_style)],
        [Paragraph("FR12", table_cell_style), Paragraph("RESTful JSON API", table_cell_style), Paragraph("Standardized REST endpoints for restaurants, menus, order status, and Kanban system metrics.", table_cell_style)]
    ]
    fr_table = Table(fr_data, colWidths=[35, 135, 330])
    fr_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2B6CB0")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(fr_table)

    story.append(Spacer(1, 10))
    story.append(Paragraph("6. Non-Functional Requirements (NFR)", h1_style))
    nfr_data = [
        [Paragraph("<b>ID</b>", table_header_style), Paragraph("<b>Quality Attribute</b>", table_header_style), Paragraph("<b>Specification Target</b>", table_header_style)],
        [Paragraph("NFR1", table_cell_style), Paragraph("Performance & Latency", table_cell_style), Paragraph("API response time < 150ms for local queries; page load under 1.2s.", table_cell_style)],
        [Paragraph("NFR2", table_cell_style), Paragraph("Data Integrity & Transactions", table_cell_style), Paragraph("ACID compliant relational database (SQLite3) with foreign keys and index optimization.", table_cell_style)],
        [Paragraph("NFR3", table_cell_style), Paragraph("Security & Encryption", table_cell_style), Paragraph("Passwords hashed with salt using Werkzeug/bcrypt; session cookie protection against CSRF.", table_cell_style)],
        [Paragraph("NFR4", table_cell_style), Paragraph("Usability & Accessibility", table_cell_style), Paragraph("Clean UI with Tailwind CSS, high contrast text, responsive grid for desktop and mobile.", table_cell_style)],
        [Paragraph("NFR5", table_cell_style), Paragraph("Maintainability & Modularity", table_cell_style), Paragraph("Layered MVC architecture separating models, business services, routes, and views.", table_cell_style)],
        [Paragraph("NFR6", table_cell_style), Paragraph("Testability & Quality Assurance", table_cell_style), Paragraph("100% test pass rate across unit and integration tests using pytest.", table_cell_style)],
        [Paragraph("NFR7", table_cell_style), Paragraph("Availability & Fault Tolerance", table_cell_style), Paragraph("Graceful exception handling with flash feedback; zero unhandled server crashes.", table_cell_style)],
        [Paragraph("NFR8", table_cell_style), Paragraph("Extensibility", table_cell_style), Paragraph("Pluggable architecture allowing future integration of real GPS maps and payment gateways.", table_cell_style)]
    ]
    nfr_table = Table(nfr_data, colWidths=[40, 140, 320])
    nfr_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2C5282")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(nfr_table)

    story.append(PageBreak())

    # ==================== USER STORIES & PROCESS MODEL ====================
    story.append(Paragraph("7. User Stories & Acceptance Criteria", h1_style))
    story.append(Paragraph("<b>US1 (Customer Ordering):</b> As a Customer, I want to browse restaurants, add food items to my cart, apply promo codes, and place an order with my delivery address so that I can have food delivered to my room.", body_style))
    story.append(Paragraph("<i>Acceptance:</i> Cart calculates subtotal, discounts, and delivery fee; order appears in customer history with 'Placed' status.", bullet_style))
    story.append(Spacer(1, 4))
    
    story.append(Paragraph("<b>US2 (Kitchen Management):</b> As a Restaurant Owner, I want to view incoming orders and transition them to 'Kitchen Preparing' and 'Ready for Pickup' so that food preparation is smooth.", body_style))
    story.append(Paragraph("<i>Acceptance:</i> Order updates reflect on the Kanban board; kitchen orders list displays customer special notes.", bullet_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>US3 (Rider Logistics):</b> As a Delivery Rider, I want to view ready orders, accept delivery tasks, and mark them 'In Transit' and 'Delivered' so that I can earn delivery fees.", body_style))
    story.append(Paragraph("<i>Acceptance:</i> Rider dashboard shows available and active jobs; total earnings counter increments upon delivery completion.", bullet_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>US4 (Kanban Flow Optimization):</b> As a Kitchen Manager, I want a visual Kanban board with WIP limits so that we prevent kitchen congestion and ensure fast order turnover.", body_style))
    story.append(Paragraph("<i>Acceptance:</i> Warning indicator triggers when active cooking tasks exceed the configured WIP limit.", bullet_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>US5 (Platform Governance):</b> As an Administrator, I want to view platform-wide analytics (revenue, throughput, lead times) and oversee registered users.", body_style))
    story.append(Paragraph("<i>Acceptance:</i> Real-time KPIs display accurate financial totals and average fulfillment lead time in minutes.", bullet_style))

    story.append(Spacer(1, 10))
    story.append(Paragraph("8. Software Process Model Selection: Kanban", h1_style))
    story.append(Paragraph(
        "For the Food Delivery Application, <b>Kanban</b> was selected as the optimal Software Process Model. "
        "Kanban is an Agile framework rooted in Lean manufacturing principles that focuses on continuous workflow visualization, Work-In-Progress (WIP) limitation, and cycle time minimization.",
        body_style
    ))
    
    story.append(Paragraph("Core Justifications for Kanban:", h2_style))
    story.append(Paragraph("1. <b>Direct Domain Symmetry:</b> The lifecycle of a food order (Placed -> Cooking -> Packaged -> On the Way -> Delivered) is a continuous pull system identical to a Kanban production line.", bullet_style))
    story.append(Paragraph("2. <b>WIP Limitation Prevents Bottlenecks:</b> Enforcing strict WIP limits prevents kitchen queues from ballooning, ensuring food quality and rapid dispatch.", bullet_style))
    story.append(Paragraph("3. <b>Continuous Delivery over Fixed Sprints:</b> Unlike Scrum's rigid 2-week timeboxes, Kanban accommodates urgent production bug fixes and real-time operational enhancements continuously.", bullet_style))
    story.append(Paragraph("4. <b>Lead Time & Cycle Time Optimization:</b> Kanban prioritizes throughput metrics, directly translating to shorter food delivery wait times for customers.", bullet_style))

    story.append(Spacer(1, 8))
    story.append(Paragraph("9. Comparison with Alternative Process Models", h1_style))
    comp_data = [
        [Paragraph("<b>Process Model</b>", table_header_style), Paragraph("<b>Characteristics</b>", table_header_style), Paragraph("<b>Why It Is Less Suitable for FoodFlow</b>", table_header_style)],
        [Paragraph("Waterfall", table_cell_style), Paragraph("Linear sequential phases, rigid upfront specifications, late testing phase.", table_cell_style), Paragraph("Incapable of adapting to dynamic customer demands, changing payment gateways, or iterative UX feedback without restarting the entire cycle.", table_cell_style)],
        [Paragraph("Agile Scrum", table_cell_style), Paragraph("Fixed time-boxed sprints (1-4 weeks), committed sprint backlog.", table_cell_style), Paragraph("Imposes rigid boundaries unsuitable for continuous order dispatching, instant bug patching, and daily operational flow.", table_cell_style)],
        [Paragraph("Spiral Model", table_cell_style), Paragraph("Heavy risk analysis, expensive cyclical prototyping phases.", table_cell_style), Paragraph("Introduces extreme management overhead and delays unsuited for an agile consumer-facing web MVP.", table_cell_style)],
        [Paragraph("Prototype Model", table_cell_style), Paragraph("Quick throwaway prototype built before actual development.", table_cell_style), Paragraph("Lacks structured process controls for long-term maintainability and operational flow once deployed.", table_cell_style)]
    ]
    comp_table = Table(comp_data, colWidths=[75, 175, 250])
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#742A2A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#FFF5F5")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(comp_table)

    story.append(PageBreak())

    # ==================== MVP DESIGN & ARCHITECTURE ====================
    story.append(Paragraph("10. MVP System Architecture & Design Overview", h1_style))
    story.append(Paragraph(
        "The FoodFlow MVP is architected according to professional Software Engineering principles with strict separation of concerns into distinct layers: "
        "Presentation (Jinja2/Tailwind UI), Controller / Routing (Flask Blueprints), Business Logic / Services (Service Layer), and Persistence (SQLite3 Relational Schema).",
        body_style
    ))

    arch_data = [
        [Paragraph("<b>Layer</b>", table_header_style), Paragraph("<b>Module / Component</b>", table_header_style), Paragraph("<b>Responsibilities</b>", table_header_style)],
        [Paragraph("Presentation Layer", table_cell_style), Paragraph("HTML5, Tailwind CSS, Jinja2 Templates, JavaScript", table_cell_style), Paragraph("Customer ordering interface, interactive Kanban board, kitchen dashboard, rider hub, admin control panel.", table_cell_style)],
        [Paragraph("Routing & Controllers", table_cell_style), Paragraph("Flask Blueprints (auth, customer, restaurant, delivery, admin, kanban, api)", table_cell_style), Paragraph("Request validation, HTTP status codes, session management, RBAC authorization decorators.", table_cell_style)],
        [Paragraph("Service Layer", table_cell_style), Paragraph("AuthService, RestaurantService, OrderService, KanbanService", table_cell_style), Paragraph("Business rule enforcement, state transition validation, WIP limit calculation, promo codes, metrics aggregation.", table_cell_style)],
        [Paragraph("Persistence Layer", table_cell_style), Paragraph("SQLite3 Schema, db.py, seeder.py", table_cell_style), Paragraph("Transactional relational tables (users, restaurants, menu_items, orders, order_items, reviews, kanban_tasks).", table_cell_style)]
    ]
    arch_table = Table(arch_data, colWidths=[90, 160, 250])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1A365D")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(arch_table)

    story.append(Spacer(1, 10))
    story.append(Paragraph("11. Verification & Quality Assurance", h1_style))
    story.append(Paragraph(
        "A rigorous automated test suite was constructed using <b>pytest</b>, verifying 100% of core system requirements across 20 distinct unit and integration test cases. "
        "Test fixtures dynamically provision an isolated temporary SQLite database, verifying user authentication, role enforcement, menu CRUD, cart checkout calculation, state machine integrity, and REST APIs.",
        body_style
    ))

    story.append(Spacer(1, 10))
    story.append(Paragraph("12. Challenges Encountered & Mitigations", h1_style))
    story.append(Paragraph("• <b>Challenge 1: Managing Kitchen WIP Limits:</b> During surge order periods, preventing kitchen staff overload without dropping orders.<br/><i>Mitigation:</i> Implemented a Backlog stage that queues orders safely and alerts managers when cooking WIP threshold is reached.", body_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("• <b>Challenge 2: Invalid Order State Transitions:</b> Preventing riders or users from skipping fulfillment steps.<br/><i>Mitigation:</i> Built a formal state transition map in the domain model (`ORDER_STATUS_FLOW`) that strictly validates all transitions.", body_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("• <b>Challenge 3: Role-Based Access Control:</b> Ensuring customers cannot manipulate kitchen orders or admin settings.<br/><i>Mitigation:</i> Implemented `@role_required` decorators on Flask routes with role hierarchy verification.", body_style))

    story.append(Spacer(1, 10))
    story.append(Paragraph("13. Conclusion & Next Milestones", h1_style))
    story.append(Paragraph(
        "Lab 2 has established a robust, modular, and fully functional Minimum Viable Product for the Food Delivery Application under the Kanban Agile process model. "
        "The clean layered architecture and comprehensive automated test suite provide an extensible foundation for upcoming semester labs covering advanced design patterns, continuous integration, and performance profiling.",
        body_style
    ))

    doc.build(story)
    print(f"Report generated successfully: {output_filename}")

if __name__ == '__main__':
    build_pdf_report()
