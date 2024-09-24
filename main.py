from cProfile import label
from timeit import template

import pandas as pd
from black.comments import children_contains_fmt_on
from dash import dcc, html, Input, Output
import dash
import plotly.graph_objects as go
from datetime import datetime
import plotly.express as px

def set_config(img_name):
    return {
             "displaylogo": False,
             "modeBarButtonsToRemove": [
                 "zoom",
                 "pan",
                 "zoomIn",
                 "zoomOut",
                 "resetView",
                 "autoScale",
                 "resetScale",
                 "lasso2d",
                 "select2d"
             ],
             "toImageButtonOptions": {
                 "format": "png",
                 "filename": img_name,
                 "height": 700,
                 "width": 1300,
                 "scale": 1,
             },
         }
df = pd.read_csv('data/earthquake_1995-2023.csv')
df['country'] = [val[1]  if len(val) > 1 else "Otros"  for val in df['title'].str.split(",")]
df['alert'] = df['alert'].fillna("blue")
df["date"] =  pd.to_datetime(df["date_time"], dayfirst=True).dt.date
colors = {
    "green": "#99CC99",
    "blue": "#99CCFF",
    "yellow": "#FFF2B3",
    "orange": "#FFCC99",
    "red": "#FF9999"
}
df["colors"] = [colors[c] for c in df['alert']]
group = df.groupby('country').agg({"title":"count"}).reset_index()
group['country'] = [c if t > 10 else "Otros" for c, t in zip(group['country'],group['title'])]
group = group.groupby('country').agg({"title":"sum"}).reset_index()


pie = go.Figure(data=[go.Pie(values=group['title'], labels=group['country'])])
pie.update_traces(textinfo='none', hole=.4)
pie.update_layout(
    title=dict(text='Cantidad de Terremotos por país', font=dict(size=14), x=0.5),
    legend=dict(x=1, y=0.5, traceorder="normal", orientation="v"),
    height=200,
    margin={'l': 0, 't': 22, 'b': 0, 'r': 0},
    annotations=[dict(text="Total", font_size=20, showarrow=False, xanchor="center")]
)

external_stylesheets = [
    "https://cdnjs.cloudflare.com/ajax/libs/sweetalert/1.1.3/sweetalert.min.css"
]

external_scripts = [
    "https://cdn.jsdelivr.net/npm/sweetalert2@11",
    "https://cdn.tailwindcss.com"
]

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    external_scripts=external_scripts,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title="Terremotos mundiales"
app._favicon = "favicon.ico"
app.layout = html.Div(
    className="bg-gray-100 min-h-screen p-6",
    children=[
        html.Div(
            className="flex flex-col items-center bg-white shadow-lg p-8 rounded-lg mb-8",
            children=[
                html.Div(
                    className="flex flex-col md:flex-row justify-between w-full mb-6",
                    children=[
                        html.Div(
                            className="w-full md:w-1/4 mb-6 md:mb-0",
                            children=[
                            html.H1(
                            "Terremotos Mundiales",
                            className="text-4xl font-bold mb-4 text-neutral-400"
                                ),
                                html.H2("Filtros", className="text-2xl font-semibold mb-4"),
                                html.Div(
                                    className="mb-6",
                                    children=[
                                        html.Label("Magnitud", className="block text-lg font-medium mb-2"),
                                        dcc.RangeSlider(df['magnitude'].min(), df['magnitude'].max(), 0.1,
                                            value=[df['magnitude'].min()+1, df['magnitude'].max()-1],
                                            id='magnitude_slider',
                                            marks=None,
                                            tooltip={"placement": "bottom", "always_visible": True}
                                        ),
                                    ]
                                ),
                                html.Div(
                                    className="mb-6",
                                    children=[
                                        html.Label("Tsunami", className="block text-lg font-medium mb-2"),
                                        dcc.Checklist(
                                            options=[{'label': 'Tsunami', 'value': 'Tsunami'}],
                                            value=[],
                                            id="tsunami_checkbox",
                                            className="inline-block align-middle",
                                            style={"transform": "scale(1.25)", "margin-left": "10px"}
                                        ),
                                    ]
                                ),
                                html.Div(
                                    className="mb-6",
                                    children=[
                                        html.Label("Rango de Fechas", className="block text-lg font-medium mb-2"),
                                        dcc.DatePickerRange(
                                            id='date-range',
                                            min_date_allowed=df["date"].min(),
                                            max_date_allowed=df["date"].max(),
                                            start_date=df["date"].min(),
                                            end_date=df["date"].max(),
                                            className="mt-2 w-[90%]",
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        html.Div(
                            className="w-full md:w-3/4",
                            children=[
                                html.H3("Mapa de ocurrencias de terremotos",
                                        className="font-bold text-[#D48B2E]"),
                                html.H5("Fuente de datos: EveryEarthquake API",
                                        className="text-xs pb-2"),
                                dcc.Graph(
                                    id="map",
                                    config=set_config('MapaTerremotos'),
                                    className="rounded-lg shadow-lg"
                                )
                            ]
                        )
                    ]
                )
            ]
        ),
        html.Div(
            className="flex flex-col md:flex-row justify-between w-full mb-8",
            children=[
                html.Div(
                    className="flex flex-col md:flex-row space-y-4 md:space-y-0 md:space-x-4 w-full md:w-1/2",
                    children=[
                        html.Div(
                            className="flex flex-col items-center bg-white p-4 rounded-lg shadow-lg w-full h-[120px] justify-center",
                            children=[
                                html.H1(df["magnitude"].max(), className="text-2xl font-bold text-gray-700"),
                                html.P("Magnitud máxima histórico", className="text-sm text-gray-500 text-center")
                            ]
                        ),
                        html.Div(
                            className="flex flex-col items-center bg-white p-4 rounded-lg shadow-lg w-full h-[120px] justify-center",
                            children=[
                                html.H1(f"{df['depth'].mean():.2f}", className="text-2xl font-bold text-gray-700"),
                                html.P("Profundidad promedio (Km) histórico", className="text-sm text-gray-500 text-center")
                            ]
                        ),
                        html.Div(
                            className="flex flex-col items-center bg-white p-4 rounded-lg shadow-lg w-full h-[120px] justify-center",
                            style={"margin-right": "16px"},
                            children=[
                                html.H1(df.shape[0], className="text-2xl font-bold text-gray-700"),
                                html.P("Conteo Terremotos histórico", className="text-sm text-gray-500 text-center")
                            ]
                        )
                    ]
                ),
                html.Div(
                    className="flex flex-col bg-white p-6 rounded-lg shadow-lg w-full md:w-1/2 justify-center",
                    children=[
                        dcc.Graph(
                            id="pie_total",
                            figure=pie,
                            config=set_config("TotalTerremotos"),
                            className="w-full h-full",
                            style={"height": "100%"}
                        )
                    ]
                )
            ]
        ),
        html.Div(
            className="flex flex-col space-y-6 w-full",
            children=[
                html.Div(
                    className="w-full mb-4 text-center",
                    children=[
                        html.H2("Serie temporal de magnitudes de terremotos", className="text-xl font-semibold")
                    ]
                ),
                html.Div(
                    className="w-full rounded-lg shadow-lg bg-white py-[10px]",
                    children=[
                    dcc.Graph(
                    id="magnitude-timeseries",
                    config=set_config("SerieTiempoMagnitud"),
                    className="w-full"
                ),
                    ]
                ),
                html.Div(
                    className="w-full mb-4 text-center",
                    children=[
                        html.H2("Serie temporal de profundidad de terremotos", className="text-xl font-semibold")
                    ]
                ),
                html.Div(
                    className="w-full rounded-lg shadow-lg bg-white py-[10px]",
                    children=[
                    dcc.Graph(
                    id="depth-timeseries",
                    config=set_config("SerieTiempoProfundidad"),
                    className="w-full"
                )
                    ]
                )
            ]
        )
    ]
)


@app.callback(
    Output("map","figure"),
    Output("depth-timeseries","figure"),
    Output("magnitude-timeseries","figure"),
    Input("magnitude_slider", "value"),
    Input("tsunami_checkbox", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def dashboard(slider_value,checkbox_value, start_date, end_date):

    data = map_data(slider_value[0],slider_value[1], checkbox_value, start_date, end_date)
    fig = go.Figure(go.Scattermap(
            lat=data['latitude'],
            lon=data['longitude'],
            mode='markers',
            marker=go.scattermap.Marker(
                size=(2**data['magnitude'])/10,
                color=data['colors']
            ),
            text=[val for val in data['title']],
        ))
    fig.update_layout(
        margin={'l': 0, 't': 0, 'b': 0, 'r': 10},
        showlegend=False,
        height=500
    )

    fig2 = go.Figure(
        go.Scatter(mode="markers", x=df["date"], y=df["depth"])
    )
    fig2.update_layout(
        margin={'l': 0, 't': 0, 'b': 0, 'r': 10},
        xaxis_title='Año',
        xaxis_title_font=dict(size=12),
        yaxis_title='Profundidad',
        yaxis_title_font=dict(size=12),
        xaxis=dict(range=[df["date"].min(), df["date"].max()]),
        showlegend=False,
        height=200,
        template="simple_white"
    )
    fig2.update_xaxes(rangeslider_visible=True,
                      rangeslider=dict(range=[df["date"].min(), df["date"].max()]))

    df["year"] = pd.to_datetime(df["date_time"], dayfirst=True).dt.year
    grupo_year = df.groupby(["year","magnitude"])['title'].count().reset_index()
    fig3 = px.bar(grupo_year, x="year", y="title", color="magnitude",color_continuous_scale="portland")
    fig3.update_layout(
        barmode='stack',
        margin={'l': 0, 't': 0, 'b': 0, 'r': 10},
        xaxis_title='Año',
        xaxis_title_font=dict(size=12),
        yaxis_title='Conteo',
        yaxis_title_font = dict(size=12),
        height=200,
        template="simple_white"
    )
    fig3.update_xaxes(rangeslider_visible=True)
    fig3.update_coloraxes(showscale=False)


    return fig, fig2, fig3


def map_data(slider_min,slider_max, checkbox_value, start_date, end_date):
    tsunami = 1 if checkbox_value==[] else 0
    start_date = datetime.strptime(start_date,"%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    return df[
        (df['magnitude']>= slider_min) &
        (df['magnitude']<= slider_max) &
        (df['tsunami']<= tsunami) &
        (df['date'] >= start_date) &
        (df['date'] <= end_date)
    ]

if __name__ == "__main__":
    app.run_server(debug=False)