import gosling as gos
import streamlit as st



def get_enhancer_track(enhancer_height:int):
    """
    Make an enhancer track
    """

    ######~~~~~~~~~~~
    #Enhancer Track
    ######~~~~~~~~~~~
    enhancer_data = gos.csv(
        
        url = '../data/ProEnhancers_Ithinkmm10.bed',
        
        chromosomeField = 'chromosome',
        genomicFields=['chromStart', 'chromEnd'],
        sampleLength=20000,
        separator=","
    )

    
    enhancer_track = gos.Track(enhancer_data).mark_rect().encode(
        color = gos.Color('hit:N',
            range = ['#c98e00'],
        ),
        x=gos.X("chromStart:G", axis = 'none'),
        xe="chromEnd:G",
        tooltip=["chromStart:G", "chromEnd:G"]
    ).properties(
        title="  Enhancers",
        height = enhancer_height
    )

    return enhancer_track

# #col1,col2 = st.columns([1,4])

# with st.sidebar:
#     st.header('test')


# result=st_gos.from_gos(
#     spec=ideagram(mywidth=1000, myheight=50),
#     id='id2'
# )