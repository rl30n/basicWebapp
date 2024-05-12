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
default_page_size = 1
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['search_term']
        print(f"Buscamos {query}")
        # Implementar la lógica de búsqueda aquí
        response = app_search.search(
            engine_name=my_engine_name,
            query=query,
            page_size=default_page_size
        )
        print("*******************************")
        print(response)
        print("*******************************")
        response_treated = json.dumps(response.body)
        results_json = json.loads(response_treated)
        resultados_totales = results_json["meta"]["page"]["total_results"]

        print(f"Hay {resultados_totales} resultados")
        results_array= results_json['results']
        print("*******************************")
        print(results_array)
        print("*******************************")

        # Procesa los resultados de la consulta
        processed_results = []
        for result in results_array:
            processed_result = {
                "titulo": result["titulo"]["raw"],
                "preparacion": result["preparacion"]["raw"],
            # ... Procesar otros campos relevantes
            }
            print("*******************************")
            print(processed_result)
            print("*******************************")
            processed_results.append(processed_result)

            print("*******************************")
            print(processed_results)
            print("*******************************")

        # Envía los resultados procesados a la plantilla HTML
        return render_template("show_results.html", results=processed_results)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)