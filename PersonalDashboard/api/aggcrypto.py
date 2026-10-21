import asyncio
import json
import websockets
import time


async def candle(pair: str, callback):
    if not pair : return 
    pair = pair.lower()
    BINANCE_URL = f"wss://stream.binance.com:9443/ws/{pair}@aggTrade"
    prices = []
    print("API: Connecting")
    print(pair)
    async with websockets.connect(BINANCE_URL) as ws:
        print("API: connected")
        while True:
            message = await ws.recv()
            payload = json.loads(message)
            
            prices.append(payload["p"])

            if len(prices) > 24: # start from 0
                prices.pop(0)
            await callback(pair, [{"price": p} for p in prices])
#running it asyncio.run(candle(pair)) pair must be a list
