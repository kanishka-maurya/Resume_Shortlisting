import tempfile
import os
import zipfile 
import streamlit as st
def save_uploaded_file(uploaded_file):
    """
    Save the uploaded ZIP file to a temporary directory.
    Returns the path to the saved file.
    """
    try:
        # Create a temporary directory for uploads
        st.info("here")
        temp_dir = os.path.join(tempfile.gettempdir(), "streamlit_uploads")
        os.makedirs(temp_dir, exist_ok=True)

        # Clear existing ZIP files in the directory
        for filename in os.listdir(temp_dir):
            if filename.endswith(".zip"):
                st.info("inside zip")
                os.remove(os.path.join(temp_dir, filename))

        # Save the new uploaded ZIP file
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.info(file_path)    
        return file_path
    except Exception as e:
        st.info(e)

def extract_zip(zip_path):
    """
    Extract the contents of the ZIP file to a temporary directory.
    Returns the path to the extraction directory.
    """
    try:
        # Create a temporary directory for extraction
        extract_dir = os.path.join(tempfile.gettempdir(), "streamlit_extracted")
        os.makedirs(extract_dir, exist_ok=True)

        # Clear existing files in the extraction directory
        for filename in os.listdir(extract_dir):
            file_path = os.path.join(extract_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                import shutil
                shutil.rmtree(file_path)

        # Extract the ZIP file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        return extract_dir
    except zipfile.BadZipFile:
        print("The uploaded file is not a valid ZIP archive.")
        return None
    except Exception as e:
        print(f"Error extracting ZIP file: {e}")
        return None







