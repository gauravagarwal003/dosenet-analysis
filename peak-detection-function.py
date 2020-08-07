import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy.signal import find_peaks

def within(num, num2):
    if abs(num2 - num) <= 100:
        return True
    else:
        return False
    
def peak_detection(file_name):
    
    index_of_indices = []
    indices_final = []
    
    cpm_data = pd.read_csv(file_name)
    cpm_array = cpm_data['cpm'].to_numpy()
    indices = find_peaks(cpm_data['cpm'], height = cpm_data['cpm'].mean() + cpm_data['cpm'].std() * 3.5)[0]
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x = cpm_data['deviceTime_local'], y = cpm_data['cpm'], name = file_name))
    fig2.update_layout(xaxis_title = "deviceTime_local", yaxis_title = "CPM", legend_title = "Legend")

    indices = [x + cpm_data['cpm'].index[0] for x in indices]
    for i in indices:
        indices_final.append(cpm_data['deviceTime_local'][i])

    fig2.add_trace(go.Scatter(
        x=indices_final,
        y=cpm_array[indices],
        mode='markers',
        marker=dict(
            size=8,
            color='red',
            symbol='cross'
        ),
        name='Detected Peaks'
    ))

    title = file_name + " (CPM peaks)"
    fig2.update_layout(
        title={
            'text': title
        }
    )
    timer = 0
    count = 0
    counter = 1
    for i in indices:
        while within(indices[count], indices[counter]):
            timer = timer + 1
            if counter == len(indices) - 1:
                break
            counter = counter + 1
        if timer >= 3:
            index_of_indices.append(count)
            index_of_indices.append(counter - 1)
        timer = 0
        count = count + 1
   
    count = 0
    final_indices = []
    for i in index_of_indices:
        fig2.add_shape(dict(type="line", x0=cpm_data['deviceTime_local'][indices[i]], y0=cpm_data['cpm'].min(),
                            x1=cpm_data['deviceTime_local'][indices[i]], y1=cpm_data['cpm'].max(),
                            line=dict(color="black", width=1)))
        count = count + 1

    fig2.show()
    for i in index_of_indices:
        final_indices.append(cpm_data['deviceTime_local'][indices[i]])

    count = 0
    for i in final_indices:
        if count < len(final_indices) - 1 and count % 2 == 0:
            print(i[:-6], " through ", final_indices[count + 1][:-6])
        count = count + 1
