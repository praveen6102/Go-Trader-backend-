from fastapi import FastAPI
import ccxt
import pandas as pd
import pandas_ta as ta

app = FastAPI()
exchange = ccxt.binance()

@app.get("/signal")
def get_signal(symbol: str = "BTC/USDT", timeframe: str = "5m", risk: str = "balanced"):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=200)
    df = pd.DataFrame(ohlcv, columns=["time","open","high","low","close","volume"])

    df["ema20"] = ta.ema(df["close"], length=20)
    df["ema50"] = ta.ema(df["close"], length=50)
    df["rsi"] = ta.rsi(df["close"], length=14)
    macd = ta.macd(df["close"])
    df["macd"] = macd["MACD_12_26_9"]
    df["macd_signal"] = macd["MACDs_12_26_9"]

    last = df.iloc[-1]
    price = last["close"]
    signal = "WAIT"

    if last["ema20"] > last["ema50"] and last["rsi"] < 45 and last["macd"] > last["macd_signal"]:
        signal = "BUY"
    elif last["ema20"] < last["ema50"] and last["rsi"] > 55 and last["macd"] < last["macd_signal"]:
        signal = "SELL"

    if risk == "conservative":
        sl = price * 0.995
        tp = price * 1.01
    elif risk == "aggressive":
        sl = price * 0.99
        tp = price * 1.03
    else:
        sl = price * 0.993
        tp = price * 1.02

    return {
        "app": "Go Traders",
        "symbol": symbol,
        "timeframe": timeframe,
        "signal": signal,
        "entry": round(price, 2),
        "stop_loss": round(sl, 2),
        "target": round(tp, 2),
        "risk": risk
  }# Go-Trader-backend-
from fastapi import FastAPI
import ccxt
import pandas as pd
import pandas_ta as ta

app = FastAPI()
exchange = ccxt.binance()

@app.get("/signal")
def get_signal(symbol: str = "BTC/USDT", timeframe: str = "5m", risk: str = "balanced"):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=200)
    df = pd.DataFrame(ohlcv, columns=["time","open","high","low","close","volume"])

    df["ema20"] = ta.ema(df["close"], length=20)
    df["ema50"] = ta.ema(df["close"], length=50)
    df["rsi"] = ta.rsi(df["close"], length=14)
    macd = ta.macd(df["close"])
    df["macd"] = macd["MACD_12_26_9"]
    df["macd_signal"] = macd["MACDs_12_26_9"]

    last = df.iloc[-1]
    price = last["close"]
    signal = "WAIT"

    if last["ema20"] > last["ema50"] and last["rsi"] < 45 and last["macd"] > last["macd_signal"]:
        signal = "BUY"
    elif last["ema20"] < last["ema50"] and last["rsi"] > 55 and last["macd"] < last["macd_signal"]:
        signal = "SELL"

    if risk == "conservative":
        sl = price * 0.995
        tp = price * 1.01
    elif risk == "aggressive":
        sl = price * 0.99
        tp = price * 1.03
    else:
        sl = price * 0.993
        tp = price * 1.02

    return {
        "app": "Go Traders",
        "symbol": symbol,
        "timeframe": timeframe,
        "signal": signal,
        "entry": round(price, 2),
        "stop_loss": round(sl, 2),
        "target": round(tp, 2),
        "risk": risk
    }
