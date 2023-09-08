from fastapi import FastAPI, HTTPException, Response, status, APIRouter
from fastapi.params import Body, Depends
# here pydantic is the library which is already in env because we have used fastapi[all]
from typing import Optional, List
from ..database import engine, get_db
from .. import models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func

# Binding the models
models.Base.metadata.create_all(bind=engine)

# tags params is used to add tag for FastAPI doc, It's not required
router = APIRouter(
    tags=['Posts']
)

# we can set limit params to set the limit of retrive data
# in orm we can use it like db.query(models.Post).limit(limit).all()

# we can skip the results as well through set the skip params in method
# in orm we can use it like db.query(models.Post).offset(skip).all()

# we can search the results as well through set the search params in method like search:optional[str] = ""
# in orm we can use it like db.query(models.Post).filter(models.Post.title.contains(search))




@router.get("/posts",response_model=List[schemas.GetPost])
def get_posts(db:Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user)):

    # ...... SQL code ......
    '''
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    '''
    # ...... ORM CODE ......
    
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id)
    # Left Outer Join
    '''
    results = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id == models.Post.id, isouter=True
    ).group_by(models.Post.id).all()
    print(results)
    '''
    # return {'data':posts}
    return posts


@router.post("/create_new_posts")
def create_new_posts(new_posts:schemas.Post, db:Session = Depends(get_db), 
                     current_user: int = Depends(oauth2.get_current_user)):
    # we can convert the variable in dict as well
    # print(new_posts.dict())

    # ...... SQL code ......
    '''
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) 
                   RETURNING * """,
                   (new_posts.title,new_posts.content,new_posts.published))
    new_cursor = cursor.fetchone()
    conn.commit()
    '''
    # ...... ORM CODE ......

    # Below print statement convert the new_posts in dict and ** unpack the fields
    # print(**new_posts.dict())
    '''
    new_cursor = models.Post(
        title=new_posts.title, content=new_posts.content, published= new_posts.published
        )
    '''
    new_cursor = models.Post(owner_id=current_user.id,**new_posts.dict())
    db.add(new_cursor)
    db.commit()
    db.refresh(new_cursor)
    return {"data" : new_cursor}

@router.get("/posts/{id}",response_model=schemas.GetPost)
def get_post(id:int,db:Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):

    # ...... SQL code ......
    '''
    cursor.execute(""" SELECT * FROM posts WHERE ID = %s """,(str(id),))
    new_cursor = cursor.fetchone()
    '''
    # ...... ORM code ......
    # new_cursor = db.query(models.Post).filter(models.Post.id == id).all()
    new_cursor = db.query(models.Post).filter(models.Post.id == id).first()

    
    if not new_cursor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} not found")
    if new_cursor.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not autherized to perform requested Item")
    
    # return {'data':new_cursor}
    return new_cursor

@router.delete("/posts/{id}")
def delete_post(id:int, db:Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):

    # ...... SQL code ......
    '''
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """,(str(id),))
    new_cursor = cursor.fetchone()
    conn.commit()
    '''
    # ...... ORM code ......
    new_cursor = db.query(models.Post).filter(models.Post.id == id)
    post = new_cursor.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not autherized to perform requested Item")
    new_cursor.delete(synchronize_session=False)
    db.commit()
    return {'data':'Record deleted'}


@router.post("/update_posts/{id}")
def update_post(id:int,updated_posts:schemas.Post, db:Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # we can convert the variable in dict as well
    # print(new_posts.dict())
    # ...... SQL code ......
    '''
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s 
                   WHERE id = %s RETURNING * """,
                   (new_posts.title,new_posts.content,new_posts.published,str(id)))
    new_cursor = cursor.fetchone()
    conn.commit()
    '''
    # ...... ORM code ......
    update_query = db.query(models.Post).filter(models.Post.id == id)
    new_cursor = update_query.first()
    
    
    if new_cursor == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} not found")
    
    if new_cursor.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not autherized to perform requested Item")
    
    update_query.update(updated_posts.dict(),synchronize_session=False)
    db.commit()
    
    return {"data" : update_query.first()}
