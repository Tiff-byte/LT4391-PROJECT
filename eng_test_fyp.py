import os
from openai import OpenAI

os.environ['OPENAI_API_KEY'] = "sk-21449230e01a4f07a024fff5972941cc"
client = OpenAI(api_key=os.environ.get('OPEN_API_KEY'),base_url="https://api.deepseek.com")
import pandas as pd
question = pd.read_csv("ENG_QUESTION_FYP.csv")["questions"]
answers = []
for questions in question:
    print("\n=================\nMy question is:",questions)
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": questions},
        ],
        stream=False
    )
    answer = response.choices[0].message.content
    print(answer)
    answers.append(answer)
df = pd.read_csv("ENG_QUESTION_FYP.csv")
df['answers'] = answers
df.to_csv("answer.csv")