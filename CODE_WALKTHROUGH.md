# Code Walkthrough - Sound Foundation Edtech Academy

## 1. Authentication Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    AUTHENTICATION FLOW                       │
└─────────────────────────────────────────────────────────────┘

NEW USER:
  Register Form → Validation → Create User (is_active=False)
       ↓                    ↓
   (GET/POST)          Create OTP
       ↓                    ↓
  register.html       send_otp_email()
                           ↓
  ┌────────────────────────────────────┐
  │     /auth/verify-otp/              │
  │  (Session Token Stored)            │
  └────────────────────────────────────┘
       ↓
  User enters OTP
       ↓
  verify_otp(user, otp) → is_otp_verified = True
       ↓
  Redirect to login
  ┌────────────────────────────────────┐
  │  Account now pending admin approval │
  └────────────────────────────────────┘

LOGIN:
  Email + Password → authenticate() → Successful
       ↓
  login(request, user)
       ↓
  Redirect to /auth/profile/
  ┌────────────────────────────────────┐
  │   User Dashboard (Profile Page)     │
  │ - View Info                         │
  │ - Upload Picture                    │
  │ - See Status                        │
  │ - Logout                            │
  └────────────────────────────────────┘

LOGOUT:
  Click Logout → user_logout()
       ↓
  logout(request)
       ↓
  Redirect to home
```

## 2. View Function Explanations

### views.py - register()
```python
def register(request):
    # Line 1-8: Check if email already exists & is verified
    # Line 9-14: If exists but not verified, resend OTP
    # Line 15-28: Create new user, set inactive, generate OTP
    # Line 29: Store session token for OTP verification
    # Line 30: Return form on GET request
```

**Key Points:**
- Prevents duplicate registrations
- Uses session to track OTP verification progress
- Password handled by form (not plain text)
- User is_active=False until verified

### views.py - user_login()
```python
def user_login(request):
    # Check if user exists
    # If verified: authenticate & login
    # If not verified: show OTP verification prompt
    # If doesn't exist: show registration prompt
```

**Key Points:**
- Uses Django authenticate() function
- Checks OTP verification status
- Redirects based on account state

### views.py - verify_otp_view()
```python
def verify_otp_view(request):
    # Get OTP from form & session token
    # Verify token & get user ID
    # Check OTP validity
    # Mark user as verified
    # Notify admins of new user
    # Redirect to login
```

**Key Points:**
- Verifies token before processing
- Sets is_otp_verified flag
- Sends admin notification email

### views.py - profile()
```python
@login_required  # Decorator - redirects unauthenticated users
def profile(request):
    # Get user's profile object
    # If POST: Save profile picture
    # If GET: Display profile form
    # Render profile template with form
```

**Key Points:**
- Protected by @login_required decorator
- Gets Profile via OneToOneField
- Handles file uploads securely
- Cloudinary storage configured

### views.py - user_logout()
```python
def user_logout(request):
    logout(request)  # Clears session
    messages.success(...)  # User feedback
    return redirect('home')  # Back to homepage
```

## 3. Template Context Variables

### Available in all templates:
```django
{{ user }}                    # Current user object
{{ user.email }}              # User email
{{ user.is_authenticated }}   # Boolean - is user logged in?
{{ user.first_name }}         # First name
{{ user.last_name }}          # Last name
{{ user.profile.profile_picture }} # Profile image
{{ messages }}                # Django messages list
```

### In register.html:
```django
{{ form }}                    # Registration form
{{ form.email }}              # Email field
{{ form.password }}           # Password field
{{ form.email.errors }}       # Field-specific errors
{{ form.non_field_errors }}   # General form errors
```

### In profile.html:
```django
{{ request.user.profile.profile_picture.url }}  # Image URL
{{ request.user.get_role_display }}             # Role name
{{ request.user.is_active }}                    # Account active?
{{ request.user.is_otp_verified }}              # Email verified?
```

## 4. URL Routing Flow

```
┌─ User visits URL
│
├─ / (home) 
│  └─ core/views.py → home() → templates/home.html
│
├─ /auth/register/
│  └─ account/views.py → register() → templates/extends/auth/register.html
│
├─ /auth/login/
│  └─ account/views.py → user_login() → templates/extends/auth/login.html
│
├─ /auth/verify-otp/
│  └─ account/views.py → verify_otp_view() → templates/extends/auth/verify_otp.html
│
├─ /auth/profile/
│  └─ @login_required → account/views.py → profile() → templates/extends/pages/profile.html
│
└─ /auth/logout/
   └─ @login_required → account/views.py → user_logout() → redirect home
```

## 5. Form Data Flow

### Registration Form Submission:
```
User fills form
      ↓
HTML <form method="POST"> → Django view
      ↓
form = CustomUserCreationForm(request.POST)
      ↓
form.is_valid() → Validates all fields
      ↓
form.save() → Saves to database
      ↓
Redirect to OTP verification
```

### Profile Picture Upload:
```
User selects file
      ↓
<form enctype="multipart/form-data">
      ↓
Django receives request.FILES
      ↓
ProfileForm(request.POST, request.FILES)
      ↓
form.save() → Upload to Cloudinary
      ↓
Image URL stored in database
      ↓
Display in profile.html
```

## 6. Security Features

### CSRF Protection
```django
<form method="POST">
    {% csrf_token %}  <!-- Prevents cross-site attacks -->
    ...
</form>
```

### Password Security
```python
form = CustomUserCreationForm(request.POST)
# Password never stored as plain text
# Django uses default hasher (PBKDF2)
# Password field type="password" in HTML
```

### Authentication Decorators
```python
@login_required
def profile(request):
    # Redirects to LOGIN_URL if not authenticated
    # Prevents unauthorized access
```

### Session Management
```python
login(request, user)   # Creates session
logout(request)        # Destroys session
request.user           # Accesses current user from session
```

## 7. Database Relationships

```
CustomUser (1)
    ↓
    └──→ OneToOneField ←──── Profile (1)
         (user field)         

One CustomUser → One Profile
Each user can only have one profile
Each profile belongs to exactly one user
```

## 8. Message System Usage

### Sending Messages:
```python
from django.contrib import messages

messages.success(request, 'Registration successful!')
messages.error(request, 'Email already exists.')
messages.info(request, 'Please check your email.')
messages.warning(request, 'Action required.')
```

### Displaying Messages:
```django
{% if messages %}
    {% for message in messages %}
        <div class="alert alert-{{ message.tags }}">
            {{ message }}
        </div>
    {% endfor %}
{% endif %}
```

## 9. Static Files & Media

### Static Files (CSS, JS, Images):
```
/static/css/style.css      → Downloaded once
/static/js/main.js         → Downloaded once
/static/assets/logo.svg    → Downloaded once
```

### Media Files (User Uploads):
```
Profile pictures → Cloudinary Storage
Accessed via: request.user.profile.profile_picture.url
```

## 10. Template Inheritance Chain

```
base.html (Main template)
│
├── Includes: nav.html (Navigation)
│
├── Extends to: home.html
│   └── Overrides: {% block content %}
│
├── Extends to: register.html
│   └── Overrides: {% block title %}, {% block content %}
│
├── Extends to: login.html
│   └── Overrides: {% block title %}, {% block content %}
│
├── Extends to: verify_otp.html
│   └── Overrides: {% block title %}, {% block content %}
│
└── Extends to: profile.html
    └── Overrides: {% block title %}, {% block extra_css %}, {% block content %}
```

## 11. Common Patterns in Code

### Pattern 1: Check User State
```python
if request.user.is_authenticated:
    # User is logged in
else:
    # User is not logged in
```

### Pattern 2: Redirect on Condition
```python
if user.is_otp_verified:
    # Proceed with login
else:
    # Redirect to OTP verification
    return redirect('otp_verification')
```

### Pattern 3: Save Form Data
```python
if form.is_valid():
    instance = form.save(commit=False)  # Don't save yet
    instance.is_active = False           # Modify before save
    instance.save()                      # Now save
```

### Pattern 4: Conditional Template Rendering
```django
{% if user.is_authenticated %}
    <!-- Show for logged-in users -->
{% else %}
    <!-- Show for logged-out users -->
{% endif %}
```

## 12. Error Handling

### Try-Except Pattern:
```python
try:
    user = CustomUser.objects.get(email=email)
except CustomUser.DoesNotExist:
    # Handle user not found
```

### Form Validation:
```python
if form.is_valid():
    # Process valid data
else:
    # Render form with errors
    return render(request, 'template.html', {'form': form})
```

### Display Field Errors:
```django
{% if form.email.errors %}
    <span class="error">{{ form.email.errors.0 }}</span>
{% endif %}
```

---

**This walkthrough covers the core concepts. Study each section and trace the code flow when implementing new features.**
