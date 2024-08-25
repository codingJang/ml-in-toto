# C2PA & in-toto Integration for Securing ML Workflows

Welcome to the project that integrates C2PA and in-toto to secure machine learning (ML) workflows. This project demonstrates how to use in-toto for verifying steps in an ML pipeline while ensuring the datasets involved are signed and verified using C2PA.

## Overview

This project aims to secure ML workflows by leveraging:
- **C2PA (Coalition for Content Provenance and Authenticity)**: A standard for verifying content to mitigate disinformation.
- **in-toto**: A framework for securing the integrity of software supply chains.

The combination of these tools allows us to ensure that datasets and models used in ML workflows are authentic and traceable from creation to deployment.

## Features

- **in-toto Verification**: Ensure that each step in the ML pipeline, from data preparation to model distribution, is securely recorded and verified.
- **C2PA Integration (Coming Soon)**: Verify that datasets used in the workflow are authentic and signed, ensuring the originality of the data.

## Installation

### Requirements

- Python 3.12 (Tested on MacOS and Ubuntu 20.04 LTS)
- Additional Python packages listed in `requirements.txt`

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/c2pa-in-toto.git
   cd c2pa-in-toto
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Demo

To see the ML workflow verification in action:

1. **Run the demo script:**
   ```bash
   bash run_all.sh
   ```

   This script executes a full ML pipeline, including data preparation, model training, testing, and distribution. in-toto records and verifies each step, ensuring the integrity of the process.

2. **Clean up generated files:**
   ```bash
   bash delete.sh
   ```

## Project Structure

Before running `run_all.sh`, the project structure is as follows:

```
.
├── Alice
│   ├── create_layout.py
│   └── mnist-prep
│       └── src
│           ├── build_dataset.py
│           └── check_dataset.py
├── Bob
│   └── mnist-train
│       └── src
│           ├── net.py
│           └── train.py
├── Carl
│   └── mnist-test
│       └── src
│           ├── net.py
│           └── test.py
├── Diana
│   └── mnist-dist
│       └── src
│           ├── app.py
│           ├── build_dist.sh
│           └── dist.py
├── README.md
├── delete.sh
├── requirements.txt
└── run_all.sh
```

After running `run_all.sh`, the structure expands to include generated datasets, models, and verification metadata.

## Known Limitations

- **Shared Test Dataset**: The current demo shares the test dataset with the model trainer, which could introduce bias or overfitting. This is for demonstration purposes and should be avoided in real-world implementations.
- **C2PA Plugin**: The C2PA plugin for dataset verification is not yet implemented, meaning dataset authenticity cannot yet be verified in this demo.
- **in-toto Wrapping**: Developers might find wrapping their commands with in-toto cumbersome. Future updates may include a more streamlined process.

## Future Development

- **Implement C2PA Plugin**: Integrate C2PA verification into the workflow.
- **GUI Installer**: Develop an installer with GUI elements to make verification processes more user-friendly and accessible to end-users.

## Contribution

We welcome contributions from developers interested in enhancing this project. Here’s how you can contribute:

1. **Fork the repository.**
2. **Create a branch**: `git checkout -b feature-name`.
3. **Commit your changes**: `git commit -am 'Add new feature'`.
4. **Push to the branch**: `git push origin feature-name`.
5. **Submit a pull request**.

## License

This project is licensed under the Apache License 2.0. You can find the full license [here](LICENSE).
