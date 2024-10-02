from flask import Blueprint, request, jsonify
from src.services.coordinates_api import obtener_coordenadas
from pymongo import MongoClient
from src.utils.functions.normalize_text import normalize
from config import mongo

coord_bp = Blueprint('coord', __name__)

client = MongoClient(mongo['mongodb_url'])
database_name = client[mongo['mongodb_db_name']]
collection_name = mongo['mongodb_db_name_coordinates']


@coord_bp.route('/obtener-coordenadas', methods=['GET'])
def get_coordinates():
    subnivel_1 = normalize(request.args.get('subnivel_1'))
    subnivel_3 = normalize(request.args.get('subnivel_3'))
    subnivel_4 = normalize(request.args.get('subnivel_4'))

    if subnivel_1 == "NA" or subnivel_3 == "NA" or subnivel_4 == "NA":
        return jsonify({"error": "Faltan parámetros o son inconsistentes: subnivel_1, subnivel_3, subnivel_4 mal ingresados"}), 400

    lat_prov, lon_prov, lat_city, lon_city = obtener_coordenadas(
        database_name, collection_name, subnivel_1, subnivel_3, subnivel_4)

    if not lat_prov or not lon_prov or not lat_city or not lon_city:
        return jsonify({"error": "No se pudieron obtener las coordenadas"}), 500

    return jsonify({
        "lat_subnivel_3": lat_prov,
        "lon_subnivel_3": lon_prov,
        "lat_subnivel_4": lat_city,
        "lon_subnivel_4": lon_city
    })
