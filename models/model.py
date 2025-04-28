from datetime import datetime
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime




class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(225), unique=True, nullable=True)
    password = Column(String, nullable=True)



# ---------------------------------------------------------------------------------

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(225), nullable=True)
    description = Column(String(225), nullable=True)
    author_id = Column(Integer, ForeignKey("users.id"))


# ---------------------------------------------------------------------------------

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    title = Column(String(225), nullable=True)
    video_url = Column(String(225), nullable=True)
    content = Column(String(225), nullable=True)



# ----------------------------------------------------------------------------------

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    text = Column(String(225), nullable=True)
    created_at = Column(DateTime, default=datetime.now)



# ---------------------------------------------------------------------------------

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    stars = Column(Integer, nullable=True)
