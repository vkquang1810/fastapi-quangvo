from typing import List, Optional

from sqlalchemy import or_, func, outerjoin

from .. import models, schemas, oauth2
from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response
from ..database import engine, SessionLocal, get_db

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.PostOut])
def get_all_posts(
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user),
        limit: int = 10,
        skip: int = 0,
        search: Optional[str] = None
):
    # Base query to get all posts by the current user
    query = db.query(models.Post).filter(models.Post.owner_id == current_user.id)

    # Filter the posts based on the search string
    if search is not None:
        search_str = f"%{search}%"
        query = query.filter(
            or_(
                models.Post.title.ilike(search_str),
                models.Post.content.ilike(search_str)
            )
        )

    # Apply limit and offset to the query
    posts = query.limit(limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()


    print(results)
    return results





@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.dict(), owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{post_id}", response_model=schemas.PostOut)
def get_post_by_id(post_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == post_id).first()
    if post:
        return post
    else:
        raise HTTPException(status_code=404, detail="Post not found")


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id).first()

    if deleted_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform request action")

    db.delete(deleted_post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    existing_post = db.query(models.Post).filter(models.Post.id == id).first()

    if existing_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if existing_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform request action")

    existing_post.title = post.title
    existing_post.content = post.content
    existing_post.published = post.published
    db.commit()

    return existing_post
