from src.controllers.admin_controller import AdminController
from src.dependencies.dependencies import admin_jwt_token_checker
from src.schemas.house_schemas import House
from src.schemas.user_schemas import User

from src.schemas.user_schemas import *
from src.schemas.auth_schemas import *
from src.controllers.auth_controller import Authoriser

from fastapi import APIRouter, Depends

admin_router = APIRouter()

admin_controller = AdminController()

@admin_router.post(
        path="/admin/create_house",
        tags=["admin"])
async def create_house(house: House, user:User = Depends(admin_jwt_token_checker)):
    response = await admin_controller.create_house(house)
    return response

@admin_router.post(
        path="/admin/delete_all_data",
        tags=["admin"])
async def delete_all_data(user:User = Depends(admin_jwt_token_checker)):
    response = await admin_controller.delete_all_data()
    return response

@admin_router.post(
        path = "/admin/reset_all_points",
        tags=["admin"])
async def reset_all_points(user:User = Depends(admin_jwt_token_checker)):
    response = await admin_controller.reset_all_points_and_rooms()
    return response

@admin_router.post(
        path="/admin/delete_all_users",
        tags=["admin"])
async def delete_all_users(user:User = Depends(admin_jwt_token_checker)):
        response = await admin_controller.delete_all_users()
        return response


@admin_router.post(
        path = "/admin/house_raw_points",
        tags=["admin"])
async def house_raw_points(user:User = Depends(admin_jwt_token_checker)):
        response = await admin_controller.get_house_raw_points()
        return response

@admin_router.post(
        path = "/admin/god_allegiance",
        tags=["admin"])
async def god_allegiance(user:User = Depends(admin_jwt_token_checker)):
        response = await admin_controller.get_gods_allegiance()
        return response

@admin_router.post(
      path = "/admin/create_facilitator",
      tags=["admin"]
)
async def create_facilitator(register_request:RegisterRequest, user:User = Depends(admin_jwt_token_checker)):
    authoriser = await Authoriser.get_instance()
    response = await authoriser.register(register_request, Role.facilitator)
    return response

@admin_router.post(
      path = "/admin/create_gl",
      tags=["admin"]
)
async def create_gl(register_request:RegisterRequest, user:User = Depends(admin_jwt_token_checker)):
    authoriser = await Authoriser.get_instance()
    response = await authoriser.register(register_request, Role.gl)
    return response