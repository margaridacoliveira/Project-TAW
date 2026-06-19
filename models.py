from peewee import *
from datetime import datetime

db = SqliteDatabase('database.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    name = CharField()
    email = CharField(unique=True)
    password = CharField()
    is_admin = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'users'


class Category(BaseModel):
    name = CharField(unique=True)

    class Meta:
        table_name = 'categories'


class Event(BaseModel):
    title = CharField()
    description = TextField()
    date = DateTimeField()
    location = CharField()
    organizer = CharField()
    category = ForeignKeyField(Category, backref='events', null=True)
    max_participants = IntegerField(null=True)
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'events'

    def is_full(self):
        """Check if event has reached maximum participants"""
        if self.max_participants is None:
            return False
        return self.registrations.count() >= self.max_participants

    def available_spots(self):
        """Get number of available spots"""
        if self.max_participants is None:
            return None
        return max(0, self.max_participants - self.registrations.count())


class Registration(BaseModel):
    user = ForeignKeyField(User, backref='registrations')
    event = ForeignKeyField(Event, backref='registrations')
    registered_at = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'registrations'
        indexes = (
            (('user', 'event'), True),  # Unique constraint
        )


def create_tables():
    """Create all database tables"""
    with db:
        db.create_tables([User, Category, Event, Registration])


def initialize_db():
    """Initialize database connection and create tables if needed"""
    db.connect(reuse_if_open=True)
    create_tables()
