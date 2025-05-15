import re
import sys
import os
import argparse
import subprocess
from datetime import datetime

def extract_bad_rocs(file_path, blacklisted_only=False):
    bad_rocs = []
    print(f"[INFO] Reading input file: {file_path}")
    
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("---") or line.startswith("*****") or not line:
                continue
            if blacklisted_only and "BLACKLISTED" not in line:
                continue
            match = re.search(r'->\s*(\S+)_ROC\[(\d+):(\d+)\]', line)
            if match:
                base = match.group(1)
                start = int(match.group(2))
                end = int(match.group(3))
                for i in range(start, end + 1):
                    bad_rocs.append(f"Bad ROC: {base}_ROC{i} 999")
            else:
                print(f"[WARN] Skipped line (no ROC range found): {line}")

    print(f"[INFO] Total ROCs extracted: {len(bad_rocs)}")
    return bad_rocs

def write_list_to_file(rocs, output_path):
    print(f"[INFO] Writing expanded list to: {output_path}")
    with open(output_path, 'w') as f:
        for roc in rocs:
            f.write(f"{roc}\n")

def main():
    parser = argparse.ArgumentParser(description="Wrapper for rocs.py using expanded masked ROC list")
    parser.add_argument("original_list", help="Path to original masked channels list")
    parser.add_argument("-blacklisted", action="store_true", help="Use only BLACKLISTED ROCs")
    parser.add_argument("-save", action="store_true", help="Keep list.txt after running")

    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    output_dir = f"automasked/plots_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)

    expanded_rocs = extract_bad_rocs(args.original_list, args.blacklisted)

    list_file = os.path.join(output_dir, "list.txt")
    write_list_to_file(expanded_rocs, list_file)

    if not os.path.exists("rocs.py"):
        print("[ERROR] Could not find rocs.py in current directory.")
        sys.exit(1)

    cmd = ["python", "rocs.py", list_file, "--output-dir", output_dir]
    print(f"[INFO] Running command: {' '.join(cmd)}")

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    print(result.stdout)
    print(result.stderr)

    if result.returncode == 0:
        print(f"[SUCCESS] Plots generated in {output_dir}")
    else:
        print("[ERROR] rocs.py script failed to run")

    if not args.save:
        try:
            os.remove(list_file)
            print(f"[INFO] Removed intermediate file: {list_file}")
        except Exception as e:
            print(f"[WARN] Could not delete {list_file}: {e}")

if __name__ == "__main__":
    main()
