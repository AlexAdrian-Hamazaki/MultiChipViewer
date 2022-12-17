import gosling as gos
# import streamlit as st
# import streamlit_gosling as st_gos

def get_gene_overlay(gene_height:int):
    """
    Make an ideagram with Genes
    """
    # DATA
    genes = gos.csv(
        url = '../data/ProProteinCodingGenes.csv',
        chromosomeField = 'chromosome',
        genomicFields=['chromStart', 'chromEnd'],
        sampleLength=20000,
        separator=","
    )

    
    # BASE TRACK
    base = gos.Track(genes).encode(
        row=gos.Row("strand:N", domain=["+", "-"]),
        color=gos.Color("strand:N", domain=["+", "-"], range=["#737373", "#737373"]),
        tooltip=["chromStart:G", "chromEnd:G", "strand:N", "symbol:N"]
        ).properties(
            title="  Genes",
)

    # GENE SYMBOLS
    gene_label = base.mark_text(dy=15).encode(
        x=gos.X("chromStart:G"),
        xe="chromEnd:G",
        text="symbol:N",
        size=gos.value(15)
    ).visibility_lt(
        measure="width",
        threshold="|xe-x|",
        transitionPadding=10,
        target="mark",
    )

    # PROTEIN CODING GENE BODIES
    protein_coding = base.mark_rect().encode(
        x=gos.X("chromStart:G", axis="bottom"),
        xe="chromEnd:G",
        size=gos.value(15)
        )

    plus_gene_head = base.mark_triangleRight(align="left").encode(
            x=gos.X("chromEnd:G"),
            size=gos.value(15)
            ).transform_filter(
                field="strand", oneOf=["+"]
            )

    minus_gene_head = base.mark_triangleLeft(align="right").encode(
        x=gos.X("chromStart:G"),
        size=gos.value(15)
        ).transform_filter(
        field="strand", oneOf=["-"]
        )   

    # return gene_label, protein_coding

    overlay = gos.overlay(gene_label, protein_coding, plus_gene_head, minus_gene_head ).properties(
        title="Gene Annotation",
        layout="linear",
        height = gene_height)

    return overlay


#col1,col2 = st.columns([1,4])


#DIAGNOSTICS

# st.set_page_config(layout='wide')

# with st.sidebar:
#     st.header('test')

# domain = gos.GenomicDomain(chromosome='chr1', interval=[31000000,31500000])

# result=st_gos.from_gos(
#     spec=get_gene_track(mywidth=5000, myheight=50, domain=domain),
#     id='id1')