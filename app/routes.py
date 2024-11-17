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
    try:
        data = Komik("").latest()
        return Result("success", data, 200)
    except Exception as e:
        return Result(f"error {e}", {"data": None}, 400)
        
@bp.route("/populer/")
def populer():
    try:
        data = Komik("manga/?status=&order=popular").search()
        return Result("success", data, 200)
    except Exception as e:
        return Result(f"error {e}", {"data": None}, 400)
        
@bp.route("/genre-list/")
def genrelist():
    try:
        data = Komik("manga/?status=&order=popular").genrelist()
        return Result("success", data, 200)
    except Exception as e:
        return Result(f"error {e}", {"data": None}, 400)
        
@bp.route("/search/")
def search():
    genre = request.args.get("genre", "")
    status = request.args.get("status", "")
    type = request.args.get("type", "")
    order = request.args.get("order", "")
    page = request.args.get("page", 1, type=int)
    try:
        data = Komik(f"manga/?page={page}&genre%5B%5D={genre}&status={status}&type={type}&order={order}").search()
        return Result("success", data, 200)
    except Exception as e:
        return Result(f"error {e}", {"data": None}, 400)
        
@bp.route("/komik/<slug>/")
def detail(slug):
    try:
        data = Komik(f"https://komikstation.co/manga/{slug}").detail()
        return Result("success", data, 200)
    except Exception as e:
        return Result(f"error {e}", {"data": None}, 400)
        
@bp.route("/chapter/<slug>/")
def viewchapter(slug):
    try:
        data = Komik(f"https://komikstation.co/{slug}").viewchapter()
        return Result("success", data, 200)
    except Exception as e:
        return Result(f"error {e}", {"data": None}, 400)
