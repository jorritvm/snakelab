import sys
import subprocess

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_one_subprocess.py <script_to_run>")
        sys.exit(1)
    script_to_run = sys.argv[1]
    # Run the script as a subprocess
    subprocess.run([sys.executable, script_to_run])

