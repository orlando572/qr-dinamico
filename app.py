from flask import Flask, redirect

app = Flask(__name__)

# URL
URL_ACTUAL = "https://picsum.photos/800"


@app.route("/")
def home():
    return "Servidor QR funcionando"


@app.route("/qr")
def qr():
    return redirect(URL_ACTUAL)


if __name__ == "__main__":
    app.run()
