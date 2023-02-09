#
# @function_jwt.py Copyright (c) 2023 Jalasoft.
# 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia.
# All rights reserved.
#
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#

from jwt import encode
from jwt import decode
from jwt import exceptions
from os import getenv
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from flask import jsonify


def expire_date(time: int):
    """Defines the expiration date of the tokenLogin"""

    now = datetime.now(tz=timezone.utc)
    new_date = now + timedelta(hours=time)
    print(new_date)
    return new_date


def write_token(data: dict):
    """Writes the tokenLogin"""

    token = encode(payload={**data, "exp": expire_date(1)},
                   key=getenv("SECRET"), algorithm="HS256")
    print(token.encode("UTF-8"))
    return token.encode("UTF-8")


def validate_token(token, output=False):
    """Defines validation of the tokenLogin"""

    try:
        if output:
            return decode(token, key=getenv("SECRET"), algorithms=["HS256"])
        decode(token, key=getenv("SECRET"), algorithms=["HS256"])
    except exceptions.DecodeError:
        response = jsonify({"message": "Invalid Token"})
        response.status_code = 401
        return response
    except (exceptions.ExpiredSignatureError) as e:
        print("errorrrr: ", e)
        response = jsonify({"message": "Token Expired"})
        response.status_code = 401
        return response
