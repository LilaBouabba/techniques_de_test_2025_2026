from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.get("/triangulation/<pointSetId>")
    def triangulation(pointSetId):
        raise NotImplementedError("API not implemented yet")

    return app
