import os

from flask import Flask, jsonify
from flask_cors import CORS

from db import ensure_indexes, ping_db
from routes.auth import auth_bp
from routes.lists import lists_bp
from routes.share import share_bp
from routes.tasks import tasks_bp


def create_app():
    app = Flask(__name__)

    client_origin = os.getenv("CLIENT_ORIGIN", "http://localhost:5173")
    CORS(
        app,
        resources={r"/api/*": {"origins": [client_origin, "http://127.0.0.1:5173"]}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    )

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(lists_bp, url_prefix="/api/lists")
    app.register_blueprint(tasks_bp, url_prefix="/api/tasks")
    app.register_blueprint(share_bp, url_prefix="/api/share")

    @app.get("/")
    def root():
        return jsonify({"message": "Todo Management API is running"}), 200

    @app.get("/api/health")
    def health():
        try:
            ping_db()
            return jsonify({"status": "ok", "database": "connected"}), 200
        except Exception as exc:
            return jsonify({"status": "error", "database": "disconnected", "message": str(exc)}), 500

    @app.errorhandler(404)
    def not_found(_):
        return jsonify({"message": "Route not found"}), 404

    @app.errorhandler(500)
    def server_error(_):
        return jsonify({"message": "Internal server error"}), 500

    try:
        ping_db()
        ensure_indexes()
    except Exception as exc:
        app.logger.warning("MongoDB is not ready yet: %s", exc)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
