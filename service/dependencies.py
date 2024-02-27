from persistence.sqlite_db import SessionLocal


DEFAULT_PAGE_SIZE = 5


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
