from flask import Flask, request, render_template, jsonify, send_file
from PIL import Image, ExifTags
import os
import json
from collections import OrderedDict
import io

# Flask-Anwendung erstellen
app = Flask(__name__)

# Verzeichnis für hochgeladene Bilder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Speicher für die letzten Metadaten
latest_metadata = None  # Hier werden die aktuellen Metadaten gespeichert

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    global latest_metadata  # Aktuelle Metadaten global speichern

    if 'file' not in request.files:
        return jsonify({'error': 'No file part in request'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Datei speichern
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    image = Image.open(filepath)

    result = OrderedDict()
    result['format'] = image.format
    result['info'] = OrderedDict()

    if image.format == "JPEG":
        # EXIF-Daten auslesen
        exif_data = image._getexif()
        if exif_data:
            exif_info = OrderedDict()
            for tag_id, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag_id, tag_id)  # EXIF-Tag-Name
                exif_info[tag_name] = str(value)  # EXIF-Wert als Zeichenfolge

            user_comment = exif_info.get("UserComment", "Nicht gefunden")

            result['info']['User Comment'] = user_comment
        else:
            result['error'] = "Keine EXIF-Daten gefunden."

    elif image.format == "PNG":
        # PNG-Metadaten auslesen
        prompt_text = ""
        negative_prompt_text = ""
        steps_text = ""

        for key, value in image.info.items():
            if isinstance(value, str):
                if "Negative prompt:" in value:
                    parts = value.split("Negative prompt:")
                    prompt_text = parts[0].strip()

                    if "Steps:" in parts[1]:
                        steps_split = parts[1].split("Steps:")
                        negative_prompt_text = steps_split[0].strip()
                        steps_text = "Steps:" + steps_split[1].strip()
                    else:
                        negative_prompt_text = parts[1].strip()

        result['info']['Prompt'] = prompt_text
        result['info']['Negative Prompt'] = negative_prompt_text
        result['info']['Steps'] = steps_text

    else:
        result['error'] = "Unsupported file format"

    # Metadaten speichern
    latest_metadata = result  # Metadaten global speichern
    return jsonify(result)

@app.route('/download', methods=['GET'])
def download():
    # Prüfen, ob aktuelle Metadaten vorhanden sind
    if latest_metadata is None:
        return jsonify({'error': 'No metadata to download'})

    # Metadaten als JSON-Datei vorbereiten
    json_data = json.dumps(latest_metadata, indent=4)
    filename = "metadata.txt"  # Dateiname für den Download
    json_bytes = json_data.encode("utf-8")  # In Bytes umwandeln

    # Byte-Objekt für den Download erstellen
    file_obj = io.BytesIO(json_bytes)  # Bytes in einem Speicherobjekt
    file_obj.seek(0)  # An den Anfang des Streams gehen

    return send_file(
        file_obj,
        as_attachment=True,
        download_name=filename,  # Name der herunterladbaren Datei
        mimetype='text/plain'  # Mimetype für Textdateien
    )

# Flask-App starten
if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Läuft auf allen Schnittstellen mit Port 5000