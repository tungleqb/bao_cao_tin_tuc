"""
Script kiểm thử Giai đoạn 3:
- Tự động đăng nhập host và client qua API
- Kết nối WebSocket
- Gửi/nhận dữ liệu qua SwitchManager
"""

import asyncio
import websockets
import httpx

API_URL = "http://localhost:8000"
HOST_LOGIN = {"username": "tester2", "password": "123457",
  "role": "llm_host"}
CLIENT_LOGIN = {"username": "tester1", "password": "123456",
  "role": "client"}

async def get_token(user_data):
    async with httpx.AsyncClient() as client:
        res = await client.post(f"{API_URL}/auth/login", json=user_data)
        res.raise_for_status()
        return res.json()["access_token"]

async def mock_host(token):
    uri = f"ws://localhost:8000/ws/host?token={token}"
    async with websockets.connect(uri) as ws:
        print("✅ Host connected")
        try:
            while True:
                msg = await ws.recv()
                print(f"📩 Host received: {msg}")
                await ws.send("✅ Reply from host")
        except websockets.ConnectionClosed:
            print("❌ Host disconnected")

async def mock_client(token):
    await asyncio.sleep(1)
    uri = f"ws://localhost:8000/ws/client?token={token}"
    async with websockets.connect(uri) as ws:
        print("✅ Client connected")
        await ws.send("Hello from client")
        response = await ws.recv()
        print(f"📩 Client received: {response}")
        assert "Reply from host" in response

async def main():
    host_token, client_token = await asyncio.gather(
        get_token(HOST_LOGIN),
        get_token(CLIENT_LOGIN),
    )
    await asyncio.gather(
        mock_host(host_token),
        mock_client(client_token),
    )

if __name__ == "__main__":
    asyncio.run(main())
