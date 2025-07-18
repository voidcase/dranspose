#!/bin/env python
from dranspose.protocol import VirtualWorker, VirtualConstraint
import requests

ntrig = int(input("number of triggers:"))

resp = requests.post("http://localhost:5000/api/v1/mapping",
    json={
        "eiger": [
            [
                VirtualWorker(constraint=VirtualConstraint(2 * i)).model_dump(
                    mode="json"
                )
            ]
            for i in range(1, ntrig)
        ],
    },
)
print(resp)
