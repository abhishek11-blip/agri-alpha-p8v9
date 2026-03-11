  
**TECHNICAL ASSESSMENT**

**MaaS Application Development**

Use Case Document for Fresher Candidates

| Document Version | 1.0 |
| :---- | :---- |
| **Date** | March 2026 |
| **Assessment Duration** | 5 Working Days |
| **Difficulty Level** | Fresher / Entry Level |

# **1\. Introduction**

Welcome to the Amnex Technical Assessment. This document presents a practical use case for developing a simplified Mobility-as-a-Service (MaaS) application. The purpose of this assessment is to evaluate your logical reasoning, problem-solving approach, code quality, and ability to design practical solutions.

## **1.1 What is MaaS?**

Mobility-as-a-Service (MaaS) integrates multiple forms of transportation into a single, accessible platform. Users can plan journeys, book tickets, and pay for various transport modes (buses, metros, bikes, cabs) through one unified application.

## **1.2 Assessment Objectives**

* Evaluate your understanding of basic software architecture  
* Assess your ability to design database schemas  
* Test your API design and implementation skills  
* Observe your problem-solving approach and logical thinking  
* Evaluate code quality, documentation, and best practices

## **1.3 Technology Stack (Choose Any)**

You may use any technology stack you are comfortable with. Recommended options:

* **Backend:** .NET Core / Node.js / Python (Flask/Django) / Java Spring Boot  
* **Frontend:** React / Angular / Vue.js / Simple HTML+CSS+JS  
* **Database:** PostgreSQL / MySQL / SQLite / MongoDB  
* **Mobile (Optional):** React Native / Flutter / Native Android/iOS

# **2\. Use Case: City Transit Pass System**

## **2.1 Business Context**

A city transportation authority wants to launch a digital transit pass system that allows commuters to purchase passes valid across multiple transport modes. The system should enable users to buy passes, validate them during travel, and view their journey history.

## **2.2 User Personas**

| Persona | Description | Key Needs |
| :---- | :---- | :---- |
| **Commuter** | Daily traveler using public transport | Buy passes, validate during travel, view history |
| **Validator** | Bus conductor or metro gate operator | Validate commuter passes, record trips |
| **Admin** | Transport authority staff | Manage pass types, view reports, configure fares |

## **2.3 Functional Requirements**

### **FR-01: User Registration & Authentication**

* Users should be able to register with mobile number and basic profile information  
* Implement login functionality with session management  
* Support role-based access (Commuter, Validator, Admin)

### **FR-02: Pass Management**

* Display available pass types (Daily, Weekly, Monthly)  
* Each pass type should have: name, validity period, price, applicable transport modes  
* Users can purchase passes (simulate payment \- no real payment integration needed)  
* Generate unique pass code/QR upon purchase  
* Show active and expired passes in user profile

### **FR-03: Pass Validation**

* Validator can enter pass code to validate  
* System checks: pass validity, applicable transport mode, usage limits  
* Record each validation as a trip entry  
* Show validation result (Valid/Invalid with reason)

### **FR-04: Journey History**

* Commuters can view their trip history  
* Show: date, time, transport mode, route (if available)  
* Filter by date range

### **FR-05: Admin Dashboard**

* View total passes sold (daily/weekly/monthly)  
* View total validations per transport mode  
* CRUD operations for pass types

# **3\. Technical Requirements**

## **3.1 Database Design**

Design a normalized database schema covering at minimum:

* **Users:** id, name, mobile, email, password\_hash, role, created\_at  
* **PassTypes:** id, name, validity\_days, price, transport\_modes, max\_trips\_per\_day  
* **UserPasses:** id, user\_id, pass\_type\_id, pass\_code, purchase\_date, expiry\_date, status  
* **Trips:** id, user\_pass\_id, validated\_by, transport\_mode, route\_info, validated\_at  
* **TransportModes:** id, name, code (e.g., BUS, METRO, FERRY)

## **3.2 API Design**

Implement RESTful APIs with proper HTTP methods and status codes:

| Method | Endpoint | Description |
| :---- | :---- | :---- |
| POST | /api/auth/register | Register new user |
| POST | /api/auth/login | User login |
| GET | /api/passes/types | List available pass types |
| POST | /api/passes/purchase | Purchase a pass |
| GET | /api/passes/my-passes | Get user's passes |
| POST | /api/validate | Validate a pass |
| GET | /api/trips/history | Get trip history |
| GET | /api/admin/dashboard | Admin statistics |

## **3.3 Business Logic Requirements**

1. **Pass Expiry:** A pass should automatically be marked expired when validity period ends  
2. **Daily Trip Limit:** If max\_trips\_per\_day is set, validation should fail after limit is reached  
3. **Transport Mode Check:** Validation should fail if pass doesn't cover the transport mode being used  
4. **Duplicate Validation Prevention:** Prevent same pass from being validated twice within 5 minutes (anti-passback)

# **4\. Deliverables**

## **4.1 Required Submissions**

| \# | Deliverable | Description |
| :---- | :---- | :---- |
| 1 | **Source Code Repository** | GitHub/GitLab repository with complete source code, proper folder structure, and meaningful commit history |
| 2 | **README.md** | Setup instructions, tech stack used, API documentation, assumptions made, known limitations |
| 3 | **Database Schema** | ER diagram or schema file with explanation of design decisions |
| 4 | **API Collection** | Postman collection or Swagger/OpenAPI documentation for testing APIs |
| 5 | **Working Application** | Either deployed URL or Docker setup for local testing |

## **4.2 Bonus Points (Optional)**

* Unit tests for critical business logic  
* Input validation and proper error handling  
* API rate limiting implementation  
* Basic QR code generation for passes  
* Mobile-responsive UI design  
* Logging and monitoring setup

# **5\. Evaluation Criteria**

Your submission will be evaluated using both AI-assisted code analysis and manual review. The following criteria will be assessed:

| Criterion | Weightage | What We Look For |
| :---- | :---- | :---- |
| **Code Quality** | 20% | Clean, readable code; proper naming conventions; consistent formatting; appropriate comments |
| **Architecture & Design** | 25% | Proper separation of concerns; scalable design patterns; thoughtful database schema; API design quality |
| **Functionality** | 25% | All required features working; proper business logic implementation; edge case handling |
| **Problem Solving** | 15% | Approach to complex requirements; creative solutions; handling of constraints |
| **Documentation** | 10% | Clear README; API documentation; design decisions explained; setup instructions |
| **Best Practices** | 5% | Git usage; security considerations; error handling; input validation |

## **5.1 AI-Assisted Code Review**

Your code repository will be analyzed using AI tools to generate objective findings. The AI review will assess:

* Code structure and organization  
* Implementation completeness against requirements  
* Potential bugs, security vulnerabilities, or anti-patterns  
* Database design efficiency  
* API design adherence to REST principles  
* Test coverage and quality (if tests provided)

## **5.2 Follow-up Interview**

Based on the AI analysis and manual review, follow-up questions will be prepared for the face-to-face interview. These questions will focus on:

* Explaining your design decisions and trade-offs  
* Discussing alternative approaches you considered  
* How you would extend or scale the solution  
* Clarifying any flagged issues from the code review  
* Real-world scenarios and how your system would handle them

# **6\. Important Guidelines**

## **6.1 Use of AI Tools**

**Important:** You are permitted and encouraged to use AI coding assistants (GitHub Copilot, ChatGPT, Claude, etc.) to help with your implementation. However, you must be able to explain every piece of code you submit. During the interview, you may be asked to modify or extend any part of your code live.

## **6.2 Time Management**

* You have 5 working days to complete this assessment  
* Focus on core functionality first before attempting bonus features  
* A working MVP is more valuable than an incomplete feature-rich application  
* Document any features you planned but couldn't implement due to time constraints

## **6.3 Assumptions & Clarifications**

* Document all assumptions you make  
* If any requirement is unclear, make a reasonable assumption and document it  
* You may reach out to the HR contact for clarifications (within first 2 days only)

## **6.4 What NOT To Do**

* Do not copy code from existing transit applications verbatim  
* Do not submit code you cannot explain  
* Do not spend excessive time on UI polish at the cost of functionality  
* Do not implement features not specified in requirements

# **7\. Submission Process**

## **7.1 How to Submit**

5. Push your complete code to a public GitHub/GitLab repository  
6. Ensure the repository contains all deliverables listed in Section 4  
7. Reply to the assessment email with your repository link  
8. Include any deployment URL if you have hosted the application

## **7.2 Submission Checklist**

| ☐ | Source code with proper folder structure |
| :---- | :---- |
| ☐ | README.md with setup instructions |
| ☐ | Database schema (SQL file or ER diagram) |
| ☐ | API documentation (Postman/Swagger) |
| ☐ | At least 10 meaningful git commits |
| ☐ | Working application (deployed or Docker setup) |
| ☐ | Design decisions documented |

## **7.3 Post-Submission**

After submission:

9. Your code will be analyzed by our AI assessment system within 24-48 hours  
10. A technical review will be conducted by our engineering team  
11. You will be contacted within 5 working days with next steps  
12. If selected, a technical interview will be scheduled to discuss your submission

# **8\. Sample Test Scenarios**

Use these scenarios to validate your implementation:

### **Scenario 1: Happy Path \- Pass Purchase & Validation**

13. User registers and logs in  
14. User views available pass types  
15. User purchases a Monthly Metro+Bus pass  
16. User receives pass code  
17. Validator validates the pass for Metro \- should succeed  
18. User views trip in journey history

### **Scenario 2: Invalid Transport Mode**

19. User purchases a Metro-only pass  
20. Validator attempts to validate for Bus transport  
21. Expected: Validation fails with 'Transport mode not covered' message

### **Scenario 3: Expired Pass**

22. User has an expired pass  
23. Validator attempts to validate  
24. Expected: Validation fails with 'Pass expired' message

### **Scenario 4: Daily Limit Exceeded**

25. User has a Daily pass with max 4 trips/day  
26. User completes 4 trips  
27. Validator attempts 5th validation  
28. Expected: Validation fails with 'Daily trip limit reached' message

### **Scenario 5: Anti-Passback (Duplicate Validation)**

29. User validates pass at 10:00 AM  
30. Same pass is attempted to be validated at 10:02 AM  
31. Expected: Validation fails with 'Please wait before next validation' message

# **9\. Contact Information**

For any queries or clarifications regarding this assessment:

| HR Contact | \[HR Email to be filled\] |
| :---- | :---- |
| **Query Deadline** | Within first 2 days of receiving this document |
| **Submission Deadline** | 5 working days from date of receipt |

**We look forward to reviewing your submission\!**  
Good luck\!