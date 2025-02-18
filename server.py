import os
import time
import json
import logging
from flask import Flask, request, render_template, send_from_directory, make_response




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





@app.route('/static/<path:filename>')
def static_files(filename):
    response = make_response(send_from_directory('static', filename))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response



# POST route to handle user input
@app.route('/', methods=['POST'])
def submit():
    """Handle form submission and process inputs."""
    try:
        # Get form data from the request
        form_data = request.form.to_dict()
        logging.debug(f"Received form data: {form_data}")


        # Check which form is being submitted based on form identifier
        if 'room_x_range' in form_data:  # Room form
            # Save room data to room_data.txt
            room_data_file = 'static/room_data.txt'
            with open(room_data_file, 'w') as f:
                json.dump(form_data, f)
            logging.info(f"Saved room data to {room_data_file}.")


        elif 'config_x_range' in form_data:  # Configuration form
            # Save configuration data to config_data.txt
            config_data_file = 'static/config_data.txt'
            with open(config_data_file, 'w') as f:
                json.dump(form_data, f)
            logging.info(f"Saved configuration data to {config_data_file}.")
        
        else:
            logging.warning("Unknown form submission detected.")


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
    app.run(debug=True, host='127.0.0.1', port=5000)