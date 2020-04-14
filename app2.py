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
import shapefile
import datetime

app = dash.Dash(__name__,)

shape = shapefile.Reader('./shape/TOWN_MOI_1090324.shp')
df_map = pd.read_csv("./mapData.csv", dtype={'view':'str'})
df_map = df_map.query("county in ('新北市', '臺北市')")
name = shape.records()
data = shape.shapeRecords()

features = []
shpData = {}
for i in range(len(name)):
    info = {
        'type':'Feature', 
        'geometry':data[i].shape.__geo_interface__,
        'properties':{
            'district':name[i][2] + name[i][3],
        },
        'id':name[i][2] + name[i][3]
    }
    features.append(info)   
shpData = {
    'type':'FeatureCollection',
    'features':features
}


app.layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    dcc.RadioItems(
                        id='site_picker',
                        options=[
                            {
                                'label': '房仲網', 
                                'value': '房仲網'
                            },
                            {
                                'label': '好房網', 
                                'value': '好房網'
                            },
                        ],
                        value='房仲網',
                    )
                ),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="mapplot")),
            ],
        ),
    ]
)


# 趨勢圖資料
@app.callback(
    [
        dash.dependencies.Output('mapplot', 'figure'),
    ],
    [
        dash.dependencies.Input('site_picker', 'value'),
    ]
)
def area_view(site):
    df_map_site = df_map[df_map['site'] == site]
    fig = go.Figure(
        go.Choroplethmapbox(
            geojson=shpData, 
            z=df_map_site.view,  # 分色資料依據
            locations=df_map_site.name,   # df的key
            colorscale='YlOrRd',
            marker=dict(opacity=0.8),
            colorbar=dict(thickness=20),
        )
    )
    fig.update_layout(
        mapbox_zoom=8.5,
        mapbox_center={"lat": 25.0093, "lon": 121.6186},
        mapbox_style="open-street-map",
    )
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        height=600,
    )

    return fig

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8052, debug=True)



