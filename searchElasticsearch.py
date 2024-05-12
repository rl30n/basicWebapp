from flask import Flask, render_template, request
from elastic_enterprise_search import AppSearch
from elastic_enterprise_search.exceptions import NotFoundError  # Corrected import
import json
import re
from elasticsearch import Elasticsearch
import pprint
from zulu import Zulu
import logging
import ecs_logging
import traceback
app = Flask(__name__)

myendpoint = "http://localhost:3002"
mybearer = "private-c6i87ttdhr3sv9i1a65p5v39"
my_engine_name = "es-testing-recipes-engine"
language_default = "es"


# Configuración de la conexión a App Search
app_search = AppSearch(
    myendpoint,
    bearer_auth=mybearer
)
default_page_size = 10

# Ruta principal
@app.route("/")
def index():
    # Recibe parámetros de búsqueda del usuario
    query = request.args.get("q")
    filters = request.args.get("filters")

    # Realiza la consulta a App Search
    results = app_search.search(
        engine="YOUR_ENGINE_NAME",
        query=query,
        filters=filters,
    )

    # Procesa los resultados de la consulta
    processed_results = []
    for result in results["results"]:
        processed_result = {
            "title": result["title"],
            "description": result["description"],
            # ... Procesar otros campos relevantes
        }
        processed_results.append(processed_result)

    # Envía los resultados procesados a la plantilla HTML
    return render_template("index.html", results=processed_results)