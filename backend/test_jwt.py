
from auth_utils import create_access_token, verify_access_token

token = create_access_token(user_id=123)

print("Token generated:", bool(token))
print("Decoded payload:", verify_access_token(token))
print("Invalid token:", verify_access_token("not-a-valid-token"))
