from app.settings import DBSettings
from app.app_entrypoint import create_app


DBSettings().setup_db()
app = create_app()
