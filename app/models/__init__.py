from app.db.session import Base

# Import model modules here so Alembic or create_all can discover them
from app.models.user import User  # noqa: F401
from app.models.service import Service  # noqa: F401
from app.models.blog import BlogPost  # noqa: F401
from app.models.lead import Lead  # noqa: F401
from app.models.header import HeaderColumn, ComboboxItem  # noqa: F401
