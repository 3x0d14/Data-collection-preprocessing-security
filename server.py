import pandas as pd
import numpy as np
from bokeh.models import ColumnDataSource,Select, Slider
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.layouts import column, row
from sklearn import preprocessing

##to run : >bokeh serve --show [app_name].py

THRESH = 0.25

'''
The following function will help us better visualize our data. 
While fixing our threshold to 0.25, 
if the compound of the analysis is bellow it will be considered a negative feeling and therefore will be coloured in red, 
as for the compound that surpasses the threshold it will be coloured in green.'''
def rg(x):
    global THRESH
    if x >= THRESH:
        return "#00ff00"
    else:
        return "#ff0000"

#data loading 
df = pd.read_csv("BTCSENPRICE_1643467845.csv")


#normalizing df for further operations
gloc = df.iloc[:,2:].values #returns a numpy array
min_max_scaler = preprocessing.MinMaxScaler()
g_scaled = min_max_scaler.fit_transform(gloc)
normalized_df = pd.DataFrame(g_scaled,columns=df.columns[2:])
normalized_df= pd.concat([df.iloc[:,:2], normalized_df], axis=1)


# data source for figure
x=np.arange( 77 )
source = ColumnDataSource(data=dict(x=x,top=df["compound"],y=normalized_df['low'],color=tuple(map(rg,df["compound"]))))#,y2=normalized_df['high'],y3=normalized_df['open'],y4=normalized_df['close'],color=tuple(map(rg,df["compound"]))))


# figure
TITLE = "BITCOIN sentiment analysis"
TOOLS = "hover,pan,wheel_zoom,box_zoom,reset,save"

p1 = figure(tools= TOOLS, toolbar_location="above",  title=TITLE, 
              x_range=[-5,79])
p1.toolbar.logo = "grey"
p1.background_fill_color = "#f4e9e3"
p1.xaxis.axis_label = "Days"
p1.yaxis.axis_label = "Positivity thermometer"
p1.grid.grid_line_color = "white"

p1.hover.tooltips = [
    ("Day", "$index"),
    ("Compound","$y")
]


    #plots of compound and prices (prices: low,high,open,close)
p1.vbar(x="x", top="top", color='color',source=source,width=0.5)
p1.line('x','y', line_color='blue',line_width=1,source=source)


# controllers
datestart = Select(title="Starting date of the analysis", options=list(df["date"].astype(str).values))
dateend = Select(title="Ending date of the analysis",options=list(df["date"].astype(str).values))
thre = Slider(title="Compound threshold for positive", value=0.25, start=0, end=1, step=0.05)
selectplot =Select(title="Select which plot to show",options=['low','high','open','close'],value="low")

controls = [thre,datestart,dateend,selectplot]


# function that allows to update data upon changes
def update_data(attrname, old, new):
    global THRESH
    THRESH = thre.value
    ds = datestart.value 
    de = dateend.value

    if not ds:
        ds = str(df["date"].iloc[0])
    if not de:
        de = str(df["date"].iloc[-1])    
    up_g = df[df["date"] >= ds].copy()
    up_g = up_g[up_g["date"] <= de].copy()

    up_g2 = normalized_df[normalized_df["date"] >= ds].copy()
    up_g2 = up_g2[up_g2["date"] <= de].copy()
    x = range(up_g.shape[0])
    source.data = dict(x=x,top=up_g["compound"] ,y=up_g2[selectplot.value],color=tuple(map(rg,up_g["compound"])))#,y2=up_g2['high'],y3=up_g2['open'],y4=up_g2['close'] ,color=tuple(map(rg,up_g["compound"])))

# plots update
for w in controls:
    w.on_change('value',update_data)

inputs1 = column(*controls, width=500)

curdoc().add_root(row(inputs1, p1, width=800))
curdoc().title = "Controllers"
