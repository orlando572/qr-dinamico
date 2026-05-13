import os

from flask import (
    Flask,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)

app = Flask(__name__)

app.secret_key = "cambia_esta_clave"

PASSWORD = "redgas572"

UPLOAD_FOLDER = "uploads"
IMAGE_NAME = "imagen_actual.jpg"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/qr")
def qr():

    image_path = os.path.join(UPLOAD_FOLDER, IMAGE_NAME)

    if not os.path.exists(image_path):
        return "No hay imagen subida"

    return send_from_directory(UPLOAD_FOLDER, IMAGE_NAME)


@app.route("/", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":
        password = request.form.get("password")

        if password == PASSWORD:
            session["admin"] = True

            return redirect("/admin")

        else:
            error = "Contraseña incorrecta"

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


@app.route("/admin", methods=["GET", "POST"])
def admin():

    if not session.get("admin"):
        return redirect("/")

    mensaje = None

    if request.method == "POST":
        file = request.files.get("imagen")

        if file and file.filename != "":
            path = os.path.join(UPLOAD_FOLDER, IMAGE_NAME)

            file.save(path)

            mensaje = "Imagen actualizada"

    return render_template("admin.html", mensaje=mensaje)


if __name__ == "__main__":
    app.run(debug=True)
