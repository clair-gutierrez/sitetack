# Sitetack: A Deep Learning Model that Improves PTM Prediction by Using Known PTMs

## Overview  
Post-translational modifications (PTMs) increase the diversity of the proteome and are vital to organismal life and therapeutic strategies. Here we have developed models that use known PTM sites in prediction via sequence-based deep learning algorithms. Specifically, PTM locations were encoded as a separate amino acid before sequences were encoded via word embedding and passed into a convolutional neural network that predicts the probability of a modification at a given site. 

## Models
- PTMs: Phosphorylation (S, T), Phosphorylation (Y), Glycosylation (N), Glycosylation (S, T), Ubiquitination (K), SUMOylation (K), Acetylation (K), Methylation (K), Methylation (R), Pyroglutamylation (Q), Palmitoylation (C), Hydroxylation (P), and Hydroxylation (K).
- Kinase specific models for 68 kinases (To be added)
- N-glycosylation seqon specific models (To be added)
- O-glycosylation substype specific models for O-GalNAc, O-GlcNAc, and O-HexNAc 
- Prediction of O-GlcNAc using phosphoryaltion (S, T) sites. (To be added)


## Requirements 
Sitetack is available as a free webtool at: sitetack.net

For code for dataset generation, model training, and test set analysis see the train folder along with instructions for building your own model.

For the local tool, Docker and Docker Compose are required to run Sitetack docker images. See Docker's documentation for installation instructions.

## Installation and Setup via Docker
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
