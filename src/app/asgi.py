from app.app_entrypoint import create_app
from app.settings import DBSettings

DBSettings().setup_db()
app = create_app()
