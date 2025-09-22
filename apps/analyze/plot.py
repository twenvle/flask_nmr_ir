import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from flask import current_app


def nmr(user_texts, selected_type, magnification, space, height=500, width=1000):
    if selected_type == "h_nmr":
        left = 15
        right = 0
    elif selected_type == "c_nmr":
        left = 220
        right = 0
    elif selected_type == "f_nmr":
        left = 200
        right = -200

    data_list = []
    for user_text in user_texts:
        file_path = Path(current_app.config["UPLOAD_FOLDER"], user_text.text_path)
        n = len(data_list)
        df = pd.read_csv(file_path, delimiter="\t")

        x = df[df.columns[0]]
        y = df[df.columns[1]]

        maxi_y = y.max()

        y = y * magnification[n] / maxi_y

        if n != 0:
            y = y + n * space[n - 1]

        layout = {
            "height": height,
            "width": width,
            "xaxis": {
                "range": [left, right],
                "showline": True,
                "linecolor": "black",
                "ticks": "inside",
                "title": "Chemical shift [ppm]",
            },
            "yaxis": {"showticklabels": False},
            "plot_bgcolor": "white",
        }

        data = go.Scatter(x=x, y=y, name="", showlegend=False, line={"color": "black"})
        data_list.append(data)

    fig = go.Figure(data=data_list, layout=go.Layout(layout))

    fig.update_layout(
        {
            "xaxis": {
                "title": {"font": {"size": 30, "family": "Arial"}},
                "tickfont": {"size": 24, "family": "Arial"},
            },
            "font": {"color": "black"},
        }
    )

    return fig.to_html(full_html=False)


def ir(user_texts, magnification, space, height=500, width=1000):
    data_list = []
    for user_text in user_texts:
        file_path = Path(current_app.config["UPLOAD_FOLDER"], user_text.text_path)
        n = len(data_list)
        df = pd.read_csv(
            file_path,
            header=73,
            skipfooter=39,
            delimiter="\t",
            engine="python",
        )
        # skipfooter=3979

        x = df[df.columns[0]]
        y = df[df.columns[1]]

        Y = 100 - y
        y_max = Y.max()
        Y = Y / y_max
        Y = Y * magnification[n]
        y = 1 - Y

        if n != 0:
            y = y + n * space[n]

        layout = {
            "height": height,
            "width": width,
            "xaxis": {
                "range": [4000, 400],
                "showline": True,
                "linecolor": "black",
                "ticks": "inside",
                "title": "wavenumber [cm<sup>-1</sup>]",
            },
            "yaxis": {"showticklabels": False},
            "plot_bgcolor": "white",
        }

        data = go.Scatter(x=x, y=y, name="", showlegend=False, line={"color": "black"})
        data_list.append(data)
    fig = go.Figure(data=data_list, layout=go.Layout(layout))

    fig.update_layout(
        {
            "xaxis": {
                "title": {"font": {"size": 30, "family": "Arial"}},
                "tickfont": {"size": 24, "family": "Arial"},
            },
            "font": {"color": "black"},
        }
    )

    return fig.to_html(full_html=False)
