import pandas as pd
import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go
from datetime import datetime
from Report import get_report

def load_report_data():
    """Charge et formate les données du rapport"""
    try:
        report = get_report()

        if 'Date' in report:
            report['Date'] = datetime.strptime(report['Date'], '%Y-%m-%d').strftime('%d %B %Y')

        return report

    except Exception as e:
        return {'error': f'Erreur de chargement: {str(e)}'}

app = dash.Dash(__name__)
app.title = "Dashboard Solana"

app.layout = html.Div([
    dcc.Store(id='theme-store', data={'dark': True}),

    # En-tête
    html.Div([
        html.H1("📊 Tableau de Bord SOLANA",
                style={'marginBottom': '5px', 'fontSize': '40px'}),
        html.Div(id='last-update', style={'fontSize': '16px'}),
    ], id='header', style={'textAlign': 'center', 'padding': '30px 10px'}),

    # Bouton de changement de thème
    html.Div([
        html.Button("🌓 Basculer le thème", id='theme-toggle', n_clicks=0,
                    style={'padding': '10px 20px', 'fontSize': '16px',
                           'borderRadius': '6px', 'border': 'none',
                           'cursor': 'pointer'})
    ], style={'textAlign': 'center', 'marginBottom': '20px'}),

    # Contenu principal
    html.Div([
        # Graphique
        html.Div([
            dcc.Graph(id='price-chart', config={'displayModeBar': False})
        ], id='graph-section', style={'flex': '2', 'padding': '20px'}),

        # Rapport
        html.Div([
            html.H3("📄 Rapport Quotidien",
                    style={'paddingBottom': '10px', 'fontSize': '24px'}),
            html.Div(id='report-content', style={'marginTop': '20px'})
        ], id='report-section', style={'flex': '1', 'padding': '20px'})
    ], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'center', 'gap': '20px'}),

    dcc.Interval(id='interval-update', interval=60 * 1000, n_intervals=0)
], id='main-container', style={'fontFamily': 'Arial, sans-serif', 'minHeight': '100vh'})


@app.callback(
    [Output('price-chart', 'figure'),
     Output('report-content', 'children'),
     Output('last-update', 'children'),
     Output('main-container', 'style'),
     Output('header', 'style'),
     Output('theme-toggle', 'style'),
     Output('graph-section', 'style'),
     Output('report-section', 'style')],
    [Input('interval-update', 'n_intervals'),
     Input('theme-store', 'data')]
)
def update_dashboard(n, theme_data):
    is_dark = theme_data.get('dark', True)

    # Définition du thème
    bg_color = '#121212' if is_dark else '#f5f5f5'
    text_color = 'white' if is_dark else '#222'
    card_bg = '#1e1e2f' if is_dark else '#ffffff'
    accent_color = '#00CC96'

    try:
        df = pd.read_csv("data.csv", index_col=0, parse_dates=True)
        df.index = df.index.tz_localize('UTC').tz_convert('Europe/Paris')

        fig = go.Figure(
            data=[go.Scatter(
                x=df.index,
                y=df['lastPr'],
                mode='lines+markers',
                line=dict(color=accent_color, width=2),
                marker=dict(size=6, color='#7FDBFF'),
                name='Prix (USDT)'
            )],
            layout=go.Layout(
                title="Évolution du Prix",
                xaxis_title="Heure (Paris)",
                yaxis_title="Prix (USDT)",
                paper_bgcolor=bg_color,
                plot_bgcolor=bg_color,
                font=dict(color=text_color),
                hovermode='x unified'
            )
        )
    except Exception as e:
        fig = go.Figure(layout=go.Layout(
            title="Erreur de chargement des données",
            paper_bgcolor=bg_color,
            font=dict(color='red')
        ))

    # Rapport
    report_data = load_report_data()

    if 'error' in report_data:
        report_content = html.Div([
            html.P(report_data['error'], style={'color': 'red'})
        ])
    else:
        cards = []
        for key, value in report_data.items():
            cards.append(
                html.Div([
                    html.Div(key.replace('_', ' ').title(), style={'fontWeight': 'bold'}),
                    html.Div(str(value), style={'fontSize': '22px', 'color': accent_color, 'margin': '8px 0'})
                ], style={
                    'backgroundColor': card_bg,
                    'padding': '12px 16px',
                    'borderRadius': '8px',
                    'marginBottom': '12px',
                    'boxShadow': '0 2px 6px rgba(0,0,0,0.2)'
                })
            )
        report_content = html.Div(cards)

    last_update = f"Dernière mise à jour: {pd.Timestamp.now().tz_localize('UTC').tz_convert('Europe/Paris').strftime('%d/%m/%Y %H:%M:%S')}"

    # Styles dynamiques
    container_style = {'fontFamily': 'Arial, sans-serif', 'minHeight': '100vh', 'backgroundColor': bg_color, 'color': text_color}
    header_style = {'textAlign': 'center', 'padding': '30px 10px', 'color': text_color}
    button_style = {'padding': '10px 20px', 'fontSize': '16px', 'borderRadius': '6px', 'border': 'none',
                    'cursor': 'pointer', 'backgroundColor': accent_color, 'color': 'white'}
    graph_style = {'flex': '2', 'padding': '20px', 'backgroundColor': card_bg, 'borderRadius': '10px',
                   'boxShadow': '0 4px 12px rgba(0,0,0,0.2)'}
    report_style = {'flex': '1', 'padding': '20px', 'backgroundColor': card_bg, 'borderRadius': '10px',
                    'boxShadow': '0 4px 12px rgba(0,0,0,0.2)', 'color': text_color}

    return fig, report_content, last_update, container_style, header_style, button_style, graph_style, report_style


@app.callback(
    Output('theme-store', 'data'),
    Input('theme-toggle', 'n_clicks'),
    prevent_initial_call=True
)
def toggle_theme(n_clicks):
    return {'dark': n_clicks % 2 == 0}


if __name__ == '__main__':
    app.run(debug=True, port=8050)
