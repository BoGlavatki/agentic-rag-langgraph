from dotenv import load_dotenv, find_dotenv
from flask import Flask, request, jsonify, render_template
from ice_breaker import ice_break_with

import requests
from urllib.parse import unquote

load_dotenv(find_dotenv())

app = Flask(__name__)


@app.route("/ice_break")
def index():
    return render_template("index.html")


@app.route("/proxy-image")
def proxy_image():
    """Proxy für LinkedIn-Bilder"""
    image_url = request.args.get("url")
    if not image_url:
        return "URL fehlt", 400

    try:
        # Hole das Bild über Server
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(image_url, headers=headers, stream=True)

        if response.status_code == 200:
            return (
                response.content,
                200,
                {
                    "Content-Type": response.headers.get("Content-Type", "image/jpeg"),
                    "Cache-Control": "max-age=3600",
                },
            )
        else:
            return "Bild nicht verfügbar", 404
    except:
        return "Fehler beim Laden", 500


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        # Get name from request
        data = request.get_json()
        if not data or "name" not in data:
            return jsonify({"error": "Name ist erforderlich"}), 400

        name = data["name"].strip()
        if not name:
            return jsonify({"error": "Name darf nicht leer sein"}), 400
        print(f"Received name: {name}")
        # Call your ice_break_with function
        summary, linkedin_url = ice_break_with(name)
        print(f"LinkedIn URL: {linkedin_url}")

        photo_url = f"/proxy-image?url={linkedin_url.get('linkedInUrl')}"
        positions = linkedin_url.get("positions").get("positionHistory")
        current_position = positions[0].get(
            "title", "Aktuelle Position nicht verfügbar"
        )
        # Return structured response that matches your HTML template
        response = {
            "name": name,
            "linkedin_url": photo_url,
            "title": current_position,
            "summary": summary.summary if hasattr(summary, "summary") else str(summary),
            "facts": summary.facts if hasattr(summary, "facts") else [],
            "ice_breakers": [
                f"Sprechen Sie über {name}s Erfahrung bei {summary.company if hasattr(summary, 'company') else 'dem Unternehmen'}",
                f"Fragen Sie nach {name}s aktuellen Projekten",
                f"Diskutieren Sie gemeinsame Interessen oder Branchen-Trends",
            ],
            "location": linkedin_url.get("location", "Standort nicht verfügbar"),
            "company": positions[0].get("companyName", "Unternehmen nicht verfügbar"),
            "skills": linkedin_url.get("skills", [])[:10],
        }

        return jsonify(response)

    except Exception as e:
        print(f"Error in analyze endpoint: {str(e)}")
        return jsonify({"error": f"Fehler bei der Analyse: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5001)
