"""
Test WebSocket Giai đoạn 3: Host ↔ Client ↔ SwitchManager
Yêu cầu server FastAPI đang chạy tại http://localhost:8000
"""

import asyncio
import websockets
import json

HOST_URL = "ws://localhost:8000/ws/host?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0ZXIyIiwicm9sZSI6ImxsbV9ob3N0IiwiZXhwIjoxNzQzMzUwMjc3fQ.VP1OHEkZxx0MUgTcmCw2Ds1OljozmB2dQML1LguYzr8"
CLIENT_URL = "ws://localhost:8000/ws/client?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0ZXIxIiwicm9sZSI6ImNsaWVudCIsImV4cCI6MTc0MzM1MDIxMn0.qzYlAfnFrDwklz8ycQLIxBcJ1OXEUukXskef5sA0Ow0"

async def mock_host():
    async with websockets.connect(HOST_URL) as ws:
        print("✅ Host connected and waiting")
        try:
            while True:
                msg = await ws.recv()
                print(f"📩 Host received: {msg}")
                await ws.send("✅ Reply from host")
        except websockets.ConnectionClosed:
            print("❌ Host disconnected")

async def mock_client():
    await asyncio.sleep(1)  # Wait for host to connect
    async with websockets.connect(CLIENT_URL) as ws:
        print("✅ Client connected")
        await ws.send("Hello from client")
        response = await ws.recv()
        print(f"📩 Client received: {response}")
        assert "Reply from host" in response

async def run_test():
    await asyncio.gather(
        mock_host(),
        mock_client(),
    )

if __name__ == "__main__":
    asyncio.run(run_test())
