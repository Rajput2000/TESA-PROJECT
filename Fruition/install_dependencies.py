import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

dependencies = [
    "fastapi",
    "uvicorn[standard]",
    "pillow",
    "jinja2",
    "tensorflow==2.18.0",
    "numpy"
]

# Optional: for better JSON compatibility (if needed)
dependencies.append("python-multipart")

for package in dependencies:
    try:
        install(package)
        print(f"✅ Installed: {package}")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install: {package}")

# Create & activate a virtual environment:
# python -m venv venv
# source venv/bin/activate     # Linux/macOS
# .\venv\Scripts\activate   


# Run the install script:
# python install_dependencies.py
