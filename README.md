# Benchmarking and Improving OCR Systems for Southeast Asian Languages

## Overview

While Optical Character Recognition (OCR) has been widely studied for high-resource languages such as English and Chinese, its performance on Southeast Asian (SEA) languages remains largely unexplored.
This study addresses this gap by evaluating three OCR tools — EasyOCR, Tesseract, and the transformer-based General OCR Theory (GOT) — on English, Indonesian, Vietnamese, and Thai. We introduce a reusable pipeline for collecting textual data from Wikipedia and benchmarking OCR tools.
Contrary to popular belief, our results show that OCR tools perform well on complex scripts like Vietnamese and Thai, with most errors arising from misclassifying characters outside the target language. Additionally, we demonstrate the effectiveness of fine-tuning GOT with limited training data, yielding notable improvements on Vietnamese and Thai.

This repository is part of my Final Year Project (CP4101 B.Comp. Dissertation) at the National University of Singapore.

Check out my [final report](/docs/final-report/final-report.pdf) and [slide deck](/docs/slide-deck.pdf) for my findings!

## Installation & Setup

> [!NOTE]
> Benchmarking and fine-tuning OCR tools on a large-scale requires lots of compute. Hence, I recommend using a compute cluster for running this project, instead of your local machine. For details on how to run scripts on the NUS SoC Compute Cluster, refer to this [document](/ocr-benchmarking-on-sea-languages/cluster_scripts/README.md).

1. Clone this repository.

```
git clone https://github.com/jasonqiu212/ocr-benchmarking-on-sea-languages.git
cd ocr-benchmarking-on-sea-languages
```

2. Create a [virtual environment](https://docs.python.org/3/library/venv.html) for this project.

```
python3 -m venv .venv
```

3. Start the virtual environment.

```
source .venv/bin/activate
```

> To deactivate the virtual environment, enter `deactivate`.

4. Install the required Python packages from `requirements.txt`.

```
pip install -r requirements.txt
```
