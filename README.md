# Seed & Sprout

![GitHub Last Commit](https://img.shields.io/github/last-commit/PriyanshBordia/Slice-of-a-Pizza)
[![GitHub issues](https://img.shields.io/github/issues/PriyanshBordia/Slice-of-a-Pizza)](https://github.com/PriyanshBordia/Slice-of-a-Pizza/issues)
[![GitHub forks](https://img.shields.io/github/forks/PriyanshBordia/Slice-of-a-Pizza)](https://github.com/PriyanshBordia/Slice-of-a-Pizza/network)
[![GitHub stars](https://img.shields.io/github/stars/PriyanshBordia/Slice-of-a-Pizza)](https://github.com/PriyanshBordia/Slice-of-a-Pizza/stargazers)
[![GitHub license](https://img.shields.io/github/license/PriyanshBordia/Slice-of-a-Pizza)](https://github.com/PriyanshBordia/Slice-of-a-Pizza/blob/master/LICENSE)

A vegan restaurant ordering app — dine in or take away.

- Full ordering flow: menu browsing, topping customization, cart, checkout, order history
- Social authentication via Google and Apple (django-allauth)
- Dynamic UI with HTMX and Alpine.js — no heavy JS framework
- Dark mode, responsive layout, artisan design system (Tailwind CSS)
- Dockerized with PostgreSQL, CI via GitHub Actions

## Quick Start

Requires Docker and Docker Compose.

```bash
docker compose up
# Open http://localhost:8001
```

The entrypoint automatically runs migrations and collects static files on startup.

Then seed the menu:

```bash
docker compose exec web python manage.py seed_menu
```

To configure OAuth or email, copy `.env.example` to `.env` and fill in the relevant values.

## Features

### Ordering

- Browse menu by category (bowls, wraps, salads, smoothies, sides, desserts)
- Customize items with toppings
- HTMX-powered cart updates (no full page reloads)
- Checkout with optional order notes
- Order status tracking (placed, preparing, ready, completed)

### Authentication

- Username/password registration and login
- Google OAuth and Apple Sign-In
- Password reset via email

### UX

- Dark mode toggle (persisted in localStorage)
- Toast notifications
- Confetti animation on order placement
- Sticky category navigation
- Mobile-responsive design

## Tech Stack

| Category | Technology |
|----------|-----------|
| Backend | Django 4.2 (LTS), Python 3.11, Gunicorn (production) |
| Database | PostgreSQL 15 (SQLite fallback) |
| Frontend | Tailwind CSS, HTMX, Alpine.js |
| Auth | django-allauth (Google, Apple) |
| Infrastructure | Docker, Docker Compose, GitHub Actions |

## Project Structure

```
Slice-of-a-Pizza/
├── orders/                  # Main Django app
│   ├── models.py            # Core models (MenuItem, Topping, Cart, Order, etc.)
│   ├── views.py             # Menu, cart, checkout views
│   ├── templates/orders/    # HTML templates
│   ├── static/orders/       # CSS and icons
│   └── management/commands/ # seed_menu command
├── pizza/                   # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env.example
```

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | PostgreSQL connection string |
| `SECRET_KEY` | Django secret key |
| `DEBUG` | Enable debug mode |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts |
| `GOOGLE_OAUTH_CLIENT_ID` / `SECRET` | Google sign-in credentials |
| `APPLE_CLIENT_ID` / `SECRET` / `KEY_ID` / `PRIVATE_KEY` | Apple sign-in credentials |
| `EMAIL_HOST_USER` / `PASSWORD` | SMTP email credentials (optional) |

See `.env.example` for defaults. OAuth and email variables are optional — the app runs without them.

## Testing

```bash
docker compose run --rm web python manage.py test
```

Covers models, auth flows, cart operations, and checkout.

## License

MIT — see [LICENSE](LICENSE).
