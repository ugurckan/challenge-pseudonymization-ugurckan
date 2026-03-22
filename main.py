from pseudonymization.process import process_patients
from pseudonymization.utils.date import today

if __name__ == "__main__":
    print(f"Processing is starting at {today().strftime('%Y-%m-%d %H:%M:%S')}")
    process_patients("patients.csv", "pii.csv", "health.csv")
    print(f"Processing is finished at {today().strftime('%Y-%m-%d %H:%M:%S')}")
