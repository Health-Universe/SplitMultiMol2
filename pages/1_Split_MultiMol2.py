import streamlit as st
import subprocess
import os
import zipfile
from io import BytesIO
import time

from split_multimol2 import split_multimol2, write_multimol2, write_multimol2_chunks

st.title("Multi-Mol2 File Splitter")

# Command
def run_split_multimol2(multimol2_file, out_dir):
    command = ["python", "split_multimol2.py", multimol2_file, out_dir]
    subprocess.run(command, capture_output=True, text=True)
    
# Create Zip file
def create_zip(directory):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED, False) as zipf:
        for foldername, _, filenames in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                zipf.write(file_path, os.path.relpath(file_path, directory))

    zip_buffer.seek(0)
    return zip_buffer

# Upload
mol2_file = st.file_uploader("Upload", type=["mol2"], help="**Input:** Multi-mol2 File \n\n**Output:** Zip of split Mol2 Files")

# Run
if mol2_file is not None:
    run_button = st.button("Run", help="Splitting Multi-Mol2 File")
    if run_button:
        with st.spinner("Running..."):
            time.sleep(2)
            out_dir = "output_mol2_files"
            os.makedirs(out_dir, exist_ok=True)
            with open(os.path.join(out_dir, mol2_file.name), "wb") as f:
                f.write(mol2_file.read())
            run_split_multimol2(os.path.join(out_dir, mol2_file.name), out_dir)
        zip_buffer = create_zip(out_dir)
        st.divider()
        st.subheader("Download")
        st.download_button(label="Download Multi-Mol2 Zip File", data=zip_buffer.getvalue(), file_name="output_files.zip")

