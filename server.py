from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure upload folder exists
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "mp4", "avi"}

def allowed_file(filename):
    """Check if the uploaded file has a valid extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/run/<script>", methods=["POST"])
def run_script(script):
    """
    Runs different Python scripts based on the requested action.

    - `main.py` and `video_analysis.py` require a file upload.
    - `main1.py` and `live_analysis.py` run directly (no file needed).
    """

    # ✅ Handle Image & Video Uploads (For `main.py` & `video_analysis.py`)
    if script in ["main", "video_analysis"]:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files["file"]
        
        if file.filename == "" or not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type"}), 400

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        if script == "main":
            python_script = "main.py"
        elif script == "video_analysis":
            python_script = "video_analysis.py"

        try:
            subprocess.Popen(["python", python_script, file_path], shell=True)
            return jsonify({"message": f"{python_script} started successfully with {file_path}!"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # ✅ Handle Live Analysis Scripts (`main1.py` & `live_analysis.py`) - No File Needed
    elif script in ["main1", "live_analysis"]:
        python_script = f"{script}.py"  # Convert script name to filename

        try:
            subprocess.Popen(["python", python_script], shell=True)
            return jsonify({"message": f"{python_script} started successfully!"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    else:
        return jsonify({"error": "Invalid script"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
