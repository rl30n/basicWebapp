from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def handle_choice():
    action = request.form["action"]
    if action == "search":
        # Redirect to search recipe functionality (potentially render a search form first)
        # Replace with your search logic
        return "Te estamos llevando a la página de búsqueda..."
    elif action == "write":
        # Redirect to basicform.py using Flask's url_for() function
        return redirect(url_for("basicform"))  # Assuming basicform.py has a route named "basicform"
    else:
        return "Opción no válida"

# Consider additional routes for search and basic form functionalities
@app.route("/basicform")
def basic_form():
    # Render the basicform.html template (if it exists)
    return render_template("basicform.html")

if __name__ == "__main__":
    app.run(debug=True)