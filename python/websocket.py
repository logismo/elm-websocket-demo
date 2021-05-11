#!/usr/bin/env python

import asyncio
import websockets
import random

class WebSocket:
    running = False
    tasks = []
    size_ar = 50
    speed = 0.0159
    array = []

    async def init_array(self):
        self.array = [int(x) for x in random.sample(range(1,self.size_ar + 1), self.size_ar)]
    
    async def send_message(self, websocket, msg, speed = None):
        if speed is None:
            speed = self.speed
        await websocket.send(msg)
        await asyncio.sleep(speed)
    
    async def bubble_sort(self, websocket):
        for i in range(len(self.array)):
            count = 0
            for j in range(len(self.array) - i - 1):
                if self.array[j] > self.array[j+1]:
                    count += 1
                    self.array[j], self.array[j+1] = self.array[j+1], self.array[j]
                    await self.send_message(websocket, f"{self.array} \n\n Sorting...")

    async def selection_sort(self, websocket):
        for i in range(len(self.array) - 1):
            smallest = i
            for j in range(i + 1, len(self.array)):
                if self.array[j] < self.array[smallest]:
                    smallest = j
            self.array[i], self.array[smallest] = self.array[smallest], self.array[i]
            await self.send_message(websocket, f"{self.array} \n\n Sorting...")

    async def merge_sort(self, websocket, array):
        if len(array) > 1:
            middle = len(array) // 2
            left = array[middle:]
            right = array[:middle]

            await self.merge_sort(websocket, left)
            await self.merge_sort(websocket, right)

            i = j = k = 0
            
            while i < len(left) and j < len(right):
                if left[i] < right[j]:
                    array[k] = left[i]
                    i += 1
                    await self.send_message(websocket, f"{array} \n\n Sorting...")
                else:
                    array[k] = right[j]
                    j += 1
                    await self.send_message(websocket, f"{array} \n\n Sorting...")
                k += 1
            while i < len(left):
                array[k] = left[i]
                i += 1
                k += 1
                await self.send_message(websocket, f"{array} \n\n Sorting...")

            while j < len(right):
                array[k] = right[j]
                j += 1
                k += 1
                await self.send_message(websocket, f"{array} \n\n Sorting...")

    async def read(self, message, websocket):
        if self.running:
            self.tasks[0].cancel()
            self.tasks.pop(0)

        self.running = True
        print("start")
        await self.init_array()
        await self.send_message(websocket, f"{self.array} \n\n Sorting...")

        if message == "merge":
            await self.merge_sort(websocket, self.array)
        elif message == "selection":
            await self.selection_sort(websocket)
        elif message == "bubble":
            await self.bubble_sort(websocket)
        
        # array = [int(x) for x in random.sample(range(1,101), 100)]
        # for i in range(len(array)):
        #     count = 0
        #     for j in range(len(array) - i - 1):
        #         if array[j] > array[j+1]:
        #             count += 1
        #             array[j], array[j+1] = array[j+1], array[j]
        #             await websocket.send(f"{array}")
        #             await asyncio.sleep(0.0159)
        
        await self.send_message(websocket, f"{self.array} \n\n Done!")
        self.running = False
        self.tasks = []
        # else:
        #     if message != self.cur_sort:
        #         print("stop and restart")
            # loop = asyncio.get_event_loop()
            # self.tasks[0].cancel()
            # self.running = False
            # self.tasks = []
    
    async def echo(self, websocket, path):
        loop = asyncio.get_event_loop()
        try:
            async for message in websocket:
                self.tasks.append(loop.create_task(self.read(message, websocket), name=f"algo{len(self.tasks)}"))
        except websockets.exceptions.ConnectionClosed:
            pass
        # async for message in websocket:
        #     if not self.running:
        #         self.running = True
        #         print("running")
        #         array = [int(x) for x in random.sample(range(1,201), 200)]
        #         for i in range(len(array)):
        #             count = 0
        #             for j in range(len(array) - i - 1):
        #                 if array[j] > array[j+1]:
        #                     count += 1
        #                     array[j], array[j+1] = array[j+1], array[j]
        #                     await websocket.send(f"{array}")
        #                     await asyncio.sleep(0.008)
        #         self.running = False
            # else:
            #     print("running")

ws = WebSocket()
asyncio.get_event_loop().run_until_complete(
    websockets.serve(ws.echo, 'localhost', 3456))
asyncio.get_event_loop().run_forever()