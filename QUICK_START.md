# Sound Foundation Edtech Academy - Quick Start Guide

## Project Structure
```
student-dashboard-be/
├── core/                          # Project settings & URLs
│   ├── settings.py               # Django configuration
│   ├── urls.py                   # Main URL routes
│   └── views.py                  # Home view
│
├── account/                       # User authentication app
│   ├── models.py                 # CustomUser & Profile models
│   ├── views.py                  # Auth views (register, login, etc.)
│   ├── urls.py                   # Auth URL routes
│   ├── forms.py                  # Registration & Profile forms
│   └── migrations/               # Database migrations
│
├── templates/
│   ├── base.html                 # Main template (all pages extend)
│   ├── home.html                 # Homepage
│   ├── includes/
│   │   └── nav-bar/
│   │       └── nav.html          # Navigation bar
│   └── extends/
│       ├── auth/
│       │   ├── register.html     # Registration page
│       │   ├── login.html        # Login page
│       │   └── verify_otp.html   # OTP verification
│       └── pages/
│           └── profile.html      # User profile page
│
├── static/
│   ├── assets/
│   │   └── logo.svg              # SFEA logo
│   ├── css/
│   │   └── style.css             # Main stylesheet
│   └── js/
│       └── main.js               # JavaScript utilities
│
└── manage.py                      # Django management script
```

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py migrate
```

### 3. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 4. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 5. Run Development Server
```bash
python manage.py runserver
```

The server will start at `http://localhost:8000`

## Page Routes

### Public Pages
- `/` - Homepage
- `/auth/register/` - User registration
- `/auth/login/` - User login
- `/auth/verify-otp/` - OTP verification

### Protected Pages (Login Required)
- `/auth/profile/` - User profile & settings

### Admin Pages
- `/admin/` - Django admin panel

## Key Features

### 1. User Registration
- Email, name, phone, registration number
- Password with strength requirements
- OTP verification
- Email confirmation

### 2. User Login
- Email & password authentication
- OTP verification for unverified accounts
- Auto-redirect to profile on success

### 3. User Profile
- View account information
- Upload profile picture
- Status indicators (verified, active)
- Account logout

### 4. Navigation
- Dynamic navbar based on auth status
- User dropdown menu when logged in
- Mobile-responsive design
- Logo and branding

## User Roles

```
STUDENT    - Regular student user
INSTRUCTOR - Instructor/Teacher
ADMIN      - Administrator access
```

## Database Models

### CustomUser
```python
- email (unique)
- first_name
- last_name
- phone_number
- student_reg_no
- role (STUDENT/INSTRUCTOR/ADMIN)
- is_active
- is_otp_verified
- is_staff
```

### Profile
```python
- user (OneToOneField)
- profile_picture (ImageField)
```

## Form Fields & Validation

### Registration Form
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| email | Email | ✓ | Must be unique |
| first_name | Text | | Max 30 chars |
| last_name | Text | | Max 30 chars |
| phone_number | Text | | Max 15 chars |
| student_reg_no | Text | ✓ | Max 20 chars |
| role | Choice | ✓ | STUDENT/INSTRUCTOR/ADMIN |
| password | Password | ✓ | Min 8 chars, numbers + letters |

### Login Form
| Field | Type | Required |
|-------|------|----------|
| email | Email | ✓ |
| password | Password | ✓ |

### Profile Form
| Field | Type | Required |
|-------|------|----------|
| profile_picture | Image | | Max 5MB, JPG/PNG |

## Testing User Flows

### New User Registration
1. Click "Get Started" or visit `/auth/register/`
2. Fill registration form
3. Check email for OTP code
4. Enter OTP at `/auth/verify-otp/`
5. Redirected to login
6. Login with email/password
7. Redirected to `/auth/profile/`

### Existing User Login
1. Visit `/auth/login/`
2. Enter email & password
3. Redirected to `/auth/profile/`

### Upload Profile Picture
1. Go to `/auth/profile/`
2. Click "📤 Upload Photo"
3. Select image file
4. Click "💾 Save Changes"
5. Picture displays in profile

## Customization

### Change Colors
Edit `static/css/style.css`:
```css
:root {
  --primary-dark-orange: #d2691e;
  --primary-orange: #ff8c00;
  --primary-black: #1a1a1a;
  --primary-brown: #6b4423;
}
```

### Modify Templates
All HTML pages extend `base.html`. Edit blocks:
```django
{% block title %}Page Title{% endblock %}
{% block extra_css %}Optional CSS{% endblock %}
{% block content %}Page content{% endblock %}
{% block extra_js %}Optional JS{% endblock %}
```

### Add New Pages
1. Create template in `templates/extends/pages/`
2. Extend `base.html`
3. Add view in `account/views.py` or create new app
4. Add route in `account/urls.py` or app-specific urls
5. Include in `core/urls.py`

## Environment Variables Required

In `.env` file:
```
CLOUD_NAME=your_cloudinary_name
API_KEY=your_cloudinary_key
API_SECRET=your_cloudinary_secret

SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
EMAIL=noreply@sfea.com

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_USE_TLS=True
```

## Common Issues & Solutions

### Static files not loading
```bash
python manage.py collectstatic --noinput
```

### Profile picture not uploading
- Check Cloudinary credentials in `.env`
- Ensure `pillow` is installed: `pip install pillow`

### OTP not received
- Check SMTP settings in `.env`
- Test email configuration in Django shell

### Login not redirecting
- Verify `LOGIN_URL = 'login'` in `settings.py`
- Check URL name matches: `name='login'`

## Development Workflow

1. **Create new feature**: Create branch
2. **Add views**: In `account/views.py`
3. **Create template**: In `templates/`
4. **Add routes**: In `account/urls.py`
5. **Test**: Visit URL and verify
6. **Commit**: Git commit changes
7. **Push**: Deploy to server

## Production Checklist

- [ ] Update `DEBUG = False` in settings
- [ ] Set `ALLOWED_HOSTS` in settings
- [ ] Use environment variables for secrets
- [ ] Run migrations on production database
- [ ] Collect static files: `python manage.py collectstatic`
- [ ] Set up SSL/HTTPS
- [ ] Configure email service
- [ ] Set up database backups
- [ ] Monitor error logs

## Support & Resources

- Django Documentation: https://docs.djangoproject.com/
- Cloudinary: https://cloudinary.com/
- Bootstrap (if used): https://getbootstrap.com/

---

**Last Updated**: April 20, 2026
**Version**: 1.0
**Status**: Ready for Development
