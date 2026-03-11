Dhaval, since you already **created a Next.js app**, the best way to approach this is to treat the frontend like a **small production product**. A **PRD (Product Requirements Document)** will define:

- product goals
- user flows
- UI screens
- API integration
- state management
- folder architecture
- validations
- edge cases

Below is a **complete Frontend PRD tailored for your MaaS assessment**.

---

# Frontend PRD

**Project:** MaaS Transit Pass System
**Frontend:** Next.js (React)
**Developer:** Dhaval Prajapati
**Document Version:** 1.0
**Date:** March 2026

---

# 1. Product Overview

The MaaS Transit Pass System allows commuters to purchase and use digital transit passes across multiple transport modes (bus, metro, ferry).

The frontend application will provide interfaces for three user roles:

- **Commuter**
- **Validator**
- **Admin**

The frontend will communicate with backend REST APIs to handle authentication, pass management, validation, and analytics.

---

# 2. Product Goals

The frontend should:

- Provide a **simple and responsive UI**
- Support **role-based dashboards**
- Integrate with backend APIs
- Display **pass information clearly**
- Enable **pass validation quickly**
- Show **trip history and analytics**

The UI should prioritize **usability over heavy design**.

---

# 3. User Roles

## 3.1 Commuter

Capabilities:

- Register
- Login
- View available passes
- Purchase passes
- View active passes
- View expired passes
- View journey history

---

## 3.2 Validator

Capabilities:

- Login
- Enter pass code
- Select transport mode
- Validate pass
- View validation result

---

## 3.3 Admin

Capabilities:

- Login
- View statistics dashboard
- Manage pass types
- View validation reports

---

# 4. Application Architecture

### Framework

Next.js (App Router)

### Rendering Strategy

| Page            | Rendering |
| --------------- | --------- |
| Auth pages      | Client    |
| Dashboard       | Client    |
| Pass listing    | Server    |
| Admin analytics | Client    |

---

### State Management

Recommended options:

- React Context
- Zustand

Global state required for:

- user session
- role
- auth token

---

### API Communication

Use:

```
axios
```

Create centralized API client.

Example:

```
/services/api.ts
```

---

# 5. Application Routes

## Public Routes

```
/login
/register
```

---

## Commuter Routes

```
/dashboard
/passes
/my-passes
/trips
```

---

## Validator Routes

```
/validator
```

---

## Admin Routes

```
/admin
/admin/pass-types
/admin/dashboard
```

---

# 6. UI Screens

---

# 6.1 Authentication

## Login Page

Route:

```
/login
```

Fields:

- email
- password

Actions:

- login
- redirect to dashboard

API:

```
POST /api/auth/login
```

UI Components:

- input fields
- submit button
- error message

---

## Register Page

Route:

```
/register
```

Fields:

- name
- email
- mobile
- password
- role

API:

```
POST /api/auth/register
```

Validation:

- email format
- password min length
- required fields

---

# 6.2 Dashboard

Route:

```
/dashboard
```

Content depends on role.

---

### Commuter Dashboard

Sections:

- Active Pass
- Quick Purchase
- Recent Trips

Example cards:

```
Active Pass
Expiry Date
Transport Modes
```

---

### Validator Dashboard

Simple interface.

Fields:

```
pass code
transport mode dropdown
```

Button:

```
Validate
```

Display result:

```
VALID
INVALID
REASON
```

---

### Admin Dashboard

Statistics cards:

```
passes sold today
passes sold weekly
passes sold monthly
```

Charts (optional):

```
validations by transport mode
```

---

# 6.3 Pass Types Page

Route:

```
/passes
```

API:

```
GET /api/passes/types
```

Display:

Pass cards.

Example:

```
Monthly Pass
Validity: 30 days
Price: ₹800
Modes: Bus + Metro
```

Actions:

```
Purchase Pass
```

---

# 6.4 Purchase Flow

Steps:

1. User clicks purchase
2. Confirmation modal
3. Call API
4. Show pass code

API:

```
POST /api/passes/purchase
```

Response:

```
pass_code
expiry_date
```

Display:

```
PASS-382HF8
Valid till 2026-04-01
```

---

# 6.5 My Passes

Route:

```
/my-passes
```

API:

```
GET /api/passes/my-passes
```

Sections:

Active Passes
Expired Passes

Each pass card shows:

```
pass_code
type
expiry_date
status
transport_modes
```

Optional:

QR Code display.

---

# 6.6 Trip History

Route:

```
/trips
```

API:

```
GET /api/trips/history
```

Filters:

- date range
- transport mode

Display table:

```
Date
Time
Mode
Route
Validator
```

---

# 6.7 Validator Screen

Route:

```
/validator
```

Fields:

```
Pass Code
Transport Mode
```

Button:

```
Validate
```

API:

```
POST /api/validate
```

Response:

```
VALID
INVALID
REASON
```

Examples:

```
Pass expired
Transport mode not covered
Daily limit reached
```

---

# 6.8 Admin Pass Type Management

Route:

```
/admin/pass-types
```

Table:

```
Name
Validity
Price
Transport Modes
Max Trips
```

Actions:

```
Create
Edit
Delete
```

---

# 7. Components

Common reusable components:

```
Button
Input
Modal
Card
Table
Dropdown
Badge
Loader
Toast
```

---

# 8. UI Layout

Main layout components:

```
Navbar
Sidebar
Content Area
Footer
```

---

# 9. Folder Structure

Recommended Next.js structure.

```
src
 ├ app
 │  ├ login
 │  ├ register
 │  ├ dashboard
 │  ├ passes
 │  ├ my-passes
 │  ├ trips
 │  ├ validator
 │  └ admin
 │
 ├ components
 │  ├ ui
 │  ├ pass
 │  ├ dashboard
 │  └ forms
 │
 ├ services
 │  ├ api.ts
 │  ├ authService.ts
 │  ├ passService.ts
 │  └ tripService.ts
 │
 ├ hooks
 │  ├ useAuth
 │  ├ usePasses
 │
 ├ context
 │  └ AuthContext
 │
 ├ utils
 │  ├ constants
 │  └ helpers
```

---

# 10. Authentication Handling

Store token in:

```
HTTP-only cookie
```

or

```
localStorage
```

Auth flow:

```
login → save token → fetch profile → redirect
```

Protect routes using middleware.

Example:

```
middleware.ts
```

---

# 11. Error Handling

Display user-friendly errors.

Examples:

```
Invalid credentials
Pass expired
Transport mode not allowed
```

Use toast notifications.

---

# 12. Loading States

Show loading when:

- API calls
- pass purchase
- validation

Use:

```
skeleton loaders
```

---

# 13. Form Validation

Use:

```
React Hook Form
+
Zod
```

Validate:

- required fields
- email
- password

---

# 14. Responsive Design

The UI should work on:

- desktop
- tablet
- mobile

Use:

```
Tailwind CSS
```

---

# 15. Security Considerations

Frontend should:

- hide admin routes from other users
- validate inputs
- sanitize form data

---

# 16. Edge Cases

Handle scenarios:

### Expired pass

Display:

```
Expired
```

---

### No passes purchased

Show:

```
You have no passes yet
```

---

### API failure

Show:

```
Something went wrong
```

---

# 17. Performance Optimization

Use:

- code splitting
- lazy loading
- memoization

Example:

```
dynamic imports
```

---

# 18. Testing

Optional but recommended.

Test:

- login flow
- pass purchase
- validation

Tools:

```
Jest
React Testing Library
```

---

# 19. API Integration

Create centralized service functions.

Example:

```
getPassTypes()
purchasePass()
validatePass()
getTrips()
```

---

# 20. Deployment

Deploy on:

```
Vercel
```

Environment variables:

```
NEXT_PUBLIC_API_URL
```

---

# 21. Success Criteria

Frontend will be considered successful if:

- Users can login and register
- Pass types are visible
- Pass purchase works
- Validator can validate pass
- Trip history loads
- Admin dashboard displays stats

---

# 22. Future Enhancements

Potential features:

- QR code scanning
- push notifications
- mobile app version
- payment integration

---

If you want, I can also give you **3 extremely useful things for this assessment**:

1️⃣ **Exact UI wireframes for all pages**
2️⃣ **Best frontend architecture to impress reviewers**
3️⃣ **Pre-built folder structure + starter code for Next.js**

That will make your submission **look like a senior developer built it**, not a fresher.
