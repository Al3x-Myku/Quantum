import numpy as np
from qiskit import QuantumCircuit, ClassicalRegister
from qiskit_aer import AerSimulator
import warnings

warnings.filterwarnings('ignore', category=DeprecationWarning)

def create_alice_circuit(bits, bases):
    n = len(bits)
    qc = QuantumCircuit(n, name='Alice_Circuit')
    for i in range(n):
        if bits[i] == 1: qc.x(i)
        if bases[i] == 1: qc.h(i)
    qc.barrier()
    return qc

def measure_message(qc, bases):
    n = qc.num_qubits
    if not qc.cregs:
        cr = ClassicalRegister(n)
        qc.add_register(cr)
    for i in range(n):
        if bases[i] == 1: qc.h(i)
    qc.measure(range(n), range(n))
    return qc

def run_bb84_simulation(with_eve=False, key_length=32):
    log = []
    log.append(f"--- Rulare simulare BB84 {'CU' if with_eve else 'FĂRĂ'} spion (Lungime Cheie: {key_length}) ---")
    alice_bits = np.random.randint(2, size=key_length)
    alice_bases = np.random.randint(2, size=key_length)
    log.append(f"Biții originali ai lui Alice: {''.join(map(str, alice_bits))}")
    log.append(f"Bazele alese de Alice:       {''.join(map(str, alice_bases))} (0=Rectiliniu, 1=Diagonal)")
    qc = create_alice_circuit(list(alice_bits), list(alice_bases))
    if with_eve:
        log.append("\n<span class='text-danger'>ALERTĂ: Eve interceptează canalul cuantic!</span>")
        eve_bases = np.random.randint(2, size=key_length)
        log.append(f"Bazele alese de Eve:          {''.join(map(str, eve_bases))}")
        eve_qc = measure_message(qc.copy(), list(eve_bases))
        simulator = AerSimulator()
        result = simulator.run(eve_qc, shots=1).result()
        eve_measured_bits_str = list(result.get_counts().keys())[0]
        eve_measured_bits = [int(bit) for bit in eve_measured_bits_str[::-1]]
        log.append(f"Biții măsurați de Eve:        {''.join(map(str, eve_measured_bits))}")
        qc = create_alice_circuit(eve_measured_bits, list(eve_bases))
    bob_bases = np.random.randint(2, size=key_length)
    log.append(f"Bazele alese de Bob:          {''.join(map(str, bob_bases))}")
    full_qc = measure_message(qc.copy(), list(bob_bases))
    simulator = AerSimulator()
    result = simulator.run(full_qc, shots=1, memory=True).result()
    bob_measured_bits_str = result.get_memory()[0]
    bob_measured_bits = [int(bit) for bit in bob_measured_bits_str[::-1]]
    log.append("\n--- Procesul de cernere (compararea bazelor pe un canal public) ---")
    alice_key, bob_key = [], []
    match_indices_str = ""
    for i in range(key_length):
        if alice_bases[i] == bob_bases[i]:
            alice_key.append(alice_bits[i])
            bob_key.append(bob_measured_bits[i])
            match_indices_str += '✓'
        else:
            match_indices_str += '✗'
    log.append(f"Potrivire baze (Alice vs Bob): {match_indices_str}")
    mismatches = sum(a != b for a, b in zip(alice_key, bob_key))
    qber = (mismatches / len(alice_key)) if len(alice_key) > 0 else 0.0
    verdict_class = 'text-success'
    if qber > 0.1:
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
    return {'log': "\n".join(log)}

def run_e91_demo():
    """
    Service function to run the E91 protocol demo.
    Returns a dictionary with the circuit diagram and results.
    """
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.barrier()

    qc.measure([0, 1], [0, 1])
    
    circuit_diagram = qc.draw(output='text')

    simulator = AerSimulator()
    result = simulator.run(qc, shots=1024).result()
    counts = result.get_counts()

    observation = "Observație: Rezultatele sunt întotdeauna perfect corelate ('00' sau '11'). " \
                  "Acest lucru demonstrează principiul inseparabilității (entanglement) " \
                  "folosit în protocolul E91. Orice încercare de spionaj ar distruge această corelație."

    return {
        'circuit': str(circuit_diagram),
        'counts': counts,
        'observation': observation
    }