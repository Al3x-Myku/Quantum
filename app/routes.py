from flask import render_template, current_app

# Get current app from context to register routes
app = current_app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bloch')
def bloch():
    return render_template('bloch.html')

# --- SIMULARI SINGLE-PLAYER ---
@app.route('/bb84')
def bb84():
    return render_template('bb84.html')

@app.route('/bb84_eve')
def bb84_eve():
    return render_template('bb84_eve.html')

@app.route('/e91')
def e91():
    # Presupunand ca ai un e91.html
    return render_template('e91.html')

@app.route('/quantum_slots')
def quantum_slots():
    return render_template('quantum_slots.html')

@app.route('/quantum_sweeper')
def quantum_sweeper_eve():
    return render_template('quantum_sweeper.html')

# --- JOC INTERACTIV LOCAL (MULTI-TAB) ---

# Ruta pentru Lobby
@app.route('/interactive_bb84')
def interactive_bb84_lobby():
    """Randeaza lobby-ul de unde se pot crea jocuri locale."""
    return render_template('interactive_bb84.html')

@app.route('/minigames')
def minigames():
    return render_template('minigames.html')


# Ruta pentru paginile de joc ale participantilor
@app.route('/play_bb84_local')
def play_bb84_local():
    """
    Randeaza pagina de joc. JavaScript-ul de pe aceasta pagina va prelua
    gameId si rolul din URL pentru a afisa UI-ul corespunzator.
    """
    # Vom crea acest fisier in pasul urmator.
    return render_template('play_bb84_local.html')


@app.route('/lobby')
def lobby():
    return render_template('lobby.html')