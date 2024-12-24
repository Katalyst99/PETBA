from flask import Blueprint
from .auth_routes import *
from .budget_routes import *
from .summary_routes import *
from .trans_routes import *


auth_bp = Blueprint('auth', __name__)
budget_bp = Blueprint('budget', __name__)
summary_bp = Blueprint('summary', __name__)
trans_bp = Blueprint('trans', __name__)
