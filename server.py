import os
import time
import json
import logging
from flask import Flask, request, render_template

# Initialize Flask app
app = Flask(__name__)

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Helper function to wait for file creation with a timeout
def wait_for_file(file_path, timeout=30):
    """Wait for a file to be created, with a timeout."""
    start_time = time.time()
    while not os.path.exists(file_path):
        if time.time() - start_time > timeout:
            logging.error(f"Timeout waiting for file: {file_path}")
            return False  # File not created within timeout
        time.sleep(1)
    return True

# Home route for the web UI
@app.route('/')
def index():
    """Render the main page with sliders and submit button."""
    logging.debug("Rendering index page.")
    return render_template('index.html', image_path="", form_data={})

# POST route to handle user input
@app.route('/', methods=['POST'])
def submit():
    """Handle form submission and process inputs."""
    try:
        # Get form data
        form_data = request.form.to_dict()
        logging.debug(f"Received form data: {form_data}")

        # Save form data to inputs.txt
        inputs_file = 'static/inputs.txt'
        with open(inputs_file, 'w') as f:
            json.dump(form_data, f)
        logging.info(f"Saved form data to {inputs_file}.")

        # Prepare to process screenshot
        screenshot_file = 'static/screenshot.jpg'
        if os.path.exists(screenshot_file):
            os.remove(screenshot_file)  # Remove old screenshot
            logging.debug(f"Removed old screenshot: {screenshot_file}")

        # Wait for Grasshopper or Rhino to generate the screenshot
        if not wait_for_file(screenshot_file, timeout=30):
            raise FileNotFoundError("Screenshot was not created in time.")

        # Render the updated page with the new screenshot
        return render_template('index.html', image_path=screenshot_file, form_data=form_data)

    except Exception as e:
        # Log the error and return the error message to the UI
        logging.error(f"Error processing request: {e}")
        return render_template('index.html', image_path="", form_data=form_data, error=str(e))

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)