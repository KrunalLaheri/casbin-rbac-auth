# routers.py

from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from fastapi import Depends, HTTPException, APIRouter
from core.permission_checker import check_permission
from core.security import create_access_token, pwd_context
from database.casbin import get_enforcer
from database.db import get_db
from models.auth import CasbinRule
from schemas.auth import CasbinRuleCreate, LoginRequest



casbin_router = APIRouter(prefix="/casbin", tags=["Casbin Auth"])

# Dummy user database
fake_users_db = {
    "john": {"username": "john", "password": pwd_context.hash("password"), "role": "admin"},
    "krunal": {"username": "krunal", "password": pwd_context.hash("password"), "role": "subadmin"},
    "dev": {"username": "dev", "password": pwd_context.hash("password"), "role": "user"},
}


@casbin_router.post("/token")
async def login_for_access_token(request: LoginRequest):
    user = fake_users_db.get(request.username)
    if not user or not pwd_context.verify(request.password, user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    # Create JWT token with role
    access_token = create_access_token(data={"sub": request.username, "role": user["role"]})
    return {"access_token": access_token, "token_type": "bearer"}


@casbin_router.get("/admin", dependencies=[Depends(check_permission)])
async def admin_panel():
    return {"message": "Welcome to Admin Panel"}


@casbin_router.post("/admin", dependencies=[Depends(check_permission)])
async def create_admin_resource():
    return {"message": "Admin Resource Created"}


@casbin_router.get("/articles", dependencies=[Depends(check_permission)])
async def view_articles():
    return {"message": "Viewing Articles"}


@casbin_router.post("/articles", dependencies=[Depends(check_permission)])
async def create_article():
    return {"message": "Article Created"}


@casbin_router.post("/add-role")
async def add_role(user: str, role: str, enforcer=Depends(get_enforcer)):
    enforcer.add_role_for_user(user, role)
    return {"message": f"Role {role} assigned to {user}"}


@casbin_router.post("/add-policy")
async def add_policy(role: str, obj: str, act: str, enforcer=Depends(get_enforcer)):
    enforcer.add_policy(role, obj, act)
    return {"message": f"Policy added: {role} can {act} {obj}"}


async def create_casbin_rule(db: Session, rule: CasbinRuleCreate):
    db_rule = CasbinRule(
        ptype=rule.ptype,
        v0=rule.v0,
        v1=rule.v1,
        v2=rule.v2,
        v3=rule.v3,
        v4=rule.v4,
        v5=rule.v5,
    )
    db.add(db_rule)
    await db.commit()
    await db.refresh(db_rule)
    return db_rule


async def get_casbin_rules(db: Session, skip: int = 0, limit: int = 10):
    result = db.execute(select(CasbinRule).offset(skip).limit(limit))
    return result.scalars().all()


# Create a Casbin rule
@casbin_router.post("/casbin-rule/", response_model=CasbinRuleCreate)
async def create_casbin_rule_endpoint(rule: CasbinRuleCreate, db: Session = Depends(get_db)):
    return await create_casbin_rule(db=db, rule=rule)

# Get all Casbin rules
@casbin_router.get("/casbin-rules/", response_model=List[CasbinRuleCreate])
async def get_casbin_rules_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    rules = await get_casbin_rules(db=db, skip=skip, limit=limit)
    return rules
