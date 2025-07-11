import time
from typing import AsyncGenerator, Optional
from dranspose import ingester
from dranspose.event import StreamData
from dranspose.protocol import StreamName, ZmqUrl

class DummySettings(ingester.IngesterSettings):
    upstream_url: ZmqUrl

class DummyIngester(ingester.Ingester):

    def __init__(self, settings: Optional[DummySettings] = None):
        super().__init__(settings)
        self.settings = settings

    async def run_source(self, stream: StreamName) -> AsyncGenerator[StreamData | ingester.IsSoftwareTriggered, None]:
        print(f"{stream=}")
        data = StreamData(typ="derp", frames=[b"berpity"])
        time.sleep(1)
        yield data
