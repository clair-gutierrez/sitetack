
Here are select datasets and code used to train models. 

## Overview
- All training and analysis was done using jupyter notebooks
- We recommend setting up an environment to ensure the necessary packages are in the correct version and don't interfere with your global python install. We used conda to do this, and evironment setup instructions can be found in the conda documentation: https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html

## Packages
For a complete list of packages used please see the package_requirements file. We recommend setting up your environment with these packages (this should take ~5-60min to set up):
- Python >= 3.8, <3.11
- Tensorflow = 2.10.0
- Numpy = 1.26.0
- Pandas = 2.1.1
- Jupyter = 1.0.0
- Matplotlib = 3.8
- Scikit-learn = 1.3.0
- tqdm  >=4.0
- scipy >=1.11

If you are using conda to set up an environment, you can use the provided .yml file to easily set up an envirnoment with the correct packages:
```
conda env create -f sitetack_conda_env.yml
```
This will create an environment with the name: sitetack-env

## Datasets
- For the datasets used in this study, the data for each are in their own folder. The specific test, train, and validation sets are not included due to size concerns, but the lists of what sites were included as positives and the reference proteome used are included so similar sets can be generated. If you want the exact sets we used please reach out. 
- Datasets are named based on the source they were obtained from
- For human datasets the reference proteome used is: UP000005640_9606

## Build your own model
The code was made general enought to build models on any PTM dataset. Please see instructions in the Construct_datasets_train_models notebook. 

## Demo and 
For demo purposes they jupyter notebooks are set for and show the outputs for the generation of Ubiquitination (K) from the MusiteDeep dataset for human proteins. 

To recapitutalte the results of this study, the PTM name and dataset can be changed in the jupyter notebook to match the files for the other datasets. 

## CD-Hit removal of similar kmers
To access CD Hit, the library pycdhit was used. As a note, this code with pycdhit will only work on Unix systems. See pycdhit documentation of installation instructions: https://pypi.org/project/py-cdhit/

### CD-Hit Citations

## Notes
Dataset generation and training on a personal computer can take anywhere from seconds to a couple days and depends on dataset size and your system capabilites. 
