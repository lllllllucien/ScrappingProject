import json
import pandas as pd
import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.graph_objs as go
from datetime import datetime
from Report import get_report

def load_report_data():
    """Charge et formate les données du rapport"""
    try:
        report = get_report()
            
        # Formatage des dates si nécessaire
        if 'Date' in report:
            report['Date'] = datetime.strptime(report['Date'], '%Y-%m-%d').strftime('%d %B %Y')
                
        return report
        
    except Exception as e:
        return {'error': f'Erreur de chargement: {str(e)}'}

app = dash.Dash(__name__)

app.layout = html.Div([
    # Header
    html.Div([
        html.H1("Tableau de Bord SOLANA", 
                style={'color': '#00CC96', 'marginBottom': '10px'}),
        html.Div(id='last-update', 
                style={'color': '#7FDBFF'})
    ], style={'textAlign': 'center', 'padding': '20px'}),
    
    # Main Content
    html.Div([
        # Graph Section
        html.Div([
            dcc.Graph(id='price-chart')
        ], style={'width': '70%', 'display': 'inline-block'}),
        
        # Report Section
        html.Div([
            html.H3("Rapport Quotidien", 
                   style={'color': '#00CC96', 'borderBottom': '1px solid #00CC96', 
                          'paddingBottom': '10px'}),
            html.Div(id='report-content',
                    style={'marginTop': '20px'})
        ], style={'width': '28%', 'display': 'inline-block', 'verticalAlign': 'top',
                 'padding': '15px', 'backgroundColor': '#222', 'borderRadius': '8px',
                 'marginLeft': '2%'})
    ], style={'padding': '20px'}),
    
    dcc.Interval(id='interval-update', interval=60*1000, n_intervals=0)
], style={'backgroundColor': '#111', 'minHeight': '100vh'})

@app.callback(
    [Output('price-chart', 'figure'),
     Output('report-content', 'children'),
     Output('last-update', 'children')],
    Input('interval-update', 'n_intervals')
)
def update_dashboard(n):
    # Update price chart
    try:
        df = pd.read_csv("data.csv", index_col=0, parse_dates=True)
        df.index = df.index.tz_localize('UTC').tz_convert('Europe/Paris')
        
        fig = go.Figure(
            data=[go.Scatter(
                x=df.index,
                y=df['lastPr'],
                mode='lines+markers',
                line=dict(color='#00CC96', width=2),
                marker=dict(size=6, color='#7FDBFF'),
                name='Prix (USDT)'
            )],
            layout=go.Layout(
                title="Evolution du Prix",
                xaxis_title="Heure (Paris)",
                yaxis_title="Prix (USDT)",
                paper_bgcolor='#111',
                plot_bgcolor='#111',
                font=dict(color='white'),
                hovermode='x unified'
            )
        )

    except Exception as e:
        fig = go.Figure(layout=go.Layout(
            title="Erreur de chargement des données",
            paper_bgcolor='#111',
            font=dict(color='red')
        ))
    
    # Load and format report
    report_data = load_report_data()
    
    if 'error' in report_data:
        report_content = html.Div([
            html.P(report_data['error'], style={'color': 'red'})
        ])
    else:
        # Create report cards for each metric
        cards = []
        for key, value in report_data.items():
            cards.append(
                html.Div([
                    html.Div(key.replace('_', ' ').title()),
                    html.Div(str(value), 
                            style={'fontSize': '18px', 'color': '#00CC96',
                                  'margin': '10px 0'})
                ], style={'marginBottom': '15px', 'borderBottom': '1px solid #333',
                         'paddingBottom': '10px'})
            )
        
        report_content = html.Div(cards)
    
    # Last update timestamp
    last_update = f"Dernière mise à jour: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
    
    return fig, report_content, last_update

if __name__ == '__main__':
    app.run(debug=True, port=8050)