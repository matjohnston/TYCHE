<div id="top"></div>

<!-- PROJECT LOGO -->
<br />
<div align="center">

<h3 align="center">TYCHE</h3>

  <p align="center">
    Goddess of Chance: Crypto analyzer
    <br />
</div>



<!-- ABOUT THE PROJECT -->
## About The Project
Simple crypto analyzer to source and identify viable tradable altcoins

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

python >= 3.8
pip >= 21.0

### for ***Windows***:

1. In PowerShell run: ```Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process```
2. Navigate to root of folder: ```cd tyche```
3. Create local environment: ```py -3 -m venv .venv```
4. Enable local environment: ```pip install -r requirements_windows.txt```


<p align="right">(<a href="#top">back to top</a>)</p>


### Usage

```python index.py```

It will then create the following structure:
reports/coinMarketCap/[mm-dd-yyyy]
with the following files:
  lowCap.csv
  microCap.csv
  midCap.csv
