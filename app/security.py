from fastapi_login import LoginManager
from .config import settings
manager = LoginManager(
    secret=settings.secret_key_admin, token_url="/login", use_cookie=True)
manager.cookie_name = "auth"


@manager.user_loader()
async def get_user_data(email: str):
    return email
