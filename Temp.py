import asyncio
from bleak import BleakClient

MAC = "C8:5C:CC:A8:DE:D9"

async def show_services():
    async with BleakClient(MAC) as client:
        print("✅ 已连接，正在读取服务列表：")
        services = client.services
        for s in services:
            print(f"\nService UUID: {s.uuid}")
            for char in s.characteristics:
                print(f"  -> Char UUID: {char.uuid} | 权限:{char.properties}")

asyncio.run(show_services())
