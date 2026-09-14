import streamlit as st
import random

# Set up Streamlit Page Layout Styling
st.set_page_config(page_title="JEE/JAM Quantum Hub", page_icon="✨", layout="centered")

# Custom CSS styling injecting standard color schemes via markdown to isolate blocks
st.markdown("""
    <style>
    .orb-s { color: #60a5fa; font-weight: bold; }
    .orb-p { color: #f97316; font-weight: bold; }
    .orb-d { color: #c084fc; font-weight: bold; }
    .orb-f { color: #4ade80; font-weight: bold; }
    .exception-box {
        background-color: rgba(239, 68, 68, 0.1);
        border: 1px solid #ef4444;
        padding: 15px;
        border-radius: 8px;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# CORE ENGINE DATA STRUCTURES
# =====================================================================
atom_list = [
    'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na','Mg',
    'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn','Fe',
    'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr','Y', 'Zr',
    'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb','Te', 'I', 'Xe',
    'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd','Tb', 'Dy', 'Ho', 'Er',
    'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir','Pt', 'Au', 'Hg', 'Tl', 'Pb',
    'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th','Pa', 'U', 'Np', 'Pu', 'Am', 'Cm',
    'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No','Lr','Rf'
]

nl_pairs = [
    (1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (4, 0), (3, 2), (4, 1),
    (5, 0), (4, 2), (5, 1), (6, 0), (4, 3), (5, 2), (6, 1), (7, 0),
    (5, 3), (6, 2)
]

l_orbitals = {0: 's', 1: 'p', 2: 'd', 3: 'f'}
block_map = {0: 's', 1: 'p', 2: 'd', 3: 'f'}
noble_gases = [('Rn', 86), ('Xe', 54), ('Kr', 36), ('Ar', 18), ('Ne', 10), ('He', 2)]

exceptions = {
    'Cr': [['1s', 2], ['2s', 2], ['2p', 6], ['3s', 2], ['3p', 6], ['4s', 1], ['3d', 5]],
    'Cu': [['1s', 2], ['2s', 2], ['2p', 6], ['3s', 2], ['3p', 6], ['4s', 1], ['3d', 10]],
    'Nb': [['1s', 2], ['2s', 2], ['2p', 6], ['3s', 2], ['3p', 6], ['4s', 2], ['3d', 10], ['4p', 6], ['5s', 1], ['4d', 4]],
    'Mo': [['1s', 2], ['2s', 2], ['2p', 6], ['3s', 2], ['3p', 6], ['4s', 2], ['3d', 10], ['4p', 6], ['5s', 1], ['4d', 5]],
    'Ru': [['1s', 2], ['2s', 2], ['2p', 6], ['3s', 2], ['3p', 6], ['4s', 2], ['3d', 10], ['4p', 6], ['5s', 1], ['4d', 7]],
    'Rh': [['1s', 2], ['2s', 2], ['2p', 6], ['3s', 2], ['3p', 6], ['4s', 2], ['3d', 10], ['4p', 6], ['5s', 1], ['4d', 8]],
    'Pd': [['1s', 2], ['2s', 2], ['2p', 6], ['3s', 2], ['3p', 6], ['4s', 2], ['3d', 10], ['4p', 6], ['5s', 0], ['4d', 10]],
    'Ag': [['1s', 2], ['2s', 2], ['2p', 6], ['3s', 2], ['3p', 6], ['4s', 2], ['3d', 10], ['4p', 6], ['5s', 1], ['4d', 10]],
    'Pt': [['1s', 2], ['2s', 2], ['2p', 6], ['3s', 2], ['3p', 6], ['4s', 2], ['3d', 10], ['4p', 6], ['5s', 2], ['4d', 10], ['5p', 6], ['6s', 1], ['4f', 14], ['5d', 9]],
    'Au': [['1s', 2], ['2s', 2], ['2p', 6], ['3s', 2], ['3p', 6], ['4s', 2], ['3d', 10], ['4p', 6], ['5s', 2], ['4d', 10], ['5p', 6], ['6s', 1], ['4f', 14], ['5d', 10]],
}

# =====================================================================
# ENGINE PARSING LOGIC
# =====================================================================
def superscript(num):
    return "".join(["⁰¹²³⁴⁵⁶⁷⁸⁹"[ord(c)-ord('0')] for c in str(num)])

def get_html_colored_string(config_list):
    spans = []
    for shell, count in config_list:
        if count > 0: # Do not render empty shells like Pd's 5s⁰ unless explicit
            orb_type = shell[-1]
            spans.append(f'<span class="orb-{orb_type}">{shell}{superscript(count)}</span>')
    return ' '.join(spans)

def get_shorthand_html(full_config, total_electrons):
    for gas, atomic_num in noble_gases:
        if total_electrons > atomic_num:
            short_shells = full_config[:]
            electrons_removed = 0
            idx = 0
            while idx < len(short_shells) and electrons_removed < atomic_num:
                electrons_removed += short_shells[idx][1]
                idx += 1
            valence_html = get_html_colored_string(short_shells[idx:])
            return f'[{gas}] {valence_html}'
    return get_html_colored_string(full_config)

def calculate_period_group(config_list, block, element):
    if element == 'H': return 1, "1", "IA"
    if element == 'He': return 1, "18", "Zero"
    
    period = max(int(shell[:-1]) for shell, _ in config_list)
    outer_s = next((count for shell, count in config_list if shell == f'{period}s'), 0)
    outer_p = next((count for shell, count in config_list if shell == f'{period}p'), 0)
    outer_d = next((count for shell, count in config_list if shell == f'{period-1}d'), 0)
    
    classical_map = {
        1: "IA", 2: "IIA", 3: "IIIB", 4: "IVB", 5: "VB", 6: "VIB", 7: "VIIB",
        8: "VIII", 9: "VIII", 10: "VIII", 11: "IB", 12: "IIB",
        13: "IIIA", 14: "IVA", 15: "VA", 16: "VIA", 17: "VIIA", 18: "Zero"
    }
    
    if block == 's': iupac = outer_s
    elif block == 'p': iupac = outer_s + outer_p + 10
    elif block == 'd': iupac = outer_s + outer_d
    else: return period, "3", "IIIB (Lanthanide/Actinide)"
        
    return period, str(iupac), classical_map.get(int(iupac) if str(iupac).isdigit() else 3, "N/A")

# Build the data table loop smoothly
database = {}
nl_idx, n_elec = 0, 0
n, l = nl_pairs[nl_idx]
ideal_config = [[f'{n}{l_orbitals[l]}', 0]]

for idx, element in enumerate(atom_list, start=1):
    n_elec += 1
    if n_elec > 2 * (2 * l + 1):
        nl_idx += 1
        n, l = nl_pairs[nl_idx]
        ideal_config.append([f'{n}{l_orbitals[l]}', 1])
        n_elec = 1 
    else:
        # FIXED: Explicitly target the count integer inner element of the nested list structure
        ideal_config[-1][1] += 1
    
    final_config = exceptions.get(element, [item[:] for item in ideal_config])
    
    # FIXED: Safely isolate the string object text token to fetch character block symbols
    block = final_config[-1][0][-1] if element != 'He' else 's'
    p_num, g_num, c_num = calculate_period_group(final_config, block, element)
    
    database[element.lower()] = {
        'symbol': element, 'z': idx, 'block': block, 'period': p_num,
        'iupac': g_num, 'classical': c_num,
        'full_html': get_html_colored_string(final_config),
        'short_html': get_shorthand_html(final_config, idx),
        'is_exception': element in exceptions
    }

# =====================================================================
# STREAMLIT USER INTERFACE
# =====================================================================
st.title("✨ JEE / JAM Quantum Chemistry Hub")
st.caption("Advanced Electronic Configuration Analyzer & Coordination Matrix Dashboard")

# Search and Input Fields 
col_input, col_rand = st.columns([4, 1])
with col_input:
    query = st.text_input("Search Element Symbol:", value="Cr", placeholder="Type element e.g., Cu, Fe...").strip().lower()
with col_rand:
    st.write("##") 
    if st.button("🎲 Random"):
        query = random.choice(atom_list).lower()

if query in database:
    el = database[query]
    
    st.subheader(f"🔎 Analytical Analysis: {el['symbol']} (Z = {el['z']})")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Block Category", f"{el['block'].upper()}-Block")
    c2.metric("Period Level", f"n = {el['period']}")
    c3.metric("IUPAC / Classical Group", f"{el['iupac']} ({el['classical']})")
    
    st.markdown("### 📊 Electronic Orbitals Breakdown")
    st.markdown(f"**Shorthand Notation:**")
    st.markdown(f"<div style='background-color:#1e293b; padding:10px; border-radius:5px; font-size:1.2rem; color:#ffffff;'>{el['short_html']}</div>", unsafe_allow_html=True)
    
    st.markdown(f"**Full Quantum Matrix String:**")
    st.markdown(f"<div style='background-color:#1e293b; padding:10px; border-radius:5px; font-size:1.1rem; color:#ffffff;'>{el['full_html']}</div>", unsafe_allow_html=True)
    
    if el['is_exception']:
        st.markdown(f"""
        <div class="exception-box">
            <h4 style="color:#ef4444; margin:0 0 5px 0;">⚠️ JEE / JAM EXAM CRITICAL EXCEPTION ALERT</h4>
            <p style="margin:0; font-size:0.95rem; color:#f8fafc;">
                <strong>{el['symbol']}</strong> is a registered Aufbau Anomaly! It rejects regular structural sequences. 
                Instead, it alters valence electron numbers to secure half-filled or fully-filled d-matrix stability levels, maximizing internal quantum exchange energy.
            </p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.warning("Element code unrecognised. Please pass symbols matching values in the standard periodic array.")




