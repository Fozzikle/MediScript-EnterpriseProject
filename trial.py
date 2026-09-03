def load_patients(base_folder):
    patients = []
    base_path = os.path.join(base_folder, "Patient Data")

    if not os.path.exists(base_path):
        return patients

    for patient_name in os.listdir(base_path):
        patient_path = os.path.join(base_path, patient_name, "Patient Information", "patient_data.json")
        if os.path.exists(patient_path):
            with open(patient_path, "r") as f:
                data = json.load(f)
                patients.append(data)
    return patients