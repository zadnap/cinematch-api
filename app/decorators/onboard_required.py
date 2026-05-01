from functools import wraps
from flask import jsonify

def onboard_required(fn):
    @wraps(fn)
    def wrapper(user, *args, **kwargs):
        if not user.is_onboarded:
            return jsonify({
                "success": False,
                "message": "You must complete onboarding first"
            }), 403

        return fn(user, *args, **kwargs)

    return wrapper