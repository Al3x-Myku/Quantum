import numpy as np
from qiskit import QuantumCircuit, ClassicalRegister
from qiskit_aer import AerSimulator
import warnings
import io

# Suppress deprecation warnings from Qiskit for a cleaner output
warnings.filterwarnings('ignore', category=DeprecationWarning)

def create_alice_circuit(bits, bases):
    """Prepares qubits based on Alice's bits and bases."""
    n = len(bits)
    qc = QuantumCircuit(n, name='Alice_Circuit')
    for i in range(n):
        if bits[i] == 1:
            qc.x(i)  # Apply X-gate for bit '1'
        if bases[i] == 1:
            qc.h(i)  # Apply H-gate for basis '+'
    qc.barrier()
    return qc

def measure_message(qc, bases):
    """Measures qubits in the circuit based on the given bases."""
    n = qc.num_qubits
    if not qc.cregs:
        cr = ClassicalRegister(n)
        qc.add_register(cr)

    for i in range(n):
        if bases[i] == 1:
            qc.h(i)  # Apply H-gate to measure in '+' basis

    qc.measure(range(n), range(n))
    return qc

def run_bb84_simulation(with_eve=False, key_length=32):
    """
    Service function to run the BB84 simulation.
    It returns a dictionary with logs and results instead of printing.
    """
    log = []
    log.append(f"--- Rulare simulare BB84 {'CU' if with_eve else 'FĂRĂ'} spion (Lungime Cheie: {key_length}) ---")

    # 1. Alice prepares her bits and bases
    alice_bits = np.random.randint(2, size=key_length)
    alice_bases = np.random.randint(2, size=key_length)
    log.append(f"Biții originali ai lui Alice: {''.join(map(str, alice_bits))}")
    log.append(f"Bazele alese de Alice:       {''.join(map(str, alice_bases))} (0=Rectiliniu, 1=Diagonal)")

    eve_bases_str = None
    eve_measured_str = None

    # Create Alice's quantum circuit
    qc = create_alice_circuit(list(alice_bits), list(alice_bases))

    # 2. Eve intercepts (if present)
    if with_eve:
        log.append("\n<span class='text-danger'>ALERTĂ: Eve interceptează canalul cuantic!</span>")
        eve_bases = np.random.randint(2, size=key_length)
        eve_bases_str = ''.join(map(str, eve_bases))
        log.append(f"Bazele alese de Eve:          {''.join(map(str, eve_bases))}")

        # Eve measures Alice's qubits and resends them
        eve_qc = measure_message(qc.copy(), list(eve_bases))
        simulator = AerSimulator()
        result = simulator.run(eve_qc, shots=1).result()
        eve_measured_bits_str = list(result.get_counts().keys())[0]
        # Qiskit returns strings in reverse order, so we fix it
        eve_measured_bits = [int(bit) for bit in eve_measured_bits_str[::-1]]
        eve_measured_str = ''.join(map(str, eve_measured_bits))
        log.append(f"Biții măsurați de Eve:        {''.join(map(str, eve_measured_bits))}")

        # Eve prepares new qubits based on her measurements to send to Bob
        qc = create_alice_circuit(eve_measured_bits, list(eve_bases))

    # 3. Bob chooses his bases and measures
    bob_bases = np.random.randint(2, size=key_length)
    log.append(f"Bazele alese de Bob:          {''.join(map(str, bob_bases))}")

    full_qc = measure_message(qc.copy(), list(bob_bases))
    simulator = AerSimulator()
    result = simulator.run(full_qc, shots=1, memory=True).result()
    bob_measured_bits_str = result.get_memory()[0]
    bob_measured_bits = [int(bit) for bit in bob_measured_bits_str[::-1]]

    # 4. Sifting: Alice and Bob compare bases publicly
    log.append("\n--- Procesul de cernere (compararea bazelor pe un canal public) ---")
    alice_key = []
    bob_key = []
    match_indices_str = ""
    for i in range(key_length):
        if alice_bases[i] == bob_bases[i]:
            alice_key.append(alice_bits[i])
            bob_key.append(bob_measured_bits[i])
            match_indices_str += '✓'
        else:
            match_indices_str += '✗'
    log.append(f"Potrivire baze (Alice vs Bob): {match_indices_str}")

    # 5. QBER Calculation and Verdict
    mismatches = sum(a != b for a, b in zip(alice_key, bob_key))
    qber = (mismatches / len(alice_key)) if len(alice_key) > 0 else 0.0

    verdict_class = 'text-success'
    if qber > 0.1: # A common threshold for detecting Eve
        verdict = "VERDICT: QBER depășește pragul de securitate! SPIONAJ DETECTAT! Cheia este aruncată."
        verdict_class = 'text-danger'
    else:
        verdict = "VERDICT: Canalul este considerat sigur. Cheia este validă."
    
    log.append("\n--- Rezultate Finale ---")
    log.append(f"Lungimea cheii inițiale: {key_length}")
    log.append(f"Lungimea cheii cernute: {len(alice_key)}")
    log.append(f"Cheia cernută a lui Alice: {''.join(map(str, alice_key))}")
    log.append(f"Cheia cernută a lui Bob:   {''.join(map(str, bob_key))}")
    log.append(f"Număr de nepotriviri: {mismatches}")
    log.append(f"Rata de Eroare Cuantică (QBER): {qber:.2%}")
    log.append(f"\n<span class='{verdict_class} fw-bold'>{verdict}</span>")

    return {
        'log': "\n".join(log)
    }

def run_e91_demo():
    """
    Service function to run the E91 protocol demo.
    Returns a dictionary with the circuit diagram and results.
    """
    # Create a Bell state: |Φ+⟩ = (|00⟩ + |11⟩)/√2
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.barrier()

    # Alice and Bob measure their qubits
    qc.measure([0, 1], [0, 1])
    
    # Capture circuit drawing
    circuit_text = str(qc.draw(output='text'))

    # Simulate the circuit
    simulator = AerSimulator()
    result = simulator.run(qc, shots=1024).result()
    counts = result.get_counts()

    observation = "Observație: Rezultatele sunt întotdeauna perfect corelate ('00' sau '11'). " \
                  "Acest lucru demonstrează principiul inseparabilității (entanglement) " \
                  "folosit în protocolul E91. Orice încercare de spionaj ar distruge această corelație."

    return {
        'circuit': circuit_text,
        'counts': counts,
        'observation': observation
    }