from fastapi import APIRouter,status
from fastapi.responses import JSONResponse
from helpers.utils import *
import json
import random
from uuid import uuid4
import time
from llm_store.groq import groq
from review.review_generated_sample import Review

from dotenv import load_dotenv
load_dotenv(override=True)

with open("./config/config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

samples_reviewr = Review()
model_id = config["selected_model"]
llm = groq(model_name=config["models"][model_id]["model_name"],max_tokens=config["models"][model_id]["max_tokens"])
rating_distribution = generate_ratings(config["project"]["total_samples"],config["rating_distribution"])
personas_distripuation = generate_persona_indexes_with_distribution(config["project"]["total_samples"],config["persona_distribution"])


router = APIRouter()

@router.post("/", summary="Generate Reviews According to the configuration file")
async def generate():

    AcceptedList = []
    AcceptedSamples = {}
    for i in range(config["project"]["total_samples"]):
        for j in range(3):
            focus_value = random.getrandbits(1)
            user_message = f"""
            Acording to this configurate review a review, Here is the Config:
            Domain: {config["project"]["domain"]}
            Persona Name: {config["personas"][personas_distripuation[i]]["name"]}
            Persona Tone: {config["personas"][personas_distripuation[i]]["tone"]}
            Persona focus: {config["personas"][personas_distripuation[i]]["focus"][focus_value]}
            Minimum number of words: {config["review_rules"]["min_words"]}
            Maximum number of words: {config["review_rules"]["max_words"]}
            Rating of the review: {rating_distribution[i]}
            """


            start = time.time()
            review = llm.infere(user_message)
            end = time.time()
            revierw_json = json_extract(review)

            sample = {
                "id": str(uuid4()),
                "model": config['models'][model_id]['model_name'],
                "Persona_Name": config["personas"][personas_distripuation[i]]["name"],
                "Persona_Tone": config["personas"][personas_distripuation[i]]["tone"],
                "Persona_focus": config["personas"][personas_distripuation[i]]["focus"][focus_value],
                "rating": revierw_json["rate"],
                "text": revierw_json["review"],
                "gen_time_ms": round(end-start,2),
                "attempt": j
            }

            result = samples_reviewr.accept_or_reject(sample,config,AcceptedList)
            if result["accepted"]:
                AcceptedList.append(sample["text"])
                AcceptedSamples[i] = sample
                save_dict_as_json(AcceptedSamples,
                                  config["output"]["dataset_path"].split(".json")[0] + "_" + config['models'][model_id][
                                      'model_name'] + ".json")
                break
            elif j == 2:
                AcceptedList.append(sample["text"])
                AcceptedSamples[i] = sample
                save_dict_as_json(AcceptedSamples,config["output"]["dataset_path"].split(".json")[0]+"_"+config['models'][model_id]['model_name']+".json")


    return JSONResponse(status_code=status.HTTP_200_OK, content=AcceptedSamples)
