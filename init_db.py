from app import create_app, db
from app.models import Genre

GENRES = [
    (28, "Action"),
    (12, "Adventure"),
    (16, "Animation"),
    (35, "Comedy"),
    (80, "Crime"),
    (99, "Documentary"),
    (18, "Drama"),
    (10751, "Children"),
    (14, "Fantasy"),
    (36, "History"),
    (27, "Horror"),
    (10402, "Musical"),
    (9648, "Mystery"),
    (10749, "Romance"),
    (878, "Sci-fi"),
    (10770, "TV Movie"),
    (53, "Thriller"),
    (10752, "War"),
    (37, "Western"),
]

def seed_genres():
    for gid, name in GENRES:
        if not db.session.get(Genre, gid):
            db.session.add(Genre(id=gid, name=name.strip()))

    db.session.commit()
    print("Genres seeded")


def init_db():
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Database tables created")
        seed_genres()


if __name__ == "__main__":
    init_db()