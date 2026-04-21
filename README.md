# Sound Foundation Edtech Academy — Student Dashboard (Django)

This repository contains the backend for the Sound Foundation Edtech Academy student dashboard built with Django 6.0.

## Overview
- Custom user model with email-based authentication and OTP email verification.
- OTP flow: register -> receive OTP via email -> verify OTP -> account pending admin approval.
- Profile management with Cloudinary image uploads.
- Simple frontend templates and JS utilities included in `templates/` and `static/`.

## Quick start (development)
1. Create and activate a Python virtualenv:

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` in project root and set required environment variables (see next section).

4. Run migrations and create a superuser:

```bash
python manage.py migrate
python manage.py createsuperuser
```

5. Run the development server:

```bash
python manage.py runserver
```

6. Visit `http://localhost:8000`.

## Required environment variables
Create a `.env` file containing at least the following values for local testing:

```
DEBUG=True
SECRET_KEY=your_secret_key_here
DEFAULT_FROM_EMAIL=your-email@example.com
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...
```

Notes:
- For local development over HTTP, cookies created with `secure=True` will not be sent by browsers. If you see cookie-related issues during development, set the cookie `secure` flag to `False` in `account/views.py` for local testing only.

## OTP / Verification flow
- Token generation and verification use Django's `signing.dumps` / `signing.loads` with a salt (`account.utils.create_token`).
- The token is stored in an HttpOnly cookie named `otp_session_token` and validated during OTP verification.
- A resend-OTP API is available at `/auth/resend-otp/` (POST) — the frontend calls it via AJAX from the OTP verification page.

## Admin approval
After verifying OTP, user accounts are marked as `is_otp_verified=True` and then remain `is_active=False` until an admin approves them via the admin panel. Users are shown an "Awaiting approval" page and receive an admin notification email.

## Useful files & locations
- `account/views.py` — registration, login, OTP verification, resend API, profile
- `account/otp_models.py` — OTP model
- `account/utils/otp/` — `create_otp.py`, `verify_otp.py`
- `account/utils/create_token.py` — token creation/verification
- `templates/extends/auth/verify_otp.html` — OTP UI (60s resend timer)
- `templates/extends/auth/awaiting_approval.html` — awaiting approval page

## Running tests
(If you add tests) run:

```bash
python manage.py test
```

## Development notes
- Keep `.env` out of source control (it's in `.gitignore`).
- For production: set `DEBUG=False`, configure `ALLOWED_HOSTS`, use a proper email provider, enable HTTPS, and set `secure=True` on cookies.

## Contributing
Feel free to open issues or create pull requests for new features or fixes.

## License
Add your license here.
