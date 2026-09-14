# jee-quantum-chemistry-hub
# ✨ JEE / JAM Quantum Chemistry Hub

An interactive, pure-Python data science dashboard designed for competitive exam aspirants (JEE/JAM/GATE). It dynamically computes electron configurations, handles complex Aufbau anomalies, maps column coordinates, and applies color-coded orbital visualizations.

## 🚀 Features Built From Scratch
* **Aufbau Anomaly Engine:** Tracks real chemical exceptions (Cr, Cu, Pd, etc.) and exposes structural exchange energy stabilities.
* **Dual-Group Mapping:** Bridges the gap between IUPAC columns (1-18) and Classical Group notations (IA-VIII) seamlessly to prevent exam traps.
* **Noble Gas Shorthand Compactor:** Automatically condenses heavy configurations down using preceding inert cores.
* **Color-Coded Orbital Matrix:** Uses isolated block tracking to format s, p, d, and f subshells with unique styles.

## 🛠️ Local Setup
To run this application on your local machine, open your system terminal and execute:

```bash
pip install streamlit
python -m streamlit run jeequestionchem.py
```
