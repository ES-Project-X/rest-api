from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, Float
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
from uuid import uuid4

# TODO: Implement cascade(?)

route_point = Table("route_point", Base.metadata,
    Column("route_id", Integer, ForeignKey("routes.id"), nullable=False, index=True),
    Column("point_id", Integer, ForeignKey("points.id"), nullable=False, index=True),
    Column("order", Integer, nullable=False)
) 

poi_status = Table("poi_status", Base.metadata,
    Column("poi_id", Integer, ForeignKey("pois.id"), nullable=False, index=True),
    Column("status_id", Integer, ForeignKey("status.id"), nullable=False, index=True)
)

route_status = Table("route_status", Base.metadata,
    Column("route_id", Integer, ForeignKey("routes.id"), nullable=False, index=True),
    Column("status_id", Integer, ForeignKey("status.id"), nullable=False, index=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, default=uuid4())
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    image_url = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow())
    total_xp = Column(Integer, default=0)
    birth_date = Column(DateTime, nullable=False)
    added_pois_count = Column(Integer, default=0)
    received_ratings_count = Column(Integer, default=0)
    given_ratings_count = Column(Integer, default=0)

class Point(Base):
    __tablename__ = "points"

    id = Column(Integer, primary_key=True, index=True, default=uuid4())
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    routes = relationship("Route", secondary=route_point, back_populates="points")

class POI(Point):
    __tablename__ = "pois"

    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    type = Column(String, nullable=False)
    added_by = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    picture_url = Column(String, nullable=False)
    rating_positive = Column(Integer, default=0)
    rating_negative = Column(Integer, default=0)
    status_history = relationship("Status", secondary=poi_status, back_populates="pois")

class UserPOI(Base):
    __tablename__ = "user_poi"

    id = Column(Integer, primary_key=True, index=True, default=uuid4())
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    poi_id = Column(Integer, ForeignKey("pois.id"), nullable=False, index=True)
    rating = Column(Integer, nullable=False)
    status_cooldown = Column(DateTime, nullable=False)

class Status(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True, index=True, default=uuid4())
    date = Column(DateTime, nullable=False)
    balance = Column(Integer, nullable=False)
    pois = relationship("POI", secondary=poi_status, back_populates="status_history")
    routes = relationship("Route", secondary=route_status, back_populates="status_history")

class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True, default=uuid4())
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    added_by = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    picture_url = Column(String, nullable=False)
    rating_positive = Column(Integer, default=0)
    rating_negative = Column(Integer, default=0)
    points = relationship("Point", secondary=route_point, back_populates="routes")
    status_history = relationship("Status", secondary=route_status, back_populates="routes")
