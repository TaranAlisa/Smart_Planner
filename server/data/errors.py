from flask import make_response, jsonify
import uuid


def api_error(code, message, data, path, err_code):
    d = data
    if err_code == 400 or err_code == 404 or 409 <= err_code <= 422:
        return make_response(jsonify({
            "code": code,
            "message": message,
            "traceID": str(uuid.uuid4()),
            "timestamp": f"{d.date()}T{d.hour}:{d.minute}:{d.second}Z",
            "path": path,
        }), err_code)
    else:
        return make_response(jsonify({
            "code": code,
            "message": message,
            "traceID": str(uuid.uuid4()),
            "timestamp": f"{d.date()}T{d.hour}:{d.minute}:{d.second}Z",
            "path": path
        }), err_code)