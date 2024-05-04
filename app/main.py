from flask import Flask, render_template, request, redirect, Response, jsonify
import os
from PIL import Image
from database import db, DImage
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_prompts(db, img_path: str) -> None:
    """
    Extract prompts from an image, check if it exists in the database, and add it if not.

    Args:
        db: The database session.
        img_path (str): The path to the image file.

    Returns:
        None
    """
    image = Image.open(img_path)
    existing_image = db.session.query(DImage).filter_by(img_path=img_path).first()
    if existing_image:
        logger.info(f"{img_path} existing, skipping")
        return
    else:
        logger.info(f"{img_path} added to database")

    prompt_text: str = ""
    negative_prompt_text: str = ""

    for key, value in image.info.items():
        if isinstance(value, str):
            if "Negative prompt:" in value:
                parts = value.split("Negative prompt:")
                prompt_text = parts[0].strip()

                if "Steps:" in parts[1]:
                    steps_split = parts[1].split("Steps:")
                    negative_prompt_text = steps_split[0].strip()

                else:
                    negative_prompt_text = parts[1].strip()

    re_path = img_path.split("static/")
    new = DImage(positive=prompt_text, negative=negative_prompt_text, img_path=re_path[1])
    db.session.add(new)
    db.session.commit()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "keep-me-secret")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///database.db")
    db.init_app(app)
    with app.app_context():
        db.create_all()
    logger.info("Application initialised")

    @app.route("/", methods=["GET"])
    def main() -> str:
        """
        Render the main HTML page.

        Returns:
            str: The rendered HTML content.
        """
        logger.info("Showing main Page")
        return render_template("main.html")

    @app.route("/scan", methods=["GET"])
    def scan() -> Response:
        """
        Scan the 'static/images' directory for PNG files,
        extract prompts from them, and redirect to the main page.

        Returns:
            str: A redirect response to the main page.
        """

        os.makedirs("static/images", exist_ok=True)
        logger.info("Scanning directory for PNG files")
        logger.info(f"Files in directory: {len(os.listdir('static/images'))}")
        for file_name in os.listdir("static/images"):
            if file_name.endswith(".png"):
                get_prompts(db, "static/images/" + file_name)
        return redirect("/")

    @app.route("/search", methods=["POST"])
    def search() -> str:
        _search = request.form.get("search")
        logger.info(f"searched for: {_search}")
        paths = db.session.query(DImage.img_path).filter(DImage.positive.like(f"%{_search}%")).all()
        results = [path[0] for path in paths]
        logger.info(f"Found: {results}")
        return render_template("search.html", q=results)

    @app.route("/img_info")
    def get_img_info():
        image_name = request.args.get('imageName')
        image_info = db.session.query(DImage).filter_by(img_path=image_name).first()
        if image_info:
            return jsonify({'positive': image_info.positive, 'negative': image_info.negative})
        else:
            return jsonify({'error': 'Image information not found'}), 404

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)