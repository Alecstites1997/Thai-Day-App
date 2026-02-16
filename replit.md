# Thai Day App

## Overview

Thai Day App is a simple food ordering web application for a "Thai Day" event. It allows users to submit Thai food orders through a public-facing form, and provides an admin interface for viewing and managing those orders. Orders are stored in a local JSON file (`orders.json`).

- **User-facing page**: A form where people enter their name, order (e.g., Pad Thai), and optional notes (allergies, special requests).
- **Admin page**: A table view of all submitted orders with the ability to delete individual orders or clear all orders. Protected by a simple query parameter key (`thaiday2025`).
- **Thank you page**: Confirmation shown after successful order submission.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend: Flask (Python)
- The app uses **Flask** as its web framework, serving server-rendered HTML templates.
- Routes handle order submission (`POST /`), order display (`GET /`), a thank-you page (`/thanks`), and admin operations (`/admin`, `/admin/delete/<id>`, `/admin/clear`).
- The `main.py` file contains all route logic in a single file — there is no separation into blueprints or modules. This is appropriate given the app's small scope.

### Data Storage: JSON File
- Orders are persisted in a local `orders.json` file on disk.
- `load_orders()` and `save_orders()` functions handle reading/writing the JSON file.
- Order IDs are assigned sequentially based on the current length of the orders list (`len(orders) + 1`), which means IDs can collide after deletions. If this becomes a problem, consider using UUIDs or a proper database.
- **No database is used.** If scaling is needed, consider migrating to SQLite or PostgreSQL.

### Templating: Jinja2
- Flask's built-in Jinja2 templating renders all HTML pages from the `templates/` directory.
- Templates: `index.html` (order form), `thanks.html` (confirmation), `admin.html` (order management), `locked.html` (unauthorized access).

### Authentication
- Admin access is protected by a simple query parameter key: `?key=thaiday2025`. This is not secure authentication — it's a basic access gate suitable for a small internal/event app.
- There is no user authentication for placing orders.

### GitHub Integration (Optional)
- `push_github.py` contains code to push files to a GitHub repository using Replit's GitHub connector. It uses the `PyGithub` library and attempts to read an OAuth access token from Replit's connector API. This is a utility script, not part of the main app flow.

### Key Design Decisions
- **Single-file architecture**: All backend logic lives in `main.py`. This keeps things simple for a small app.
- **File-based storage over database**: Chosen for simplicity. The tradeoff is no concurrent write safety and no query capabilities. Fine for low-traffic event use.
- **No CSS framework**: Minimal inline styles in templates. The app is intentionally simple and functional.

## External Dependencies

### Python Packages
- **Flask**: Web framework for routing and templating.
- **PyGithub**: Used only in `push_github.py` for optional GitHub integration (not required for the main app).

### Runtime
- **Python 3**: The app runs as a standard Python Flask application.
- No external databases, APIs, or third-party services are required for core functionality.
- No environment variables are required for the main app (the admin key is hardcoded as `thaiday2025`).

### Deployment
- Deployed on Replit at `https://thai-day-app--alecstites1997.replit.app`.
- Flask's built-in development server is likely used; for production, consider adding Gunicorn.