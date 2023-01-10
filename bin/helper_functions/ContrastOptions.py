import streamlit as st
import StreamlitFunctions
import Contrasts


def display_no_contrast_options(datasets:Contrasts.datasets):
    with st.sidebar:
        StreamlitFunctions.display_dataset_loader(datasets)
        SelectionMethod = StreamlitFunctions.display_selection_method()

    ############### Add Search box to locate a Gene by Symbol @ to go there
    if SelectionMethod == "By Gene":
        ChromosomeSelection , IntervalSelection = StreamlitFunctions.display_via_gene()
    ############### Add Selection Box to choose what Chromosome and Interval you are looking at

    elif SelectionMethod == 'By Chromosome and Position':
        ChromosomeSelection , IntervalSelection = StreamlitFunctions.display_via_location()
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! INSTANTIATION MAIN ###################!!!!!!!!!!!!
    #ChromosomeSelection, IntervalSelection = StreamlitFunctions.get_domain_info(SelectionMethod)

    return ChromosomeSelection , IntervalSelection 


def display_yes_contrast_options(contrasts:Contrasts.contrasts):
    with st.sidebar:
        #Displays ALL the contrast loading options
        StreamlitFunctions.display_contrast_loader(contrasts)


        #Displays ALL the Selection Method navigation methods
        SelectionMethod = StreamlitFunctions.display_selection_method()

                           
    ############### Add Search box to locate a Gene by Symbol @ to go there
    if SelectionMethod == "By Gene":
        ChromosomeSelection , IntervalSelection = StreamlitFunctions.display_via_gene()
    ############### Add Selection Box to choose what Chromosome and Interval you are looking at

    elif SelectionMethod == 'By Chromosome and Position':
        ChromosomeSelection , IntervalSelection = StreamlitFunctions.display_via_location()
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! INSTANTIATION MAIN ###################!!!!!!!!!!!!

    return ChromosomeSelection, IntervalSelection
