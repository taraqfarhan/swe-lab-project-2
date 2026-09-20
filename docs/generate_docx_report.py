import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, fill_hex):
    """Set background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set cell internal margins (padding) in dxa."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_docx_report(output_filename="docs/Project_Design_Report.docx"):
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    doc = Document()

    # Configure Margins (1 inch everywhere)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Base Normal Style
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Arial'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(6)

    # Helper function for adding styled headings
    def add_sec_heading(text, level=1):
        p = doc.add_paragraph()
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.bold = True
        if level == 1:
            run.font.size = Pt(16)
            run.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D) # Dark Navy
            p.paragraph_format.space_before = Pt(16)
            p.paragraph_format.space_after = Pt(6)
        elif level == 2:
            run.font.size = Pt(13)
            run.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0) # Blue
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(4)
        elif level == 3:
            run.font.size = Pt(12)
            run.font.color.rgb = RGBColor(0x2D, 0x37, 0x48) # Charcoal
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(2)
        return p

    def add_body_p(text, bold_prefix="", italic=False):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = 'Arial'
            r_pre.font.size = Pt(12)
            r_pre.bold = True
        r_text = p.add_run(text)
        r_text.font.name = 'Arial'
        r_text.font.size = Pt(12)
        r_text.italic = italic
        return p

    def add_bullet_item(text, bold_prefix=""):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = 'Arial'
            r_pre.font.size = Pt(12)
            r_pre.bold = True
        r_text = p.add_run(text)
        r_text.font.name = 'Arial'
        r_text.font.size = Pt(12)
        return p

    def style_table(table, col_widths, headers, data):
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        
        # Header Row
        hdr_row = table.rows[0]
        for idx, heading in enumerate(headers):
            cell = hdr_row.cells[idx]
            cell.width = col_widths[idx]
            set_cell_background(cell, "1A365D")
            set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.space_before = Pt(0)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(heading)
            r.font.name = 'Arial'
            r.font.size = Pt(10.5)
            r.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

        # Data Rows
        for r_idx, row_data in enumerate(data):
            row = table.rows[r_idx + 1]
            bg_color = "F7FAFC" if r_idx % 2 == 1 else "FFFFFF"
            for c_idx, val in enumerate(row_data):
                cell = row.cells[c_idx]
                cell.width = col_widths[c_idx]
                set_cell_background(cell, bg_color)
                set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.space_before = Pt(0)
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                r = p.add_run(val)
                r.font.name = 'Arial'
                r.font.size = Pt(10)
                r.font.color.rgb = RGBColor(0x22, 0x22, 0x22)

    # Document Header Note
    note_p = doc.add_paragraph()
    note_p.paragraph_format.space_after = Pt(18)
    r_note = note_p.add_run("CSE 3206 – Software Engineering Sessional | Rajshahi University of Engineering & Technology (RUET)")
    r_note.font.name = 'Arial'
    r_note.font.size = Pt(10)
    r_note.font.color.rgb = RGBColor(0x71, 0x80, 0x96)
    r_note.italic = True

    # =========================================================================
    # SECTION 3: PROJECT TITLE
    # =========================================================================
    add_sec_heading("3. Project Title")
    add_body_p("FoodFlow – Modern Multi-Tenant Food Delivery Application with Kanban Flow Management", bold_prefix="Full Project Name: ")
    add_body_p(
        "FoodFlow is an on-demand, multi-tier food ordering and logistics management system engineered to connect university campus consumers, partner restaurant kitchens, delivery couriers, and system administrators into a synchronized, continuous workflow.",
        bold_prefix="Overview: "
    )

    # =========================================================================
    # SECTION 4: PROBLEM STATEMENT
    # =========================================================================
    add_sec_heading("4. Problem Statement")
    add_body_p(
        "In university and urban localities, food ordering processes frequently suffer from severe operational friction. Traditional ordering mechanisms rely on disorganized phone calls or uncoordinated web forms lacking real-time progress transparency. During peak dining hours (such as lunch and dinner breaks), restaurant kitchens face sudden surges in incoming orders without capacity regulation, leading to catastrophic kitchen bottlenecks, delayed food preparation, cold food deliveries, and stressed kitchen staff."
    )
    add_body_p(
        "Furthermore, the hand-off between kitchen staff and delivery couriers lacks coordination. Delivery drivers are often dispatched prematurely or after excessive delays because kitchens cannot effectively signal when food is packaged and ready for pickup. This lack of transparency and Work-In-Progress (WIP) control causes elevated delivery lead times, customer dissatisfaction, and revenue loss for local eateries."
    )

    # =========================================================================
    # SECTION 5: PROJECT OBJECTIVES
    # =========================================================================
    add_sec_heading("5. Project Objectives")
    add_body_p("The key objectives of the FoodFlow system for Lab Milestone 2 are defined as follows:")
    add_bullet_item(" Develop a functional, modular Minimum Viable Product (MVP) using Python and Flask covering customer ordering, restaurant menu management, rider delivery fulfillment, and administrative control.", bold_prefix="1. Functional MVP Development:")
    add_bullet_item(" Apply Lean Kanban principles to the order fulfillment lifecycle by establishing explicit Work-In-Progress (WIP) limits across preparation and transit stages to eliminate kitchen bottlenecks.", bold_prefix="2. Process Model Implementation:")
    add_bullet_item(" Provide step-by-step visual tracking for customers, reflecting real-time state changes from order placement to doorstep delivery.", bold_prefix="3. End-to-End Order Transparency:")
    add_bullet_item(" Design a layered, clean MVC and Service-Oriented Architecture that facilitates maintainability, automated testing, and future semester milestones (Design Patterns, CI/CD, and Advanced Metrics).", bold_prefix="4. Robust Software Engineering Foundation:")
    add_bullet_item(" Deliver an automated unit and integration test suite with 100% verification across all critical functional workflows.", bold_prefix="5. Quality Assurance:")

    # =========================================================================
    # SECTION 6: STAKEHOLDER ANALYSIS
    # =========================================================================
    add_sec_heading("6. Stakeholder Analysis")
    add_body_p("A thorough stakeholder analysis was conducted to identify all primary actors interacting with the system, their operational responsibilities, and their core expectations.")
    
    st_headers = ["Stakeholder", "Role & Description", "Key Needs & System Goals"]
    st_data = [
        ["Customer (Foodie)", "End-user seeking quick, hot meals within the university campus and residential areas.", "Intuitive restaurant browsing, category filtering, transparent pricing, discount coupons, easy checkout, and live order tracking."],
        ["Restaurant Owner / Kitchen Staff", "Culinary merchant managing dishes, prices, and kitchen order queues.", "Immediate incoming order alerts, dynamic menu item CRUD, toggleable stock availability, and a visual kitchen queue with WIP limits."],
        ["Delivery Courier (Rider)", "Logistics personnel transporting packaged orders from eateries to customers.", "Real-time list of ready-for-pickup orders, clear pickup and delivery addresses, quick status toggling, and earnings summary."],
        ["System Administrator", "Platform governance authority overseeing ecosystem reliability and business health.", "System-wide analytics (revenue, order counts, lead time averages), user and restaurant oversight, and Kanban process throughput monitoring."]
    ]
    st_table = doc.add_table(rows=len(st_data) + 1, cols=3)
    style_table(st_table, [Inches(1.5), Inches(2.2), Inches(2.8)], st_headers, st_data)

    # =========================================================================
    # SECTION 7: FUNCTIONAL REQUIREMENTS
    # =========================================================================
    add_sec_heading("7. Functional Requirements (FR)")
    add_body_p("The system implements 12 comprehensive functional requirements fulfilling all user roles and system operations:")
    
    fr_headers = ["ID", "Requirement Title", "Detailed Functional Description"]
    fr_data = [
        ["FR1", "User Authentication & RBAC", "The system shall support user registration and authentication with secure salted password hashing, maintaining distinct roles: Customer, Restaurant Owner, Delivery Rider, and Administrator."],
        ["FR2", "Restaurant Catalog & Filtering", "The system shall allow users to browse all partner restaurants with dynamic category filtering (Italian, Japanese, Fast Food) and live text keyword searching."],
        ["FR3", "Menu Management (CRUD)", "Restaurant owners shall be able to create, view, update, and delete menu items, including name, description, category, price, image URL, and stock availability toggle."],
        ["FR4", "Shopping Cart & Checkout", "The system shall maintain an interactive session-based shopping cart supporting quantity adjustment, item removal, promotional discount application (e.g., RUET10, KANBAN5), and delivery details input."],
        ["FR5", "Order State Progression", "The system shall manage order lifecycles strictly through valid sequential Kanban states: Placed -> Preparing -> Ready -> In Transit -> Delivered (or Cancelled)."],
        ["FR6", "Delivery Job Assignment", "The system shall allow delivery riders to view orders in 'Ready for Pickup' status, claim delivery jobs, and update the order state upon dispatch and completion."],
        ["FR7", "Multi-Channel Payment Simulation", "The system shall support payment method selection including Cash on Delivery (COD), simulated Credit/Debit Card, and simulated Digital Wallet (bKash/Nagad)."],
        ["FR8", "Customer Order History & Tracking", "The system shall provide customers with historical order receipts and a live visual step-by-step progress tracker indicating the active stage and timestamps."],
        ["FR9", "Ratings & Dynamic Reviews", "Customers shall be permitted to submit ratings (1-5 stars) and textual feedback for delivered orders, automatically updating the restaurant's average rating."],
        ["FR10", "Live Interactive Kanban Board", "The system shall display a real-time Kanban management board featuring 5 order fulfillment columns with configurable WIP limits and visual overflow alerts."],
        ["FR11", "System Analytics & Oversight", "Administrators shall have access to aggregated metrics including gross platform revenue, active WIP volume, average lead times, and user/restaurant directories."],
        ["FR12", "RESTful JSON API Services", "The system shall expose standardized REST API endpoints for restaurants, menus, order statuses, and Kanban system performance metrics."]
    ]
    fr_table = doc.add_table(rows=len(fr_data) + 1, cols=3)
    style_table(fr_table, [Inches(0.6), Inches(1.8), Inches(4.1)], fr_headers, fr_data)

    # =========================================================================
    # SECTION 8: NON-FUNCTIONAL REQUIREMENTS
    # =========================================================================
    add_sec_heading("8. Non-Functional Requirements (NFR)")
    add_body_p("The system complies with 10 critical non-functional quality attributes to ensure robustness, performance, and security:")

    nfr_headers = ["ID", "Quality Attribute", "Specification & Target Metric"]
    nfr_data = [
        ["NFR1", "Performance & Latency", "The application shall render web views in under 1.2 seconds and process API queries within 150 milliseconds under standard campus loads."],
        ["NFR2", "Data Integrity & ACID Reliability", "All database transactions shall maintain strict ACID compliance with relational foreign key enforcement and indexed lookups using SQLite3."],
        ["NFR3", "Security & Encryption", "User passwords shall be hashed using Werkzeug salted SHA-256/bcrypt algorithms; session cookies shall be signed and protected against tampering."],
        ["NFR4", "Usability & Responsive Design", "The user interface shall adapt responsively to mobile, tablet, and desktop viewports using Tailwind CSS with clear visual feedback for all user actions."],
        ["NFR5", "Modularity & Maintainability", "The codebase shall adhere to strict separation of concerns into Models, Services, Route Blueprints, and Presentation Templates."],
        ["NFR6", "Testability & Verification", "The core business logic and state machine shall achieve 100% automated test pass rate across unit and integration test suites using pytest."],
        ["NFR7", "Availability & Fault Tolerance", "The system shall handle errors gracefully through flash message alerts and exception trapping without unhandled server termination."],
        ["NFR8", "Portability", "The application shall execute seamlessly across modern operating systems (macOS, Linux, Windows) with standard Python 3.10+ virtual environments."],
        ["NFR9", "Extensibility", "The architecture shall allow future plug-and-play integration of real GPS mapping APIs, third-party payment gateways, and WebSocket real-time feeds."],
        ["NFR10", "WIP Capacity Management", "The system shall actively enforce configurable Work-In-Progress thresholds, providing visual indicators when kitchen queues approach saturation."]
    ]
    nfr_table = doc.add_table(rows=len(nfr_data) + 1, cols=3)
    style_table(nfr_table, [Inches(0.6), Inches(1.8), Inches(4.1)], nfr_headers, nfr_data)

    # =========================================================================
    # SECTION 9: USER STORIES / USE CASES
    # =========================================================================
    add_sec_heading("9. User Stories / Use Cases")
    add_body_p("Five detailed user stories illustrating end-to-end user workflows and their formal acceptance criteria:")

    # US 1
    add_sec_heading("User Story 1: Customer Food Ordering & Promo Checkout", level=2)
    add_body_p("As a registered Customer, I want to browse partner restaurant menus, add desired dishes to my shopping cart, apply promotional discount codes, and submit my campus delivery address, so that I can conveniently order fresh meals delivered to my dormitory room.", bold_prefix="Description: ")
    add_bullet_item("The user can select item quantities and view instant subtotal calculations.", bold_prefix="Acceptance Criteria 1:")
    add_bullet_item("Applying valid promo codes (e.g., 'RUET10') recalculates the total amount with discounts applied.", bold_prefix="Acceptance Criteria 2:")
    add_bullet_item("Submitting the order generates a unique Order ID and places the order into 'Order Placed' (Backlog) status.", bold_prefix="Acceptance Criteria 3:")

    # US 2
    add_sec_heading("User Story 2: Kitchen Order Preparation & Queue Flow", level=2)
    add_body_p("As a Restaurant Owner, I want to receive incoming customer orders on my kitchen dashboard and transition them to 'Kitchen Preparing' and 'Ready for Pickup', so that my kitchen staff can prepare food in a controlled, orderly sequence.", bold_prefix="Description: ")
    add_bullet_item("New orders appear immediately in the kitchen feed with customer notes and item lists.", bold_prefix="Acceptance Criteria 1:")
    add_bullet_item("Clicking 'Start Cooking' moves the order into the 'Preparing' Kanban column.", bold_prefix="Acceptance Criteria 2:")
    add_bullet_item("Marking the meal ready updates the status to 'Ready for Pickup' and alerts available couriers.", bold_prefix="Acceptance Criteria 3:")

    # US 3
    add_sec_heading("User Story 3: Delivery Rider Job Pickup & Drop-off", level=2)
    add_body_p("As a Delivery Rider, I want to view all packaged orders ready for pickup, claim delivery tasks, and mark them as 'In Transit' and 'Delivered', so that I can transport food promptly and track my accumulated delivery earnings.", bold_prefix="Description: ")
    add_bullet_item("Riders can view pickup locations, drop-off addresses, and earning amounts for ready orders.", bold_prefix="Acceptance Criteria 1:")
    add_bullet_item("Accepting a job assigns the rider's ID to the order and moves it to the rider's active task list.", bold_prefix="Acceptance Criteria 2:")
    add_bullet_item("Marking an order delivered updates the customer's tracker, closes payment status, and increments the rider's total earnings.", bold_prefix="Acceptance Criteria 3:")

    # US 4
    add_sec_heading("User Story 4: Kanban WIP Limit Enforcement & Bottleneck Alerting", level=2)
    add_body_p("As a Restaurant Operations Manager, I want the system to enforce Work-In-Progress limits on active kitchen preparation and dispatch columns, so that the kitchen is never overloaded and food freshness is maintained.", bold_prefix="Description: ")
    add_bullet_item("The system maintains configurable WIP thresholds for each fulfillment stage.", bold_prefix="Acceptance Criteria 1:")
    add_bullet_item("If active orders in a column exceed the WIP limit, the column displays a visual 'WIP EXCEEDED' warning badge.", bold_prefix="Acceptance Criteria 2:")
    add_bullet_item("Managers can dynamically adjust WIP limits via an administrative modal based on current staffing.", bold_prefix="Acceptance Criteria 3:")

    # US 5
    add_sec_heading("User Story 5: Platform Analytics & System Governance", level=2)
    add_body_p("As a System Administrator, I want to access a consolidated governance dashboard showing platform revenue, order fulfillment counts, and average delivery lead times, so that I can evaluate service efficiency and manage registered users.", bold_prefix="Description: ")
    add_bullet_item("The dashboard aggregates gross revenue from completed orders in real time.", bold_prefix="Acceptance Criteria 1:")
    add_bullet_item("Key Kanban metrics (Average Lead Time, Cycle Time, Throughput) are clearly displayed.", bold_prefix="Acceptance Criteria 2:")
    add_bullet_item("Administrators can view all registered users across all roles and audit platform order records.", bold_prefix="Acceptance Criteria 3:")

    # =========================================================================
    # SECTION 10: SELECTED SOFTWARE PROCESS MODEL
    # =========================================================================
    add_sec_heading("10. Selected Software Process Model: Kanban")
    add_body_p(
        "For the Food Delivery Application (FoodFlow), the Kanban Process Model was selected as the designated software engineering and operational framework. Kanban is an Agile methodology derived from Lean production principles that emphasizes visual workflow management, continuous task flow, explicit capacity constraints, and cycle time reduction."
    )
    add_body_p(
        "Unlike time-boxed iterative models, Kanban operates as a continuous pull system where work items are pulled into active phases only when capacity becomes available. FoodFlow implements a dual-layer Kanban architecture: applying Kanban principles to both the software development lifecycle (tracking engineering tasks from backlog to deployment) and the runtime business domain (guiding customer orders from receipt to delivery)."
    )

    # =========================================================================
    # SECTION 11: JUSTIFICATION OF PROCESS MODEL
    # =========================================================================
    add_sec_heading("11. Justification of Process Model")
    add_body_p("The selection of Kanban is strongly justified by the following engineering and domain-specific factors:")
    add_bullet_item(" The lifecycle of a food order (Placed -> Cooking -> Packaged -> Dispatched -> Delivered) represents an unbroken, continuous physical pull system. Modeling software and operations with Kanban creates a natural 1-to-1 mapping between business reality and system logic.", bold_prefix="1. Domain Symmetry:")
    add_bullet_item(" In traditional restaurant software, unconstrained order volume causes kitchen congestion. By enforcing strict WIP limits (e.g., maximum 5 concurrent cooking orders), kitchens maintain optimal throughput without degradation in food quality or accuracy.", bold_prefix="2. Bottleneck Elimination via WIP Limits:")
    add_bullet_item(" Food delivery platforms operate continuously 24/7. Fixed sprint boundaries (like in Scrum) create artificial delivery delays. Kanban allows instant deployment of bug fixes, pricing updates, and feature enhancements as soon as they are tested.", bold_prefix="3. Continuous Delivery & Flexibility:")
    add_bullet_item(" Kanban places primary emphasis on reducing Lead Time (elapsed time from order placement to doorstep receipt) and Cycle Time (active preparation and transit time), directly aligning with customer satisfaction goals.", bold_prefix="4. Cycle Time & Lead Time Optimization:")
    add_bullet_item(" Kanban provides lightweight process discipline without unnecessary ceremony overhead (such as sprint planning, daily standups, and story pointing), maximizing development velocity for the MVP.", bold_prefix="5. Reduced Management Overhead:")

    # =========================================================================
    # SECTION 12: COMPARISON WITH ALTERNATIVE MODELS
    # =========================================================================
    add_sec_heading("12. Comparison with Alternative Models")
    add_body_p("To substantiate the selection of Kanban, a comparative analysis was performed against major alternative software process models:")

    comp_headers = ["Process Model", "Key Characteristics", "Suitability for FoodFlow", "Primary Drawbacks / Why Less Suitable"]
    comp_data = [
        ["Kanban (Selected)", "Continuous pull flow, visual board, explicit WIP limits, real-time adaptability.", "Optimal (100% Fit)", "Requires team discipline to adhere strictly to WIP limits."],
        ["Waterfall Model", "Linear-sequential phases (Requirements -> Design -> Code -> Test -> Deploy).", "Unsuitable", "Rigid upfront specifications; unable to accommodate shifting market feedback; testing occurs too late in the lifecycle."],
        ["Agile Scrum", "Fixed time-boxed sprints (1-4 weeks), sprint backlogs, fixed sprint goals.", "Suboptimal", "Rigid sprint boundaries cannot accommodate 24/7 continuous order flow, emergency bug fixes, and real-time courier adjustments."],
        ["Spiral Model", "Risk-driven, iterative prototyping with heavy formal risk analysis phases.", "Unsuitable", "Excessive documentation overhead, high cost, and slow turnaround unsuited for consumer web applications."],
        ["RAD (Rapid App Dev)", "Component assembly, rapid prototyping, short timeboxed development.", "Suboptimal", "Focuses on rapid UI construction but lacks continuous flow management and operational WIP controls post-launch."],
        ["Prototype Model", "Quick throwaway mockups to discover requirements before coding.", "Suboptimal", "Useful for UI discovery but lacks a formal operational process model for managing live production workloads."]
    ]
    comp_table = doc.add_table(rows=len(comp_data) + 1, cols=4)
    style_table(comp_table, [Inches(1.2), Inches(1.8), Inches(1.3), Inches(2.2)], comp_headers, comp_data)

    # =========================================================================
    # SECTION 13: MVP DESIGN OVERVIEW
    # =========================================================================
    add_sec_heading("13. MVP Design Overview")
    add_body_p(
        "The FoodFlow MVP is built using a clean, layered architecture ensuring high cohesion and loose coupling across all subsystems."
    )

    add_sec_heading("13.1 Layered Architecture Overview", level=2)
    add_bullet_item(" HTML5, Tailwind CSS, FontAwesome icons, Jinja2 template inheritance, and responsive JavaScript utilities providing intuitive user interfaces for all roles.", bold_prefix="• Presentation Layer (UI):")
    add_bullet_item(" Modular Flask Blueprints (auth_bp, customer_bp, restaurant_bp, delivery_bp, admin_bp, kanban_bp, api_bp) handling HTTP routing, request parsing, session management, and role-based authorization decorators.", bold_prefix="• Controller & Routing Layer:")
    add_bullet_item(" Encapsulated Python service classes (AuthService, RestaurantService, OrderService, KanbanService) managing business logic, state progression rules, WIP saturation checking, and discount computations.", bold_prefix="• Service & Domain Logic Layer:")
    add_bullet_item(" Relational SQLite3 database with foreign key enforcement, custom indexing, and automated migration/seeder scripts.", bold_prefix="• Persistence Layer:")

    add_sec_heading("13.2 Database Schema & Entity Relationships", level=2)
    add_body_p("The persistence layer models 7 interconnected relational entities:")
    add_bullet_item(" `users` (id, username, email, password_hash, role, full_name, phone, address, created_at)")
    add_bullet_item(" `restaurants` (id, owner_id FK, name, description, cuisine_type, address, phone, image_url, rating, is_active)")
    add_bullet_item(" `menu_items` (id, restaurant_id FK, name, description, category, price, image_url, is_available)")
    add_bullet_item(" `orders` (id, order_number, customer_id FK, restaurant_id FK, rider_id FK, status, total_amount, discount_amount, delivery_fee, delivery_address, payment_method, payment_status, placed_at, delivered_at)")
    add_bullet_item(" `order_items` (id, order_id FK, menu_item_id FK, item_name, unit_price, quantity, subtotal)")
    add_bullet_item(" `reviews` (id, order_id FK, customer_id FK, restaurant_id FK, rating, comment, created_at)")
    add_bullet_item(" `kanban_tasks` (id, title, description, category, priority, column_name, assignee, lead_time_hours)")
    add_bullet_item(" `kanban_wip_limits` (column_name PK, wip_limit)")

    add_sec_heading("13.3 Order Fulfillment State Machine", level=2)
    add_body_p("Order state transitions follow an explicit directed graph preventing illegal status leaps:")
    add_body_p("Placed (Backlog) ──> Preparing (Cooking, WIP: 5) ──> Ready (Packaged, WIP: 4) ──> In Transit (Rider Dispatch, WIP: 6) ──> Delivered (Completed)", italic=True)

    # =========================================================================
    # SECTION 15: CHALLENGES ENCOUNTERED
    # =========================================================================
    add_sec_heading("15. Challenges Encountered & Mitigation Strategies")
    add_body_p("During the analysis, design, and implementation of the MVP, several engineering challenges were addressed:")
    
    add_bullet_item(" During peak simulation testing, order submission bursts threatened to overload the kitchen cooking queue.<br/><b>Mitigation:</b> Implemented an asynchronous Backlog queue that buffers incoming orders, coupled with visual 'WIP EXCEEDED' banner alerts on the Kanban board to trigger managerial intervention.", bold_prefix="1. Managing Kitchen Queue Surges:")
    add_bullet_item(" Ensuring that couriers and restaurant owners cannot bypass mandatory workflow states (e.g., jumping from Placed directly to Delivered).<br/><b>Mitigation:</b> Enforced a strict state transition matrix (`ORDER_STATUS_FLOW`) within the domain model, returning explicit validation errors on illegal transitions.", bold_prefix="2. Invalid Order State Transitions:")
    add_bullet_item(" Preventing unauthorized access across multi-tenant user portals (e.g., customers modifying restaurant menus).<br/><b>Mitigation:</b> Developed custom `@role_required` and `@login_required` decorators in Flask that inspect session tokens before route execution.", bold_prefix="3. Role-Based Access Control Security:")
    add_bullet_item(" When re-seeding the SQLite database during testing, SQLite's internal sequence table caused foreign key mismatch errors on cached autoincrement IDs.<br/><b>Mitigation:</b> Refactored the database seeder to explicitly clean the `sqlite_sequence` table and map deterministic primary keys.", bold_prefix="4. Database Auto-Increment Sequence Integrity:")

    # =========================================================================
    # SECTION 16: CONCLUSION
    # =========================================================================
    add_sec_heading("16. Conclusion")
    add_body_p(
        "In Lab Milestone 2, the team successfully conducted a comprehensive requirement analysis and implemented a fully functional Minimum Viable Product (MVP) for the Food Delivery Application (FoodFlow) using Python and the Kanban Process Model."
    )
    add_body_p(
        "By applying Kanban principles across both the software engineering lifecycle and the runtime order pipeline, the system demonstrates how Work-In-Progress limits and continuous flow visualization eliminate kitchen bottlenecks and reduce delivery lead times. The modular layered architecture, clean REST APIs, and 100% automated test coverage provide a rock-solid foundation for upcoming semester labs covering advanced design patterns, continuous integration, and performance benchmarking."
    )

    doc.save(output_filename)
    print(f"Project Design Report DOCX created successfully at: {output_filename}")

if __name__ == '__main__':
    create_docx_report()
