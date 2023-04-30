
# The Python parser of the site about the calorie content of food

Collects all the information from the site and writes it to: **json** dictionary, **csv** table and **html** code.

The output is 20 MB of pure information that can be used anywhere, be it a calorie calculator, a diet plan, a nutritionist application


## Installation


Install the **requests**, **lxml**, **BeautifulSoup4** libraries in your virtual environment if necessary, or use the already created venv of the project
```bash
  pip install requests lxml BeautifulSoup4
```
Next, clear the **data folder** just in case you want to run the program, because there will be an overlap of information, everything will be duplicated.
## Tech Stack

**Client:** Python, Json

**Used libaries:** 
```Python 
import random
from time import sleep
import requests
from bs4 import BeautifulSoup
import json
import csv
```


## Run

Clone the project

```bash
  git clone https://github.com/IIvannM/foodScraper
```

Go to the project directory and run in

```bash
  cd project-path
  
  python main.py
```



____

If you have any feedback, write to me on **telegram** *@ivannmig*

