
# maps.py
import vizro.plotly.express as px
from vizro.models.types import capture

@capture("graph")
def criar_mapa_coropletico(df, coluna_valor='populacao'):
    fig = px.choropleth(
        df,
        geojson="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson",
        locations='sigla',
        featureidkey="properties.sigla",
        color=coluna_valor,
        hover_name='estado',
        hover_data={'regiao': True, coluna_valor: ':.1f'},
        color_continuous_scale='Blues',
        scope='south america',
        labels={coluna_valor: 'População (milhares)'}
    )
    fig.update_geos(visible=False, showsubunits=True, subunitcolor='gray', fitbounds="locations")
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    return fig