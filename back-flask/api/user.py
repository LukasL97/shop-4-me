from typing import Type, Tuple

from flask import Blueprint, request

from api.http_status import OK, BAD_REQUEST, NOT_FOUND, UNAUTHORIZED
from model.exception import UnexpectedUserTypeError, UserNotFoundError, IncorrectPasswordError
from model.user import User, Requester, Volunteer, ShopOwner

user = Blueprint('login', __name__)

def get_user_model(user_type: str) -> Type[User]:
    if user_type == 'Requester': return Requester
    if user_type == 'Volunteer': return Volunteer
    if user_type == 'ShopOwner': return ShopOwner
    raise UnexpectedUserTypeError


@user.route('/login', methods=['POST'])
def login() -> Tuple[str, int]:
    user_data = request.json
    try:
        return get_user_model(user_data['userType']).login(user_data['name'], user_data['passwordHash']), OK
    except UnexpectedUserTypeError:
        return 'Unexpected user type %s' % user_data['userType'], BAD_REQUEST
    except UserNotFoundError:
        return 'User %s not found' % user_data['name'], NOT_FOUND
    except IncorrectPasswordError:
        return 'Incorrect password', UNAUTHORIZED
