from flask import Blueprint, render_template

products_bp = Blueprint("products", __name__)


@products_bp.get("/")
def index():
    # Phase 1 only proves Flask can render a page; product logic comes next.
    return render_template("index.html")
