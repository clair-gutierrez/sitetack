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
Docker and Docker Compose are required to run SiteTACK. See Docker's documentation for installation instructions.

## Installation and Setup  
To set up SiteTACK using Docker Compose, follow these steps:  

1. Clone the repository to your local machine.  
2. Optionally, create a `.env` file in the root directory of the project to customize configuration settings such as the web server port. For example, to set the application port, add the following line to the `.env` file:  

```
APP_PORT=8080
```

This step is optional, and if not set, the application will use its default port settings.  

3. Build the Docker image

```
docker-compose build
```

4. Start the app

```
docker-compose up
```

This command builds the Docker images if they don't exist and starts the containers. The web server will be accessible based on the APP_PORT setting or the default port defined in the Docker configuration.  

To stop the app, use:

```
docker-compose down
```

This command stops and removes the containers created by docker-compose up.

## License  
SiteTACK is released under the MIT License.