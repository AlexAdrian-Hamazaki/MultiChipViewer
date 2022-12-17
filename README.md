# MultiChipViewer
## A Tool to Visualize ChIP-seq and ATAC-seq Data from Multiple Experimental Conditions

---------------------------------------

## Overview of Repository

### Directories

 + scripts: Contains the scripts necessary to run MultiChipViewer
 
 + data: Contains data required to load the mice Genes, Enhancers, and Promoters
 
### Very Important Files

 + scripts/main.py: The file to be run with streamlit un order to run MultiChipViewer
 
 + environment.yml: Conda environment that needs to be activated to run MultiChipViewer
 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
## Instructions to Install MultiChipViewer
 
### Cloning Repository
 
First, clone the repository
 
```
git clone https://github.com/AlexAdrian-Hamazaki/MultiChipViewer.git
cd MultiChipViewer
```
 
### Creating the conda environment

Create and activate the required conda environment. This should instal Gosling and Streamlit

```
conda create environment.yml
conda activate MultiChipViewerEnv
```

### Activate MultiChipViewer via streamlit
```
cd scripts
streamlit run main.py
```

In the web-application that loads, users can specify names of experimental conditions of interest. Users can then load datasets into the experimental conditions.


## What code I wrote vs what code is from another package

All code in /scripts was written by me. All of the scripts utilize Gosling commands in order to visualize the Genes, Enhancers, Promoters, ChIP-seq data, and ATAC-seq data. In these scripts, all commands prefixed with "gos." are Gosling commands. The majority of work on this project was done implementing the Gosling commands in different ways. In scripts/main.py, Streamlit commands are used to create the web-application. All commands prefaced with "st." are streamlit commands. These streamlit commands were used to create an intuitive web-app design. 


