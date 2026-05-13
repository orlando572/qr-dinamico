import os

import cloudinary
import cloudinary.uploader
from flask import (
    Flask,
    redirect,
    render_template,
    request,
    session,
)

app = Flask(__name__)

# =========================
# VARIABLES DE ENTORNO
# =========================

SECRET_KEY = os.getenv("SECRET_KEY")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

CLOUD_NAME = os.getenv("CLOUD_NAME")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# =========================
# FLASK
# =========================

app.secret_key = SECRET_KEY

# =========================
# CLOUDINARY
# =========================

cloudinary.config(
    cloud_name=CLOUD_NAME,
    api_key=API_KEY,
    api_secret=API_SECRET,
    secure=True,
)

# =========================
# QR PUBLICO
# =========================


@app.route("/qr")
def qr():

    url = f"https://res.cloudinary.com/{CLOUD_NAME}/image/upload/imagen_qr"

    return redirect(url)


# =========================
# LOGIN
# =========================


@app.route("/", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":
        password = request.form.get("password")

        if password == ADMIN_PASSWORD:
            session["admin"] = True

            return redirect("/admin")

        else:
            error = "Contraseña incorrecta"

    return render_template("login.html", error=error)


# =========================
# LOGOUT
# =========================


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# =========================
# PANEL ADMIN
# =========================


@app.route("/admin", methods=["GET", "POST"])
def admin():

    if not session.get("admin"):
        return redirect("/")

    mensaje = None

    if request.method == "POST":
        file = request.files.get("imagen")

        if file and file.filename != "":
            cloudinary.uploader.upload(
                file,
                # Siempre misma imagen
                public_id="imagen_qr",
                # Reemplazar imagen anterior
                overwrite=True,
                # Limpiar cache CDN
                invalidate=True,
            )

            mensaje = "Imagen actualizada"

    return render_template("admin.html", mensaje=mensaje)


# =========================
# RUN
# =========================

if __name__ == "__main__":
    app.run(debug=True)
