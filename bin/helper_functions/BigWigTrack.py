import gosling as gos

def get_bigwig_track(bigwig_file:str, chip_height:int, name:str, color):

    bigwig_data = gos.bigwig(
            url=bigwig_file,
            column="position",
            value="value",
            end="end",
            start='start'
            )




    bigwig_track = gos.Track(bigwig_data).mark_bar(
            ).encode(
            x=gos.X("position:G", axis='none'),
            y=gos.Y("value:Q", axis = 'none'),
            color=gos.ColorValue(color),
            tooltip=[
                gos.Tooltip(field='position', type='genomic'),
                gos.Tooltip(field='value', type='quantitative')]            
        ).properties(height = chip_height,
                    title=f"  {name}",
        )

    return bigwig_track



# def point_chart(chr='1', chartType='point chart'):
#     data = gos.bigwig(
#         url='../data/ENCFF331LHP.bigWig',
#         column="position",
#         value="value",
#         end="end",
#         start='start'
#     )

#     domain = gos.GenomicDomain(chromosome=chr)

#     track = gos.Track(data).mark_point().encode(
#         x=gos.X("position:G", domain=domain, axis="top"),
#         y="value:Q",
#         color = gos.ColorValue('red')
#     )

#     chart = track.view(title='click to select an item')

#     return chart