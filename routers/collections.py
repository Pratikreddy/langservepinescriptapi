# This file is disabled for PineScript trading assistant app
# All document/textbook search functionality has been removed

# from typing import List
# from fastapi import APIRouter, Depends
# from core.auth import get_current_user, User
# from services.collection_service import CollectionService

# router = APIRouter(prefix="/collections", tags=["collections"])

# # Create service instance
# collection_service = CollectionService()

# @router.get("/")
# async def get_collections(user: User = Depends(get_current_user)):
#     return collection_service.get_available_collections()

# @router.get("/{collection_name}")
# async def get_collection_info(
#     collection_name: str,
#     user: User = Depends(get_current_user)
# ):
#     return collection_service.get_collection_info(collection_name)

# @router.post("/validate")
# async def validate_collections(
#     collection_names: List[str],
#     user: User = Depends(get_current_user)
# ):
#     valid = collection_service.validate_collections(collection_names)
#     return {
#         'requested': collection_names,
#         'valid': valid,
#         'invalid': [c for c in collection_names if c not in valid]
#     }

# Disabled router - no longer needed for PineScript app
from fastapi import APIRouter
router = APIRouter()  # Empty router to prevent import errors