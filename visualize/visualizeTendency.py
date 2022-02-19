from typing import List, Any, Dict
import pandas as pd
import plotly.express as px

def __displayGraph(data: pd.DataFrame):
    """
    Display the graph data of the tendency

    :param data: Datafram of the data to be displayed
    """

    # data = pd.DataFrame({
    #     "x": [i for i in range(5000)],
    #     "y": [i*i/2-i/3 for i in range(5000)]
    # })

    from pprint import pprint

    pprint(data)

    fig = px.line(data, x="x", y="y", title="Tendency of Crypto over time")
    fig.write_html("./dataDump/graph.html")
    #fig.show()

def __preprocessData(data: List[List[Any]]):
    """
    Preprocess the data from the rows into usable data by grabbing the median of
    every transaction in the same timestamp

    :param data: a list of the rows to be preprocessed
    """

    data = sorted(data, key=lambda x: x[3])
    data.append([-1, -1, -1, -1])
    x = []
    y = []

    sum_timestamp = 0
    n_timestamp = 0

    for i in range(1, len(data)):
        cur_row = data[i]
        prev_row = data[i-1]

        sum_timestamp += prev_row[1]
        n_timestamp += 1

        if cur_row[3] == prev_row[3]:
            continue

        avg_timestamp = sum_timestamp/n_timestamp
        y.append(avg_timestamp)
        x.append(prev_row[3])

        sum_timestamp = 0
        n_timestamp = 0

    return {"x": x, "y": y}

def visualizeTendency(data: List[List[Any]]):
    """
    Visualize the full data provided as a line chart

    :param data: List of the rows to be visualized
    """

    __displayGraph(pd.DataFrame(__preprocessData(data)))
