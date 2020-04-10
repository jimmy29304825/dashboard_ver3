import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash_daq as daq
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import datetime

app = dash.Dash(__name__,)
site_color = {'房仲網':"#ffcf3d", '好房網':"#adfc8d",}

def get_numbers(df_yesterday):
    visits = {
        'YC': {
            'all': df_yesterday[df_yesterday['訪問網站'] == '房仲網']['訪問人次'].sum(),
            'member': df_yesterday[df_yesterday['訪問網站'] == '房仲網'][df_yesterday['是否為會員'] == '會員']['訪問人次'].sum(),
            'userid': df_yesterday[df_yesterday['訪問網站'] == '房仲網'][df_yesterday['是否為會員'] == '非會員']['訪問人次'].sum(),
            'unique': df_yesterday[df_yesterday['訪問網站'] == '房仲網'][df_yesterday['是否為會員'] == '會員']['訪問用戶'].sum(),
        }, 
        'HF': {
            'all': df_yesterday[df_yesterday['訪問網站'] == '好房網']['訪問人次'].sum(),     
            'member': df_yesterday[df_yesterday['訪問網站'] == '好房網'][df_yesterday['是否為會員'] == '會員']['訪問人次'].sum(),
            'userid': df_yesterday[df_yesterday['訪問網站'] == '好房網'][df_yesterday['是否為會員'] == '非會員']['訪問人次'].sum(),
            'unique': df_yesterday[df_yesterday['訪問網站'] == '好房網'][df_yesterday['是否為會員'] == '會員']['訪問用戶'].sum(),
        }
    }
    yc_sum = "{:,}".format(visits['YC']['all'])
    yc_member = "{:,}".format(visits['YC']['member'])
    yc_userid = "{:,}".format(visits['YC']['userid'])
    hf_sum = "{:,}".format(visits['HF']['all'])
    hf_member = "{:,}".format(visits['HF']['member'])
    hf_userid = "{:,}".format(visits['HF']['userid'])
    return yc_sum, yc_member, yc_userid, hf_sum, hf_member, hf_userid


def draw_fig_time(site, df_yesterday):
    # YC time plot
    df_yesterday_time = df_yesterday[df_yesterday['訪問網站'] == site].groupby('使用裝置').sum()
    df_yesterday_time = df_yesterday_time.iloc[:, [i for i in range(2, 26)]].reset_index()
    df_yesterday_time = df_yesterday_time.melt(id_vars=["使用裝置"], var_name="時段", value_name="訪問人次")
    fig_time = px.bar(df_yesterday_time, x="時段", y="訪問人次", color='使用裝置', barmode='group')
    fig_time.update_layout(
#         font_size=18, 
        font_family='Microsoft JhengHei', 
        font_color='white',
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        
#         legend=dict(x=0, y=1.1, bgcolor='rgba(255,255,255,0)', bordercolor='rgba(255,255,255,0)', orientation='h'),
    )
    return fig_time


def draw_fig_referer(df_yesterday):
    # sunburst for referer
    df_yesterday_referer = df_yesterday.iloc[:, [1,4,5]].groupby(['訪問網站', '訪問來源']).sum().reset_index()
    fig_referer = px.sunburst(df_yesterday_referer, 
                      path=['訪問網站', '訪問來源'],  # 分類變數
                      values='訪問人次',  # 面積依據資料
                      color='訪問網站',  # 分色變數
#                       hover_data=['訪問網站'],  # 游標顯示資料
                     )
    fig_referer.update_traces(
        marker=dict(
#             colors=themeColor,
            line=dict(color='#ffffff', width=2)
        )
    )
    fig_referer.update_layout(
#         margin=dict(l=10, r=10, t=10, b=10),  # 圖形在畫布的邊界設定
        paper_bgcolor="rgba(0,0,0,0)",   # 畫布背景顏色
        plot_bgcolor="rgba(0,0,0,0)",  # 圖形背景顏色
        autosize=True,  # 自動調整大小
        font_color='white',  # 文字顏色
#         font_size=20,  # 文字大小
        font_family='Microsoft JhengHei',  # 字體
    )
    return fig_referer


def draw_fig_ad(df_yesterday):
    # sunburst for ad click
    df_yesterday_ad = df_yesterday.iloc[:, [1, -2,-1]].groupby('訪問網站').sum().reset_index().melt(id_vars=["訪問網站"], 
                                                          var_name="行為", 
                                                          value_name="人次")
    fig_ad = px.sunburst(df_yesterday_ad, 
                      path=['訪問網站', '行為'],  # 分類變數
                      values='人次',  # 面積依據資料
                      color='訪問網站',  # 分色變數
#                       hover_data=['訪問網站'],  # 游標顯示資料
                     )
    fig_ad.update_traces(
        marker=dict(
#             colors=themeColor, 
            line=dict(color='#ffffff', width=2)
        )
    )
    fig_ad.update_layout(
#         margin=dict(l=10, r=10, t=10, b=10),  # 圖形在畫布的邊界設定
        paper_bgcolor="rgba(0,0,0,0)",   # 畫布背景顏色
        plot_bgcolor="rgba(0,0,0,0)",  # 圖形背景顏色
        autosize=True,  # 自動調整大小
        font_color='white',  # 文字顏色
#         font_size=20,  # 文字大小
        font_family='Microsoft JhengHei',  # 字體
    )
    return fig_ad


def draw_fig_function(site, df_yesterday):
    # barplot for function
    df_yesterday_function = df_yesterday[df_yesterday['訪問網站'] == site].iloc[:, [1,2,33,35,37,38,40,41]].groupby(['訪問網站', '使用裝置']).sum().reset_index()
    df_yesterday_function = df_yesterday_function.melt(id_vars=['訪問網站', '使用裝置'], var_name="功能", value_name="人次")
    df_yesterday_function = df_yesterday_function.sort_values(by=['人次','訪問網站', '使用裝置', '功能'], ascending=True).reset_index(drop=True)

    fig_function = go.Figure()
    fig_function.add_trace(go.Bar(
        y=df_yesterday_function['功能'].unique(),
        x=df_yesterday_function[df_yesterday_function['使用裝置'] == 'Web版']['人次'],
        name='Web版',
        orientation='h',
        marker=dict(
            color="#00cc96",
            line=dict(color='white', width=1)
        )
    ))
    fig_function.add_trace(go.Bar(
        y=df_yesterday_function['功能'].unique(),
        x=df_yesterday_function[df_yesterday_function['使用裝置'] == '手機M版']['人次'],
        name='手機M版',
        orientation='h',
        marker=dict(
            color="#ef553b",
            line=dict(color='white', width=1)
        )
    ))
    fig_function.add_trace(go.Bar(
        y=df_yesterday_function['功能'].unique(),
        x=df_yesterday_function[df_yesterday_function['使用裝置'] == 'App']['人次'],
        name='App',
        orientation='h',
        marker=dict(
            color="#636dfa",
            line=dict(color='white', width=1)
        )
    ))
    fig_function.update_layout(
        barmode='stack', 
#         height=700, 
#         legend=dict(x=0, y=0, bgcolor='rgba(255,255,255,0)', bordercolor='rgba(255,255,255,0)', orientation='h'), 
#         font_size=18, 
        font_color='white', 
        font_family='Microsoft JhengHei',
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig_function


def draw_fig_timeSeries(site, df_timeSeries):
    df_timeSeries = df_timeSeries[df_timeSeries['訪問網站'] == site].groupby(['訪問日期', '使用裝置']).sum().reset_index().iloc[:, [0,1,2]]
    df_timeSeries_app = df_timeSeries[df_timeSeries['使用裝置'] == 'App']
    df_timeSeries_MobilePhone = df_timeSeries[df_timeSeries['使用裝置'] == '手機M版']
    df_timeSeries_Desktop = df_timeSeries[df_timeSeries['使用裝置'] == 'Web版']
    fig_timeSeries = go.Figure()
    fig_timeSeries.add_trace(
        go.Scatter(
            x=df_timeSeries_app['訪問日期'], 
            y=df_timeSeries_app['訪問人次'],
            mode='lines+markers',
            name='App'
        )
    )
    fig_timeSeries.add_trace(
        go.Scatter(
            x=df_timeSeries_MobilePhone['訪問日期'], 
            y=df_timeSeries_MobilePhone['訪問人次'],
            mode='lines+markers',
            name='手機M版'
        )
    )
    fig_timeSeries.add_trace(
        go.Scatter(
            x=df_timeSeries_Desktop['訪問日期'], 
            y=df_timeSeries_Desktop['訪問人次'],
            mode='lines+markers',
            name='Web版',           
        )
    )
    fig_timeSeries.update_layout(
        title={
            'text':'%s瀏覽量趨勢圖' % site,
#             'xanchor':'left',
#             'yanchor':'top',
            'font':{
                'color':site_color[site],
                'family':'Microsoft JhengHei',
            },
        },        
#         font_size=12, 
        height=340,
        font_family='Microsoft JhengHei', 
        font_color='white', 
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(x=0.6, y=1.2, bgcolor='rgba(255,255,255,0)', bordercolor='rgba(255,255,255,0)', orientation='h'),
    )
    return fig_timeSeries


# local資料使用    
df = pd.read_csv('./matomo_new.csv')  # 讀取資料
df['訪問日期'] = pd.to_datetime(df['訪問日期'])  # 轉換日期格式

maxdate = datetime.datetime.fromtimestamp(datetime.datetime.timestamp(df['訪問日期'].max()))
mindate = datetime.datetime.fromtimestamp(datetime.datetime.timestamp(df['訪問日期'].min()))

cards_yc_content = [
    dbc.CardImg(src=app.get_asset_url('YC2.jpg')),
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(html.H3("總流量"), xl=5),
                    dbc.Col(html.H3(id='yc_total', children='999,999,999'), xl=7)
                ],
            ),
            dbc.Row(
                [
                    dbc.Col(html.H4("會員流量"), xl=5),
                    dbc.Col(html.H4(id='yc_member', children='999,999,999'), xl=7),
                ],
            ),
             dbc.Row(
                [
                    dbc.Col(html.H4("非會員流量"), xl=5),
                    dbc.Col(html.H4(id='yc_userid', children='999,999,999'), xl=7),
                ]
            ),
        ]
    ),
]

cards_hf_content = [
    dbc.CardImg(src=app.get_asset_url('HF2.jpg')),
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(html.H3("總流量"), xl=5),
                    dbc.Col(html.H3(id='hf_total', children='999,999,999'), xl=7),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(html.H4("會員流量"), xl=5),
                    dbc.Col(html.H4(id='hf_member', children='999,999,999'), xl=7),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(html.H4("非會員流量"), xl=5),
                    dbc.Col(html.H4(id='hf_userid', children='999,999,999'), xl=7),
                ]
            ),
        ]
    ),
]

days_select = dcc.RadioItems(
    id='days_picker',
    options=[
        {
            'label': '過去30天', 
            'value': '30'
        },
        {
            'label': '過去一年', 
            'value': '365'
        },
    ],
    value='30',
)

cards = html.Div(
    [
#         dbc.Row(
#             dbc.Col(days_select,align='end', style={'text-align':'right'}, xl=10),
#         ),
        dbc.Row(
            [
                dbc.Col(dbc.Card(cards_yc_content, color="warning", inverse=True), xl=3, style={'height':'300px'}),
                dbc.Col(dcc.Graph(id="time_series_graph_yc",className='graph',), xl=9, style={'height':'300px', 'vertical-align': 'top'}),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Card(cards_hf_content, color="success", inverse=True), xl=3, style={'height':'300px'}),
                dbc.Col(dcc.Graph(id="time_series_graph_hf",className='graph',), xl=9, style={'height':'300px', 'vertical-align': 'top'}),
            ],
            className="mb-4",
        ),
    ]
)


date_form = dbc.FormGroup(
    [
        dbc.Label("請選擇日期："),
        dcc.DatePickerSingle(
            id='time_range',
            min_date_allowed=mindate,
            max_date_allowed=maxdate,
            initial_visible_month=maxdate,
            date=str(maxdate.date()),
            style=dict(bgcolor='blue')
        ),
        dbc.Col(days_select,align='end', style={'text-align':'right'}, xl=4),
    ],
)

graph = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="graph1",className='graph',), xl=4),
                dbc.Col(dcc.Graph(id="graph3",className='graph',), xl=4),
                dbc.Col(dcc.Graph(id="function_yc_graph",className='graph',), xl=4),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="graph2",className='graph',), xl=4),
                dbc.Col(dcc.Graph(id="graph4",className='graph',), xl=4),
                dbc.Col(dcc.Graph(id="function_hf_graph",className='graph',), xl=4),
            ],
            className="mb-4",
        ),
    ]
)

app.layout = html.Div(
    id='layout',
    children=[
        html.H1(id="header", children='''Matomo 線上用戶行為儀表板''', ),
        dbc.Form(date_form, ),
        cards,
        graph,
    ],
    className="dashboard",    
)

# 指定日期數據呈現
@app.callback(
    [
        dash.dependencies.Output('yc_total', 'children'),
        dash.dependencies.Output('yc_member', 'children'),
        dash.dependencies.Output('yc_userid', 'children'),
        
        dash.dependencies.Output('hf_total', 'children'),
        dash.dependencies.Output('hf_member', 'children'),
        dash.dependencies.Output('hf_userid', 'children'),
        
        dash.dependencies.Output('graph1', 'figure'),
        dash.dependencies.Output('graph2', 'figure'),
        dash.dependencies.Output('graph3', 'figure'),
        dash.dependencies.Output('graph4', 'figure'),
        
        dash.dependencies.Output('function_yc_graph', 'figure'),
        dash.dependencies.Output('function_hf_graph', 'figure'),
    ],
    [dash.dependencies.Input('time_range', 'date')]
)
def select_date(date):
    df_yesterday = df.query("訪問日期 == '%s'" % pd.Timestamp(date))
    yc_sum, yc_member, yc_userid, hf_sum, hf_member, hf_userid = get_numbers(df_yesterday)
    graph1 = draw_fig_time('房仲網',df_yesterday)
    graph2 = draw_fig_time('好房網',df_yesterday)
    graph3 = draw_fig_referer(df_yesterday)
    graph4 = draw_fig_ad(df_yesterday)
    function_yc_graph = draw_fig_function('房仲網',df_yesterday)
    function_hf_graph = draw_fig_function('好房網',df_yesterday)
    return yc_sum, yc_member, yc_userid, hf_sum, hf_member, hf_userid, graph1, graph2, graph3, graph4, function_yc_graph, function_hf_graph


# 趨勢圖資料
@app.callback(
    [
        dash.dependencies.Output('time_series_graph_yc', 'figure'),
        dash.dependencies.Output('time_series_graph_hf', 'figure'),
    ],
    [
        dash.dependencies.Input('time_range', 'date'),
        dash.dependencies.Input('days_picker', 'value'),
    ]
)
def select_date_and_days(date, days):
    date_max = pd.Timestamp(date)
    date_min = pd.Timestamp(date) - datetime.timedelta(days=int(days))
    df_timeSeries = df.query("訪問日期 <= '%s' and 訪問日期 >= '%s'" % (date_max, date_min))
    
    fig_timeSeries_HF = draw_fig_timeSeries('好房網', df_timeSeries)
    fig_timeSeries_YC = draw_fig_timeSeries('房仲網', df_timeSeries)
   
    return fig_timeSeries_YC, fig_timeSeries_HF

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8051, debug=True)