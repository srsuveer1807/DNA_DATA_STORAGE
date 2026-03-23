# import streamlit as st
# from encoder import encode_text
# from decoder import decode_dna_full
# from mutations import introduce_mutations
# import hashlib
# import time
# import os
# from datetime import datetime

# # -------------------------
# # Page + Enhanced Styling
# # -------------------------
# st.set_page_config(layout="wide", page_title="DNA Storage Demo", page_icon="🧬")

# # Modern, vibrant CSS styling with improved text visibility
# st.markdown(
#     """
#     <style>
#     /* === GLOBAL BASE COLORS === */
#     html, body, [class*="stAppViewContainer"] {
#         background-color: #0e0f16 !important;
#         color: #e4e4e7 !important;
#     }

#     /* --- Headings --- */
#     h1, h2, h3, h4, h5, h6 {
#         color: #ffffff !important;
#     }

#     /* === FORM STYLING (dark panels) === */
#     div[data-testid="stForm"] label {
#         color: #ffffff !important;   /* White for form labels */
#         font-weight: 600;
#         font-size: 1rem;
#     }

#     div[data-testid="stForm"] input,
#     div[data-testid="stForm"] textarea {
#         background-color: #1a1b26 !important;
#         color: #ffffff !important;
#         border: 1px solid #333 !important;
#         border-radius: 8px !important;
#     }

#     /* Sliders */
#     div[data-testid="stSlider"] label {
#         color: #ffffff !important;
#         font-weight: 600;
#     }

#     /* === METRICS / INFO BOXES (light backgrounds) === */
#     div[data-testid="stMetricLabel"],
#     div[data-testid="stMarkdown"] strong {
#         color: #000000 !important;   /* Black text for better readability */
#         font-weight: 600;
#     }

#     /* Tabs */
#     .stTabs [data-baseweb="tab"] {
#         color: #000000 !important;
#         font-weight: 500;
#     }

#     /* === BADGES / STATUS BOXES === */
#     [data-testid="stMetricValue"] {
#         color: #ffffff !important;   /* Keep values readable */
#     }
    
#     /* === Center Align Tabs === */
#     .stTabs [data-baseweb="tab-list"] {
#         justify-content: center !important;  /* Center the tabs */
#     }

#     /* Tabs Styling */
#     .stTabs [data-baseweb="tab"] {
#         color: #ffffff !important;     /* White text for all tabs */
#         font-weight: 600;
#         margin: 0 15px;  /* Add spacing between tabs */
#     }

#     /* Active tab styling */
#     .stTabs [data-baseweb="tab"][aria-selected="true"] {
#         border-bottom: 3px solid #ef4444 !important; /* Red underline for active tab */
#         color: #ffffff !important;
#     }

#     /* Download button styling */
#     .download-btn {
#         background: linear-gradient(45deg, #4ecdc4, #44a08d) !important;
#         color: white !important;
#         border: none !important;
#         border-radius: 8px !important;
#         padding: 10px 20px !important;
#         font-weight: 600 !important;
#         margin-top: 10px !important;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# st.title("🧬 DNA Data Storage Simulator")
# st.markdown("### Explore molecular data storage with error correction and mutation analysis")

# # -------------------------
# # Session State
# # -------------------------
# if 'results' not in st.session_state:
#     st.session_state.results = None
# if 'previous_params' not in st.session_state:
#     st.session_state.previous_params = None
# if 'file_initialized' not in st.session_state:
#     st.session_state.file_initialized = False

# # -------------------------
# # Initialize DNA Storage File
# # -------------------------
# def initialize_dna_file(filename="dna_sequences.txt"):
#     """Initialize or clear the DNA storage file."""
#     os.makedirs("dna_storage", exist_ok=True)
#     filepath = os.path.join("dna_storage", filename)
    
#     # Create file with header if it doesn't exist or needs to be cleared
#     header = f"""DNA SEQUENCE STORAGE FILE
# Created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
# ============================================

# """
    
#     with open(filepath, "w", encoding="utf-8") as f:
#         f.write(header)
    
#     return filepath

# # Initialize file on first run
# if not st.session_state.file_initialized:
#     st.session_state.dna_filepath = initialize_dna_file()
#     st.session_state.file_initialized = True

# # -------------------------
# # Utility Functions
# # -------------------------
# def get_cache_key(text, redundancy, severity):
#     """Generate a unique cache key based on input parameters."""
#     params_str = f"{text}_{redundancy}_{severity}"
#     return hashlib.md5(params_str.encode()).hexdigest()

# def save_dna_to_file(dna_sequence, original_text, redundancy, mutation_rate, filename="dna_sequences.txt"):
#     """Save DNA sequence and metadata to a text file."""
#     # Create directory if it doesn't exist
#     os.makedirs("dna_storage", exist_ok=True)
#     filepath = os.path.join("dna_storage", filename)
    
#     # Prepare the entry with timestamp
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     entry = f"""
# === DNA SEQUENCE ENTRY ===
# Timestamp: {timestamp}
# Original Text: "{original_text}"
# Redundancy Level: {redundancy}x
# Mutation Rate: {mutation_rate:.2f}%
# Sequence Length: {len(dna_sequence)} bases
# DNA Sequence:
# {dna_sequence}
# === END OF ENTRY ===

# """
    
#     # Append to file
#     with open(filepath, "a", encoding="utf-8") as f:
#         f.write(entry)
    
#     return filepath

# def process_text(text, redundancy, severity):
#     """Process text to DNA with redundancy + mutation."""
#     # Encode
#     dna = encode_text(text, redundancy=redundancy)
    
#     # Mutate
#     num_mutations = max(1, int(len(dna) * severity / 100))
#     mutated = introduce_mutations(dna, num_mutations=num_mutations)
    
#     # Calculate stats
#     mismatch = sum(1 for a, b in zip(dna, mutated) if a != b)
#     mutation_rate = (mismatch / max(1, len(dna))) * 100
    
#     # Decode both
#     try:
#         decoded_original = decode_dna_full(dna, redundancy)
#     except Exception as e:
#         decoded_original = f"Error: {e}"
    
#     try:
#         decoded_mutated = decode_dna_full(mutated, redundancy)
#     except Exception as e:
#         decoded_mutated = f"Error: {e}"
    
#     return {
#         'dna': dna,
#         'mutated': mutated,
#         'mutation_rate': mutation_rate,
#         'decoded_original': decoded_original,
#         'decoded_mutated': decoded_mutated,
#         'params': (text, redundancy, severity)
#     }

# # -------------------------
# # File Download Function
# # -------------------------
# def create_download_button(filepath, button_text="Download DNA Sequences"):
#     """Create a download button for the DNA sequences file."""
#     with open(filepath, "rb") as f:
#         dna_data = f.read()
    
#     st.download_button(
#         label=button_text,
#         data=dna_data,
#         file_name=os.path.basename(filepath),
#         mime="text/plain",
#         key="download_dna"
#     )

# # -------------------------
# # Input Form
# # -------------------------
# with st.form("dna_encoding_form"):
#     st.subheader("⚙️ Encoding Parameters")
    
#     col1, col2 = st.columns(2)
#     with col1:
#         text_input = st.text_input("Enter text to store:", "Hello DNA World!", 
#                                  help="The text you want to encode into DNA sequence")
#     with col2:
#         redundancy_input = st.slider(
#             "Redundancy Level", 
#             min_value=1, 
#             max_value=10, 
#             value=3,
#             help="Number of times to repeat the payload for error correction"
#         )
    
#     severity_input = st.slider(
#         "Mutation Severity (%)", 
#         min_value=0, 
#         max_value=100, 
#         value=5,
#         help="Percentage of DNA bases to mutate (0-100%)"
#     )
    
#     # File name input
#     filename_input = st.text_input(
#         "Filename to save DNA sequences:", 
#         "dna_sequences.txt",
#         help="Name of the file where DNA sequences will be stored"
#     )
    
#     col1, col2 = st.columns(2)
#     with col1:
#         submitted = st.form_submit_button("🚀 Encode and Process DNA")
#     with col2:
#         # Add a button to clear the file
#         if st.form_submit_button("🗑️ Clear DNA File"):
#             st.session_state.dna_filepath = initialize_dna_file(filename_input)
#             st.success("DNA storage file cleared!")

# # -------------------------
# # Processing
# # -------------------------
# current_params = (text_input, redundancy_input, severity_input)
# params_changed = current_params != st.session_state.previous_params

# if submitted or (st.session_state.results and params_changed):
#     if not text_input.strip():
#         st.error("⚠️ Please enter some text to encode.")
#     else:
#         with st.spinner("🔬 Encoding and processing DNA..."):
#             # Progress animation
#             progress_bar = st.progress(0)
#             for i in range(0, 101, 20):
#                 time.sleep(0.1)
#                 progress_bar.progress(i)
            
#             st.session_state.results = process_text(text_input, redundancy_input, severity_input)
#             st.session_state.previous_params = current_params
            
#             # Save DNA sequences to file
#             try:
#                 filepath_original = save_dna_to_file(
#                     st.session_state.results['dna'],
#                     text_input,
#                     redundancy_input,
#                     0.0,  # No mutation for original
#                     filename_input
#                 )
                
#                 filepath_mutated = save_dna_to_file(
#                     st.session_state.results['mutated'],
#                     text_input,
#                     redundancy_input,
#                     st.session_state.results['mutation_rate'],
#                     filename_input
#                 )
                
#                 st.session_state.dna_filepath = filepath_original
#             except Exception as e:
#                 st.error(f"Error saving DNA sequences: {e}")
                
#         if submitted:
#             st.success("✅ Processing complete!")

# # -------------------------
# # Download Section
# # -------------------------
# st.markdown("---")
# st.subheader("💾 Download DNA Sequences")

# if os.path.exists(st.session_state.dna_filepath):
#     file_stats = os.stat(st.session_state.dna_filepath)
#     file_size_kb = file_stats.st_size / 1024
    
#     col1, col2 = st.columns([2, 1])
#     with col1:
#         st.info(f"DNA sequences file: {st.session_state.dna_filepath} ({file_size_kb:.2f} KB)")
#     with col2:
#         create_download_button(st.session_state.dna_filepath)
# else:
#     st.info("No DNA sequences file available yet. Process some DNA first.")

# # -------------------------
# # Results
# # -------------------------
# if st.session_state.results:
#     results = st.session_state.results
    
#     # Parameters summary
#     st.subheader("📊 Current Parameters")
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         st.markdown(f"<div style='background: rgba(79, 195, 247, 0.9); color: white; padding: 15px; border-radius: 10px; margin: 8px 0;'>📝 Text: {results['params'][0]}</div>", unsafe_allow_html=True)
#     with col2:
#         st.markdown(f"<div style='background: rgba(102, 187, 106, 0.9); color: white; padding: 15px; border-radius: 10px; margin: 8px 0;'>🔁 Redundancy: {results['params'][1]}x</div>", unsafe_allow_html=True)
#     with col3:
#         st.markdown(f"<div style='background: rgba(239, 83, 80, 0.9); color: white; padding: 15px; border-radius: 10px; margin: 8px 0;'>🧪 Mutation: {results['params'][2]}%</div>", unsafe_allow_html=True)
    
#     # File saving info
#     st.info(f"💾 DNA sequences saved to: {st.session_state.dna_filepath}")
    
#     # Tabs for different views
#     tab1, tab2, tab3 = st.tabs(["🧾 Original DNA", "⚡ Mutated DNA", "🔍 Comparison"])
    
#     # --- Original DNA
#     with tab1:
#         st.subheader("Original DNA Sequence")
#         st.code(results['dna'][:500] + ("..." if len(results['dna']) > 500 else ""), language="text")
#         st.markdown(f"<div style='background: rgba(186, 104, 200, 0.9); color: white; padding: 15px; border-radius: 10px; margin: 8px 0;'>Total length: {len(results['dna'])} bases</div>", unsafe_allow_html=True)
        
#         st.subheader("Decoded Result")
#         if results['decoded_original'].startswith("Error:"):
#             st.markdown(f"<div style='background: rgba(239, 83, 80, 0.9); color: white; padding: 15px; border-radius: 10px; margin: 8px 0;'>❌ {results['decoded_original']}</div>", unsafe_allow_html=True)
#         else:
#             st.markdown(f"<div style='background: rgba(102, 187, 106, 0.9); color: white; padding: 15px; border-radius: 10px; margin: 8px 0;'>✅ {results['decoded_original']}</div>", unsafe_allow_html=True)
    
#     # --- Mutated DNA
#     with tab2:
#         st.subheader("Mutated DNA Sequence")
#         st.code(results['mutated'][:500] + ("..." if len(results['mutated']) > 500 else ""), language="text")
#         st.markdown(f"<div style='background: rgba(186, 104, 200, 0.9); color: white; padding: 15px; border-radius: 10px; margin: 8px 0;'>Total length: {len(results['mutated'])} bases</div>", unsafe_allow_html=True)
        
#         col_metric1, col_metric2 = st.columns(2)
#         with col_metric1:
#             st.metric("Mutation Rate", f"{results['mutation_rate']:.2f}%", 
#                      help="Percentage of bases that were mutated")
#         with col_metric2:
#             st.metric("Sequence Length", f"{len(results['dna'])} bases", 
#                      help="Total number of DNA bases")
        
#         st.subheader("Decoded Result")
#         if results['decoded_mutated'].startswith("Error:"):
#             st.markdown(f"<div style='background: rgba(239, 83, 80, 0.9); color: white; padding: 15px; border-radius: 10px; margin: 8px 0;'>❌ {results['decoded_mutated']}</div>", unsafe_allow_html=True)
#         else:
#             st.markdown(f"<div style='background: rgba(102, 187, 106, 0.9); color: white; padding: 15px; border-radius: 10px; margin: 8px 0;'>✅ {results['decoded_mutated']}</div>", unsafe_allow_html=True)
    
#     # --- Comparison
#     with tab3:
#         st.subheader("Base-by-Base Comparison (First 100 bases)")
        
#         diff_html = """
#         <div style='font-family: monospace; font-size: 16px; line-height: 1.8; 
#                    background: rgba(0,0,0,0.9); padding: 20px; border-radius: 12px; 
#                    color: white;'>"""
#         for i, (orig, mut) in enumerate(zip(results['dna'][:100], results['mutated'][:100])):
#             if orig != mut:
#                 diff_html += f"<span style='background:linear-gradient(45deg, #ff6b6b, #ee5a24); padding:2px 4px; border-radius:4px; margin:2px; font-weight:bold;'> {orig}→{mut} </span>"
#             else:
#                 diff_html += f"<span style='background:rgba(46, 204, 113,0.3); padding:2px 4px; border-radius:4px; margin:2px;'> {orig} </span>"
#         diff_html += "</div>"
#         st.markdown(diff_html, unsafe_allow_html=True)
        
#         # Decoding comparison
#         st.subheader("Decoded Text Comparison")
#         col1, col2 = st.columns(2)
#         with col1:
#             st.markdown("**Original DNA Decoded**")
#             if results['decoded_original'].startswith("Error:"):
#                 st.error(results['decoded_original'])
#             else:
#                 st.success(f"✅ {results['decoded_original']}")
#         with col2:
#             st.markdown("**Mutated DNA Decoded**")
#             if results['decoded_mutated'].startswith("Error:"):
#                 st.error(results['decoded_mutated'])
#             else:
#                 st.success(f"✅ {results['decoded_mutated']}")

# else:
#     st.info("👆 Enter text and parameters above, then click **Encode and Process DNA** to begin.")
#     st.markdown("""
#     <div style='background: rgba(255,255,255,0.95); padding: 25px; border-radius: 15px; margin: 25px 0; font-size: 1.1rem; color: #000000;'>
#     <h4 style='color: #000000; font-weight: 700;'>🎯 How it works:</h4>
#     <ul style='font-weight: 500; color: #000000;'>
#     <li>Enter text to encode into DNA sequence</li>
#     <li>Set redundancy level for error correction</li>
#     <li>Apply mutations to test robustness</li>
#     <li>Compare original vs mutated DNA decoding</li>
#     <li>DNA sequences are automatically saved to a text file</li>
#     <li>Download the file using the download button below</li>
#     </ul>
#     </div>
#     """, unsafe_allow_html=True)



from flask import Flask, render_template, request, send_file, redirect, url_for
from encoder import encode_text
from decoder import decode_dna_full
from mutations import introduce_mutations
import os
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

# -------------------------------
# File Setup
# -------------------------------
os.makedirs("dna_storage", exist_ok=True)
DNA_FILE = "dna_storage/dna_sequences.txt"

def initialize_dna_file():
    header = f"""DNA SEQUENCE STORAGE FILE
Created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
============================================

"""
    with open(DNA_FILE, "w", encoding="utf-8") as f:
        f.write(header)

# Only create if not exists
if not os.path.exists(DNA_FILE):
    initialize_dna_file()

# -------------------------------
# Utility Functions
# -------------------------------
def highlight_mutations(original, mutated):
    result = []
    for o, m in zip(original, mutated):
        if o == m:
            result.append(m)
        else:
            result.append(f"<span style='color:red;font-weight:bold'>{m}</span>")
    return "".join(result)

def save_dna_to_file(dna_sequence, original_text, redundancy, mutation_rate):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"""
=== DNA SEQUENCE ENTRY ===
Timestamp: {timestamp}
Original Text: "{original_text}"
Redundancy Level: {redundancy}x
Mutation Rate: {mutation_rate:.2f}%
Sequence Length: {len(dna_sequence)} bases
DNA Sequence:
{dna_sequence}
=== END OF ENTRY ===

"""
    with open(DNA_FILE, "a", encoding="utf-8") as f:
        f.write(entry)

def process_text(text, redundancy, severity):
    dna = encode_text(text, redundancy)

    num_mutations = int(len(dna) * severity / 100)

    if num_mutations > 0:
        mutated = introduce_mutations(dna, num_mutations=num_mutations)
    else:
        mutated = dna

    mismatch = sum(1 for a, b in zip(dna, mutated) if a != b)
    mutation_rate = (mismatch / max(1, len(dna))) * 100

    decoded_original = decode_dna_full(dna, redundancy)
    decoded_mutated = decode_dna_full(mutated, redundancy)

    highlighted = highlight_mutations(dna, mutated)

    save_dna_to_file(dna, text, redundancy, 0.0)
    save_dna_to_file(mutated, text, redundancy, mutation_rate)

    return {
        "text": text,
        "dna": dna,
        "mutated": mutated,
        "highlighted_mutations": highlighted,
        "mutation_rate": round(mutation_rate, 2),
        "decoded_original": decoded_original,
        "decoded_mutated": decoded_mutated
    }
# -------------------------------
# Routes
# -------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form["text"]
        redundancy = int(request.form["redundancy"])
        severity = int(request.form["severity"])

        results = process_text(text, redundancy, severity)
        return render_template("result.html", results=results)

    return render_template("index.html")

@app.route("/download")
def download_file():
    return send_file(DNA_FILE, as_attachment=True)

@app.route("/clear")
def clear_file():
    initialize_dna_file()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)