from sqlalchemy import Column, Integer, String, ForeignKey, Table, Date, DateTime, Float, UUID, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import date, datetime
from uuid import uuid4

# TODO: Implement cascade(?)

route_point = Table("route_point", Base.metadata,
    Column("route_id", UUID, ForeignKey("routes.id"), nullable=False, index=True),
    Column("point_id", UUID, ForeignKey("points.id"), nullable=False, index=True),
    Column("order", Integer, nullable=True, index=True)
) 

poi_status = Table("poi_status", Base.metadata,
    Column("poi_id", UUID, ForeignKey("pois.id"), nullable=False, index=True),
    Column("status_id", UUID, ForeignKey("status.id"), nullable=False, index=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, index=True, default=uuid4)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    cognito_id = Column(String, unique=True, nullable=False, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    image_url = Column(String, default="https://img.myloview.com/stickers/default-avatar-profile-icon-vector-social-media-user-photo-700-205577532.jpg")
    created_at = Column(Date, default=date.today())
    total_xp = Column(Integer, default=0)
    birth_date = Column(Date, nullable=False)
    added_pois_count = Column(Integer, default=0)
    received_ratings_count = Column(Integer, default=0)
    given_ratings_count = Column(Integer, default=0)

class Point(Base):
    __tablename__ = "points"

    id = Column(UUID, primary_key=True, index=True, default=uuid4)
    latitude = Column(Float, nullable=False, index=True)
    longitude = Column(Float, nullable=False, index=True)
    routes = relationship("Route", secondary=route_point, back_populates="points")

class POI(Point):
    __tablename__ = "pois"

    id = Column(UUID, ForeignKey("points.id"), primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    type = Column(String, nullable=False)
    added_by = Column(UUID, ForeignKey("users.id"), nullable=False, index=True)
    picture_url = Column(String, nullable=False)
    rating_positive = Column(Integer, default=0)
    rating_negative = Column(Integer, default=0)

class UserPOI(Base):
    __tablename__ = "user_poi"

    id = Column(UUID, primary_key=True, index=True, default=uuid4)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False, index=True)
    poi_id = Column(UUID, ForeignKey("pois.id"), nullable=False, index=True)
    rating = Column(Boolean, nullable=False)
    existence_cooldown = Column(DateTime, nullable=False, default=datetime.now())
    last_status_given = Column(Date, nullable=True)

class Status(Base):
    __tablename__ = "status"

    id = Column(UUID, primary_key=True, index=True, default=uuid4)
    date = Column(Date, nullable=False, default=date.today())
    balance = Column(Integer, nullable=False, default=0)
    poi_id = Column(UUID, ForeignKey("pois.id"), nullable=False, index=True)

class Route(Base):
    __tablename__ = "routes"

    id = Column(UUID, primary_key=True, index=True, default=uuid4)
    name = Column(String, nullable=False)
    added_by = Column(UUID, ForeignKey("users.id"), nullable=False, index=True)
    points = relationship("Point", secondary=route_point, back_populates="routes")

class UserRoute(Base):
    __tablename__ = "user_route"

    id = Column(UUID, primary_key=True, index=True, default=uuid4)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False, index=True)
    route_id = Column(UUID, ForeignKey("routes.id"), nullable=False, index=True)
    rating = Column(Boolean, nullable=False)
    status_cooldown = Column(DateTime, nullable=False)
