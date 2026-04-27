import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import pickle

# Loading data
with open("crm_clean_data.pickle", "rb") as f:
    calls, contacts, spend, deals = pickle.load(f)

# Data preparation
deals['created_time'] = pd.to_datetime(deals['created_time'])
deals['is_success'] = deals['stage'].apply(lambda x: 1 if x == 'Payment Done' else 0)
deals['month'] = deals['created_time'].dt.to_period('M').astype(str)
deals['offer_total_amount'] = pd.to_numeric(deals['offer_total_amount'], errors='coerce').fillna(0)

# Get lists for filters
managers = ['All'] + sorted(deals['deal_manager'].dropna().unique().tolist())
cities = ['All'] + sorted(deals['city'].dropna().unique().tolist())
products = ['All'] + sorted(deals['product'].dropna().unique().tolist())
education = ['All'] + sorted(deals['education_type'].dropna().unique().tolist())

# Minimum and maximum dates
min_date = deals['created_time'].min().date()
max_date = deals['created_time'].max().date()




# CREATING THE APPLICATION

app = dash.Dash(__name__)

app.layout = html.Div([
    # Title
    html.H1('CRM Analytics', style={'textAlign': 'center', 'marginBottom': '20px', 'color': '#2c3e50'}),

    
    # Filters
    html.Div([
        html.Div([
            html.Label('Period:', style={'fontWeight': 'bold'}),
            dcc.DatePickerRange(
                id='date-range',
                start_date=min_date,
                end_date=max_date,
                display_format='DD.MM.YYYY',
                style={'width': '100%'}
            )
        ], style={'width': '18%', 'display': 'inline-block', 'marginRight': '2%', 'verticalAlign': 'top'}),
        
        html.Div([
            html.Label('Manager:', style={'fontWeight': 'bold'}),
            dcc.Dropdown(id='manager-filter', options=[{'label': m, 'value': m} for m in managers], value='All')
        ], style={'width': '18%', 'display': 'inline-block', 'marginRight': '2%', 'verticalAlign': 'top'}),
        
        html.Div([
            html.Label('City:', style={'fontWeight': 'bold'}),
            dcc.Dropdown(id='city-filter', options=[{'label': c, 'value': c} for c in cities], value='All')
        ], style={'width': '18%', 'display': 'inline-block', 'marginRight': '2%', 'verticalAlign': 'top'}),
        
        html.Div([
            html.Label('Product:', style={'fontWeight': 'bold'}),
            dcc.Dropdown(id='product-filter', options=[{'label': p, 'value': p} for p in products], value='All')
        ], style={'width': '18%', 'display': 'inline-block', 'marginRight': '2%', 'verticalAlign': 'top'}),
        
        html.Div([
            html.Label('Education:', style={'fontWeight': 'bold'}),
            dcc.Dropdown(id='education-filter', options=[{'label': e, 'value': e} for e in education], value='All')
        ], style={'width': '18%', 'display': 'inline-block', 'verticalAlign': 'top'})
    ], style={'padding': '15px', 'backgroundColor': '#f8f9fa', 'borderRadius': '8px', 'marginBottom': '20px'}),

    
    # 4 KPIs
    html.Div([
        html.Div(id='kpi-revenue', style={'flex': '1', 'margin': '0 5px', 'padding': '15px', 'backgroundColor': 'white', 'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'textAlign': 'center'}),
        html.Div(id='kpi-deals', style={'flex': '1', 'margin': '0 5px', 'padding': '15px', 'backgroundColor': 'white', 'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'textAlign': 'center'}),
        html.Div(id='kpi-conversion', style={'flex': '1', 'margin': '0 5px', 'padding': '15px', 'backgroundColor': 'white', 'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'textAlign': 'center'}),
        html.Div(id='kpi-aov', style={'flex': '1', 'margin': '0 5px', 'padding': '15px', 'backgroundColor': 'white', 'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'textAlign': 'center'})
    ], style={'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between', 'marginBottom': '20px'}),
    
    # 4 charts
    html.Div([
        html.Div([dcc.Graph(id='chart-calls', config={'displayModeBar': False})], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginRight': '2%'}),
        html.Div([dcc.Graph(id='chart-sources', config={'displayModeBar': False})], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
    ], style={'marginBottom': '20px'}),
    
    html.Div([
        html.Div([dcc.Graph(id='chart-managers', config={'displayModeBar': False})], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginRight': '2%'}),
        html.Div([dcc.Graph(id='chart-products', config={'displayModeBar': False})], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
    ])
    
], style={'padding': '20px', 'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#f5f5f5'})




# FUNCTION TO CREATE CALLS AND DEALS DYNAMICS CHART

def create_calls_deals_chart(df_calls, df_deals):
    """Creates a chart of calls and deals dynamics by week"""
    
    # Count number of calls per contact
    calls_cnt = df_calls.groupby('contact_id').size().reset_index(name='calls_cnt')
    
    # Join calls to deals
    deals_calls = df_deals.merge(calls_cnt, left_on='contact_name', right_on='contact_id', how='left')
    deals_calls['calls_cnt'] = deals_calls['calls_cnt'].fillna(0).astype(int)
    
    # Group by week
    weekly = deals_calls.groupby(deals_calls['created_time'].dt.to_period('W')).agg(
        total_calls=('calls_cnt', 'sum'),
        total_deals=('deals_id', 'size'),
        success_deals=('is_success', 'sum')
    ).reset_index()
    weekly['date'] = weekly['created_time'].dt.to_timestamp()
    weekly.sort_values('date', inplace=True)
    
    # Build the chart
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Left axis: all calls and all deals (with fill)
    fig.add_trace(go.Scatter(x=weekly['date'], y=weekly['total_calls'], name='All calls',
                             line=dict(color='#91ADC8', width=2), fill='tozeroy'), secondary_y=False)
    fig.add_trace(go.Scatter(x=weekly['date'], y=weekly['total_deals'], name='All deals',
                             line=dict(color='#4C8CE4', width=2), fill='tozeroy'), secondary_y=False)
    
    # Right axis: successful deals (dashed line, with fill)
    fig.add_trace(go.Scatter(x=weekly['date'], y=weekly['success_deals'], name='Successful deals',
                             line=dict(color='#53CBF3', width=2, dash='dash'), fill='tozeroy'), secondary_y=True)
    
    fig.update_xaxes(title_text='Week', tickformat='%b %y', dtick='M1')
    fig.update_yaxes(title_text='Quantity', secondary_y=False)
    fig.update_yaxes(title_text='Successful deals', secondary_y=True)
    
    fig.update_layout(
        title=dict(
            text=' Weekly dynamics of calls and deals',
            x=0.32,
            xanchor='center',
            font=dict(size=18)
        ),
        hovermode='x unified',
        plot_bgcolor='white',
        height=400,
        margin=dict(l=40, r=60, t=60, b=60),
        legend=dict(
            orientation='h',
            yanchor='top',
            y=1.1,
            xanchor='center',
            x=0.28
        )
    )
    return fig





# FUNCTION TO CREATE SOURCE EFFICIENCY CHART

def create_sources_chart(df):
    """Creates a source efficiency chart"""
    
    # Count number of leads by source
    leads_by_source = df['source'].value_counts().reset_index()
    leads_by_source.columns = ['source', 'leads']
    
    # Count number of successful deals by source
    success_by_source = df[df['is_success'] == 1]['source'].value_counts().reset_index()
    success_by_source.columns = ['source', 'success']
    
    # Merge and calculate conversion
    source_stats = leads_by_source.merge(success_by_source, on='source', how='left')
    source_stats['success'] = source_stats['success'].fillna(0)
    source_stats['conversion'] = (source_stats['success'] / source_stats['leads'] * 100).round(1)
    
    # Sort by leads and take top 10
    source_stats = source_stats.sort_values('leads', ascending=False).head(10)
    
    fig = px.scatter(source_stats, x='leads', y='conversion', size='leads', 
                     color='conversion', text='source', 
                     title='Source efficiency',
                     labels={'leads': 'Number of leads', 'conversion': 'Conversion (%)'},
                     color_continuous_scale='Blues')
    
    fig.update_layout(
        plot_bgcolor='white',
        height=400,
        margin=dict(l=40, r=40, t=50, b=40)
    )
    fig.update_traces(textposition='top center', marker=dict(sizeref=2))
    
    if len(source_stats) > 0:
        fig.add_vline(x=source_stats['leads'].mean(), line_dash="dash", line_color="gray")
        fig.add_hline(y=source_stats['conversion'].mean(), line_dash="dash", line_color="gray")
    
    return fig





# FUNCTION TO CREATE TOP MANAGERS CHART

def create_managers_chart(df):
    """Creates a top managers by revenue chart"""
    manager_revenue = df[df['is_success'] == 1].groupby('deal_manager')['offer_total_amount'].sum().reset_index()
    manager_revenue = manager_revenue.sort_values('offer_total_amount', ascending=False).head(5)
    
    fig = px.bar(manager_revenue, x='deal_manager', y='offer_total_amount', 
                 title='Top-5 managers by revenue')
    
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='Revenue')

    fig.update_traces(marker_color='#3498db')
    fig.update_layout(height=400, margin=dict(l=40, r=40, t=50, b=40), xaxis=dict(tickangle=0))
    return fig





# FUNCTION TO CREATE TOP PRODUCTS CHART

def create_products_chart(df):
    """Creates a top products by deals chart"""
    product_stats = df[df['product'].notna()].groupby('product')['deals_id'].count().reset_index()
    product_stats = product_stats[product_stats['product'] != 'Unknown'].sort_values('deals_id', ascending=False).head(8)
    
    fig = px.bar(product_stats, x='product', y='deals_id', 
                 title='Top products by deals')
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='Deals')

    fig.update_traces(marker_color='#3498db')
    fig.update_layout(height=400, margin=dict(l=40, r=40, t=50, b=40), xaxis=dict(tickangle=0))
    return fig





# CALLBACK FOR UPDATING ALL DATA

@callback(
    [Output('kpi-revenue', 'children'),
     Output('kpi-deals', 'children'),
     Output('kpi-conversion', 'children'),
     Output('kpi-aov', 'children'),
     Output('chart-calls', 'figure'),
     Output('chart-sources', 'figure'),
     Output('chart-managers', 'figure'),
     Output('chart-products', 'figure')],
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('manager-filter', 'value'),
     Input('city-filter', 'value'),
     Input('product-filter', 'value'),
     Input('education-filter', 'value')]
)
def update_dashboard(start_date, end_date, manager, city, product, education):
    
    # Filtering data
    df = deals.copy()
    df_calls = calls.copy()
    
    if start_date and end_date:
        df = df[(df['created_time'] >= start_date) & (df['created_time'] <= end_date)]
        df_calls = df_calls[(df_calls['call_start_time'] >= start_date) & (df_calls['call_start_time'] <= end_date)]
    
    if manager and manager != 'All':
        df = df[df['deal_manager'] == manager]
    
    if city and city != 'All':
        df = df[df['city'] == city]
    
    if product and product != 'All':
        df = df[df['product'] == product]
    
    if education and education != 'All':
        df = df[df['education_type'] == education]
    
    # KPIs 
    total_revenue = df[df['is_success'] == 1]['offer_total_amount'].sum()
    total_deals = len(df)
    success_deals = df['is_success'].sum()
    conversion = (success_deals / total_deals * 100) if total_deals > 0 else 0
    buyers = df[df['is_success'] == 1]['contact_name'].nunique()
    aov = total_revenue / buyers if buyers > 0 else 0
    
    kpi_style = {'fontSize': '24px', 'fontWeight': 'bold', 'color': '#2c3e50'}
    label_style = {'fontSize': '14px', 'color': '#7f8c8d', 'marginBottom': '5px'}
    
    kpi_revenue = html.Div([
        html.Div('Total revenue', style=label_style),
        html.Div(f'{total_revenue:,.0f} €', style=kpi_style)
    ])
    
    kpi_deals = html.Div([
        html.Div('Total deals', style=label_style),
        html.Div(f'{total_deals:,}', style=kpi_style)
    ])
    
    kpi_conversion = html.Div([
        html.Div('Conversion', style=label_style),
        html.Div(f'{conversion:.1f}%', style=kpi_style)
    ])
    
    kpi_aov = html.Div([
        html.Div('Average order value', style=label_style),
        html.Div(f'{aov:,.0f} €', style=kpi_style)
    ])
    
    # CHARTS
    fig_calls = create_calls_deals_chart(df_calls, df)
    fig_sources = create_sources_chart(df)
    fig_managers = create_managers_chart(df)
    fig_products = create_products_chart(df)
    
    return kpi_revenue, kpi_deals, kpi_conversion, kpi_aov, fig_calls, fig_sources, fig_managers, fig_products


if __name__ == '__main__':
    app.run(debug=True)