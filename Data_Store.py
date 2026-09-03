# imports
import os


def patient_folder_structure(patient_name, base_path):
    # Ensure base path ends with 'Patient Data'
    if not base_path.endswith("Patient Data"):
        base_path = os.path.join(base_path, "Patient Data")

    # Create main patient directory
    patient_dir = os.path.join(base_path, patient_name)
    os.makedirs(patient_dir, exist_ok=True)

    # Create subdirectories
    transcriptions = os.path.join(patient_dir, "Transcriptions")
    info = os.path.join(patient_dir, "Patient Information")
    os.makedirs(transcriptions, exist_ok=True)
    os.makedirs(info, exist_ok=True)

    # Creating transcription sub folders
    raw_folder = os.path.join(transcriptions, "Raw Transcriptions ")
    processed_folder = os.path.join(transcriptions, "Processed Transcription")
    os.makedirs(raw_folder, exist_ok=True)
    os.makedirs(processed_folder, exist_ok=True)

    return {"transcriptions": transcriptions,
            "raw": raw_folder,
            "processed": processed_folder,
            "info": info
            }
