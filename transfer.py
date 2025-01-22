import cirq
from cirq.contrib.svg import SVGCircuit

# Define three qubits
qubit_psi = cirq.NamedQubit("psi")  # The qubit to teleport
qubit_a = cirq.NamedQubit("A")      # Part of the entangled pair (Alice)
qubit_b = cirq.NamedQubit("B")      # Part of the entangled pair (Bob)

# Create the circuit
circuit = cirq.Circuit()

# Step 1: Prepare an entangled Bell state between qubit_a and qubit_b
circuit.append(cirq.H(qubit_a))      # Apply a Hadamard gate to qubit_a
circuit.append(cirq.CNOT(qubit_a, qubit_b))  # Apply a CNOT gate

# Step 2: Bell measurement of qubit_psi and qubit_a
circuit.append(cirq.CNOT(qubit_psi, qubit_a))  # Apply a CNOT gate
circuit.append(cirq.H(qubit_psi))              # Apply a Hadamard gate

# Step 3: Measure qubit_psi and qubit_a
circuit.append(cirq.measure(qubit_psi, key="m_psi"))
circuit.append(cirq.measure(qubit_a, key="m_a"))

# Step 4: Use the measurement results to apply corrections to qubit_b
# Define classical-controlled operations
classical_correction = [
    (cirq.X(qubit_b).with_classical_controls(cirq.KeyCondition("m_a"))),
    (cirq.Z(qubit_b).with_classical_controls(cirq.KeyCondition("m_psi"))),
]

circuit.append(classical_correction)

# Print the circuit
print("Quantum Teleportation Circuit:")
print(circuit)

# Simulate the circuit
simulator = cirq.Simulator()

# Define the initial state of qubit_psi (to teleport |+> state, use |0> + |1>)
initial_state = cirq.Circuit()
initial_state.append([cirq.H(qubit_psi)])

# Combine the initialization and teleportation circuits
full_circuit = initial_state + circuit

# Simulate and collect the results
result = simulator.run(full_circuit, repetitions=1)

# Display the results
print("\nResults:")
print(result)


print("\nCircuit Visualization:")
svg_circuit = SVGCircuit(full_circuit)  

svg_content = svg_circuit._repr_svg_()


if '<?xml' not in svg_content:
    svg_content = '<?xml version="1.0" encoding="UTF-8"?>\n' + svg_content


with open("circuit_visualization.svg", "w") as f:
    f.write(svg_content)

print("Circuit visualization saved as 'circuit_visualization.svg'. Open it in a browser to view.")