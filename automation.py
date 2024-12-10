import os
import subprocess
from pathlib import Path

# Paths to the two repositories

REPO_A_PATH = "/path/to/repo_a"
REPO_B_PATH = "/path/to/repo_b"

# Output directory for diffs
DIFF_OUTPUT_DIR = "./diff_output"

# tracking --sr
def run_command(command, cwd=None):
    try:
        result = subprocess.run(command, cwd=cwd, text=True, shell=True, check=True, stdout=subprocess.PIPE)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

def get_current_commit(repo_path):
    return run_command("git rev-parse HEAD", cwd=repo_path)\
        

def export_repo_to_temp(repo_path, temp_dir):
    if os.path.exists(temp_dir):
        run_command(f"rm -rf {temp_dir}")
    run_command(f"git archive HEAD | tar -x -C {temp_dir}", cwd=repo_path)
    

def compare_repos(repo_a_temp, repo_b_temp, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    diff_file = os.path.join(output_dir, "repo_diff.patch")
    command = f"diff -ruN {repo_a_temp} {repo_b_temp} > {diff_file}"
    run_command(command)
    print(f"Diff saved to {diff_file}")

def main():
   
    repo_a_temp = "./repo_a_temp"
      # Export repositories
    repo_b_temp = "./repo_b_temp"

    # Get commit hashes
    repo_a_commit = get_current_commit(REPO_A_PATH)
    repo_b_commit = get_current_commit(REPO_B_PATH)
    print(f"Repo A (commit: {repo_a_commit})")
    print(f"Repo B (commit: {repo_b_commit})")\
     

    # Export repositories
    print("Exporting repositories...")
    export_repo_to_temp(REPO_A_PATH, repo_a_temp)
   
    export_repo_to_temp(REPO_B_PATH, repo_b_temp)


    print("Comparing repositories...")
    compare_repos(repo_a_temp, repo_b_temp, DIFF_OUTPUT_DIR)

if __name__ == "__main__":
    main()
