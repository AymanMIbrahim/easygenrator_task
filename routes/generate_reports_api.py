from fastapi import APIRouter
from fastapi.responses import FileResponse
from helpers.compare_models import *
from helpers.compare_real import *
from generate_reports.generate_reports import Generate_Report

llama3 = load_samples("./output/reviews_llama-3.3-70b-versatile.json")
llama4 = load_samples("./output/llama-4-scout-17b-16e-instruct.json")
real_reviews = load_real_reviews("./output/real_reviews.json")
with open("./config/config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

GenReport = Generate_Report(config["output"]["report_path"])

router = APIRouter()

@router.post("/", summary="Generate Reports According to the generated dataset")
async def generate():
    m3 = compute_metrics(llama3)
    m4 = compute_metrics(llama4)

    m3_real = compare_synthetic_with_real(real_reviews, llama3)
    m4_real = compare_synthetic_with_real(real_reviews, llama4)

    GenReport.generate_md_report(m3, m4, m3_real, m4_real)
    return FileResponse(
        path=config["output"]["report_path"],
        media_type="text/markdown",
        filename="model_comparison.md"
    )
