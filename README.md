# SCARF: System for Comprehensive Assessment of RAG Frameworks

[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)



## Overview

SCARF (System for Comprehensive Assessment of RAG Frameworks) is a modular and flexible evaluation framework designed for systematic benchmarking of Retrieval Augmented Generation (RAG) applications. It provides an end-to-end, black-box evaluation methodology, enabling easy comparison across diverse RAG frameworks in real-world deployment scenarios.

## Features

- **Holistic RAG Evaluation**: Assess factual accuracy, contextual relevance, and response coherence.
- **Modular & Flexible**: Supports multiple deployment configurations and evaluation setups.
- **Automated Benchmarking**: Compare different vector databases and LLM serving strategies.
- **Detailed Performance Reports**: Generate insights into RAG framework efficiency and effectiveness.

## Installation

### Prerequisites

- Python 3.8+
- pip
- Docker (optional, for containerized deployment of RAG frameworks)

### Setup

 1. Clone the repository and navigate to the project directory: `git clone https://github.com/your-repo/scarf.git && cd scarf`
 2. (Optional) Set up the RAG framework components locally for testing: You can find example Dockerfiles for each component in the corresponding subfolders.
 3. Navigate to the SCARF framework-test folder: `cd frameworks-test/eus/`
 4. Install dependencies: ` cd pip install -r requirements.txt`

### Usage
 1. Configure SCARF for your needs through `config.json`
 2. Start SCARF `python test_rag_frameworks.py `

## Contributing
Contributions are welcome! Please submit issues or pull requests.

## Contact
For questions or support, reach out via GitHub Issues.

## Authors
[m.rengo], [s.beadini], [d.alfano], [r.abbruzzese] @ Eustema SpA, Italy
