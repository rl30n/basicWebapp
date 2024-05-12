from flask import Flask, render_template, request

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
        # Procesar los datos del formulario (almacenarlos en una base de datos, etc.)

        return render_template("recipe_success.html", 
                titulo=titulo,
                ingredientes_text=ingredientes_text,
                personas=personas,
                preparacion=preparacion,
                kcal=kcal,
                carbohidrato_gr=carbohidrato_gr,
                grasas_gr=grasas_gr,
                proteina_gr=proteina_gr,
                categoria = categoria
                )
    else:
        return render_template("recipe_form.html")

if __name__ == "__main__":
    app.run(debug=True)

