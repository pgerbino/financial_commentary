# use yfinance to download daily fc prices for GBPUSD=
import yfinance as yf
# use tradingpatterns to detect head and shoulders pattern
from tradingpatterns import detect_head_shoulder
# now we need to import plotly to plot the head and shoulders pattern
import plotly.graph_objects as go
import pandas as pd

def get_fx_data():
    # download daily data for GBPUSD
    data = yf.download('GBPUSD=X', start='2020-01-01')
    # data.to_csv('data/fx_data.csv')
    return data

if __name__ == '__main__':
    fx_data = get_fx_data()
    # lets see if we can detect a head and shoulders pattern
    head_and_shoulders_df = detect_head_shoulder(fx_data)
    head_and_shoulders_df.reset_index(inplace=True)
    print(head_and_shoulders_df)
    # using plotly lets plot the raw fx_data
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=head_and_shoulders_df.index, y=fx_data['Close'], mode='lines', name='Close'))
    # lets add the head and shoulders pattern to the plot
    # th ecolumn head_shoulder_pattern should be either 'Head and Shoulder' or 'Inverse Head and Shoulder' or 'NaN'
    # if the column is NaN then there is no head and shoulders pattern and don't plot anything
    # if the column is 'Head and Shoulder' then plot the head and shoulders pattern
    # if the column is 'Inverse Head and Shoulder' then plot the inverse head and shoulders pattern
    # head_and_shoulders_df = head_and_shoulders_df.dropna(subset=['head_shoulder_pattern'])  

    for index, row in head_and_shoulders_df.iterrows():
        # ignore index =0
        if index == 0:
            continue
        if row['head_shoulder_pattern'] == 'Head and Shoulder':
            # plot hte index before, current index and the index after
            fig.add_trace(go.Scatter
                (
                    x=[index - 1, index, index + 1],
                    y=[head_and_shoulders_df.loc[index - 1]['Close'], head_and_shoulders_df.loc[index]['Close'], head_and_shoulders_df.loc[index+1]['Close']],
                    mode='lines+markers', 
                    name='Head and Shoulder',
                    line=dict(color='red')
                )
            )

    fig.show()
