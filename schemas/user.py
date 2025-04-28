from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CreateUserRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str



class UserCreate(BaseModel):
    full_name: str
    email: str
    username: str
    password: str



class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    username: str
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    full_name: Optional[str]
    password: Optional[str]


# ----------------------------------------------------------------


class CourseCreate(BaseModel):
    title: str
    description: str
    author_id: int



class CourseOut(BaseModel):
    id: int
    title: str
    description: str
    author_id: int

    class Config:
        orm_mode = True


# --------------------------------------------------------

class LessonCreate(BaseModel):
    course_id: int
    title: str
    video_url: str
    content: str



class LessonOut(BaseModel):
    id: int
    course_id: int
    title: str
    video_url: str
    content: str

    class Config:
        orm_mode = True


# ----------------------------------------------------------------------------


class CommentCreate(BaseModel):
    lesson_id: int
    user_id: Optional[int] = None
    text: str
    created_at: Optional[datetime] = None

    # class Config:
    #     orm_mode = True



class CommentOut(BaseModel):
    id:int
    user_id: int
    lesson_id : int
    text: str
    created_at: datetime


    class Config:
        orm_mode = True


# -----------------------------------------------------------



class RatingCreate(BaseModel):
    user_id: int
    lesson_id: int
    stars: int = Field(..., ge=1, le=5)



class RatingOut(BaseModel):
    id: int
    user_id: int
    lesson_id : int
    stars: int = Field(..., ge=0, le=5)

    class Config:
        orm_mode = True



