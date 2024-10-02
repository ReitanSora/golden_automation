from flask import Blueprint
from flask_cors import cross_origin
from src.services.update_document import update

import sys

main = Blueprint('update_blueprint', __name__)

@cross_origin
@main.route('/', methods=['GET'])
def update_document():

    try:
        result = update()
        if result:
            return 'Actualización exitosa'
    except Exception as e:
        return f'Fallo en la actualización: {e}'
