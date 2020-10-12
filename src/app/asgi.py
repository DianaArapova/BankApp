from app.app_entrypoint import create_app, configure_app_handlers
from app.settings import DBSettings, AppSettings

DBSettings().setup_db()
app = create_app()
configure_app_handlers(app, AppSettings())
