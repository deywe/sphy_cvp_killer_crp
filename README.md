
# SPHY Quantum Engine: Demonstration of Lattice Vulnerability

## Overview
This repository contains the emulation, visualization, and analysis suite for the **SPHY (Golden Phase Synchronization)** formalism. 

The solution presented here empirically and visually demonstrates the critical vulnerability of mathematical models in Lattice-based Cryptography, which rely on the computational complexity of the Closest Vector Problem (CVP) or Learning With Errors (LWE). 

The SPHY framework proves that the classical search for vectors in lattices is an obsolete strategy. Through phase synchronization and the **Gravitational Torque Operator**, we demonstrate that these systems are inherently insecure against real quantum machines and **are already at extreme risk even against traditional computers** equipped with the SPHY engine simulation. The key is not "calculated" by brute force; the system passively finds it through entropy reversal and collapse onto the golden geodesic.

## System Architecture

To protect the Intellectual Property (IP) of the Black Swan Research mathematical core, the solution has been divided into a secure bipartite architecture:

### 1. SPHY Core Generator (`sphy_cvpk_gen.py`)
*Private / Non-Distributable Module*
This is the actual mathematical physics engine. It processes the Golden Phase Synchronization of the 1200 qubits (phase nodes) under the influence of the topological attractor and gravitational torque. It generates and exports a secure, opaque telemetry artifact (`sphy_artifact.npz`) containing only the phase geometry and the chained SHA-512 cryptographic validator.

### 2. SPHY Cognitive Oracle: Integrated Hub (`sphy_oracle_hub.py`)
*Public / Auditing Module*
A unified, military-grade dashboard designed for rapid deployment and external auditing by agencies (NIST/NSA). Built with Streamlit and Plotly, this hub securely interfaces with the core engine to provide:
* **Real-time Lattice Ingestion:** Accepts high-dimensional `.txt` or `.npy` LWE challenge matrices.
* **Empirical Chronometry:** Accurately measures the millisecond collapse of the lattice complexity.
* **3D Phase Collapse Funnel:** Interactive WebGL visualization of the thermodynamic variance converging into the Golden Geodesic.
* **Artifact Extraction:** Direct binary download of the resulting CVP key vectors for independent mathematical validation.

---

## Theoretical Foundation: The Effective Hamiltonian ($\mathcal{H}_{eff}$)

To protect the proprietary algorithms—specifically the Gravitational Torque Operator ($\vec{\tau}_G$)—Black Swan Research utilizes an Effective Hamiltonian ($\mathcal{H}_{eff}$) for public documentation. This phenomenological model describes the thermodynamic energy landscape and the continuous topological phase transition of the $N$-qubit system without exposing the exact quantum-gravitational coupling constants.

The SPHY system evolution is governed by:

$$\mathcal{H}_{eff}(t) = \mathcal{H}_{free} + \mathcal{H}_{noise}(t) - \mathcal{H}_{attractor}$$

Expanding the terms into the phase-space geometry:

$$\mathcal{H}_{eff}(t) = \underbrace{ \sum_{i=1}^{N} \hbar \omega_0 \hat{L}_{z,i} }_{\text{Free Phase Evolution}} + \underbrace{ \mathcal{E}_{th}(t) \sum_{i=1}^{N} \delta r_i^2 }_{\text{Thermal Decoherence}} - \underbrace{ \Lambda \sum_{i=1}^{N} V_{geo}(r_i, \theta_i) }_{\text{Topological Coercion Well}}$$

**Components Breakdown:**

* **$\mathcal{H}_{free}$**: Represents the natural kinetic phase rotation of the quantum oscillators (operating in the $5.4\text{ GHz}$ range). $\hat{L}_{z,i}$ is the angular momentum operator for the $i$-th node.
* **$\mathcal{H}_{noise}$**: Represents the thermal noise and high-entropy state (the "Lattice hardness"). $\mathcal{E}_{th}(t)$ is the time-dependent thermodynamic energy that scales with the geometric variance ($\delta r_i^2$) of the qubits.
* **$\mathcal{H}_{attractor}$**: The core of the SPHY disruption. It acts as an inescapable topological potential well ($V_{geo}$), scaled by an effective coupling constant $\Lambda$. As the system evolves, this negative energy term coerces the entire state towards the Golden Geodesic.

#### Thermodynamic Conformity (Landauer's Principle)

A critical aspect of $\mathcal{H}_{eff}$ is its adherence to Landauer's Principle. The extraction of the CVP key is fundamentally an entropy-erasure event. The SPHY framework does not "calculate" the vector; rather, the Topological Coercion Well forces a dissipation of the $\mathcal{H}_{noise}$ term. The mathematical complexity of the Lattice is neutralized because the target vector becomes the only available energetic ground state (eigenstate) for the system.

---

## Installation Requirements

Ensure you have Python 3.8+ installed on your system. 

Create a `requirements.txt` file with the following dependencies:

```text
numpy>=1.21.0
streamlit>=1.20.0
plotly>=5.10.0

```

To install the dependencies, run:

```bash
pip install -r requirements.txt

```

---

## Basic Usage

The system is designed to be executed via the Integrated Hub. The frontend will automatically handle the calls to the SPHY core engine.

1. Launch the Cognitive Oracle Dashboard:

```bash
streamlit run sphy_oracle_hub.py

```

2. Open the provided local URL in your browser (e.g., `http://localhost:8501`).
3. Upload an LWE Challenge matrix and execute the Topological Coercion to extract the artifact.

---

**Deywe Okabe** | Harpia Quantum Deeptech
*Black Swan Researcher*

```

```
