from typing import Annotated
from fastapi import APIRouter, Depends, Response, status
from bms.api.services.users import UsersService
from bms.api.models import users as models

router = APIRouter(prefix="/users")
TABLE="bms.users"

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
        user: models.UserCreate,
        service: Annotated[UsersService, Depends()],
        response: Response
    ):
    result = await service.create_user(user=user)
    if result:
        return {'userid': result[0]}

    # User already exists
    response.status_code = 200
    return {'message': "User with this username already exists"}



@router.delete("/{username}", status_code=status.HTTP_200_OK)
async def delete_user(
        username: str,
        service: Annotated[UsersService, Depends()]
    ):
    await service.delete_user(username)

@router.post("/login", status_code=200, response_model=models.LoginResponse)
async def login(
        user: models.UserCredentials,
        service: Annotated[UsersService, Depends()],
        response: Response
    ):
    result = await service.login(user)
    if type(result) is models.LoginFailedResponse:
        response.status_code = status.HTTP_401_UNAUTHORIZED

    return result
