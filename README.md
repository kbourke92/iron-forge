# IronForge Gym Store

<a id="top"></a>

## Table of Contents

* [Live Project](#live-project)
* [Business Goals](#business-goals)
* [User Goals](#user-goals)
* [Agile Methodology](#agile-methodology)
* [Design](#design)
* [Data Model / ERD](#data-model--erd)
* [Features](#features)
* [Testing](#testing)
* [Validation](#validation)
* [Deployment](#deployment)
* [Security Features](#security-features)
* [Business Model & UX Rationale](#business-model--ux-rationale)
* [Future Features](#future-features)
* [Credits](#credits)
* [Licence](#licence)

---

IronForge Gym Store is a full-stack Django e-commerce application that allows customers to browse, purchase, and manage orders for gym and fitness equipment online.

The site is designed to provide a smooth and user-focused experience, from discovering products and filtering by category to securely completing purchases through Stripe and reviewing previous orders through a personalised account dashboard.

Built using Django, JS and Stripe, the application demonstrates full-stack development principles including user authentication, database management, payment processing, role-based access control, responsive design, and secure deployment practices. 

Key features include product search and filtering, session-based shopping cart functionality, Stripe payment integration, order history management, staff-only administration tools, and a custom business dashboard for monitoring store performance.

> This README documents the application structure, development decisions, features, testing strategy, and deployment process in line with full-stack e-commerce project assessment criteria. Full manual testing steps and validation evidence are provided in **TESTING.md**.

[Back to Top](#top)

---

## Live Project

* **Live Site:** INSERT LIVE URL
* **Repository:** https://github.com/kbourke92/iron-forge

[Back to Top](#top)

---

## Business Goals

* Provide a professional online platform for purchasing gym and fitness equipment.
* Deliver a streamlined ecommerce experience with minimal friction during checkout.
* Allow customers to browse, search, and filter products efficiently.
* Enable secure online payments through Stripe.
* Improve customer retention through user accounts and order history functionality.
* Provide staff users with effective inventory and order management tools.
* Create a scalable foundation for future ecommerce growth and feature expansion.

[Back to Top](#top)

---

## User Goals

* Browse gym equipment quickly and efficiently.
* Search for specific products using keywords.
* Filter products by category.
* View clear product information and pricing.
* Add, update, and remove items from a shopping cart.
* Complete purchases securely.
* Create an account and review previous orders.
* Manage personal account information.

[Back to Top](#top)

---

## Agile Methodology

* Managed using a GitHub Project Board.
* Development was organised using Agile principles and iterative releases.
* User stories were grouped into epics and prioritised using the MoSCoW framework.

### Epics

* Product Catalogue
* Shopping Cart
* Checkout & Payments
* User Authentication
* User Profiles
* Administration & Dashboard
* Deployment & Security

### MoSCoW Prioritisation

#### Must Have

* Product catalogue
* Search functionality
* Shopping cart
* Stripe checkout
* User registration and authentication
* Order history
* Product management

#### Should Have

* Category filtering
* Staff dashboard
* Responsive design
* Order management tools

#### Could Have

* Product reviews
* Wishlist functionality
* Promotional discounts
* Email notifications

### User Stories (Examples)

* As a registered user I can view previous orders so that I can track my purchases.
* As a staff member I can manage products so that inventory remains up to date.
* As an administrator I can monitor store activity through a dashboard so that business performance can be reviewed.


[Back to Top](#top)

---

## Design

* **Wireframes** (created during the planning phase and stored in `docs/readme/`):

  * Homepage
  * Product Listing Page
  * Product Detail Page
  * Shopping Cart
  * Checkout
  * User Profile
  * Staff Dashboard

* **Typography:** Modern sans-serif typography selected for readability and professional presentation.

* **Colour Palette:** Industrial-inspired colour scheme reflecting the IronForge fitness brand with dark neutrals, strong contrast, and high-visibility call-to-action elements.

* **Responsiveness:** Built using Bootstrap's responsive grid system to ensure full functionality across desktop, tablet, and mobile devices.

### Data Model / ERD

![ERD](docs/readme/erd.png)

The application uses a relational database structure consisting of:

* Users
* Profiles
* Categories
* Products
* Orders
* Order Items

Relationships are designed to support efficient product management, customer ordering, and administrative reporting.

[Back to Top](#top)
