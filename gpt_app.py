api_key="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"

import os
from openai import OpenAI

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Tell me who killed Einstein.",
        }
    ],
    model="gpt-3.5-turbo",
)

print(chat_completion.choices[0].message)
