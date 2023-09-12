# Social media network analysis

In this repo you will find a basic code to analyze public data from social networks.
The code was presented on a talk on [Stackconf conference 2023](https://docs.google.com/presentation/d/1al3fLS50SXYUwGpn6zDjnrkM-gfIvUx_1qQk2akqPeg/edit?usp=sharing) in Berlin.

## Architecture

![Alt text](https://github-production-user-asset-6210df.s3.amazonaws.com/74717402/266946664-06cd1401-fcfc-4ac5-ac5f-a59598f7f4e3.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20230912%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20230912T204219Z&X-Amz-Expires=300&X-Amz-Signature=d15055bc95d47e56ac581aeef8d596617560f1b113160f1b7654d6470934738c&X-Amz-SignedHeaders=host&actor_id=74717402&key_id=0&repo_id=530804070)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.

```bash
pip3 install -r requirements.txt
```

## Usage

Update credentials in the required fields.

To run the collector head to "collector" directory and run

```bash
python3 collector.py
```

To run the analyzer head to "analyzer" directory and run

```bash
python3 analyzer.py
```
