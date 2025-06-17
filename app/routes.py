from flask import render_template, jsonify, request, current_app
from . import services


app = current_app

@app.route('/')
def index():
    """Renders the main homepage."""
    return render_template('index.html')

@app.route('/bloch')
def bloch():
    """Renders the interactive Bloch Sphere page."""
    return render_template('bloch.html')

@app.route('/bb84')
def bb84():
    """Renders the BB84 simulation page (no spy)."""
    return render_template('bb84.html')

@app.route('/bb84_eve')
def bb84_eve():
    """Renders the BB84 simulation page (with spy)."""
    return render_template('bb84_eve.html')

@app.route('/e91')
def e91():
    """Renders the E91 simulation page."""
    return render_template('e91.html')


@app.route('/api/run_bb84', methods=['POST'])
def api_run_bb84():
    """API endpoint to run the BB84 simulation."""
    try:
        data = request.get_json()
        key_length = int(data.get('key_length', 32))
        with_eve = data.get('with_eve', False)
        
        if not 8 <= key_length <= 128:
             return jsonify(error="Key length must be between 8 and 128."), 400

        result = services.run_bb84_simulation(with_eve=with_eve, key_length=key_length)
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Error in BB84 simulation: {e}")
        return jsonify(error=str(e)), 500

@app.route('/api/run_e91', methods=['POST'])
def api_run_e91():
    """API endpoint to run the E91 simulation."""
    try:
        result = services.run_e91_demo()
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Error in E91 simulation: {e}")
        return jsonify(error=str(e)), 500