import gosling as gos
import streamlit as st
import streamlit_gosling as st_gos
import pandas as pd 

from GoslingEnhancers import get_enhancer_track
from GoslingPromoters import get_promoter_track
from GoslingGenes import get_gene_overlay
from BigWigTrack import get_bigwig_track
from ChipMerge import get_merge_track
import StreamlitFunctions
import ContrastOptions
import Contrasts


import importlib

importlib.reload(Contrasts)
#@st.cache TODO separate functions into what can be cached and what doesnt need to be cached
def main(container_width:int,
        chromosome_selection, 
        interval:list, 
        chip_height:int, 
        gene_height:int, 
        enhancer_height:int, 
        promoter_height:int,
        datasets:Contrasts.datasets,
        MergedChip:bool,
        EnableContrasts:bool,
        contrasts:Contrasts.contrasts):
    """
    Make an ideagram with Enhancers AND Promoters
    """

    ######~~~~~~~~~~~
    #Create Domain of Selection
    ######~~~~~~~~~~~
 
    domain = gos.GenomicDomain(chromosome=chromosome_selection, interval=interval)
    # ChromFilter = gos.IncludeFilter(field='chromosome', include=mydomain, type=mydomain)

    ######~~~~~~~~~~~
    #Enhancer Track
    ######~~~~~~~~~~~
    enhancer_track = get_enhancer_track(enhancer_height=20)

    ######~~~~~~~~~~~
    #Promoter Track
    ######~~~~~~~~~~~
    promoter_track = get_promoter_track(promoter_height=20)

    ######~~~~~~~~~~~
    # Genes Overlay
    ######~~~~~~~~~~~

    gene_overlay = get_gene_overlay(gene_height=gene_height)

    ######~~~~~~~~~~~
    # If Contrasts are Disabled...
    ######~~~~~~~~~~~

    if not EnableContrasts:

        chipseq_tracks = []

        for dataset in datasets.lod:
            track = get_bigwig_track(bigwig_file= dataset.url, 
                                        chip_height = chip_height, 
                                        name = dataset.name, 
                                        color = dataset.color).properties(
                                                            width=container_width)

            chipseq_tracks.append(track)

        chip_vert = gos.vertical(*chipseq_tracks).properties(
                    spacing = 0,
                    linkingId = "vert")

        ######~~~~~~~~~~~
        # If Merged view is Disabled...
        ######~~~~~~~~~~~
        
        vis = gos.stack(gene_overlay, enhancer_track, promoter_track).properties(
                    spacing = 0, width=container_width, linkingId = "vert")

        vis = gos.vertical(vis, chip_vert).properties(spacing = 30,
                    xDomain=domain, linkingId = "vert")


        ######~~~~~~~~~~~
        # If Merged view is Enabled...
        ######~~~~~~~~~~~
        if MergedChip:
            if len(st.session_state['datasets'].lod) == 0:
                return vis
                
            urls =[dataset.url for dataset in st.session_state['datasets'].lod]
            print(f'URLS {urls}')

            merged_track = get_merge_track(chip_height=chip_height*5,
                                                chip_data_files=[dataset.url for dataset in st.session_state['datasets'].lod], 
                                                colors = [dataset.color for dataset in st.session_state['datasets'].lod]).properties(
                    spacing = 0, width=container_width, linkingId = "vert")


            vis = gos.vertical(vis, merged_track).properties(
                                xDomain=domain, spacing = 40, linkingId = "vert")

        return vis

    if EnableContrasts:
        #chipseq_stacks: A List of stacks. Each stack corresponds to a contrast's chipseq profiles
        chipseq_stacks_l = []
        for contrast in contrasts.loc:
            #chipseq_tracks: A List of tracks. Each track is from a dataset in the current contrast
            chipseq_tracks = []

            for dataset in contrast.datasets.lod:
                track = get_bigwig_track(bigwig_file= dataset.url, chip_height = chip_height, name = dataset.name, color = dataset.color)
                chipseq_tracks.append(track)
                #Each dataset has its own track. 
            
            #Make 1 stack that corresponds to all of the tracks in the current contrast
            # NB: A chipseq stack is of type "view"

            chipseq_stack = gos.stack(*chipseq_tracks).properties(
                    xDomain=domain, spacing = 0, width=container_width)


            # Append new stack.
            chipseq_stacks_l.append(chipseq_stack)

            #add int for background color reasons


        # Combine all Chipseq Stacks into one stack
        # We cannot do this because we don't have a "view"?
        #contrast_stack = gos.stack(*chipseq_stacks_l)
        chipseq_vertical = gos.vertical(*chipseq_stacks_l, spacing = 32)


        # NB a Vertical is a "View" type
        print(f'Chipseq_vertical {type(chipseq_vertical)}')
       

        vis = gos.stack(gene_overlay, enhancer_track, promoter_track).properties(
                    xDomain=domain, spacing = 0, width=container_width)
        print(f'Enhancer {type(enhancer_track)}')
        print(f'Promoter {type(promoter_track)}')
        print(f'Gene_Overlay {type(gene_overlay)}')

        #vis is a view
        print(f'Vis {type(vis)}')

        # I think you can add two views together easily right?
        vis2 = gos.vertical(vis, chipseq_vertical,  spacing = 37).properties(
            linkingId = "-",
            xDomain = domain)


        contrast_names = st.session_state['contrasts'].get_names()
        print(contrast_names)
        
        if MergedChip:

            if contrasts.get_num_datasets() == 0:
                return vis2
                
            merged_tracks = []

            for contrast in contrasts.loc:
                if contrast.get_len_datasets() == 0:
                    continue

                dataset_urls = contrast.get_datasets_urls()
                dataset_colors = contrast.get_datasets_colors()

                print(f'URLS {dataset_urls}')
                print(f'COLORS {dataset_colors}')
                

                #SOMETHING IS WRONG WITH MERGED_TRACK
                merged_track = get_merge_track(chip_height = 75,
                                                chip_data_files = dataset_urls,
                                                colors = dataset_colors).properties(
                                                    width=container_width)
                print(type(merged_track))

                merged_tracks.append(merged_track)




            merged_vis = gos.vertical(*merged_tracks, spacing = 0)
            vis2 = gos.vertical(vis2, merged_vis, spacing = 50).properties(
                linkingId = "-",
                xDomain = domain
                )


        

        return vis2





    # return full_vis




######## Page Config
#This must Be the first "st" script you call
#Makes sure stuff loads on the left, not the middle
st.set_page_config(layout='wide')

############### Add Search box for selection method

if 'datasets' not in st.session_state.keys():
    datasets = Contrasts.datasets(lod=[])
    st.session_state['datasets'] = datasets
else:
    datasets = st.session_state['datasets']

if 'contrasts' not in st.session_state.keys():
    contrasts = Contrasts.contrasts(loc = [])
    st.session_state['contrasts'] = contrasts
else:
    contrasts = st.session_state['contrasts']

if 'EnableContrasts' not in st.session_state.keys():
    st.session_state['EnableContrasts'] = False
EnableContrasts = st.session_state['EnableContrasts']

if not EnableContrasts:
    ChromosomeSelection, IntervalSelection = ContrastOptions.display_no_contrast_options(datasets)
else:
    ChromosomeSelection, IntervalSelection = ContrastOptions.display_yes_contrast_options(contrasts)


with st.sidebar:
    #multiple_contrasts=st.checkbox(label = "Enable Multiple Contrasts", help="Enabling Multiple Contrasts allows you to compare ChIPseq, and ATACseq of multiple categorical contrasts at once. For example: several time series, or several cell types")
    EnableContrasts=StreamlitFunctions.display_enablecontrast_check_box()


with st.sidebar:
    MergedChip=StreamlitFunctions.display_merged_checkbox()

if st.session_state['EnableContrasts'] == False:
    st.markdown("""## SingleChIPViewer""")
    st.markdown("""###### mm10 Construct | Scroll and Zoom to Explore Data""" )
elif st.session_state['EnableContrasts'] == True:
    st.markdown("""## MultiChIPViewer""")
    st.markdown("""###### mm10 Construct | Scroll and Zoom to Explore Data""")


col1, col2 = st.columns([1,15], gap = 'medium')

with col1:

    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')



    contrasts = st.session_state['contrasts']

    #num_datasets has the number of datasets for each ocntrast indexed
    num_datasets = []
    for contrast in contrasts.loc:
        num_datasets.append(contrast.get_len_datasets())


    #Only look at 1 onwards for contrasts because first contrast name is always placed in the same place
    for i,contrast in enumerate(contrasts.loc):

        if i == 0:

            st.markdown("""<p> </p>""", unsafe_allow_html=True)
            st.markdown("""<p> </p>""", unsafe_allow_html=True)

            name = str(contrast.name)
            st.subheader(name)

        elif num_datasets[i] == 0:
            continue

        else:
            
            prev_num = num_datasets[i-1]

            spacing_dic = {0:0, 1:0, 2:2, 3:4, 4:7, 5:9, 6:11, 7:13, 8:15, 9:17}
            
            req_spaces = spacing_dic[prev_num]

            for i in range(req_spaces):
                st.text('')
            
            name = str(contrast.name)
            st.subheader(name)


    if MergedChip:

        st.text('')
        st.text('')
        st.text('')
        st.text('')
        st.text('')


        for i,contrast in enumerate(contrasts.loc):

            if i == 0:

                st.markdown("""<p> </p>""", unsafe_allow_html=True)
                st.markdown("""<p> </p>""", unsafe_allow_html=True)

                name = str(contrast.name)
                st.subheader(name)


            else:
                

                spacing = 2

                name = str(contrast.name)
                st.subheader(name)

            

with col2:

    result=st_gos.from_gos(
        spec=main(container_width=1550,
                    chip_height=36, 
                    gene_height=100, 
                    promoter_height = 40, 
                    enhancer_height = 40, 
                    chromosome_selection=ChromosomeSelection, 
                    interval=IntervalSelection,
                    datasets = datasets,
                    MergedChip=MergedChip,
                    EnableContrasts=EnableContrasts,
                    contrasts=contrasts),
        id='id1', 
        #This height changes the height of the streamlit container
        height = 5000)






