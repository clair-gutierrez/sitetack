
Here are select datasets and code used to train models. 

## Overview
- All training and analysis was done using jupyter notebooks
- We recommend setting up an environment to ensure the necessary packages are in the correct version and don't interfere with your global python install. We used conda to do this, and evironment setup instructions can be found in the conda documentation: https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html

## Packages
For a complete list of packages used please see the package_requirements file. In general we used:
Python >= 3.8, <3.11
Tensorflow = 2.10.0
Pandas = 2.1.1
Jupyter = 1.0.0
Matplotlib = 3.8

## Datasets
- For the datasets used in this study, the data for each are in their own folder. The specific test, train, and validation sets are not included due to size concerns, but the lists of what sites were included as positives and the reference proteome used are included so similar sets can be generated. If you want the exact sets we used please reach out. 
- Datasets are named based on the source they were obtained from
- For human datasets the reference proteome used is: UP000005640_9606

## Build your own model
The code was made general enought to build models on any PTM dataset. Please see instructions in the Construct_datasets_train_models notebook. 

## Notes
Dataset generation and training on a personal computer can take anywhere from seconds to a couple days and depends on dataset size and your system capabilites. 
