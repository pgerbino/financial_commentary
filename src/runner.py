import yfinance as yf
from tradingpatterns import detect_head_shoulder

# use yfinance to download daily fc prices for GBPUSD
# use tradingpatterns to detect head and shoulders pattern
# now we need to import plotly to plot the head and shoulders pattern
import plotly.graph_objects as go

def get_fx_head_and_shoulders_df():
    # download daily head_and_shoulders_df for GBPUSD
    head_and_shoulders_df = yf.download('GBPUSD=X', start='2020-01-01')
    # head_and_shoulders_df.to_csv('head_and_shoulders_df/fx_head_and_shoulders_df.csv')
    return head_and_shoulders_df

if __name__ == '__main__':
    fx_head_and_shoulders_df = get_fx_head_and_shoulders_df()
    # lets see if we can detect a head and shoulders pattern
    head_and_shoulders_df = detect_head_shoulder(fx_head_and_shoulders_df)
    head_and_shoulders_df.reset_index(inplace=True)
    print(head_and_shoulders_df)
    # using plotly lets plot the raw fx_head_and_shoulders_df
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=head_and_shoulders_df.index, y=fx_head_and_shoulders_df['Close'], mode='lines', name='Close'))
    # lets add the head and shoulders pattern to the plot
    # the column head_shoulder_pattern should be either 'Head and Shoulder' or 'Inverse Head and Shoulder' or 'NaN'
    # if the column is NaN then there is no head and shoulders pattern and don't plot anything
    # if the column is 'Head and Shoulder' then plot the head and shoulders pattern
    # if the column is 'Inverse Head and Shoulder' then plot the inverse head and shoulders pattern
    # head_and_shoulders_df = head_and_shoulders_df.dropna(subset=['head_shoulder_pattern'])

    for index, row in head_and_shoulders_df.iterrows():
        # ignore index = 0
        if index == 0:
            continue
        if row['head_shoulder_pattern'] == 'Head and Shoulder':
            # plot the index before, current index, and the index after
            fig.add_trace(go.Scatter(
                x=[index - 1, index, index + 1],
                y=[head_and_shoulders_df.loc[index - 1]['High'], head_and_shoulders_df.loc[index]['High'], head_and_shoulders_df.loc[index+1]['High']],
                mode='lines+markers',
                name='Head and Shoulder',
                line=dict(color='red')
            ))
        elif row['head_shoulder_pattern'] == 'Inverse Head and Shoulder':
            # plot the index before, current index, and the index after
            fig.add_trace(go.Scatter(
                x=[index - 1, index, index + 1],
                y=[head_and_shoulders_df.loc[index - 1]['Close'], head_and_shoulders_df.loc[index]['Close'], head_and_shoulders_df.loc[index+1]['Close']],
                mode='lines+markers',
                name='Inverse Head and Shoulder',
                line=dict(color='green')
            ))

    fig.show()

    head_and_shoulders_df.to_csv('./head_and_shoulders.csv')

    # Initialize variables
    total_return = 0

    # Define a fixed profit/loss percentage for simplicity (this can be adjusted)
    profit_threshold = 0.02  # 2% profit target
    loss_threshold = -0.01   # 1% loss threshold

    trades = []

    for i in range(len(head_and_shoulders_df) - 1):
        if head_and_shoulders_df.loc[i, 'head_shoulder_pattern'] == 'Head and Shoulder':
            # Calculate the neckline as the average of two lows around the head
            neckline = (head_and_shoulders_df.loc[i-1, 'Low'] + head_and_shoulders_df.loc[i+1, 'Low']) / 2

            # Simulate shorting when price breaks below the neckline
            entry_price = neckline
            # exit price is the minimum of the low prices after the head and the profit target
            # it is the minimum because we want to exit at the lowest price
            exit_price = min(head_and_shoulders_df.loc[i+1:, 'Low'].min(), entry_price * (1 + profit_threshold))
            trade_return = (entry_price - exit_price) / entry_price

            # Stop out at loss threshold
            if trade_return < loss_threshold:
                trade_return = loss_threshold

            trades.append(('Normal', trade_return))
            total_return += trade_return

        elif head_and_shoulders_df.loc[i, 'head_shoulder_pattern'] == 'Inverse Head and Shoulder':
            # Calculate the neckline as the average of two highs around the head
            neckline = (head_and_shoulders_df.loc[i-1, 'High'] + head_and_shoulders_df.loc[i+1, 'High']) / 2

            # Simulate going long when price breaks above the neckline
            entry_price = neckline
            exit_price = max(head_and_shoulders_df.loc[i+1:, 'High'].max(), entry_price * (1 + profit_threshold))
            trade_return = (exit_price - entry_price) / entry_price

            # Stop out at loss threshold
            if trade_return < loss_threshold:
                trade_return = loss_threshold

            trades.append(('Inverse', entry_price, exit_price, trade_return))
            total_return += trade_return

    # Output the total net return
    print(f"Total Net Return from Trading Necklines: {total_return * 100:.2f}%")
    for trade in trades:
        print(trade)