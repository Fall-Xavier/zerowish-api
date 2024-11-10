import random
from flask import Blueprint,request
from .service import Komik
from .result import Result

bp = Blueprint("api", __name__)

@bp.after_request
def add_header(response):
    response.headers["Content-Type"] = "application/json"
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,PUT,POST,DELETE,OPTIONS"
    return response
    
@bp.route("/latest/")
def latest():
    page = request.args.get("page", 1, type=int)
    try:
        data = Komik(f"komik-terbaru/page/{page}/","latest").main()
        return Result("success", data, 200)
    except Exception as e:
        return Result(f"error {e}", {"data": None}, 400)
        
