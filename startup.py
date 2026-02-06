# This will prompt each model so that ollama will load each of them into memory

from ollama import ChatResponse,chat
## smollm2:135m
#
models = ["deepseek-r1:1.5b","llama3.2:1b","gemma3:1b","lfm2.5-thinking:latest","qwen3:0.6b","phi4-mini:3.8b","falcon3:1b","oroboroslabs/base-q-v1:latest","Mm77shallm/meshal:latest","JorgeAtLLama/herodotus:latest","qwen3:8b"]
for i in models:
    response: ChatResponse = chat(model=i, messages=[
      {
        'role': 'user',
        'content': 'Hello',
      },
    ])
#print(response['message']['content'])
## or access fields directly from the response object
#print(response.message.content)