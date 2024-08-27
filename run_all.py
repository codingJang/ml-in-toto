#!/usr/bin/env python3

import argparse
import subprocess
import os
from pathlib import Path
import sys

def run_command(command, cwd=None, check=True):
    """
    Helper function to run shell commands.
    """
    print(f"Running command: {' '.join(command)}")
    try:
        subprocess.run(command, cwd=cwd, check=check)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {' '.join(command)}")
        print(e)
        sys.exit(1)

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Run the full pipeline with optional parameters.")
    parser.add_argument('--corrupt', action='store_true', help='Use corrupted dataset.')
    parser.add_argument('--dry-run', action='store_true', help='Run in dry-run mode.')
    parser.add_argument('--epochs', type=int, default=10, help='Number of epochs for training.')
    args = parser.parse_args()

    # Set dataset paths based on --corrupt flag
    ORIGINAL_ROOT = Path("./data")
    CORRUPTED_ROOT = Path("./data") if args.corrupt else Path("./corrupt_data")
    CHECK_CORRUPTED = "--is-corrupted" if args.corrupt else ""

    # Set threshold based on --dry-run flag
    THRESHOLD = 50.0 if args.dry_run else 95.0

    # Base directories
    base_dir = Path.cwd()
    alice_dir = base_dir / "Alice"
    bob_dir = base_dir / "Bob"
    carl_dir = base_dir / "Carl"
    diana_dir = base_dir / "Diana"
    enduser_dir = base_dir / "EndUser"

    # Ensure all necessary directories exist
    for directory in [alice_dir, bob_dir, carl_dir, diana_dir, enduser_dir]:
        if not directory.exists():
            print(f"Error: Directory {directory} does not exist.")
            sys.exit(1)

    # 1. Generate RSA keys
    run_command(["python", "rsa-keygen.py"])

    # 2. Alice's operations
    os.chdir(alice_dir)
    run_command(["python", "create_layout.py"])

    run_command([
        "in-toto-record", "start",
        "--step-name", "make-dataset",
        "--use-dsse",
        "--signing-key", "alice",
        "--materials", "mnist-prep/src/*"
    ])

    os.chdir(alice_dir / "mnist-prep")
    run_command([
        "python", "src/build_dataset.py",
        "--original-root", str(ORIGINAL_ROOT),
        "--corrupted-root", str(CORRUPTED_ROOT)
    ])

    check_dataset_command = ["python", "src/check_dataset.py", "--root", str(ORIGINAL_ROOT)]
    if CHECK_CORRUPTED:
        check_dataset_command.append(CHECK_CORRUPTED)
    run_command(check_dataset_command)

    os.chdir(alice_dir)
    run_command([
        "in-toto-record", "stop",
        "--step-name", "make-dataset",
        "--use-dsse",
        "--signing-key", "alice",
        "--products", "mnist-prep/src/*", "mnist-prep/data/*", "mnist-prep/corrupt_data/*", "mnist-prep/images/*"
    ])

    # Copy dataset to Bob and Carl using rsync
    run_command([
        "rsync", "-av", "--checksum", "--progress",
        f"{alice_dir}/mnist-prep/data/", f"{bob_dir}/mnist-train/data/"
    ])

    run_command([
        "rsync", "-av", "--checksum", "--progress",
        f"{alice_dir}/mnist-prep/data/", f"{carl_dir}/mnist-test/data/"
    ])

    # 3. Bob's operations
    os.chdir(bob_dir)
    run_command([
        "in-toto-record", "start",
        "--step-name", "train-model",
        "--use-dsse",
        "--signing-key", "bob",
        "--materials", "mnist-train/src/*", "mnist-train/data/*"
    ])

    os.chdir(bob_dir / "mnist-train")
    train_command = [
        "python", "src/train.py",
        f"--epochs", str(args.epochs),
        "--save-model"
    ]
    if args.dry_run:
        train_command.append("--dry-run")
    run_command(train_command)

    os.chdir(bob_dir)
    run_command([
        "in-toto-record", "stop",
        "--step-name", "train-model",
        "--use-dsse",
        "--signing-key", "bob",
        "--products", "mnist-train/src/*", "mnist-train/models/*", "mnist-train/data/*"
    ])

    # Copy models to Carl and Diana using rsync
    run_command([
        "rsync", "-av", "--checksum", "--progress",
        f"{bob_dir}/mnist-train/models/", f"{carl_dir}/mnist-test/models/"
    ])

    run_command([
        "rsync", "-av", "--checksum", "--progress",
        f"{bob_dir}/mnist-train/models/", f"{diana_dir}/mnist-dist/models/"
    ])

    # 4. Carl's operations
    os.chdir(carl_dir)
    run_command([
        "in-toto-record", "start",
        "--step-name", "test-model",
        "--use-dsse",
        "--signing-key", "carl",
        "--materials", "mnist-test/src/*", "mnist-test/data/*", "mnist-test/models/*"
    ])

    os.chdir(carl_dir / "mnist-test")
    run_command([
        "python", "src/test.py",
        "--no-mps"
    ])

    os.chdir(carl_dir)
    run_command([
        "in-toto-record", "stop",
        "--step-name", "test-model",
        "--use-dsse",
        "--signing-key", "carl",
        "--products", "mnist-test/src/*", "mnist-test/logs/*"
    ])

    # Copy logs to Diana using rsync
    run_command([
        "rsync", "-av", "--checksum", "--progress",
        f"{carl_dir}/mnist-test/logs/", f"{diana_dir}/mnist-dist/logs/"
    ])

    # 5. Diana's operations
    os.chdir(diana_dir)
    run_command([
        "in-toto-record", "start",
        "--step-name", "distribute",
        "--use-dsse",
        "--signing-key", "diana",
        "--materials", "mnist-dist/src/*", "mnist-dist/logs/*", "mnist-dist/models/*"
    ])

    os.chdir(diana_dir / "mnist-dist")
    run_command([
        "python", "src/dist.py",
        "--threshold", str(THRESHOLD)
    ])

    os.chdir(diana_dir)
    run_command([
        "in-toto-record", "stop",
        "--step-name", "distribute",
        "--use-dsse",
        "--signing-key", "diana",
        "--products", "mnist-dist/src/*", "mnist-dist/logs/*", "mnist-dist/models/*", "mnist-dist/build/*", "mnist-dist/dist/*"
    ])

    # Copy distribution to EndUser using rsync
    run_command([
        "rsync", "-av", "--checksum", "--progress",
        f"{diana_dir}/mnist-dist/dist/", f"{enduser_dir}/dist/"
    ])

    run_command([
        "rsync", "-av", "--checksum", "--progress",
        f"{diana_dir}/mnist-dist/models/", f"{enduser_dir}/models/"
    ])

    # 6. Final verification and execution at EndUser
    os.chdir(base_dir)
    files_to_copy = [
        alice_dir / "root.layout",
        alice_dir / "alice.pub",
        *alice_dir.glob("make-dataset.*.link"),
        *bob_dir.glob("train-model.*.link"),
        *carl_dir.glob("test-model.*.link"),
        *diana_dir.glob("distribute.*.link"),
    ]

    for file in files_to_copy:
        run_command([
            "rsync", "-av", "--checksum", "--progress",
            str(file), str(enduser_dir)
        ])

    os.chdir(enduser_dir)
    run_command([
        "in-toto-verify",
        "-v",
        "--layout", "root.layout",
        "--verification-keys", "alice.pub",
        "--inspection-timeout", "60"
    ])

    # Execute the final application
    run_command(["dist/app/app"])

    print("Pipeline executed successfully.")

if __name__ == "__main__":
    main()
