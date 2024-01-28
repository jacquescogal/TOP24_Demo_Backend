from fastapi import APIRouter, Depends
from src.schemas.user_schemas import *
from src.schemas.auth_schemas import *
from src.controllers.auth_controller import Authoriser
from src.dependencies.dependencies import player_jwt_token_checker, gl_jwt_token_checker, facilitator_jwt_token_checker
from fastapi.responses import JSONResponse
auth_router = APIRouter()


"""
Unprotected routes
"""
@auth_router.post(
        path="/user/login",
        tags=["auth", "user"])
async def user_login(login_request:LoginRequest):
    authoriser = await Authoriser.get_instance()
    response = await authoriser.authenticate(login_request, Role.player)
    return response

@auth_router.post(
        path="/gl/login",
        tags=["auth", "gl"])
async def gl_login(login_request:LoginRequest):
    authoriser = await Authoriser.get_instance()
    response = await authoriser.authenticate(login_request, Role.gl)
    return response

@auth_router.post(
        path="/facilitator/login",
        tags=["auth", "facilitator"])
async def facilitator_login(login_request:LoginRequest):
    authoriser = await Authoriser.get_instance()
    response = await authoriser.authenticate(login_request, Role.facilitator)
    return response

@auth_router.post(
        path="/gl/register_player",
        tags=["auth", "gl"])
async def gl_register_player(gl_register_player_request:GLRegisterPlayerRequest, user:User = Depends(gl_jwt_token_checker)):
    authoriser = await Authoriser.get_instance()
    response = await authoriser.gl_register_player(gl_register_player_request)
    return response

"""
Protected routes
"""

@auth_router.get(
        path='/user/check_token',
        tags=["auth", "user"]
)
async def check_token(user:User = Depends(player_jwt_token_checker)):
        return JSONResponse(status_code=200, content={'message': f"Success: {user.role} {user.username} authenticated"})


@auth_router.post(
        path="/user/change_password",
        tags=["auth", "user"])
async def user_change_password(change_password_request:ChangePasswordRequest, user:User = Depends(player_jwt_token_checker)):
    if change_password_request.username != user.username:
        return JSONResponse(status_code=401, content={'message': f"Error: {user.role} {user.username} not authorized to change password for {change_password_request.username}"})
    authoriser = await Authoriser.get_instance()
    response = await authoriser.change_password(change_password_request)
    return response


@auth_router.post(
        path="/gl/change_password",
        tags=["auth", "gl"])
async def gl_change_password(change_password_request:ChangePasswordRequest, user:User = Depends(gl_jwt_token_checker)):
    if change_password_request.username != user.username:
        return JSONResponse(status_code=401, content={'message': f"Error: {user.role} {user.username} not authorized to change password for {change_password_request.username}"})
    authoriser = await Authoriser.get_instance()
    response = await authoriser.change_password(change_password_request)
    return response



@auth_router.post(
        path="/gl/change_player_password",
        tags=["auth", "gl"])
async def gl_change_player_password(gl_change_player_password_request:GLChangePlayerPasswordRequest):
    if gl_change_player_password_request.gl_username != gl_change_player_password_request.username:
        return JSONResponse(status_code=401, content={'message': f"Error: {gl_change_player_password_request.gl_username} not authorized to change password for {gl_change_player_password_request.username}"})
    authoriser = await Authoriser.get_instance()
    response = await authoriser.gl_change_player_password(gl_change_player_password_request)
    return response



"""
Test routes
"""
@auth_router.post(
        path="/user/register",
        tags=["auth", "user"])
async def user_register(register_request:RegisterRequest):
        authoriser = await Authoriser.get_instance()
        response = await authoriser.register(register_request, Role.player)
        return response

@auth_router.post(
        path="/gl/register",
        tags=["auth", "gl"])
async def gl_register(register_request:RegisterRequest):
    authoriser = await Authoriser.get_instance()
    response = await authoriser.register(register_request, Role.gl)
    return response

@auth_router.post(
        path="/facilitator/register",
        tags=["auth", "facilitator"])
async def facilitator_register(register_request:RegisterRequest):
    authoriser = await Authoriser.get_instance()
    response = await authoriser.register(register_request, Role.facilitator)
    return response

@auth_router.get(
        path="/delete_all_users",
        tags=["auth", "user"])
async def del_test():
    authoriser = await Authoriser.get_instance()
    response = await authoriser.delete_all_users()
    return response

@auth_router.get(
        path="/get_all_users",
        tags=["auth", "gl"])
async def get_test():
    authoriser = await Authoriser.get_instance()
    response = await authoriser.get_all_users()
    return response

@auth_router.post(
        path="/get_user_jwt",
        tags=["auth", "misc"])
async def get_user_jwt(user:User):
    authoriser = await Authoriser.get_instance()
    response = await authoriser.get_jwt(user)
    return response

@auth_router.post(
        path="/test_protected",
        tags=["auth", "misc"])
async def test_protected(user:str = Depends(player_jwt_token_checker)):
    return user