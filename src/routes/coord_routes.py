from flask import Blueprint, request, jsonify
from src.services.coordinates_api import obtener_coordenadas
from pymongo import MongoClient
from config import mongo

coord_bp = Blueprint('coord', __name__)

client = MongoClient(mongo['mongodb_url'])
database_name = client[mongo['mongodb_db_name']]
collection_name = mongo['mongodb_db_name_coordinates']


@coord_bp.route('/obtener-coordenadas', methods=['GET'])
def get_coordinates():
    subnivel_1 = request.args.get('subnivel_1')
    subnivel_3 = request.args.get('subnivel_3')
    subnivel_4 = request.args.get('subnivel_4')

    if not subnivel_1 or not subnivel_3 or not subnivel_4:
        return jsonify({"error": "Faltan parámetros: subnivel_1, subnivel_3, subnivel_4 son requeridos"}), 400

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
