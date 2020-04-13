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
        'id':i
    }
    features.append(info)   
shpData = {
    'type':'FeatureCollection',
    'features':features
}

fig = go.Figure(
    go.Choroplethmapbox(
        geojson=shpData, 
        z=df_map.view,  # 分色資料依據
        locations=df_map.name,   # df的key
        colorscale='YlOrRd',
        featureidkey="properties.district",  # shp的key
    )
)
fig.update_layout(
    mapbox_zoom=6,
    mapbox_center={"lat": 23.5832, "lon": 120.5825},
    mapbox_style="carto-positron",
)
fig.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
)


app.layout = dcc.Graph(figure=fig)


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8052, debug=True)
