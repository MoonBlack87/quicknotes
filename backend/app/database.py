from sqlmodel import SQLModel, create_engine, Session
from .config import settings

DB_PATH = settings.DATA_DIR / "quicknotes.db"
engine = create_engine(
    f"sqlite:///{DB_PATH}",
    connect_args={"check_same_thread": False},
    echo=False,
)
# Enable WAL mode for better concurrent reads
with engine.connect() as conn:
    conn.exec_driver_sql("PRAGMA journal_mode=WAL")


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
