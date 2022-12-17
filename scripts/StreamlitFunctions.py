import streamlit as st
import pandas as pd
import Contrasts

def _append_dataset(new_dataset:Contrasts.dataset, datasets:Contrasts.datasets):
    if new_dataset.name != '' and new_dataset.url != '':
        #TODO ADD ABILITY TO STOP USERS FROM ADDING DATASETS OF SAME NAME
        datasets.lod.append(new_dataset)
    return datasets

def _append_contrast(new_contrast:Contrasts.contrast, contrasts:Contrasts.contrasts):
    if new_contrast.name != '':
        #TODO ADD ABILITY TO STOP USERS FROM ADDING DATASETS OF SAME NAME
        contrasts.loc.append(new_contrast)
    return contrasts

def _remove_all_datasets():
    st.session_state['datasets'] = Contrasts.datasets(lod=[])

def _remove_all_contrasts():
    st.session_state['contrasts'] = Contrasts.contrasts(loc=[])

def _coerse_for_pandas(datasets:Contrasts.datasets):
    """ coerse datasets for pandas loading
    """
    coerced = []
    for dataset in datasets.lod:
        name = dataset.name
        url = dataset.url
        color = dataset.color

        coerced.append([name, url, color])

    return coerced

def display_loaded_datasets(datasets:Contrasts.datasets):
    with st.expander(label = 'Loaded Datasets', expanded = False):
        dataset_df = pd.DataFrame(_coerse_for_pandas(datasets), columns = ["Name", "Path", "Color"])
        st.dataframe(dataset_df, use_container_width=True)

def display_loaded_datasets_in_contrasts(datasets:Contrasts.datasets):
    dataset_df = pd.DataFrame(_coerse_for_pandas(datasets), columns = ["Name", "Path", "Color"])
    st.dataframe(dataset_df, use_container_width=True)

def display_loaded_contrasts(contrasts:Contrasts.contrasts):
    with st.expander(label = 'Loaded Contrasts', expanded = False):

        for contrast in contrasts.loc:

            st.subheader(contrast.name)

            display_loaded_datasets_in_contrasts(contrast.datasets)



def display_dataset_loader(datasets:Contrasts.datasets):
    col1, col2 = st.columns(2)

    with col1:
        add_dataset = st.button(label = "Add New Dataset")
    with col2:
        remove_datasets = st.button(label = 'Remove All Datasets')

    with st.expander(label = 'Add Dataset', expanded = True):

        ds_name = st.text_input(label = "Dataset Name", label_visibility='collapsed', placeholder='Dataset Name')

        col1, col2 = st.columns([2, 15])

        with col2:
            ds_url = st.text_input(label = "Filename", 
                                    placeholder='Dataset\'s Relative Path',
                                    help = "Accepted files are \".bed\", \".bigWig\"",
                                    label_visibility='collapsed')

            ds_color = st.selectbox('Color', options = ["Red", "Blue",  "Green", "Purple", "Teal", "Pink"], label_visibility = 'collapsed')



            color_dict = {"Red":" #ff0000 ",
                "Blue":" #0037ff ",
                "Green":'#10ff00',
                        "Purple":'#bc00ff',
                        "Teal":'#00fff6',
                        "Pink":' #fc00ff '}
                        
            cur_colour = color_dict[ds_color]
            #st.color_picker(label='color_picker', value = "#FFB3B3", label_visibility='collapsed')

    new_dataset = Contrasts.dataset(name = ds_name,
                        url = ds_url,
                        color = cur_colour)


    if add_dataset:
        datasets = _append_dataset(new_dataset, datasets)


    if remove_datasets:
        _remove_all_datasets()


    display_loaded_datasets(datasets)

    #TODO REMOVE SELECTED DATSETS

    # datasets_to_remove = st.multiselect(label ='Remove Datsets', options=dataset_df['Name'])
    # remove_dataset = st.button(label = 'Remove Selected Datasets')

        
    # if remove_dataset:
    #     for index in range(len(st.session_state['datasets'])):
    #         for remove_dataset_name in datasets_to_remove:
    #             if st.session_state['datasets'][index][0] == remove_dataset_name:
    #                 del st.session_state['datasets'][index]
    #                 break #TODO FIX INDEX ERROR THAT OCCURS SOMETIMES

def get_contrast_names(contrasts:Contrasts.contrasts):
    contrast_names = []
    for contrast in contrasts.loc:
        contrast_names.append(contrast.name)
    return contrast_names



def display_contrast_loader(contrasts:Contrasts.contrasts):
    col1, col2= st.columns(2)
    
    with col1:
        add_contrast = st.button(label = "Add New Condition")

    with col2:
        remove_all_contrast = st.button(label = 'Remove Conditions')

    with st.expander(label = 'Add Condition', expanded = True):

        ct_name = st.text_input(label = "ContrastName", label_visibility='collapsed', placeholder='Contrast Name')

    
    
    remove_one = st.button(label = 'Remove Selected Condition') 


    new_contrast = Contrasts.contrast(name = ct_name,
                                        datasets = Contrasts.datasets(lod =[]))

    if add_contrast:
        contrasts.add_one_contrast(new_contrast)

    if remove_all_contrast:
        st.session_state['contrasts'].loc=[]


    # Displays the selector for selecting a contrast

    with st.expander(label = 'Add Datasets to Conditions', expanded = True):
        contrast_names = get_contrast_names(contrasts)

        selected_contrast = st.selectbox(label = 'Select Contrast To Add Dataset Onto',
                                        options = contrast_names, key = 'key2', label_visibility='collapsed')

        ds_name = st.text_input(label = "Dataset Name", label_visibility='collapsed', placeholder='Dataset Name')

        col1, col2 = st.columns([2, 15])

        with col2:
            ds_url = st.text_input(label = "Filename", 
                                    placeholder='Dataset\'s Relative Path',
                                    help = "Accepted files are \".bed\", \".bigWig\"",
                                    label_visibility='collapsed')

            ds_color = st.selectbox('Color', options = ["Red", "Blue",  "Green", "Purple", "Teal", "Pink"], label_visibility = 'collapsed')



            color_dict = {"Red":" #ff0000 ",
                "Blue":" #0037ff ",
                "Green":'#10ff00',
                        "Purple":'#bc00ff',
                        "Teal":'#00fff6',
                        "Pink":' #fc00ff '}
                        
            cur_colour = color_dict[ds_color]
            #st.color_picker(label='color_picker', value = "#FFB3B3", label_visibility='collapsed')

    new_dataset = Contrasts.dataset(name = ds_name,
                        url = ds_url,
                        color = cur_colour)

    col1, col2 = st.columns(2)


    with col1:
        add_dataset = st.button(label = "Add Dataset to Condition")
    with col2:
        remove_datasets = st.button(label = 'Remove All Datasets from Condition')

    if add_dataset:
        current_contrast = None
        for contrast in contrasts.loc:
            if contrast.name == selected_contrast:
                current_contrast = contrast


        #Add new dataset to selected contrast
        current_contrast.datasets.lod.append(new_dataset)


    if remove_datasets:
        current_contrast = None
        for contrast in contrasts.loc:
            if contrast.name == selected_contrast:
                current_contrast = contrast

        #remove all datasets from a given contrast
        current_contrast.datasets = Contrasts.datasets(lod=[])


        
    # if remove_datasets:
    #     _remove_all_datasets()

    #Dislpays the loaded contrasts
    

    #display loaded contrasts function
    with st.expander(label = 'Loaded Condition and Their Datasets', expanded = False):

        if len(contrasts.loc) == 0: 
            st.write('')
        else:    
            for contrast in contrasts.loc:

                st.subheader(contrast.name)

                dataset_df = pd.DataFrame(_coerse_for_pandas(contrast.datasets), columns = ["Name", "Path", "Color"])
                st.dataframe(dataset_df, use_container_width=True)

    

    








        # col1, col2,col3 = st.columns(3)

        # with col1:
        #     ds_name = st.text_input(label = "Dataset Name", label_visibility='collapsed', placeholder='Dataset Name')

        # with col2:
        #     ds_url = st.text_input(label = "Filename", 
        #                             placeholder='Dataset Path',
        #                             help = "Accepted files are \".bed\", \".bigWig\"",
        #                             label_visibility='collapsed')
        # with col3:

        #     ds_color = st.color_picker(label='color_picker', value = "#FFB3B3", label_visibility='collapsed')




def display_enablecontrast_check_box():
    return st.checkbox(label = "Enable Multiple Contrasts", help="Enabling Multiple Contrasts allows you to compare ChIPseq, and ATACseq of multiple categorical contrasts at once. For example: several time series, or several cell types", key = 'EnableContrasts')


def display_merged_checkbox():
    return st.checkbox(label = "Display Overlap Graph",
                            value = False,
                            key = 'merged_chip',
                            help="Enable a view that displays the data in an overlapping fashion")

def display_selection_method():
    return st.radio(label = "Choose Search Method",
                                    options=['By Gene', 'By Chromosome and Position'],
                                    key = 'selection_method')


def display_via_gene():
    with st.sidebar:
        GeneSelection = st.selectbox(label = 'Input or Select Gene Symbol',
                                #options = the gene names
                                options = pd.read_csv('../data/ProGeneNamesmm10.csv', header=None, names = ['genes'])['genes'],
                                #index provides the default option which should take you to Mecp2
                                index = 10992,
                                #key is for accessing value via st.sessionstate.key
                                key = 'gene')


    ProProteinCodingGenes = pd.read_csv('../data/ProProteinCodingGenes.csv', sep=",")

    # Upon Startup. Will locate Alcf Gene info. Set domain to Alcf Interval and Chromosome.
    gene_row = ProProteinCodingGenes.loc[ProProteinCodingGenes['symbol'] == GeneSelection].squeeze()

    #Note: gene_row[6] is added/substracted to increase the window frame
    IntervalSelection = [gene_row[1]-gene_row[6]/2, gene_row[2]+gene_row[6]/2]
    ChromosomeSelection = gene_row[0]

    return ChromosomeSelection, IntervalSelection


def display_via_location():
    with st.sidebar:
        st.subheader("Select Chromosome")
        ChromosomeSelection = st.selectbox(label = 'Select Chromosome',
            #options = the chromosome string names
            options = pd.read_csv('../data/ProChromosomeNamesmm10.txt', header = None, names=['chromosomes'])['chromosomes'],
            #index provides the default option #should take to you A1cf
            index = 18,
            label_visibility ='collapsed')

        st.subheader("Select Start and End Positions")
        col1, col2 = st.columns(2)

        with col1:
            st.number_input(label = "Start", key = 'start_pos', step = 10000, value = 31868756 - 5000)


        with col2:
            st.number_input(label = 'End', key = 'end_pos', step = 10000, value = 31952365+ 50000)

    IntervalSelection = [st.session_state.start_pos, st.session_state.end_pos]

    return ChromosomeSelection, IntervalSelection

def get_domain_info(SelectionMethod): #TODO ASK GUILLAUME ABOUT CALLING FUNCTIONS THAT RE IN THE SAME FOLDER
    pass

    # ############### Add Search box to locate a Gene by Symbol @ to go there
    # if SelectionMethod == "By Gene":
    #     ChromosomeSelection , IntervalSelection = StreamlitFunctions.display_via_gene()
    # ############### Add Selection Box to choose what Chromosome and Interval you are looking at

    # elif SelectionMethod == 'By Chromosome and Position':
    #     ChromosomeSelection , IntervalSelection = StreamlitFunctions.display_via_location()
    # #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! INSTANTIATION MAIN ###################!!!!!!!!!!!!

    # return ChromosomeSelection , IntervalSelection 


    