from typing import Annotated
from datetime import timedelta
from fastapi import Depends, APIRouter, HTTPException, FastAPI
from core.auth import get_current_user, authenticate_user, create_access_token, bcrypt_context
from fastapi.security import OAuth2PasswordRequestForm
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from schemas.user import (CreateUserRequest, CourseCreate, CourseOut,
                          LessonCreate,
                          LessonOut, CommentOut,
                          CommentCreate, RatingOut, RatingCreate)
from starlette import status
from models.model import Course, Lesson, User, Comment, Rating
from models import model
from datetime import datetime



model.Base.metadata.create_all(bind=engine)
app = FastAPI()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

router_course = APIRouter(
    prefix="/course",
    tags=["course"]
)

router_lesson = APIRouter(
    prefix="/lesson",
    tags=["lesson"]
)

router_comment = APIRouter(
    prefix="/comments",
    tags=["stars"]
)


router_rating = APIRouter(
    prefix="/rating",
    tags=["rating"]
)




@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = User(
        username=create_user_request.username,
        password=bcrypt_context.hash(create_user_request.password),
    )

    db.add(create_user_model)
    db.commit()



@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return {"access_token": token, "token_type": "Bearer"}



@router.get("/user", status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return {"User": user}



@router_course.post("/course", status_code=status.HTTP_201_CREATED, response_model=CourseOut)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    db_course = Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course



@router_course.get("/", response_model=list[CourseOut])
def get_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()





@router_course.get("/{course_id}", response_model=CourseOut)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course




@router_course.put("/{course_id}", response_model=CourseOut)
def update_course(course_id: int, updated_course: CourseCreate, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    for key, value in updated_course.dict().items():
        setattr(course, key, value)
    db.commit()
    db.refresh(course)
    return course




@router_course.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(course)
    db.commit()
    return None



# --------------------------------------------------------------------------------------------



@router_lesson.post("/lesson", status_code=status.HTTP_201_CREATED, response_model=LessonOut)
def create_lesson(lesson: LessonCreate, db: Session = Depends(get_db)):
    db_lesson = Lesson(**lesson.dict())
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson


@router_lesson.get("/", response_model=list[LessonOut])
def get_lesson(db: Session = Depends(get_db)):
    return db.query(Lesson).all()



@router_lesson.get("/{lesson_id}", response_model=LessonOut)
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson



@router_lesson.put("/{lesson_id}", response_model=LessonOut)
def update_lesson(lesson_id: int, updated_lesson: LessonCreate, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    for key, value in updated_lesson.dict().items():
        setattr(lesson, key, value)
    db.commit()
    db.refresh(lesson)
    return lesson



@router_lesson.delete("/{lesson_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    db.delete(lesson)
    db.commit()
    return None

# --------------------------------------------------------------------------



@router_comment.post("/comment", status_code=status.HTTP_201_CREATED, response_model=CommentOut)
def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    db_comment = Comment(**comment.dict())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


@router_comment.get("/comment", response_model=list[CommentOut])
def get_comment(db: Session = Depends(get_db)):
    return db.query(Comment).all()



@router_comment.get("/{comment_id}", response_model=CommentOut)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment



@router_comment.put("/{comment_id}", response_model=CommentOut)
def update_comment(comment_id: int, updated_lesson: CommentCreate, db: Session = Depends(get_db)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    for key, value in updated_lesson.dict().items():
        setattr(comment, key, value)
    db.commit()
    db.refresh(comment)
    return comment



@router_comment.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    db.delete(comment)
    db.commit()
    return None



# -----------------------------------------------------------------------------------------



@router_rating.post("/rating", status_code=status.HTTP_201_CREATED, response_model=RatingOut)
def create_rating(rating: RatingCreate, db: Session = Depends(get_db)):
    db_rating = Rating(**rating.dict())
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating


@router_rating.get("/rating", response_model=list[RatingOut])
def get_rating(db: Session = Depends(get_db)):
    return db.query(Rating).all()



@router_rating.get("/{rating_id}", response_model=RatingOut)
def get_rating(rating_id: int, db: Session = Depends(get_db)):
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    return rating



@router_rating.put("/{rating_id}", response_model=RatingOut)
def update_rating(rating_id: int, updated_lesson: RatingCreate, db: Session = Depends(get_db)):
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    for key, value in updated_lesson.dict().items():
        setattr(rating, key, value)
    db.commit()
    db.refresh(rating)
    return rating


@router_rating.delete("/{rating_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rating(rating_id: int, db: Session = Depends(get_db)):
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    db.delete(rating)
    db.commit()
    return None




app.include_router(router)
app.include_router(router_course)
app.include_router(router_lesson)
app.include_router(router_comment)
app.include_router(router_rating)










