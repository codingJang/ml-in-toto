import sys
import c2pa

def inspect_c2pa_metadata(file_path):
    try:
        reader = c2pa.Reader(file_path)
        manifest = reader.get_active_manifest()
        if manifest:
            uri = manifest["thumbnail"]["identifier"]
            reader.resource_to_file(uri, "thumbnail_v2.jpg")
            print("C2PA metadata inspection passed. Thumbnail saved as thumbnail_v2.jpg")
            return True
        else:
            print("No active manifest found.")
            return False
    except Exception as err:
        print(f"Error inspecting C2PA metadata: {err}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python inspect_c2pa_metadata.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    if inspect_c2pa_metadata(file_path):
        sys.exit(0)
    else:
        sys.exit(1)
