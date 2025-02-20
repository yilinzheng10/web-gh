import os
import time
import json
import logging
from flask import Flask, request, render_template, send_from_directory, make_response

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

def wait_for_file(file_path, timeout=30):
    start_time = time.time()
    while not os.path.exists(file_path):
        if time.time() - start_time > timeout:
            logging.error(f"Timeout waiting for file: {file_path}")
            return False
        time.sleep(1)
    return True

# Home route for the configuration page
@app.route('/')
def index():
    logging.debug("Rendering index page.")
    return render_template('index.html', image_path="", form_data={})

@app.route('/store')
def next_page():
    return render_template('description.html', image_path="", form_data={})

@app.route('/static/<path:filename>')
def static_files(filename):
    response = make_response(send_from_directory('static', filename))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# POST route to handle configuration submission
@app.route('/', methods=['POST'])
def submit():
    try:
        form_data = request.form.to_dict()
        logging.debug(f"Received form data: {form_data}")
        
        # Check for configuration submission
        if 'config_x_range' in form_data and form_data.get('data_type') == 'config':
            room_number = form_data.get('room_x_range', "0")
            output_data = {
                "config_room_value": room_number,
                "config_corridor_value": form_data.get('config_x_range', "0"),
                "config_rack_value": form_data.get('config_y_range', "0")
            }
            config_data_file = os.path.join('static', f'{room_number}config.txt')
            try:
                with open(config_data_file, 'w') as f:
                    json.dump(output_data, f)
                logging.info(f"Saved configuration data to {config_data_file}.")
            except Exception as file_error:
                logging.error(f"Error writing to {config_data_file}: {file_error}")
                raise

        else:
            logging.warning("Unknown or incomplete form submission detected.")

        # Process screenshot as before
        screenshot_file = 'static/screenshot.jpg'
        if os.path.exists(screenshot_file):
            os.remove(screenshot_file)
            logging.debug(f"Removed old screenshot: {screenshot_file}")

        if not wait_for_file(screenshot_file, timeout=30):
            raise FileNotFoundError("Screenshot was not created in time.")

        return render_template('index.html', image_path=screenshot_file, form_data=form_data)

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return render_template('index.html', image_path="", form_data=form_data, error=str(e))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)