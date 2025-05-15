import os
import subprocess
import sys
import venv
import shutil
import platform

def create_virtualenv(venv_dir=".venv"):
    if not os.path.exists(venv_dir):
        print(f"Creating virtual environment in '{venv_dir}'...")
        venv.create(venv_dir, with_pip=True)
    else:
        print(f"Virtual environment '{venv_dir}' already exists.")

def install_requirements(venv_dir=".venv", requirements_file="requirements.txt"):
    pip_path = os.path.join(venv_dir, "Scripts" if os.name == "nt" else "bin", "pip")

    if not os.path.exists(pip_path):
        raise FileNotFoundError("pip not found in the virtual environment.")

    if not os.path.exists(requirements_file):
        raise FileNotFoundError(f"'{requirements_file}' not found.")

    print(f"Installing packages from '{requirements_file}'...")
    subprocess.check_call([pip_path, "install", "-r", requirements_file])

def detect_shell():
    shell = os.environ.get("SHELL", "").lower()
    if "bash" in shell:
        return "bash"
    elif "zsh" in shell:
        return "bash"  # treat zsh like bash
    elif os.name == "nt":
        parent_process = os.environ.get("ComSpec", "").lower()
        if "powershell" in parent_process:
            return "powershell"
        elif "cmd" in parent_process or "cmd.exe" in parent_process:
            return "cmd"
    return None

def write_launcher_script(shell_type, venv_dir=".venv"):
    if shell_type == "bash":
        script = f"""#!/bin/bash
source {venv_dir}/bin/activate
python3 app.py
"""
        with open("run.sh", "w") as f:
            f.write(script)
        os.chmod("run.sh", 0o755)
        print("✅ Created 'run.sh' for Bash")

    elif shell_type == "powershell":
        script = f""".\\{venv_dir}\\Scripts\\Activate.ps1
python app.py
"""
        with open("run.ps1", "w") as f:
            f.write(script)
        print("✅ Created 'run.ps1' for PowerShell")

    elif shell_type == "cmd":
        script = f"""@echo off
call {venv_dir}\\Scripts\\activate.bat
python app.py
"""
        with open("run.bat", "w") as f:
            f.write(script)
        print("✅ Created 'run.bat' for CMD")

    else:
        print("⚠️ Could not detect shell. No launcher script created.")

if __name__ == "__main__":
    venv_dir = ".venv"
    requirements_file = "requirements.txt"

    create_virtualenv(venv_dir)
    install_requirements(venv_dir, requirements_file)

    shell = detect_shell()
    write_launcher_script(shell, venv_dir)

    print("\n✅ Setup complete.")
