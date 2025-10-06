def clean_file():
    filepath = r"c:\Users\dvast\NASASpaceApps_2025\Space-Habitat-Designer\frontend\pages\page_3_result.py"
    
    # Read the file in binary mode to detect null bytes
    with open(filepath, 'rb') as file:
        content = file.read()
    
    # Remove null bytes
    cleaned_content = content.replace(b'\x00', b'')
    
    # Write back the cleaned content
    with open(filepath, 'wb') as file:
        file.write(cleaned_content)
    
    print("File cleaned successfully")

if __name__ == "__main__":
    clean_file()