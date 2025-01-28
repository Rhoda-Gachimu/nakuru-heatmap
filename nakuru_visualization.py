import streamlit as st
import pandas as pd
import numpy as np  
import datashader as ds
import datashader.transfer_functions as tf
import holoviews as hv
import colorcet
# from holoviews.element.tiles import EsriImagery
# from holoviews.operation.datashader import datashade
# hv.extension('bokeh')

st.title("Distribution of Nakuru MBS")
mb = pd.read_csv(r"DATA/Nakuru_mbs.csv", low_memory=False, usecols=['X_3857', 'Y_3857'])
st.write(mb.head())

# map_tiles  = EsriImagery().opts(alpha=0.5, width=900, height=480, bgcolor='black')
# points = hv.Points(mb, ['X_3857', 'Y_3857'])
# mb = datashade(points, x_sampling=1, y_sampling=1, cmap=colorcet.fire, width=900, height=480)
# map_tiles * mb

canvas = ds.Canvas(plot_width=800, plot_height=400)

# Create the aggregation
agg = canvas.points(mb, 'X_3857', 'Y_3857')
ds.tf.set_background(ds.tf.shade(agg, cmap=colorcet.fire), "black")

# Create the image
img = tf.shade(agg, cmap=colorcet.fire, how='log')

# Convert the image to an array and normalize to [0, 255]
rgb_data = img.to_numpy()
rgb_data = (rgb_data - rgb_data.min()) / (rgb_data.max() - rgb_data.min())
rgb_data = (rgb_data * 235).astype(np.uint8) 

# Display using Streamlit
st.image(rgb_data, caption='MB Distribution Heat Map', use_container_width=True)

# Update the image generation to clamp values
img = tf.shade(agg, cmap=colorcet.fire, how='log')

# Adjust the color mapping
img = tf.shade(agg, cmap=colorcet.fire, how='log')

# Add more detailed visualization with category colors
if 'category' in mb.columns:
    categorical_agg = canvas.points(mb, 'Y_3857', 'X_3857', 
                                  agg=ds.count_cat('category'))
    img_categorical = tf.shade(categorical_agg, color_key=dict(zip(
        mb['category'].unique(), 
        colorcet.palette['rainbow'][:len(mb['category'].unique())]
    )))
    st.image(tf.Image(img_categorical).rgb().values, 
             caption='MB Distribution by Category',
             use_column_width=True)
    
# Add zoom level control
zoom_level = st.slider('Zoom Level', 100, 1000, 400)
canvas = ds.Canvas(plot_width=zoom_level, plot_height=int(zoom_level/2))

# Add opacity-control
opacity = st.slider('Opacity', 0.0, 1.0, 0.8)
img = tf.shade(agg, cmap=colorcet.fire, how='log', alpha=opacity)