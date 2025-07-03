import pandas as pd
import vizro.plotly.express as px
from vizro import Vizro
import vizro.models as vm
from vizro.tables import dash_ag_grid
from config import SIGLAS_ESTADOS, REGIOES_ESTADOS

Vizro._reset()

def carregar_dados_planilha(caminho_arquivo):
    df2 = pd.read_excel(caminho_arquivo, header=None, usecols=[0, 1], names=['estado', 'populacao'])  
    df2['sigla'] = df2['estado'].map(SIGLAS_ESTADOS)
    df2['regiao'] = df2['sigla'].map(REGIOES_ESTADOS)
    return df2.dropna()

#CSV
df = pd.read_csv("base/dados_demograficos_brasil.csv", sep=";")
df1 = pd.read_csv("base/database_bioscan.csv", sep=";")
df2 = carregar_dados_planilha("base/POP2022_Brasil_e_UFs.xlsx")

# Cria o mapa coroplético
fig = px.choropleth(
    df2,
    geojson="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson",
    locations='sigla',
    featureidkey="properties.sigla",
    color='populacao',
    hover_name='estado',
    hover_data={'regiao': True, 'populacao': ':.1f'},
    color_continuous_scale='Blues',
    scope='south america',
    labels={'populacao': 'População (M)'}
)

#layout mapa
fig.update_geos(visible=False, showsubunits=True, subunitcolor='gray', fitbounds="locations")
fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})

#dados das tabelas
df_resumo = df2.groupby('regiao').agg(total_populacao=('populacao', 'sum'), num_estados=('estado', 'count')).reset_index()
df_resumo['total_populacao'] = df_resumo['total_populacao'].round(1)
df_detalhado = df2[['regiao', 'estado', 'populacao']].sort_values(['regiao', 'populacao'], ascending=[True, False])

#tabelas sem o parâmetro title
def criar_tabela_ag_grid(data_frame):
    return dash_ag_grid(data_frame=data_frame)

#calculos para graficos
total_masculino = df["populacao_masculina"].sum()
total_feminino = df["populacao_feminina"].sum()
df_donut = pd.DataFrame({
    "Categoria": ["População Masculina", "População Feminina"],
    "Total": [total_masculino, total_feminino]
})

# Preparação de figuras 
fig_pie = px.pie(df_donut, values="Total", names="Categoria", hole=0.5)
fig_crescimento = px.histogram(df, x='regiao', y='crescimento_populacional')

#################################################################################################################

# Definição das telas dashboard
page0 = vm.Page(
    title="Homepage",
    id="main_page",
    layout=vm.Grid(grid=[[0,1,2],[0,3,4]]),
    components=[
        vm.Card(
            text="""
            ## Lumina BI
            Lumina Lab desenvolveu uma plataforma completa para monitoramento de dados de projetos, 
            oferecendo dashboards modernos e altamente interativos.
            
            Esses recursos foram criados para facilitar a rotina de gestores de projetos, 
            permitindo:

            -> Visualização de indicadores estratégicos

            -> Análise de desempenho em tempo real

            -> Identificação de riscos e oportunidades

            -> Tomada de decisão baseada em dados confiáveis

            Com foco em tecnologia, segurança e usabilidade, a Lumina Lab ajuda empresas 
            a transformar dados complexos em insights claros, otimizando a gestão de seus 
            projetos e potencializando resultados.
            
            ![](assets/images/lumina.png#my-lumina)
            """,
            href="https://www.luminalab.ai/pt",
        ),
        vm.Card(
            text="""
            ### 
            ![](assets/images/denguezero.png#my-bioscan)
            """,
            href="/bioscan_dashboard_v3",
        ),
        vm.Card(
            text="""
            ![](assets/images/empoli-large-logo.png#my-empoli)
            """,
            href="/dados_empoli",
        ),
        vm.Card(
            text="""
            ###
            ![](assets/images/urban.jpg#my-urban)
            """,
            href="/urbanai",
        ),
        vm.Card(
            text="""
            ###
            ![](assets/images/eleodora2.png#my-eleodora)
            """,
            href="/dados_gerais",
        ),
    ],
)
      
    
#################################################################################################################
#  Telas de Direcionamentos - paginas

page1 = vm.Page(
    title="Bioscan - Dengue Zero",
    id="bioscan_dashboard_v3",
    layout=vm.Grid(grid=[[0, 1],[2, 3]]),
    components=[
        vm.Container(
            title="População por Sexo",
            components=[vm.Graph(
                figure=fig_pie,
            )],
            variant="filled"
        ),
        vm.Container(
            title="Acesso à Saúde Publica",
            components=[vm.Graph(
                figure=px.histogram(df, x="regiao", y="acesso_saude_publica"),
            )],
            variant="filled"
        ),
        vm.Container(
            title="Combate à Dengue",
            components=[vm.Graph(
            figure=px.scatter(df1, x="estados", y="focos_encontrados")
            )],
            variant="filled"
        ),
        vm.Container(
            title="Indice de Saneamento",
            components=[vm.Graph(
                figure=px.histogram(df, x="regiao", y="indice_saneamento"),
            )],
            variant="filled"
        ), 
    ],
)

page2 = vm.Page(
    title="Empoli",
    id="dados_empoli",
    layout=vm.Grid(grid=[[0, 1],[2, 3]]),
    components=[
        vm.Container(
            title="Expectativa de Vida por Região",
            components=[vm.Graph(
                figure=px.histogram(df, y="regiao", x="expectativa_vida"),
            )],
            variant="filled",
        ),
        vm.Container(
            title="IDH por Região",
            components=[vm.Graph(
                figure=px.histogram(df, y="regiao", x="idh"),
            )],
            variant="filled",
        ),
        vm.Container(
            title="Distribuição Populacional",
            components=[vm.Graph(
                figure=px.histogram(df, x="estado", y="populacao_total"),
            )],
            variant="filled",
        ),
        vm.Container(
            title="Crescimento Populacional por Região",
            components=[vm.Graph(
                figure=fig_crescimento,
            )],
            variant="filled"
        ),
    ],
    controls=[vm.Filter(column="regiao")]
)

page3 = vm.Page(
    title="Eleodora",
    id="dados_gerais",
    components=[
        vm.AgGrid(
            figure=dash_ag_grid(data_frame=df1)),
    ],
)
page4 = vm.Page(
    title="Urban AI",
    id="urbanai",
    layout=vm.Grid(grid=[[0, 1], [2, 2]]),
        components=[
            vm.Graph(
                figure=fig, title="Mapa de Distribuição Populacional"),
            vm.AgGrid(
                figure=criar_tabela_ag_grid(data_frame=df_resumo.sort_values('total_populacao', ascending=False)),
                title="Dados por Região"),
            vm.AgGrid(
                figure=criar_tabela_ag_grid(data_frame=df_detalhado),
                title="Dados por Estado")
        ],
        controls=[
            vm.Filter(column="regiao")
        ],
    )

dashboard = vm.Dashboard(pages=[page0, page1, page2, page3, page4])
Vizro().build(dashboard).run(debug=True)
