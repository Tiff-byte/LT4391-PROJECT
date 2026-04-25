import os
from openai import OpenAI

os.environ['OPENAI_API_KEY'] = "sk-b90b89f5c7d2404496ed86b15b1bfaed"
client = OpenAI(api_key=os.environ.get('OPEN_API_KEY'),base_url="https://api.deepseek.com")
import pandas as pd
question =pd.read_csv("SPOKEN_CHI_QUESTION_FYP.csv")["問題"]
answers = []
for 問題 in question:
    print("\n=================\nMy question is:", 問題)
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": 問題},
        ],
        stream=False
    )
    answer = response.choices[0].message.content
    print(answer)
    answers.append(answer)
df = pd.read_csv("SPOKEN_CHI_QUESTION_FYP.csv")
df['answers'] = answers
df.to_csv("answer2.csv")