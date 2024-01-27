from fastapi import APIRouter
from src.schemas.user_schemas import *
from src.schemas.auth_schemas import *
from src.controllers.auth_controller import Authoriser
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

"""
Protected routes
"""



@auth_router.post(
        path="/user/change_password",
        tags=["auth", "user"])
async def user_change_password(change_password_request:ChangePasswordRequest):
    authoriser = await Authoriser.get_instance()
    response = await authoriser.change_password(change_password_request)
    return response


@auth_router.post(
        path="/gl/register",
        tags=["auth", "gl"])
async def gl_register(register_request:RegisterRequest):
    authoriser = await Authoriser.get_instance()
    response = await authoriser.register(register_request, Role.gl)
    return response

@auth_router.post(
        path="/gl/change_password",
        tags=["auth", "gl"])
async def gl_change_password(change_password_request:ChangePasswordRequest):
    authoriser = await Authoriser.get_instance()
    response = await authoriser.change_password(change_password_request)
    return response

@auth_router.post(
        path="/gl/register_player",
        tags=["auth", "gl"])
async def gl_register_player(gl_register_player_request:GLRegisterPlayerRequest):
    authoriser = await Authoriser.get_instance()
    response = await authoriser.gl_register_player(gl_register_player_request)
    return response

@auth_router.post(
        path="/gl/change_player_password",
        tags=["auth", "gl"])
async def gl_change_player_password(gl_change_player_password_request:GLChangePlayerPasswordRequest):
    authoriser = await Authoriser.get_instance()
    response = await authoriser.gl_change_player_password(gl_change_player_password_request)
    return response

@auth_router.post(
        path="/facilitator/register",
        tags=["auth", "facilitator"])
async def facilitator_register(register_request:RegisterRequest):
    authoriser = await Authoriser.get_instance()
    response = await authoriser.register(register_request, Role.facilitator)
    return response


"""
Test routes
"""

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
        path="/user/register",
        tags=["auth", "user"])
async def user_register(register_request:RegisterRequest):
        authoriser = await Authoriser.get_instance()
        response = await authoriser.register(register_request, Role.player)
        return response