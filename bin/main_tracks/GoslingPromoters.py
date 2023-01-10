import gosling as gos
import streamlit as st



def get_promoter_track(promoter_height:int):
    """
    Make an ideagram with promoters
    """

    ######~~~~~~~~~~~
    #Promoter Track
    ######~~~~~~~~~~~

    promoter_data = gos.csv(
        url = '../data/ProPromotersmm10.bed',
        chromosomeField = 'chromosome',
        genomicFields=['chromStart', 'chromEnd'],
        sampleLength=20000,
        separator=","
    )


    promoter_track = gos.Track(promoter_data).mark_rect().encode(
        color = gos.Color('hit:N',
            range = ['#c9cc00'],
        ),
        x=gos.X("chromStart:G"),
        xe="chromEnd:G",
        tooltip=["chromStart:G", "chromEnd:G"]
    ).properties(
        title="  Promoters",
        height = promoter_height
    )

    return promoter_track