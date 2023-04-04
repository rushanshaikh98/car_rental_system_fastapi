from functools import wraps

import jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError

jwt_bearer = HTTPBearer()
credentials: HTTPAuthorizationCredentials = Depends(jwt_bearer)


def super_admin_required():
    """ A decorator for checking whether a user is super admin or not"""

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                payload = jwt.decode(credentials.credentials,
                                     "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7",
                                     algorithms=["HS256"])
                # Here you can perform any additional checks on the payload, like checking if the user is in a database.
                if payload.is_super_admin:
                    return fn(*args, **kwargs)
            except JWTError:
                raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return decorator

    return wrapper
