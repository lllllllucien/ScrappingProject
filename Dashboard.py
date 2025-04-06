from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.graph_objs as go
import h5py
import numpy as np

# Fonction pour charger les données depuis le fichier .h5
def load_h5():
    with h5py.File('latest_scrap.h5', 'r') as h5f:
        data = np.array(h5f['data'])
        columns = np.array(h5f['columns'], dtype='str')

    # Convertir en DataFrame
    df = pd.DataFrame(data, columns=columns)
    df['timestamp'] = df['timestamp'].apply(lambda x: x.decode('utf-8'))
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    return df



app = Dash(__name__)

# Layout
app.layout = html.Div(style={'backgroundColor': '#111'}, children=[
    html.H1("Cryptocurrency Price", style={'color': '#7FDBFF', 'textAlign': 'center'}),
    dcc.Graph(id='price-chart'),
    dcc.Interval(id='interval-update', interval=60*1000, n_intervals=0)
])

# Callback
@app.callback(
    Output('price-chart', 'figure'),
    Input('interval-update', 'n_intervals')
)
def update_graph(n):
    df = pd.read_csv("data.csv", index_col=0, parse_dates=True)
    
    # Convertir le timestamp UTC en heure locale Paris
    df.index = df.index.tz_localize('UTC').tz_convert('Europe/Paris')

    fig = go.Figure(data=[
        go.Scatter(
            x=df.index,
            y=df['lastPr'],
            mode='lines',
            line=dict(color='#00CC96'),
            name='Price (USDT)'
        )
    ])

    fig.update_layout(
        title="Live Price Over Time",
        xaxis_title="Time (Europe/Paris)",
        yaxis_title="Price (USDT)",
        paper_bgcolor='#111',
        plot_bgcolor='#111',
        font=dict(color='white')
    )

    return fig

# Démarrer le serveur
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
    pass
