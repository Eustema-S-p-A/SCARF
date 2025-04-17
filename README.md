# SCARF: System for Comprehensive Assessment of RAG Frameworks


<div align="center">
  <img src="assets/SCARF_logo.png" alt="SCARF Logo" width="200">
  <br>
  <a href="http://www.gnu.org/licenses/agpl-3.0">
    <img src="https://img.shields.io/badge/license-AGPL-blue.svg" alt="AGPL License">
  </a>
  <a href="https://arxiv.org/abs/2504.07803"> 
    <img src="https://img.shields.io/badge/Technical%20Report-arXiv%3A2504.07803-b31b1b" alt="arXiv Report"> 
  </a> 
</div>


## Overview 📖

SCARF (System for Comprehensive Assessment of RAG Frameworks) is a modular and flexible evaluation framework designed for systematic benchmarking of Retrieval Augmented Generation (RAG) applications. It provides an end-to-end, black-box evaluation methodology, enabling easy comparison across diverse RAG frameworks in real-world deployment scenarios.

## Features ✨

- **Holistic RAG Evaluation**: Assess factual accuracy, contextual relevance, and response coherence.
- **Modular & Flexible**: Supports multiple deployment configurations and evaluation setups.
- **Automated Benchmarking**: Compare different RAG Frameworks.
- **Detailed Performance Reports**: Generate insights into RAG framework efficiency and effectiveness.

## Installation 🛠️

### Prerequisites 📋

- Python 3.8+
- pip
- Docker (optional, for containerized deployment of RAG frameworks)

### Setup 🚀

 1. Clone the repository and navigate to the project directory: `git clone https://github.com/your-repo/scarf.git && cd scarf`
 2. (Optional) Set up the RAG framework components locally for testing: You can find example Dockerfiles for each component in the corresponding subfolders.
 3. Navigate to the SCARF framework-test folder: `cd frameworks-test/eus/`
 4. Install dependencies: ` cd pip install -r requirements.txt`

### Usage 📈
 1. Configure SCARF for your needs through `config.json`
 2. Start SCARF `python test_rag_frameworks.py `

## Contributing 🤝
Contributions are welcome! Please submit issues or pull requests.

## Contact 📬
For questions or support, reach out via GitHub Issues.

## Authors ✍️
[m.rengo], [s.beadini], [d.alfano], [r.abbruzzese] @ Eustema SpA, Italy

## Citation 📚  
If you use SCARF in your research or applications, please cite our technical report:

```bibtex
@techreport{SCARF,
  author = {Rengo M. , Beadini S. , Alfano, D. , Abbruzzese R.},
  title = {A System for Comprehensive Assessment of RAG Frameworks},
  institution = {Eustema SpA},
  month = {4},
  year = {2025},
  url = {https://arxiv.org/abs/2504.07803},
  eprint = {2504.07803},
  archivePrefix = {arXiv},
  primaryClass = {cs.CL},
  doi = {10.48550/arXiv.2504.07803},
  note = {Technical Report}
}
```

