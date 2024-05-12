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

myendpoint = "http://localhost:3002"
mybearer = "private-c6i87ttdhr3sv9i1a65p5v39"
my_engine_name = "es-testing-recipes-engine"
categoria = ["desayuno","merienda","snack"]
language_default = "es"
LIMIT_BULK=1
#categoria = ["comida", "cena"]
app_search = AppSearch(
    myendpoint,
    bearer_auth=mybearer
)
hash_algorithm = hashlib.sha256  # Choose your desired hash algorithm
try:
    engine_exists = app_search.get_engine(engine_name=my_engine_name)
except NotFoundError as e:
    app_search.create_engine(
        engine_name=my_engine_name,
        language=language_default,
    )
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
            "ingestion_date": "date"
        }
    )
except NotFoundError as e:
    print ("No se pudo actualizar el schema")
# Ruta del archivo PDF
ruta_pdf = "/Users/fucho/CT-App/docker-elk/ct_testing/solo_desayuno_merienda_snack.pdf"
#ruta_pdf = "/Users/fucho/CT-App/docker-elk/ct_testing/recetas_comidas_y_cena.pdf"
my_documents = []

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def recipe_form():
    if request.method == "POST":
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
          
        print (documento)
        my_documents.append(documento)

        if len(my_documents) >= LIMIT_BULK:
            response = app_search.index_documents(engine_name=my_engine_name, documents =my_documents)
            print (response)
            my_documents.clear()
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

