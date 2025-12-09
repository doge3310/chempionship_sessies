from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
import uvicorn
from db_init import UserAPI, Docs, Comment
from jwt_cr import create_jwt
from hash_password import verify


app = FastAPI()
route = APIRouter(prefix="/api/v1")


class AddComment(BaseModel):
    text: str
    date_created: str
    date_updated: str
    author_id: int


@route.post("/SignIn")
async def signin(password, username):
    user = UserAPI.get_or_none(name=username)
    dct_user = user.__data__

    if verify(password, user.password):
        return create_jwt(dct_user, 1)


@route.get("/Documents")
async def get_docs():
    return Docs.select().dicts()


@route.get("/Document/{documentId}/Comments")
async def get_comments(documentId: int):
    comments = []

    for i in Comment.select():
        data = i.__data__

        if data["document_id"] == documentId:
            comments.append(data["text"])

    return comments


@route.post("/Document/{documentId}/Comment")
async def create_comment(documentId: str, comment: AddComment):
    comment, _ = Comment.get_or_create(
        document_id=documentId,
        defaults={
            "text": comment.text,
            "date_created": comment.date_created,
            "date_updated": comment.date_updated,
            "author": comment.author_id
        })

    return comment


app.include_router(route)


if __name__ == "__main__":
    uvicorn.run("api:app", port=7000, reload=True)
