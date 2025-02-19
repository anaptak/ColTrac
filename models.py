import re
import os
import enum
from app import db

class CategoryEnum(enum.Enum):
    OPTION_A = "colTypeA"
    OPTION_B = "colTypeB"
    OPTION_C = "colTypeC"

class Collateral(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    category = db.Column(db.Enum(CategoryEnum), nullable=False)
    is_experimental = db.Column(db.Boolean, nullable=False, default=True)
    user_description = db.Column(db.Text)

    collateral_path = db.Column(db.String(255), nullable=False)
    validation_folder = db.Column(db.String(255), nullable=False)

    filename = db.Column(db.String(255), nullable=False)


    def __init__(self, category, is_experimental, collateral_path, validation_folder, user_description):

        if not isinstance(category, CategoryEnum):
            raise ValueError(f"Invalid category: {category}. Must be one of {list(CategoryEnum)}")

        self.category = category
        self.is_experimental = is_experimental

        if not self.validate_filepath(collateral_path):
            raise ValueError(f"Invalid collateral file path: {collateral_path}")

        self.collateral_path = collateral_path
        self.validation_folder = validation_folder
        self.user_description = user_description
        self.filename = self.generate_filename()

    @staticmethod
    def validate_filepath(filepath):
        """
        Ensure filename follows required format: Category_EXPT.ext or Category_POR.ext
        """
        filename_pattern = r"^[A-Za-z0-9_-]+_[A-Za-z0-9_-]+_(EXPT|POR)\.ext$"
        _, filename = os.path.split(filepath)

        return bool(re.match(filename_pattern, filename))

    def generate_filename(self):
        """
        Generate standard filename based on category/experiment status
        """
        return f"{self.category.value}_{self.subtype}_{'EXPT' if self.is_experimental else 'POR'}.ext"
