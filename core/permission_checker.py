# permission checker.py

from fastapi import HTTPException, Request, Depends

from core.security import get_current_user
from database.casbin import get_enforcer


async def check_permission(
    request: Request,
    current_user: dict = Depends(get_current_user),
    enforcer=Depends(get_enforcer),
):
    role = current_user["role"]  # Extract role from JWT
    obj = request.url.path  # Requested URL path
    act = request.method.lower()  # HTTP method (GET, POST, etc.)

    print("=========================>role: ", role)
    print("=========================>obj: ", obj)
    print("=========================>act: ", act)

    # Casbin RBAC Check
    if not enforcer.enforce(role, obj, act):
        raise HTTPException(status_code=403, detail="Forbidden: Access Denied")
