from casbin_sqlalchemy_adapter import Adapter
import casbin
from core.config import settings
DB_STR = settings.SQLALCHEMY_DATABASE_URL+settings.SQLALCHEMY_DATABASE_NAME
def get_enforcer():
    adapter = Adapter(DB_STR)
    return casbin.Enforcer("rbac_model.conf", adapter)
