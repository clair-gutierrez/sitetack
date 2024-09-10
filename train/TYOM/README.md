### Train Your Own Model (TYOM)

#### TYOM: Train your own model instructions

To allow for models to be trained using this method of encoding known PTM locations we have developed Jupyter Notebooks to train models for different contexts. To illustrate this, we have detailed this method using a dataset containing phosphorylation before and after sprinting by Parker and coworkers (Blazev et al. 2022). To use this functionality the following three things are required:
1.	A list of positive sites for the dataset in an Excel spreadsheet with one column corresponding the the “UniProt ID” and another to the “Position” in the protein. 
2.	A text file in FASTA format containing the reference proteins and their sequences, with the name formatted as such: >tr|UniProtID|…..
3.	A python environment set up with the necessary packages including Jupyter Notebook (see https://github.com/clairgutierrez/sitetack/ /train/README.md for more details)


#### Example: Looking at Pre and Post Sprinting phosphorylation datasets (Blazev et al. 2022)

The phosphorylation dataset from Parker and coworkers contains phosphoproteomic analysis of human skeletal muscle before and after different exercise modalities. We chose to use only the data for “sprint” as it showed the largest change in phosphorylation sites, which was detected with a mass error of less than or equal to 5 ppm. From this we partitioned the dataset into 3 portions: 

1.  Phosphosites that were present in both conditions (PostSprint vs PreSprint q-value >0.05)
2.  Phosphosites enriched pre-sprint (PostSprint vs PreSprint q-value ≤0.05 and Log (PostSprint/PreSprint) > 0)
3.  Phosphosites enriched post-sprint (PostSprint vs PreSprint q-value ≤0.05 and Log (PostSprint/PreSprint) < 0)

We specified that the PreSprint dataset would have all phosphosites present in both conditions and enriched in pre-sprint and the PostSprint dataset would have all phosphosites present in both conditions and enriched in post-sprint. We also obtained a reference proteome from UniProt which contained only the proteins that had a phosphosite in this study (to avoid labeling a protein site as negative if it just wasn’t detected given this is data from a single report). 

Using these datasets we trained four models (with and without phosphorylation events labeled, pre and post sprint) and evaluated the prediction accuracy of these models with and without phosphorylation locations in the pre-and post-sprint conditions. We chose an example protein, Troponin C, which is reported to be phosphorylated at S92 (which wasn’t present in our training set) and found at that position there was a large difference in prediction in the models with nearby phosphorylation locations between the pre and post sprint conditions, which was not captured by the models without phosphorylation locations. This indicates that these models were better able to capture changes in different situations (i.e pre and post exercise).
