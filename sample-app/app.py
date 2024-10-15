#!/bin/env python3

import os
from ollama import Client

client = Client(host=os.environ.get("OLLAMA_URL", "http://host.docker.internal:11434"))

try:
  stream = client.chat(
      model='mistral',
      messages=[{'role': 'user', 'content': 'Where can I find most bees in the world?'}],
      stream=True,
  )
  for chunk in stream:
    print(chunk['message']['content'], end='', flush=True)
except client.ResponseError as e:
  print('Error:', e.error)
