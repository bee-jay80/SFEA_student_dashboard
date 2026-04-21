from django.core import signing
import uuid

# Use a unique salt for OTP verification tokens so tokens for different
# purposes cannot be replayed across features.
SALT = 'account-otp-verification'


def create_verification_token(user_or_id, include_nonce=False):
    """Create a signed token containing the `user_id`.

    Accepts either a `CustomUser` instance or a user id (UUID/string).
    If `include_nonce` is True a random nonce will be included (useful
    when you also persist the nonce server-side to allow revocation).
    """
    # normalize user id
    try:
        user_id = str(user_or_id.id)
    except Exception:
        user_id = str(user_or_id)

    payload = {'user_id': user_id}
    if include_nonce:
        payload['nonce'] = str(uuid.uuid4())

    return signing.dumps(payload, salt=SALT)


def verify_verification_token(token, max_age=900):
    """Verify a token and return the payload dict on success, or None.

    `max_age` is in seconds (default 900 = 15 minutes).
    """
    try:
        data = signing.loads(token, salt=SALT, max_age=max_age)
        return data
    except (signing.BadSignature, signing.SignatureExpired):
        return None
