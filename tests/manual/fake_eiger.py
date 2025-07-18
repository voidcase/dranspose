#!/bin/env python
import zmq.asyncio as zmq
import numpy as np
from typing import Callable, Coroutine, Any
from datetime import datetime, timezone
import asyncio
import random
from pydantic_core import Url

from tests.stream1 import AcquisitionSocket

async def stream_eiger() -> Callable[
    [zmq.Context, int, int], Coroutine[Any, Any, None]
]:
    async def _make_eiger(
        ctx: zmq.Context, port: int, nframes: int, frame_time: float = 0.1
    ) -> None:
        socket = AcquisitionSocket(ctx, Url(f"tcp://*:{port}"))
        acq = await socket.start(filename="")
        width = 1475
        height = 831
        for frameno in range(nframes):
            img = np.zeros((width, height), dtype=np.uint16)
            for _ in range(20):
                img[random.randint(0, width - 1)][
                    random.randint(0, height - 1)
                ] = random.randint(0, 10)
            extra = {"timestamps": {"dummy": datetime.now(timezone.utc).isoformat()}}
            await acq.image(img, img.shape, frameno, extra_fields=extra)
            await asyncio.sleep(frame_time)
        await acq.close()
        await socket.close()

    return _make_eiger

async def run():
    eiger = await stream_eiger()
    try:
        nframes = int(input("number of frames:"))
    except ValueError:
        print("int please.")
        exit(1)
    ctx = zmq.Context()
    await eiger(ctx, 9999, nframes)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
loop.close()
