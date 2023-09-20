# Social media network analysis

In this repo you will find a basic code to analyze public data from social networks.
The code was presented on a talk on [Stackconf conference 2023](https://docs.google.com/presentation/d/1al3fLS50SXYUwGpn6zDjnrkM-gfIvUx_1qQk2akqPeg/edit?usp=sharing) in Berlin.

## Architecture

![Alt text](https://github.com/memphisdev/memphis-dev-academy/assets/74717402/f8c2ec11-e4c9-4417-b4c8-3f991af5235a/)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.

```bash
pip3 install -r requirements.txt
```

## Usage

Update credentials in the required fields.

### Collector

To run the collector head to "collector" directory and run

```bash
python3 collector.py
```

### Analyzer

To run the pre-processing head to "analyzer/pre_processing" directory and run

```bash
python3 main.py
```

To run the LDA model head to "analyzer/lda" directory and run

```bash
python3 main.py
```
