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
language_default = "es"
LIMIT_BULK=1
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
    #print (response)
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
            "categoria": "text"
        }
    )
except NotFoundError as e:
    print ("No se pudo actualizar el schema")

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
      ]
  }
)


# Assuming the response is stored in a variable named 'response'

# Access the 'facets' dictionary
facets = response.get('facets')

# If 'facets' exists, extract the 'categoria' array
categoria_array = facets.get('categoria') if facets else None
kcal_array=facets.get('kcal') if facets else None
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
else:
  print("Categoria array not found in the response.")