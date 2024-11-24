# Chargeflow Assignment

This data pipeline project is designed to process and transform financial data for an e-commerce platform as part of Chargeflow Assignment

## Table of Contents

- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Architecture](#architecture)

## Project Structure

```
ChargeflowAssignment/
├── data/------------------------------------------- Mock data of each datasources
│   ├── chargebacks.csv
│   ├── orders.json
│   ├── transactions.json
├── scripts/
│   ├── pipeline.py--------------------------------- Main Pipeline Script
│   └── __pycache__/
├── src/
│   ├── validations/-------------------------------- Validations for each datasources
│   │   ├── __pycache__/
│   │   ├── orders.py
│   │   ├── transactions.py
│   │   └── chargeback.py
│   ├── clean.py------------------------------------ Cleans the data before use
│   ├── transformation.py--------------------------- Transform the data and outputs useful analysis 
│   └── extraction.py------------------------------- Extract the data from each datasources
└── utils/
    ├── logging_config.py
    └── __pycache__/
├── architecture.png-------------------------------- AWS architecture diagram for pipeline deployment
├── README.md
├── requirements.txt-------------------------------- Python library requirements
├── config/
```

## Requirements

- Python 3.9+

## Setup

1. **Clone the repository**:
    ```sh![architecture](https://github.com/user-attachments/assets/f7cc67c4-e676-45d6-b4c8-062c77597ad4)

    git clone https://github.com/YuvalHacking/ChargeflowAssignment
    cd ChargeflowAssignment
    ```

2. **Install the required Python packages**:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

**Run the Data Pipeline**:
```sh
python -m scripts.pipeline
```

## Architecture

![Uploading architecture.png…]()
