from flask import Blueprint, request, jsonify
from app import db
from models import Collateral, CategoryEnum

bp = Blueprint("collateral_routes", __name__)

@bp.route("/collaterals", methods=["POST"])
def add_collateral():
    data = request.json

    try:
        category = CategoryEnum[data["category"]]
    except KeyError:
        return jsonify({"error": f"Invalid category. Must be one of {[e.value for e in CategoryEnum]}"}), 400

    if not Collateral.validate_filepath(data["collateral_path"]):
        return jsonify({"error": "Invalid file path format. Must follow naming convention: Category_EXPT.txt or Category_POR.txt"}), 400

    try:
        new_collateral = Collateral(
            category=category,
            is_experimental=data["is_experimental"],
            user_description=data["user_description"],
            collateral_path=data["collateral_path"],
            validation_folder=data["validation_folder"],
        )
        db.session.add(new_collateral)
        db.session.commit()

        return jsonify({"message": "Collateral added", "filename": new_collateral.filename})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@bp.route("/collaterals", methods=["GET"])
def get_collaterals():
    collaterals = Collateral.query.all()
    return jsonify([{
        "id": c.id,
        "category": c.category.value,
        "is_experimental": c.is_experimental,
        "user_description": c.user_description,
        "collateral_path": c.collateral_path,
        "validation_folder": c.validation_folder,
        "filename": c.filename
    } for c in collaterals])
