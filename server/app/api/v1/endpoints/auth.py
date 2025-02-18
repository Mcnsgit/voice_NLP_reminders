# # app/api/v1/endpoints/auth.py
# import select
# from urllib import response
# from fastapi import APIRouter, Depends, HTTPException, Response, status
# from fastapi.security import OAuth2PasswordRequestForm
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.core.security import (
#     get_current_user,
#     verify_password,
#     get_password_hash,
#     create_access_token,
# )
# from app.db.session import get_db
# from app.models.user import User
# from app.schemas.user import UserCreate, UserResponse, Token
# from datetime import timedelta
# from app.core.config import settings
# from app.core.rate_limit import RateLimitMiddleware
# from app.models import user


# # auth_rate_limit = RateLimitMiddleware(
# #     app=any, calls=5, period=300  # 5 attempts  # per 5 minutes
# # )

# router = APIRouter()
# # dependencies=[Depends(auth_rate_limit)])


# @router.post("/register", response_model=UserResponse)
# async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
#     """Register a new user"""
#     # Check if user exists
#     query = select(User).where(User.email == user_in.email)
#     result = await db.execute(query)
#     user = result.scalar_one_or_none()
#     if user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
#         )

#     # Create new user
#     user = User(
#         email=user_in.email, hashed_password=get_password_hash(user_in.password)
#     )
#     db.add(user)
#     await db.commit()
#     await db.refresh(user)
#     return user


# @router.post("/login", response_model=Token)
# async def login(
#     response: Response,
#     db: AsyncSession = Depends(get_db),
#     form_data: OAuth2PasswordRequestForm = Depends(),
# ):
#     """Authenticate user and return token"""
#     # Get user
#     query = select(User).where(User.email == form_data.username)
#     result = await db.execute(query)
#     user = result.scalar_one_or_none()

#     if not user or not verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     if not user.is_active:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
#         )

#     # Create access token
#     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": str(user.id)}, expires_delta=access_token_expires
#     )

#     response.set_cookie(
#         key="access_token",
#         value=f"Bearer {access_token}",
#         httponly=True,
#         secure=not settings.DEBUG,  # True in production
#         samesite="lax",
#         max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
#     )

#     return {"access_token": access_token, "token_type": "bearer"}


# @router.post("/logout")
# async def logout(response: Response):
#     """Logout user by clearing the cookie"""
#     response.delete_cookie(key="access_token")
#     return {"message": " successfully logged out"}


# @router.post("/refresh", response_model=Token)
# async def refresh_token(
#     current_user: User = Depends(get_current_user), reponse: Response = None
# ):
#     """Refresh access token"""
#     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": str(user.id)}, expires_delta=access_token_expires
#     )

#     if response:
#         response.set_cookie(
#             key="access_token",
#             value=f"Bearer {access_token}",
#             httponly=True,
#             secure=not settings.DEBUG,
#             samesite="lax",
#             max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
#         )
#     return {"access_token": access_token, "token_type": "bearer"}


# # TODO
# # additional security endpoints:
# #   - Password reset
# #   - Email verification
# #   - Account deactivation

# # Add security monitoring:
# #   - Log failed login attempts
# #   - Track suspicious IP addresses
# #   - Monitor unusual activity
