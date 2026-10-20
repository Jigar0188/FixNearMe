
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Table,
    Text,
    Time,
    text,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


# Many-to-many association table
professional_services = Table(
    "professional_services",
    Base.metadata,
    Column(
        "professional_id",
        Integer,
        ForeignKey("professional_profiles.id"),
        primary_key=True,
    ),
    Column(
        "service_id",
        Integer,
        ForeignKey("services.id"),
        primary_key=True,
    ),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    created_at = Column(
    DateTime,
    nullable=True,
    server_default=text("CURRENT_TIMESTAMP")
)

    professional_profile = relationship(
        "ProfessionalProfile",
        back_populates="user",
        uselist=False,
    )

    customer_bookings = relationship(
        "Booking",
        back_populates="customer",
        foreign_keys="Booking.customer_id",
    )

    reviews = relationship(
        "Review",
        back_populates="customer",
        foreign_keys="Review.customer_id",
    )


class ProfessionalProfile(Base):
    __tablename__ = "professional_profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False,
    )
    experience_years = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    service_area = Column(String, nullable=True)
    hourly_rate = Column(Numeric, nullable=True)
    is_available = Column(Boolean, nullable=True)
    rating = Column(Float, nullable=True)

    user = relationship(
        "User",
        back_populates="professional_profile",
    )

    services = relationship(
        "Service",
        secondary=professional_services,
        back_populates="professionals",
    )

    bookings = relationship(
        "Booking",
        back_populates="professional",
    )

    reviews = relationship(
        "Review",
        back_populates="professional",
    )


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)

    professionals = relationship(
        "ProfessionalProfile",
        secondary=professional_services,
        back_populates="services",
    )

    bookings = relationship(
        "Booking",
        back_populates="service",
    )


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    customer_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )
    professional_id = Column(
        Integer,
        ForeignKey("professional_profiles.id"),
        nullable=False,
    )
    service_id = Column(
        Integer,
        ForeignKey("services.id"),
        nullable=False,
    )
    service_description = Column(Text, nullable=True)
    address = Column(String, nullable=False)
    scheduled_date = Column(Date, nullable=False)
    scheduled_time = Column(Time, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=True, server_default=text("CURRENT_TIMESTAMP"))

    customer = relationship(
        "User",
        back_populates="customer_bookings",
        foreign_keys=[customer_id],
    )

    professional = relationship(
        "ProfessionalProfile",
        back_populates="bookings",
    )

    service = relationship(
        "Service",
        back_populates="bookings",
    )

    review = relationship(
        "Review",
        back_populates="booking",
        uselist=False,
    )


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    booking_id = Column(
        Integer,
        ForeignKey("bookings.id"),
        unique=True,
        nullable=False,
    )
    customer_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )
    professional_id = Column(
        Integer,
        ForeignKey("professional_profiles.id"),
        nullable=False,
    )
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=True)

    booking = relationship(
        "Booking",
        back_populates="review",
    )

    customer = relationship(
        "User",
        back_populates="reviews",
        foreign_keys=[customer_id],
    )

    professional = relationship(
        "ProfessionalProfile",
        back_populates="reviews",
    )
