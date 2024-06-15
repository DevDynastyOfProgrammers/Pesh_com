from functools import wraps
from flask import make_response
from flask_login import current_user

def auth_role(role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            roles = role if isinstance(role, list) else [role]
            # print()
            # print()
            # print(current_user.has_role(role))
            # print()
            # print()
            for r in roles:
                if current_user.has_role(r):
                    return fn(*args, **kwargs)
            return make_response({"msg": f"Missing any of roles {','.join(roles)}"}, 403)
            # if all(not current_user.has_role(r) for r in roles):
            #     return make_response({"msg": f"Missing any of roles {','.join(roles)}"}, 403)
            # return fn(*args, **kwargs)
        
        return decorator
    
    return wrapper