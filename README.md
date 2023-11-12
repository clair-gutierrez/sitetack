# SiteTACK - Sequence Analysis Tool  

## Overview  
PTM Predictor is a specialized tool designed to predict post-translational modifications (PTMs) in protein sequences. It leverages machine learning techniques to analyze protein sequences and predict potential sites of modification such as phosphorylation, glycosylation, hydroxylation, and others. This tool aims to assist researchers in understanding and exploring the complex world of protein modifications, which play a crucial role in various biological processes.

## Features  
* Versatile PTM Prediction: Supports multiple PTM types, including phosphorylation, glycosylation, and hydroxyproline, among others.  
* Sequence Input Compatibility: Accepts protein sequences in .fasta format, making it compatible with standard bioinformatics workflows.  
* Probability Thresholding: Allows users to specify a cutoff probability, enhancing the precision of PTM site prediction.  
* Advanced Encoding Techniques: Implements one-hot encoding for efficient representation and processing of protein sequences.  
* Deep Learning Integration: Utilizes TensorFlow-based neural network models for accurate prediction of PTM sites.  

## Requirements 
See pyproject.toml

## Installation and Setup
Install poetry  
```pip install poetry```

Install project using poetry  
```poetry install```

## License  
SiteTACK is released under the MIT License.  