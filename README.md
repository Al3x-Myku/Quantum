Bun venit la QKD Explorer, o aplicație web interactivă, creată pentru a face conceptele complexe ale criptografiei cuantice accesibile și distractive. Prin simulări vizuale și minigame-uri, acest proiect își propune să demonstreze principiile fundamentale care stau la baza securității cuantice, cum ar fi superpoziția, măsurătoarea, inseparabilitatea (entanglement) și detectarea spionilor.

![Pagina Principală](static/images/intro_box.gif)

## Funcționalități Principale

Platforma include o serie de module interactive, fiecare concentrându-se pe un aspect diferit al mecanicii cuantice și al QKD:

### 1. Simulări de Protocoale Fundamentale
- **Sfera Bloch Interactivă:** O vizualizare 3D a unui qubit, unde utilizatorii pot manipula unghiurile theta (θ) și phi (φ) pentru a vedea cum se schimbă vectorul de stare și probabilitățile de măsurare.
- **Simulare BB84 (fără spion):** O demonstrație animată, pas cu pas, a protocolului BB84 într-un canal ideal, arătând cum Alice și Bob stabilesc o cheie secretă comună.
- **Simulare BB84 (cu spion):** Introduce spionul "Eve" în canal. Simularea demonstrează vizual cum acțiunile lui Eve introduc erori (QBER > 0) și cum acestea pot fi detectate, compromițând cheia.
- **Simulare E91 (Entanglement):** O demonstrație vizuală a protocolului bazat pe inseparabilitate cuantică, unde o sursă emite perechi de particule corelate. Include și o verificare simplificată a inegalității Bell (Testul CHSH).

### 2. Minigames Cuantice
Pentru a explora conceptele într-un mod relaxat și distractiv, am creat o secțiune de minigames:
- **Quantum Slots:** Un joc de păcănele unde rezultatul este determinat de colapsul funcției de undă a 3 qubiți, garantând o aleatorietate cu adevărat cuantică.
- **Quantum Sweeper:** O variantă a clasicului Minesweeper unde poziția minelor nu este stabilită de la început. Primul click al jucătorului "măsoară" sistemul, colapsând starea de superpoziție și fixând configurația minelor pentru restul jocului.

### 3. Modul Interactiv Multi-Player (Local)
- **Lobby de Joc:** Permite crearea unei sesiuni de joc BB84 locale.
- **Sincronizare Multi-Tab:** Folosind `LocalStorage`, permite mai multor utilizatori (sau utilizatorului în tab-uri diferite) să joace rolurile lui Alice, Bob și Eve în timp real.
- **Panou de Observator:** O pagină dedicată care afișează în timp real, cu animații, acțiunile tuturor participanților.

---

## Tehnologii Folosite
- **Backend:** Python cu Flask
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Biblioteci & Framework-uri:**
  - Bootstrap 5 pentru layout și componente UI.
  - `particles.js` pentru fundalul animat.
  - Plotly.js pentru grafice (în Sfera Bloch și E91).
- **Concepte Cheie:**
  - Simulări cuantice realizate direct în JavaScript.
  - Sincronizare locală între tab-uri folosind `LocalStorage` și evenimentul `storage`.

---

## Instalare și Rulare

Pentru a rula acest proiect local, urmează pașii de mai jos.

### Prerechizite
- Python 3.6 sau o versiune mai recentă.
- `pip` (managerul de pachete pentru Python).

### Pași de Instalare

1.  **Clonează repository-ul:**
    ```bash
    git clone https://github.com/Al3x-Myku/Quantum
    cd Quantum
    ```

2.  **Creează și activează un mediu virtual:**
    ```bash
    # Pentru Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Pentru macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instalează dependențele:**
    Proiectul folosește un fișier `requirements.txt` pentru a gestiona pachetele necesare.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Rulează aplicația:**
    ```bash
    python .\run.py
    ```
    
    Aplicația va porni și va fi accesibilă în browser la adresa `http://127.0.0.1:5000`.

---
