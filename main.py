from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI(title="Normal Backend")

AI_BE_URL = "http://localhost:8001/analyze"

class UserInput(BaseModel):
    text: str

@app.post("/process")
def process_user_input(user_input: UserInput):
    payload = {
        "text": user_input.text
    }

    response = requests.post(AI_BE_URL, json=payload)

    if response.status_code != 200:
        return {"error": "AI service failed"}

    ai_result = response.json()

    result = {
        "original": user_input.text,
        "ai_result": ai_result["result"]
    }

    return result




#----------------------Minimal production-safe fix----------------------
# @app.post("/process")
# def process_user_input(user_input: UserInput):
#     try:
#         response = requests.post(
#             AI_BE_URL,
#             json={"text": user_input.text},
#             timeout=5
#         )
#         response.raise_for_status()
#         ai_result = response.json()

#     except requests.RequestException as e:
#         return {
#             "error": "AI service unavailable",
#             "detail": str(e)
#         }

#     return {
#         "original": user_input.text,
#         "ai_result": ai_result["result"]
#     }
