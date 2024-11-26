from flask import jsonify

def Result(status,data,status_code):
    return (
        jsonify(data),
        status_code,
    )
