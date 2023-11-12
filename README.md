# SiteTACK - Protein Sequence Analysis Tool

## Overview  
 Utilizing deep learning algorithms, it offers a methodical approach to analyzing protein sequences and identifying potential modification sites, including phosphorylation, glycosylation, and hydroxylation. The tool is developed with a focus on aiding scientific research, providing insights into the role of PTMs in biological functions.

## Features  
- **Comprehensive PTM Prediction**: Equipped to predict various PTM types such as phosphorylation, glycosylation, and hydroxyproline.
- **Sequence Input Compatibility**: Accepts protein sequences in .fasta format, compatible with standard bioinformatics workflows.
- **Probability Thresholding**: Allows setting specific probability cutoffs to enhance the precision of PTM site predictions.
- **Advanced Encoding Techniques**: Employs one-hot encoding for efficient representation and processing of protein sequences.
- **Integration of Deep Learning Models**: Utilizes TensorFlow-based neural network models for accurate PTM site prediction. 


## Requirements 
See pyproject.toml

## Installation and Setup
Install poetry  
```pip install poetry```

Install project using poetry  
```poetry install```

## License  
SiteTACK is released under the MIT License.