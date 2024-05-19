from flask import Flask, render_template, request
from elastic_enterprise_search import AppSearch
from elastic_enterprise_search.exceptions import NotFoundError  # Corrected import

from elastic_enterprise_search import AppSearch
from elastic_enterprise_search.exceptions import NotFoundError  # Corrected import
import json
import re
from elasticsearch import Elasticsearch
from zulu import Zulu
import hashlib
import logging
import ecs_logging

formatter = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=formatter, datefmt="%Y-%m-%d %H:%M:%S")

logger = logging.getLogger(__name__)  # Get a logger
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setFormatter(ecs_logging.StdlibFormatter())
logger.addHandler(handler)

myendpoint = "http://localhost:3002"
mybearer = "private-7hpkb4x8zemgyts7t6ofqqne"
my_engine_name = "es-testing-recipes-engine"
language_default = "es"
default_page_size = 10

LIMIT_BULK=1
try:
    app_search = AppSearch(
        myendpoint,
        bearer_auth=mybearer
    )
    logger.info("Conexión OK con ES")
except:
    print("No hay conexión con enterprise search")
    logger.critical("No hay coneexión con ES")

hash_algorithm = hashlib.sha256  # Choose your desired hash algorithm
try:
    engine_exists = app_search.get_engine(engine_name=my_engine_name)
    logger.info(f"Existe el engine {{my_engine_name}}")
except NotFoundError as e:
    app_search.create_engine(
        engine_name=my_engine_name,
        language=language_default,
    )
    logger.info(f"Se crea el engine {{my_engine_name}}")
try: 
    response = app_search.list_engines()
    print (response)
except NotFoundError as e:
    print ("no hay engines")
try:
    response = app_search.put_schema(
        engine_name=my_engine_name,
        schema={
            "kcal": "number",
            "proteina_gr": "number",
            "carbohidrato_gr": "number",
            "grasas_gr": "number",
            "ingestion_date": "date",
            "dificultad": "text"
        }
    )
except NotFoundError as e:
    print ("No se pudo actualizar el schema")

my_documents = []

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/advanced-search', methods=['GET','POST'])
def advanced_search():
    if request.method == 'POST':
        query = request.form['advanced_search_term']
        logger.info(f"Buscamos {query}")
    else:
        try:   
            response = app_search.search(
            engine_name=my_engine_name,
            query=" ",
            page_size=0,
            facets= 
            {   
                "categoria":
                [
                    {
                        "type": "value"
                    }
                ],
                "kcal":
                [
                    {
                        "type": "range",
                        "ranges":
                        [
                            {"from": 1, "to": 300, "name": "to300"},
                            {"from": 301, "to": 600, "name":"to600"},
                            {"from": 600, "name": "over600"}
                        ]
                    }
                ],
                "personas":
                [
                    {      
                        "type": "range",
                        "ranges":
                        [
                            {"from": 1, "to": 3, "name": "to3"},
                            {"from": 4, "to": 6, "name": "to6"},
                            {"from": 7, "name": "over7"}
                        ]
                    }
                ],
                "dificultad":
                [
                    {
                        "type": "value"
                    }
                ]
            }
            )
            #Assuming the response is stored in a variable named 'response'

            # Access the 'facets' dictionary
            facets = response.get('facets')
            logger.debug(facets)
            # If 'facets' exists, extract the 'categoria' array
            categoria_array = facets.get('categoria') if facets else None
            kcal_array=facets.get('kcal') if facets else None
            personas_array=facets.get('personas') if facets else None
            dificultad_array=facets.get('dificultad') if facets else None
            facets_array=[]
            # If 'categoria' array exists, access its data
            if categoria_array:
                categoria_data = categoria_array[0]['data']  # Assuming there's only one element in 'categoria'

                # Print the categoria data (array of dictionaries)
                #print(categoria_data)
                result_json={}
                for item in categoria_data:
                    value =item["value"]
                    count =item["count"]
                    result_json[value]=count
                #print(result_json)
                print(json.dumps(result_json, indent=2))
                facets_array.append(result_json)
            else:
                print("Categoria array not found in the response.")
            if kcal_array:
                kcal_data = kcal_array[0]['data']  # Assuming there's only one element in 'categoria'

                # Print the categoria data (array of dictionaries)
                #print(kcal_data)
                result_json={}
                for item in kcal_data:
                    value =item["name"]
                    count =item["count"]
                    result_json[value]=count
                #print(result_json)
                print(json.dumps(result_json, indent=2))
                facets_array.append(result_json)
            else:
                print("kcal array not found in the response.")
            if personas_array:
                personas_data = personas_array[0]['data']  # Assuming there's only one element in 'categoria'

                # Print the categoria data (array of dictionaries)
                #print(kcal_data)
                result_json={}
                for item in personas_data:
                    value =item["name"]
                    count =item["count"]
                    result_json[value]=count
                #print(result_json)
                print(json.dumps(result_json, indent=2))
                facets_array.append(result_json)
            else:
                print("Personas array not found in the response.")
            if dificultad_array:
                dificultad_data = dificultad_array[0]['data']  # Assuming there's only one element in 'categoria'

                # Print the categoria data (array of dictionaries)
                #print(kcal_data)
                result_json={}
                for item in dificultad_data:
                    value =item["name"]
                    count =item["count"]
                    result_json[value]=count
                print(f"Dificultad: {{result_json}}")
                print(json.dumps(result_json, indent=2))
                facets_array.append(result_json)
            else:
                print("Dificultad array not found in the response.")
        except:
            logger.error("No se puede buscar en elasticsearch")
        logger.debug(facets_array)
        return render_template('advanced_results.html',results=facets_array)
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['search_term']
        logger.info(f"Buscamos {query}")
        # Implementar la lógica de búsqueda aquí
        try:   
            response = app_search.search(
                engine_name=my_engine_name,
                query=query,
                page_size=default_page_size
            )
            logger.info(response)
        except:
            logger.error("No se puede buscar en elasticsearch")
        response_treated = json.dumps(response.body)
        results_json = json.loads(response_treated)
        resultados_totales = results_json["meta"]["page"]["total_results"]

        logger.info(f"Hay {resultados_totales} resultados")
        results_array= results_json['results']
        print("*******************************")
        logger.debug(results_array)
        print("*******************************")

        # Procesa los resultados de la consulta
        processed_results = []
        for result in results_array:
            processed_result = {
                "titulo": result["titulo"]["raw"],
                "personas": result["personas"]["raw"],
                "kcal": result["kcal"]["raw"],
                "proteina_gr": result["proteina_gr"]["raw"],
                "carbohidrato_gr": result["carbohidrato_gr"]["raw"],
                "grasas_gr": result["grasas_gr"]["raw"],
                "categoria": result["categoria"]["raw"],
                "dificultad": result["dificultad"]["raw"]
            # ... Procesar otros campos relevantes
            }
            print("*******************************")
            logger.debug(processed_result)
            print("*******************************")
            processed_results.append(processed_result)

            print("*******************************")
            logger.debug(processed_results)
            print("*******************************")

        # Envía los resultados procesados a la plantilla HTML
        return render_template("show_results.html", results=processed_results)
    
    else:
        return render_template('index.html')

@app.route("/submit-recipe", methods=["GET", "POST"])
def recipe_form():
    if request.method == "POST":
        logger.info("Arrancamos formulario")
        titulo = request.form["titulo"]
        ingredientes_text = request.form["ingredientes_text"]
        personas = request.form["personas"]
        preparacion = request.form["preparacion"]
        kcal = request.form["kcal"]
        carbohidrato_gr = request.form["carbohidrato_gr"]
        grasas_gr= request.form["grasas_gr"]
        proteina_gr = request.form["proteina_gr"]
        categoria = request.form.getlist("categoria")
        dificultad = request.form["dificultad"]
        
        # Procesar los datos del formulario (almacenarlos en una base de datos, etc.)
        timestamp_utc = Zulu.now()
        datos_json = {}
        datos_json["id"] = hashlib.sha256(titulo.encode('utf-8')).hexdigest()
        datos_json["titulo"] = titulo
        datos_json["ingredientes"] = ingredientes_text
        datos_json["preparacion"]= preparacion
        datos_json["personas"]= personas
        #datos_json["informacion"] = modified_text
        datos_json["kcal"] = kcal
        #datos_json["macronutrientes"] = info_macros
        datos_json["proteina_gr"] = proteina_gr
        datos_json["carbohidrato_gr"] = carbohidrato_gr
        datos_json["grasas_gr"] = grasas_gr
        datos_json["categoria"] = categoria
        datos_json["ingestion_date"] = timestamp_utc.isoformat()
        datos_json["dificultad"] = dificultad 
        documento_json_formatted = json.dumps(datos_json, indent=4)
        #print (documento_json_formatted)
        documento = json.loads(documento_json_formatted)
        logger.debug (f"el documento rellenado en el form es {{documento}}")
        print (documento)
        my_documents.append(documento)

        if len(my_documents) >= LIMIT_BULK:
            try:
                response = app_search.index_documents(engine_name=my_engine_name, documents =my_documents)
                logger.info (f"documento enviado {{response}}")
                my_documents.clear()
            except:
                logger.error(f"No se pudo ingestar {{documento}}")
        else:
            my_documents.append(documento)            
        return render_template("recipe_success.html", 
                titulo=titulo,
                ingredientes_text=ingredientes_text,
                personas=personas,
                preparacion=preparacion,
                kcal=kcal,
                carbohidrato_gr=carbohidrato_gr,
                grasas_gr=grasas_gr,
                proteina_gr=proteina_gr,
                categoria=categoria,
                dificultad=dificultad
                )
    else:
        return render_template("recipe_form.html")

if __name__ == "__main__":
    app.run(debug=True)
