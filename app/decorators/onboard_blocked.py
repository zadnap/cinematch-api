from functools import wraps
from flask import jsonify

def onboard_blocked(fn):
    @wraps(fn)
    def wrapper(user, *args, **kwargs):
        if user.is_onboarded:
            return jsonify({
                "success": False,
                "message": "Already onboarded"
            }), 403

        return fn(user, *args, **kwargs)

    return wrapper