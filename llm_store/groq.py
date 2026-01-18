from groq import Groq
import json
import os
from dotenv import load_dotenv
load_dotenv(override=True)

class groq():
    def __init__(self,model_name,max_tokens):
        self.client = Groq(api_key=os.getenv("GROQ_KEY"))
        self.model_name = model_name
        self.max_tokens = max_tokens
        with open("./config/config.json", "r", encoding="utf-8") as f:
            self.config = json.load(f)

        self.system_prompt = """
        You are a synthetic review generator.
        Your task is to review realistic user reviews for a given software tool
        based on the following inputs:
        - Tool name
        - User persona
        - Target rating distribution (1–5)
        - Minimum number of words
        - Maximum number of words
        
        Rules:
        1. Generate ONE review per request.
        2. The review MUST match the provided persona’s tone, vocabulary, and needs.
        3. The sentiment MUST strictly match the rating:
           - 5: very positive, strong recommendation
           - 4: positive with minor drawbacks
           - 3: neutral, mixed pros and cons
           - 2: mostly negative with some positives
           - 1: strongly negative, clear dissatisfaction
        4. Mention realistic features, workflows, or pain points relevant to the tool.
        5. Avoid generic phrases and marketing language.
        6. Do NOT repeat phrasing or structure from previous reviews.
        7. The review length MUST be between the provided min and max word count.
        8. Write the review from a specific, implied real-life usage context (e.g., a recent project, deadline pressure, team size, onboarding experience), without explicitly stating it as a story.
        9. The review should sound human-written: slight imbalance, informal transitions, or minor repetition are acceptable if natural.
        10. Do NOT follow a fixed structure (e.g., pros first then cons). The order and emphasis should feel natural and varied.
        11. Reflect how this persona typically evaluates tools (e.g., cost sensitivity, technical depth, time constraints).
        12. Avoid polished conclusions or recommendation-style endings.

        
        Output format:
        - Return VALID JSON only
        - No markdown
        - No explanations
        - No extra text
        
        JSON schema:
        {
          "review": "string",
          "rate": number
        }
        """


    def infere(self,user_message):
        messages = [
            {
                "role": "system",
                "content": self.system_prompt

            },
            {
                "role": "user",
                "content": user_message
            }
        ]
        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=0.85,
            max_completion_tokens=self.max_tokens,
            top_p=0.95,
            presence_penalty=0.5,
            frequency_penalty=0.2,
            stream=False,
            stop=None
        )

        return completion.choices[0].message.content