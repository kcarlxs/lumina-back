import pandas as pd
import vizro.plotly.express as px
from vizro import Vizro
import vizro.models as vm
from vizro.tables import dash_ag_grid

# Inicialização e leitura de dados
Vizro._reset()
df = pd.read_csv("dados_demograficos_brasil.csv", sep=";")

# Cálculos iniciais
total_masculino = df["populacao_masculina"].sum()
total_feminino = df["populacao_feminina"].sum()
df_donut = pd.DataFrame({
    "Categoria": ["População Masculina", "População Feminina"],
    "Total": [total_masculino, total_feminino]
})

# Preparação de figuras SEM títulos
fig_pie = px.pie(df_donut, values="Total", names="Categoria", hole=0.5)
fig_crescimento = px.histogram(df, x='regiao', y='crescimento_populacional')

df_melted = pd.melt(
    df,
    id_vars=["estado"],
    value_vars=["natalidade", "mortalidade"],
    var_name="tipo",
    value_name="valor"
)
fig_natal_mort = px.histogram(df_melted, x="estado", y="valor", color="tipo", barmode="group")

# Definição das páginas com títulos CORRETOS nos componentes vm.Graph
page1 = vm.Page(
    title="Dados Gerais",
    id="dados_gerais_v3",
    components=[vm.AgGrid(figure=dash_ag_grid(data_frame=df))]
)

page2 = vm.Page(
    title="Estado",
    id="estado_v3",
    layout=vm.Grid(grid=[[0, 1]]),
    components=[
        vm.Container(
            title="Distribuição Populacional",
            components=[vm.Graph(
                figure=px.histogram(df, x="estado", y="populacao_total"),
            )],
            variant="filled",
        ),
        vm.Container(
            title="PIB per Capita x Estado",
            components=[vm.Graph(
                figure=px.histogram(df, x="estado", y="pib_per_capita"),
            )],
            variant="filled",
        ),
    ],
    controls=[vm.Filter(column="estado")]
)

page3 = vm.Page(
    title="Qualidade de Vida",
    id="qualidade_vida_v3",
    layout=vm.Grid(grid=[[0, 1]]),
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
    ],
    controls=[vm.Filter(column="regiao")]
)

page4 = vm.Page(
    title="Sexualidade",
    id="sexualidade_v3",
    layout=vm.Grid(grid=[[0, 1]]),
    components=[
        vm.Container(
            title="População por Sexo",
            components=[vm.Graph(
                figure=fig_pie,
            )],
            variant="filled"
        ),
        vm.Container(
            title="Crescimento Populacional por Região",
            components=[vm.Graph(
                figure=fig_crescimento,
            )],
            variant="filled"
        ),
    ]
)

page5 = vm.Page(
    title="Natalidade vs Mortalidade",
    id="natalidade_mortalidade_v3",
    components=[vm.Graph(
        figure=fig_natal_mort,
    )]
)

page6 = vm.Page(
    title="Saúde",
    id="saude_v3",
    layout=vm.Grid(grid=[[0, 1]]),
    components=[
        vm.Container(
            title="Indice de Saniamento",
            components=[vm.Graph(
                figure=px.histogram(df, x="regiao", y="indice_saneamento"),
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
    ]
)

# Construção do dashboard
dashboard = vm.Dashboard(pages=[page1, page2, page3, page4, page5, page6])
Vizro().build(dashboard).run(debug=True)