import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

def create_histogram(data, col, name, x_title, color, row, col_num, fig, ylog=False):
    fig.add_trace(go.Histogram(x=data[col], name=name, marker=dict(color=color)), row=row, col=col_num)
    fig.update_xaxes(title_text=x_title, row=row, col=col_num)
    if ylog:
        fig.update_yaxes(type="log", row=row, col=col_num)
    return fig

def create_subplots(data_list, cols, names, x_titles, colors, rows, cols_nums, ylogs, filename):
    fig = make_subplots(rows=2, cols=2, vertical_spacing = 0.25)
    for data, col, name, x_title, color, row, col_num, ylog in zip(data_list, cols, names, x_titles, colors, rows, cols_nums, ylogs):
        fig = create_histogram(data, col, name, x_title, color, row, col_num, fig, ylog)
    fig.update_layout(font_color='black', font_family='Latin Modern Math', template='plotly_white', font_size=9,)
    fig.show()
    fig.write_image(filename, scale=2)

def supply_tracer(fig, df, x_col, y_col, types, label_prefix, row, col, color_map):
    for t in types:
        fig.add_trace(go.Scatter(
            x=df[df['fuel'] == t][x_col],
            y=df[df['fuel'] == t][y_col],
            mode='lines',
            name=f'{label_prefix} {t}',
            line=dict(color=color_map[t]),
        ), row=row, col=col)
    return fig

