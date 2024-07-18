import sys
import c2pa

def check_c2pa_metadata(file_path):
    try:
        reader = c2pa.Reader(file_path)
        manifest_store = reader.json()
        if manifest_store:
            print("C2PA metadata found.")
            return True
        else:
            print("No C2PA metadata found.")
            return False
    except Exception as err:
        print(f"Error reading C2PA metadata: {err}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_c2pa_metadata.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    if check_c2pa_metadata(file_path):
        sys.exit(0)
    else:
        sys.exit(1)
