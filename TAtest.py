import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import talib
import plotly.express as px

### Using matplotlib
# # plt.style.use("seaborn")
# # plt.rcParams["figure.figsize"] = [14, 8]
#
# df = yf.download("AAPL",
#                  start="2020-01-01",
#                  end="2020-12-31")
#
# upper, middle, lower = talib.BBANDS(df["Adj Close"], timeperiod=20)
# bbands_talib = pd.DataFrame(index=df.index,
#                             data={"bb_low": lower,
#                                   "bb_ma": middle,
#                                   "bb_high": upper})
# bbands_talib.plot(title="Bolinger Bands (TA-lib)");
# df["Adj Close"].plot(title="Apple's stock in 2020");
# # plt.show()

### Using plotly
df = yf.download("AAPL",
                 start="2020-01-01",
                 end="2020-12-31")

upper, middle, lower = talib.BBANDS(df["Adj Close"], timeperiod=20)
bbands_talib = pd.DataFrame(index=df.index,
                            data={"bb_low": lower,
                                  "bb_ma": middle,
                                  "bb_high": upper})

fig = px.line(bbands_talib,
              x=bbands_talib.index,
              y="bb_ma",
              title="Bolinger Bands (TA-lib)")

fig.add_scatter(x=df.index,
                y=df["Adj Close"],
                name="Apple's stock in 2020",
                mode="lines",
                line=dict(width=2))

fig.show()