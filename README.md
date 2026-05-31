# 🏋️ IronForge Gym Store

A full-featured Django ecommerce site for gym equipment with Stripe payments, user auth, and an admin dashboard — deployable to Heroku.

---

## Features

- 🛍️ Product catalog with category filtering & search
- 🛒 Session-based shopping cart
- 💳 Stripe Payments (PaymentIntents API)
- 👤 User registration, login, order history
- 📊 Staff dashboard + Django admin
- 🚀 Heroku-ready (PostgreSQL, WhiteNoise, Gunicorn)

---

## Local Setup

### 1. Clone & create a virtual environment
```bash
git clone <your-repo>
cd gymstore
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Create your `.env` file
```bash
cp .env.example .env
# Edit .env and fill in your Stripe keys and a secret key
```

### 3. Run migrations & seed data
```bash
python manage.py migrate
python manage.py seed_products       # Adds 10 sample products
python manage.py createsuperuser     # Create your admin user
```

### 4. Start the dev server
```bash
python manage.py runserver
```

Visit `http://localhost:8000`

---

## Stripe Setup

1. Create a free account at [stripe.com](https://stripe.com)
2. Go to **Developers → API Keys**
3. Copy your **Publishable key** (`pk_test_...`) and **Secret key** (`sk_test_...`) into `.env`
4. For webhooks (optional locally): `stripe listen --forward-to localhost:8000/webhooks/stripe/`

---

## Deploy to Heroku

### Prerequisites
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed
- Heroku account (free tier works)

### Steps

```bash
# 1. Login
heroku login

# 2. Create app
heroku create your-gymstore-name

# 3. Add PostgreSQL
heroku addons:create heroku-postgresql:essential-0

# 4. Set environment variables
heroku config:set SECRET_KEY="your-long-random-secret-key"
heroku config:set DEBUG="False"
heroku config:set STRIPE_PUBLIC_KEY="pk_live_..."
heroku config:set STRIPE_SECRET_KEY="sk_live_..."
heroku config:set STRIPE_WEBHOOK_SECRET="whsec_..."

# 5. Deploy
git init
git add .
git commit -m "Initial commit"
heroku git:remote -a your-gymstore-name
git push heroku main

# 6. Create superuser on Heroku
heroku run python manage.py createsuperuser

# 7. Seed sample products (optional)
heroku run python manage.py seed_products

# 8. Open your site
heroku open
```

### Stripe Webhook on Heroku

1. Go to [Stripe Dashboard → Webhooks](https://dashboard.stripe.com/webhooks)
2. Add endpoint: `https://your-gymstore-name.herokuapp.com/webhooks/stripe/`
3. Select event: `payment_intent.succeeded`
4. Copy the webhook signing secret into `heroku config:set STRIPE_WEBHOOK_SECRET=...`

---

## Admin Panel

- Django admin: `/admin/` — full model management
- Custom dashboard: `/dashboard/` — revenue, orders, products (staff users only)

---

## Project Structure

```
gymstore/
├── gymstore/          # Project settings & URLs
├── store/             # Products, cart, orders, Stripe
├── accounts/          # Auth (register, login, profile)
├── templates/         # All HTML templates
│   ├── base.html
│   ├── store/
│   └── accounts/
├── static/
│   ├── css/main.css
│   └── js/main.js
├── Procfile           # Heroku process file
├── runtime.txt        # Python version
└── requirements.txt
```

---

## Customisation

| What | Where |
|---|---|
| Store name / branding | `templates/base.html`, `static/css/main.css` |
| Colors | CSS variables in `static/css/main.css` |
| Add products | `/admin/` → Products → Add |
| Currency | `store/views.py` → `currency='eur'` |
| Email confirmation | Add `django.core.mail` to order creation in `store/views.py` |
