import gosling as gos
import streamlit as st

def get_merge_track(chip_height:int, chip_data_files:list, colors:list):
    
    tracks = []



    for i, chip_data_file in enumerate(chip_data_files):

        bigwig_data = gos.bigwig(
            url=chip_data_file,
            column="position",
            value="value",
            end="end",
            start='start'
            )
        

        bigwig_track = gos.Track(bigwig_data).mark_line().encode(
            x=gos.X("position:G", axis = 'none'),
            y=gos.Y("value:Q", axis = 'none'),
            color=gos.ColorValue(colors[i]),
            size=gos.value(2.5),
            tooltip=[
                gos.Tooltip(field='position', type='genomic'),
                gos.Tooltip(field='value', type='quantitative')            ],
            
        )

        tracks.append(bigwig_track)
    overlay = gos.overlay(*tracks).properties(height = chip_height)
    return overlay



    
    # return gos.overlay(tracks[0], tracks[1]).properties(height = chip_height)







    return st.write('test')


