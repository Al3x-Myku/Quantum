import numpy as np
from qiskit import QuantumCircuit, ClassicalRegister
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_vector
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore', category=DeprecationWarning)

def visualize_qubit_states():
    print("\nSe generează vizualizarea stărilor de bază ale qubitului...")

    qc_0 = QuantumCircuit(1)
    qc_1 = QuantumCircuit(1)
    qc_1.x(0)
    qc_plus = QuantumCircuit(1)
    qc_plus.h(0)
    qc_minus = QuantumCircuit(1)
    qc_minus.x(0)
    qc_minus.h(0)

    states = [Statevector(qc_0), Statevector(qc_1), Statevector(qc_plus), Statevector(qc_minus)]
    titles = ['Starea |0⟩', 'Starea |1⟩', 'Starea |+⟩', 'Starea |−⟩']

    fig, axes = plt.subplots(2, 2, figsize=(8, 8), subplot_kw={'projection': '3d'})
    axes_flat = axes.flatten()

    for i, (state, title) in enumerate(zip(states, titles)):
        plot_bloch_vector(state.data, title=title, ax=axes_flat[i])

    plt.tight_layout()
    try:
        fig.savefig("bloch_sphere_states.png")
        print("Figura 'bloch_sphere_states.png' a fost salvată.")
        plt.show()
    except Exception as e:
        print(f"Nu s-a putut afișa sau salva graficul: {e}")
        print("Este posibil să rulați într-un mediu fără interfață grafică.")

def create_alice_circuit(bits, bases):
    n = len(bits)
    qc = QuantumCircuit(n, name='Alice_Circuit')
    for i in range(n):
        if bits[i] == 1:
            qc.x(i)
        if bases[i] == 1:
            qc.h(i)
    qc.barrier()
    return qc

def measure_message(qc, bases):
    n = qc.num_qubits
    if not qc.cregs:
        cr = ClassicalRegister(n)
        qc.add_register(cr)

    for i in range(n):
        if bases[i] == 1:
            qc.h(i)

    qc.measure(range(n), range(n))
    return qc

def run_e91_demo():
    print("\n--- Rulare demonstrație E91 ---")
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.barrier()

    qc.measure([0, 1], [0, 1])

    print("Circuit E91 (stare Bell + măsurare):")
    print(qc)

    simulator = AerSimulator()
    result = simulator.run(qc, shots=1024).result()
    counts = result.get_counts()

    print("\nRezultatele măsurătorilor (1024 de rulări):")
    print(counts)
    print("Observație: Rezultatele sunt întotdeauna corelate ('00' sau '11').")
    print("Acest lucru demonstrează principiul inseparabilității folosit în E91.")

def run_bb84_simulation(with_eve=False):
    KEY_LENGTH = 32
    print(f"\n--- Rulare simulare BB84 {'CU' if with_eve else 'FĂRĂ'} spion ---")

    alice_bits = np.random.randint(2, size=KEY_LENGTH)
    alice_bases = np.random.randint(2, size=KEY_LENGTH)
    print(f"Biții originali ai lui Alice: {''.join(map(str, alice_bits))}")
    print(f"Bazele alese de Alice:       {''.join(map(str, alice_bases))}")

    if not with_eve:
        qc = create_alice_circuit(list(alice_bits), list(alice_bases))
    else:
        print("\nALERTĂ: Eve interceptează canalul cuantic!")
        eve_bases = np.random.randint(2, size=KEY_LENGTH)
        eve_measured_bits = []

        simulator = AerSimulator()
        for i in range(KEY_LENGTH):
            temp_qc = QuantumCircuit(1, 1)
            if alice_bits[i] == 1: temp_qc.x(0)
            if alice_bases[i] == 1: temp_qc.h(0)
            if eve_bases[i] == 1: temp_qc.h(0)
            temp_qc.measure(0, 0)

            result = simulator.run(temp_qc, shots=1).result()
            measured_bit = int(list(result.get_counts().keys())[0])
            eve_measured_bits.append(measured_bit)

        print(f"Bazele alese de Eve:         {''.join(map(str, eve_bases))}")
        print(f"Biții măsurați de Eve:       {''.join(map(str, eve_measured_bits))}")

        qc = create_alice_circuit(eve_measured_bits, list(eve_bases))

    bob_bases = np.random.randint(2, size=KEY_LENGTH)
    print(f"Bazele alese de Bob:         {''.join(map(str, bob_bases))}")
    full_qc = measure_message(qc.copy(), list(bob_bases))

    simulator = AerSimulator()
    result = simulator.run(full_qc, shots=1).result()

    counts = result.get_counts()
    if not counts:
        print("EROARE: Simularea nu a produs niciun rezultat. Se anulează.")
        return

    bob_measured_bits_str = list(counts.keys())[0]

    padded_str = bob_measured_bits_str.zfill(KEY_LENGTH)
    reversed_str = padded_str[::-1]
    bob_measured_bits = [int(bit) for bit in reversed_str]

    alice_key = []
    bob_key = []

    print("\n--- Procesul de cernere (compararea bazelor) ---")
    match_indices = []
    for i in range(KEY_LENGTH):
        if alice_bases[i] == bob_bases[i]:
            alice_key.append(alice_bits[i])
            bob_key.append(bob_measured_bits[i])
            match_indices.append('✓')
        else:
            match_indices.append('✗')
    print(f"Potrivire baze (A vs B):   {''.join(match_indices)}")

    if len(alice_key) > 0:
        mismatches = sum(a != b for a, b in zip(alice_key, bob_key))
        qber = mismatches / len(alice_key)
    else:
        mismatches = 0
        qber = 0.0

    print(f"\nLungimea cheii inițiale: {KEY_LENGTH}")
    print(f"Lungimea cheii cernute: {len(alice_key)}")
    print(f"Cheia cernută a lui Alice: {''.join(map(str, alice_key))}")
    print(f"Cheia cernută a lui Bob:   {''.join(map(str, bob_key))}")
    print(f"Număr de nepotriviri: {mismatches}")
    print(f"Rata de Eroare Cuantică (QBER): {qber:.2%}")

    if qber > 0.11:
        print("\nVERDICT: QBER depășește pragul de securitate! SPIONAJ DETECTAT! Cheia este aruncată.")
    else:
        print("\nVERDICT: Canalul este considerat sigur. Cheia este validă.")

def main_menu():
    while True:
        print("\n" + "="*20 + " QKD Explorer: Meniu Principal " + "="*20)
        print("1. Vizualizează Stările Qubitului pe Sfera Bloch")
        print("2. Rulează Simulare BB84 (Canal Ideal, fără spion)")
        print("3. Rulează Simulare BB84 (cu Spionul Eve)")
        print("4. Rulează Demonstrație Entanglement (Protocol E91)")
        print("5. Ieșire")
        choice = input("Introduceți alegerea dvs. (1-5): ")

        if choice == '1':
            visualize_qubit_states()
        elif choice == '2':
            run_bb84_simulation(with_eve=False)
        elif choice == '3':
            run_bb84_simulation(with_eve=True)
        elif choice == '4':
            run_e91_demo()
        elif choice == '5':
            print("La revedere!")
            break
        else:
            print("Alegere invalidă. Vă rugăm să încercați din nou.")

if __name__ == '__main__':
    main_menu()