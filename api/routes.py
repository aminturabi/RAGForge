"""HTTP route handlers."""

import os
import uuid

from flask import Blueprint, current_app, jsonify, request

from core.exceptions import DocumentLoadError
from core.registry import list_all_plugins

api_bp = Blueprint("api", __name__, url_prefix="/api")


def _service():
    return current_app.config["RAG_SERVICE"]


@api_bp.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file part in the request"}), 400

    uploaded_file = request.files["file"]
    if uploaded_file.filename == "":
        return jsonify({"success": False, "error": "No file selected"}), 400

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)
    _, ext = os.path.splitext(uploaded_file.filename)
    temp_path = os.path.join(upload_folder, f"{uuid.uuid4()}{ext}")

    try:
        uploaded_file.save(temp_path)
        result = _service().index_document(temp_path, uploaded_file.filename)
        return jsonify({"success": True, "message": "Document uploaded and indexed successfully!", **result})
    except ValueError as error:
        return jsonify({"success": False, "error": str(error)}), 400
    except DocumentLoadError as error:
        return jsonify({"success": False, "error": str(error)}), 400
    except Exception as error:
        current_app.logger.exception("Error during upload and index")
        return jsonify({"success": False, "error": f"Internal Server Error: {error}"}), 500
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


@api_bp.route("/query", methods=["POST"])
def query_collection():
    data = request.json or {}
    query = data.get("query", "")
    collection_name = data.get("collection_name", "")
    api_key_override = data.get("api_key", "").strip()
    top_k = int(data.get("top_k", 4))

    if not query.strip():
        return jsonify({"success": False, "error": "Query is required"}), 400
    if not collection_name.strip():
        return jsonify({"success": False, "error": "Collection name is required (upload a document first)"}), 400

    if not api_key_override and not os.environ.get("GROQ_API_KEY"):
        return jsonify(
            {
                "success": False,
                "error": "Groq API Key is missing. Please configure it in your environment or provide it in request.",
            }
        ), 400

    try:
        payload = _service().query(collection_name=collection_name, query=query, top_k=top_k, api_key=api_key_override)
        return jsonify({"success": True, **payload})
    except Exception as error:
        current_app.logger.exception("Error querying collection")
        return jsonify({"success": False, "error": str(error)}), 500


@api_bp.route("/collections", methods=["GET"])
def list_collections():
    try:
        return jsonify({"success": True, "collections": _service().list_collections()})
    except Exception as error:
        return jsonify({"success": False, "error": str(error)}), 500


@api_bp.route("/clear", methods=["POST"])
def clear_collection():
    data = request.json or {}
    collection_name = data.get("collection_name", "")
    if not collection_name:
        return jsonify({"success": False, "error": "Collection name is required"}), 400
    try:
        success = _service().clear_collection(collection_name)
        if success:
            return jsonify({"success": True, "message": f"Collection {collection_name} cleared successfully."})
        return jsonify({"success": False, "error": "Collection not found or could not be deleted."}), 404
    except Exception as error:
        return jsonify({"success": False, "error": str(error)}), 500


@api_bp.route("/plugins", methods=["GET"])
def get_plugins():
    try:
        return jsonify({"success": True, "plugins": list_all_plugins()})
    except Exception as error:
        return jsonify({"success": False, "error": str(error)}), 500

