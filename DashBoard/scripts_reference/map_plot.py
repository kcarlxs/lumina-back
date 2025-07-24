import vizro.models as vm
import vizro.plotly.express as px
from vizro import Vizro
import pandas as pd
from vizro.tables import dash_ag_grid
from config import SIGLAS_ESTADOS, REGIOES_ESTADOS

def carregar_dados_planilha(caminho_arquivo):
    df = pd.read_excel(caminho_arquivo, header=None, usecols=[0, 1], names=['estado', 'populacao'])
    
    #siglas e regiões
    df['sigla'] = df['estado'].map(SIGLAS_ESTADOS)
    df['regiao'] = df['sigla'].map(REGIOES_ESTADOS)
    
    return df.dropna()

#dados
df = carregar_dados_planilha("POP2022_Brasil_e_UFs.xlsx")

# mapa coroplético sem título interno
fig = px.choropleth(
    df,
    geojson="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson",
    locations='sigla',
    featureidkey="properties.sigla",
    color='populacao',
    hover_name='estado',
    hover_data={'regiao': True, 'populacao': ':.1f'},
    color_continuous_scale='Blues',
    scope='south america',
    labels={'populacao': 'População (milhares)'}
)

# layout
fig.update_geos(visible=False, showsubunits=True, subunitcolor='gray', fitbounds="locations")
fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})

# dados para as tabelas
df_resumo = df.groupby('regiao').agg(
    total_populacao=('populacao', 'sum'),
    num_estados=('estado', 'count')
).reset_index()
df_resumo['total_populacao'] = df_resumo['total_populacao'].round(1)

df_detalhado = df[['regiao', 'estado', 'populacao']].sort_values(['regiao', 'populacao'], ascending=[True, False])

def criar_tabela_ag_grid(data_frame):
    return dash_ag_grid(data_frame=data_frame)

pages = [
    vm.Page(
        title="Visão Nacional",
        layout=vm.Grid(grid=[[0, 1], [2, 2]]),
        components=[
            vm.Graph(
                figure=fig,
                title="Mapa de Distribuição Populacional" 
            ),
            vm.AgGrid(
                figure=criar_tabela_ag_grid(
                    data_frame=df_resumo.sort_values('total_populacao', ascending=False)
                ),
                title="Dados por Região" 
            ),
            vm.AgGrid(
                figure=criar_tabela_ag_grid(
                    data_frame=df_detalhado
                ),
                title="Dados por Estado" 
            )
        ],
        controls=[
            vm.Filter(column="regiao")
        ]
    )
]

#páginas por região
for regiao in sorted(df['regiao'].unique()):
    df_regiao = df[df['regiao'] == regiao]
    
    #mapa regional sem título interno
    fig_regiao = px.choropleth(
        df_regiao,
        geojson=fig.data[0].geojson,
        locations='sigla',
        featureidkey="properties.sigla",
        color='populacao',
        scope='south america'
    )
    
    pages.append(
        vm.Page(
            title=regiao,
            layout=vm.Grid(grid=[[0, 1]]),
            components=[
                vm.Graph(
                    figure=fig_regiao,
                    title=f"Mapa da {regiao}" 
                ),
                vm.AgGrid(
                    figure=criar_tabela_ag_grid(
                        data_frame=df_regiao[['estado', 'populacao']].sort_values('populacao', ascending=False)
                    ),
                    title="Detalhes"  
                )
            ]
        )
    )
dashboard = vm.Dashboard(pages=pages)
Vizro().build(dashboard).run()