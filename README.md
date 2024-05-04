# PromtGallery

This is a Flask web application that extracts prompts from images and stores them in a database. It allows users to scan a directory for PNG files, extract prompts from them, and search for images based on prompts.

## Features

- **Prompt Extraction**: Automatically extracts prompts from images and stores them in a database.
- **Search Functionality**: Allows users to search for images based on prompts.
- **Simple User Interface**: Provides a clean and intuitive web interface for interacting with the application.

---

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Lainupcomputer/PromtGallery.git
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables:

    - `SECRET_KEY`: Secret key for Flask app (optional).
    - `SQLALCHEMY_DATABASE_URI`: URI for the database (default is SQLite).

4. Run the application:

    ```bash
    python app.py
    ```

---
## Usage

1. Navigate to the application in your web browser (by default, it should be [http://localhost:5000/](http://localhost:5000/)).
2. Click on the "Scan" button to scan the directory for PNG files and extract prompts from them.
3. Use the search bar to search for images based on prompts.
4. Click on images to view detailed prompt information.

---
## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

---
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



