"""
title: Metadata Pipe
author: Michael.Dratch@parivedasolutions.com
version: 1.0.0
type: pipe
"""

import requests


class Pipe:
    def __init__(self):
        self.type = "pipe"
        self.name = "Metadata Pipe"

    def pipe(self, body: dict, __metadata__: dict) -> str:
        # Use chat_id as the session_id so each OpenWebUI conversation maps to
        # one Bedrock Agent session, giving the agent persistent memory per chat.
        body["model"] = "bedrock-agent:ZU4I3FTWD3:ZUGEI0JHLQ"
        body["extra_body"] = {"session_id": __metadata__.get("chat_id")}

        headers = {
            "Authorization": "Bearer API_KEY",
        }
        # Forward to agent
        response = requests.post(
            url="http://bedrock-access-gateway:8080/api/v1/chat/completions",
            headers=headers,
            json=body,
            stream=body.get("stream", False),
        )
        return response.iter_lines() if body.get("stream") else response.json()
