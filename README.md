BuyLyst.co

BuyLyst.co is a full-stack Python + MongoDB + React application used by trading card game stores to manage their buylist intake, pricing, cart processing, and inventory importing. It is designed to enable customers to submit cards for sale, employees to process the physical cards, and managers to intake and sync the results into an inventory system (e.g., Shopify).


---

✨ Overview

Self-hosted Flask server with JWT auth and MongoDB storage

Daily CSV imports from TCGCSV API for up-to-date product data

Public buylist interface showing cards the store wants to buy

Advanced cart system for buy requests and pricing enforcement

Admin tools for setting buy prices, tracking buy progress, disabling categories/groups

Employee workflows for processing carts in-store

Manager workflows for intaking processed carts and generating exports

Everything is logged and auditable



---

🏛️ Technologies

Layer	Stack

Backend	Flask + Flask-JWT-Extended
Database	MongoDB
Scheduler	APScheduler
Frontend	React + Tailwind (planned)
Deployment	Bare metal, self-hosted



---

🔢 Data Model Summary

products

Pulled from TCGCSV. Each product has:

internalId = productId_subTypeName

productId, groupId, categoryId

name, imageUrl, tcgplayerUrl, rarity, number, subTypeName

marketPrice, lowPrice, midPrice, highPrice, directLowPrice


buylist_entries

internalId

priceMultiplier, priceOverride

disabled: controls if it's shown to users

createdBy, createdAt, updatedBy, updatedAt


buylist_progress

internalId, maxQuantity

boughtQuantity, pendingQuantity

Used to control auto-disable behavior


buy_carts

status: draft / submitted / accepted / processed / completed

username, dropOffType, items, notes

employeeName, processedBy

payout.cash, payout.credit, payout.creditBonus

Timestamps: createdAt, submittedAt, processedAt, cancelledAt


users

username, password_hash, role

Roles: customer, employee, manager, admin


server_settings

storeName

creditBoostPercentage

conditionPercentages

enabledCategories

allowUserAccounts, allowInStoreDropOff, allowShippedDropOff


audit_logs

action, collection_name, document_id, performed_by, timestamp, details


emergency_disables

type: "group" or "category"

id, reason, disabledBy, disabledAt



---

🚀 Use Case Flow (User to Inventory)

Diagram

graph TD
  A[Customer checks buylist] --> B[Adds 3x Fenrir to cart]
  B --> C[Submits cart (in-store)]
  C --> D[Admin optionally approves cart]
  C --> E[Employee sees submitted cart]
  E --> F[Processes cart: 2 NM, 1 LP]
  F --> G[Customer selects $5 credit / rest cash]
  G --> H[Cart stored w/ payout + audit log]
  H --> I[Inventory Manager sees processed cart]
  I --> J[Reviews: corrects to 2 LP, 1 NM]
  J --> K[Marks cart reviewed]
  K --> L[Selects batch to import]
  L --> M[Generates CSV export for Shopify]
  M --> N[Uploads to Shopify, stores inventory]


---

✅ Features

Customers

Register/login with JWT

View public buylist

Fuzzy name search (e.g. "ka fen" -> "Kashtira Fenrir")

Add to cart (auto-creates draft cart)

Cannot exceed quantity limits

Cannot submit emergency-disabled items

Submit cart with drop-off type

View/cancel own carts


Admin

Set priceMultiplier or priceOverride per product

Enable/disable buylist entries

Set maxQuantity for buy goals

Auto-disable when max fulfilled

View audit logs (paginated + filtered)

Emergency disable groups/categories

Update global settings

View and modify user roles/passwords


Employees

View submitted + accepted carts

Cancel submitted carts

Process cart with adjusted conditions

Apply payout splits (cash + credit)

Auto-calculate credit bonus

Add employee notes and name


Inventory Managers

(Planned) View processed carts

(Planned) Mark reviewed, adjust final conditions/qtys

(Planned) Generate import batch

(Planned) Export to CSV for POS


Import System

Daily TCGCSV job by category

Background thread processes queue

Tracks current in-progress category

Imports groups + products + prices

Summarizes imported totals in log

Skips products that already exist


SKU Mapping

(Planned) internalId -> { NM: SKU1, LP: SKU2, ... }

Selenium fallback if SKU missing

Manual entry UI if no listing found


Area	Description

Cart approval	Accept/lock in carts before processing
Intake APIs	List processed carts, mark reviewed, fix issues
Inventory import	Store reviewed products in inventory_imports
CSV export	Create files for Shopify/etc
Analytics	Weekly/monthly spending, buy summaries
Manual SKU tool	Web UI to enter missing SKUs
POS integration	Automatically sync payouts to POS



---

🔗 API Summary

Endpoint	Role	Description

GET /buylist	public	Search cards available for buying
POST /cart/add	customer	Add item to draft cart
POST /cart/submit	customer	Submit cart for review
GET /employee/cart/get/<id>	employee	View and process cart
POST /employee/cart/process/<id>	employee	Mark cart as processed
POST /admin/buylist	admin	Create or update a buylist entry
GET /admin/audit_logs	admin	Paginated audit log viewer
POST /admin/settings	admin	Update global server config
GET /groups/all_by_category	public	Group list for filters/dropdowns



---

⚡ Development Standards

# MODIFIED comments required on all changed lines

All DB write ops and logins must include AuditLog.log()

Logging via central logger

All _id fields must be stringified before returning

Only one draft cart per user

Every model uses .collection() to define indexes



---

✍ Contributing Notes

Run main.py directly to start API server

.env file required with Mongo and JWT keys

Use Postman to test endpoints with JWT

Frontend (React) work is still upcoming



---

Here is a step-by-step, technical walkthrough of the full buylist lifecycle using the "3x Fenrir" use-case — with explicit backend endpoint calls, method types, input payloads, and the DB behavior involved at each step.


---

✅ Step-by-Step: Selling 3x Fenrir — Endpoint Flow


---

1. Customer wants to check if we're buying "Fenrir"

Action: Search the public buylist

Endpoint:
GET /buylist?name=fenrir
(optional: &categoryId=1, &groupId=123, etc.)

What Happens:

Matches enabled buylist entries

Applies emergency disables

Joins buylist_entries, products, and buylist_progress

Calculates:

remainingQuantity = maxQuantity - boughtQuantity - pendingQuantity

buyPrice = priceOverride OR priceMultiplier * marketPrice


Returns:


[
  {
    "internalId": "123-EN",
    "name": "Fenrir",
    "buyPrice": 5.00,
    "remainingQuantity": 10
  }
]

✅ Implemented via routes/public_buylist.py


---

2. Customer registers an account

Endpoint:
POST /auth/register

Body:

{ "username": "fenrirfan", "password": "hunterxhunter" }

✅ Implemented — conditional on server setting allowUserAccounts == true


---

3. Customer adds 3x Fenrir to their cart

Endpoint:
POST /cart/add

Body:

{ "internalId": "123-EN", "quantity": 3 }

What Happens:

Validates that the product is enabled and not emergency-disabled

Loads buylist entry + progress

Ensures requested_quantity + bought + pending <= maxQuantity

Creates a draft cart if needed

Adds item or increments quantity

Price and condition stored on item

Audits the change


✅ Implemented in public_cart.py


---

4. Customer submits the cart

Endpoint:
POST /cart/submit

What Happens:

Changes cart status: "draft" → "submitted"

Increments pendingQuantity in buylist_progress

Audits the action


✅ Implemented


---

5. Admin reviews carts to approve or not

Endpoint:
GET /employee/cart/list_pending

What Happens:

Returns all carts with status submitted or accepted


✅ Implemented


---

6. Employee sees cart detail

Endpoint:
GET /employee/cart/get/<cart_id>

What Happens:

Returns cart contents

If status is "submitted":

Compares items against current buylist availability

Flags any disabled or emergency-disabled items as "discontinued"



✅ Implemented (with discontinuedItems list)


---

7. Emergency disable applied to "Fenrir"

Endpoint:
POST /admin/emergency/disable

Body:

{ "type": "product", "id": "123-EN" } // or type = "group", "category"

What Happens:

Adds entry to emergency_disables

Disables it from new add-to-cart actions and buylist visibility


✅ Implemented (group/category only — product-level not supported yet)


---

8. Customer comes in with cart ID

No endpoint call here — they provide the cart ID to a store employee.


---

9. Employee processes the cart

Endpoint:
POST /employee/cart/process/<cart_id>

Body:

{
  "items": [
    { "internalId": "123-EN", "quantity": 2, "condition": "Near Mint", "priceEach": 5.0 },
    { "internalId": "123-EN", "quantity": 1, "condition": "Lightly Played", "priceEach": 5.0 }
  ],
  "employeeName": "Tom",
  "notes": "1 lightly played",
  "payout": {
    "cashPercentage": 0.667,
    "creditPercentage": 0.333
  }
}

What Happens:

Applies conditionPercentages and creditBoost from server settings

Computes total payout in cash & credit

Updates cart:

"status": "processed"

Logs payout, notes, condition details


Updates boughtQuantity in buylist_progress

Audits the change


✅ Implemented


---

10. Inventory manager sees list of processed carts

Endpoint:
GET /inventory/list_processed

Returns: All carts with status "processed" (not yet intaked)

🟡 Not implemented yet — Placeholder only


---

11. Inventory manager edits actual received items

Endpoint:
POST /inventory/review/<cart_id>

Body:

{
  "corrections": [
    { "internalId": "123-EN", "correctedCondition": "Lightly Played", "correctedQuantity": 2 }
  ],
  "notes": "Two LP, not NM"
}

What Happens:

Stores a new corrected intake section

Preserves original processed state

Allows later export of actual inventory import


🟥 NOT implemented


---

12. Manager confirms reviewed carts for import

Endpoint:
POST /inventory/finalize

Body:

{ "cartIds": ["abc123", "def456"] }

What Happens:

Aggregates product totals across all reviewed carts

Creates inventory_imports document with summary + per-cart breakdown


🟥 NOT implemented


---

13. Manager exports inventory to CSV

Endpoint:
GET /inventory/export/<import_id>?format=shopify_csv

What Happens:

Generates a .csv (or downloadable buffer) with product SKUs + quantities

Format depends on inventory system (Shopify, Square, etc.)


🟥 NOT implemented


---

14. Analytics: Spending by category, product, etc

Endpoint (example):
GET /analytics/spend_summary?categoryId=3&period=weekly

What Happens:

Aggregates processed or imported carts by category, group, or internalId

Returns total quantity + spend breakdown


🟥 NOT implemented


---

✅ Summary of Endpoint Coverage

Feature	Status	Notes

Search public buylist	✅ Implemented	
Register/Login/Auth	✅ Implemented	
Add to cart / view current cart / submit	✅ Implemented	
Emergency disables (category/group)	✅ Implemented	product-level disable not supported
View pending carts (employee)	✅ Implemented	
View single cart with discontinued detection	✅ Implemented	
Process cart with conditions + payout	✅ Implemented	
Cancel cart (customer or employee)	✅ Implemented	
Inventory review workflow	🟥 Missing	step-by-step review logic
Inventory correction and cart intake	🟥 Missing	needs actual vs processed state
Inventory import + CSV export	🟥 Missing	format per POS
Audit logs for all actions	✅ Implemented	
Admin UI for settings, emergency disable, progress, and buylist config	✅ Implemented	
Analytics endpoints for spend tracking	🟥 Missing	group/category/product filters



---

