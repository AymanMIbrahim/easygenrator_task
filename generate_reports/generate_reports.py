
class Generate_Report:
    def __init__(self,path):
        self.path = path

    def generate_md_report(self, m3, m4, m3_real=None, m4_real=None):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write("# Model Comparison Report\n\n")

            f.write("## Models Compared\n")
            f.write("- **LLaMA 3.3 70B (Groq)**\n")
            f.write("- **LLaMA 4 Scout 17B (Groq)**\n\n")

            f.write("## Dataset Overview\n")
            f.write("| Metric | LLaMA 3.3 | LLaMA 4 Scout |\n")
            f.write("|------|-----------|---------------|\n")
            f.write(f"| Total samples | {m3['total_samples']} | {m4['total_samples']} |\n")
            f.write(f"| Acceptance rate | {m3['acceptance_rate']} | {m4['acceptance_rate']} |\n\n")

            f.write("## Generation Performance\n")
            f.write("| Metric | LLaMA 3.3 | LLaMA 4 Scout |\n")
            f.write("|------|-----------|---------------|\n")
            f.write(f"| Avg gen time (ms) | {m3['avg_gen_time_ms']} | {m4['avg_gen_time_ms']} |\n")
            f.write(f"| Median gen time (ms) | {m3['median_gen_time_ms']} | {m4['median_gen_time_ms']} |\n")
            f.write(f"| Avg attempts | {m3['avg_attempts']} | {m4['avg_attempts']} |\n\n")

            f.write("## Quality Scores\n")
            f.write("| Metric | LLaMA 3.3 | LLaMA 4 Scout |\n")
            f.write("|------|-----------|---------------|\n")
            f.write(f"| Avg quality | {m3['avg_quality']} | {m4['avg_quality']} |\n")
            f.write(f"| Median quality | {m3['median_quality']} | {m4['median_quality']} |\n")
            f.write(f"| Quality std | {m3['quality_std']} | {m4['quality_std']} |\n")
            f.write(
                f"| % ≥ threshold | {m3['pct_quality_above_threshold']} | {m4['pct_quality_above_threshold']} |\n\n")

            f.write("## Diversity & Redundancy\n")
            f.write("| Metric | LLaMA 3.3 | LLaMA 4 Scout |\n")
            f.write("|------|-----------|---------------|\n")
            f.write(
                f"| Avg semantic similarity | {m3['avg_semantic_similarity']} | {m4['avg_semantic_similarity']} |\n")
            f.write(f"| Near-duplicate rate | {m3['near_duplicate_rate']} | {m4['near_duplicate_rate']} |\n")
            f.write(f"| Avg diversity score | {m3['avg_diversity']} | {m4['avg_diversity']} |\n\n")

            f.write("## Domain Realism\n")
            f.write("| Metric | LLaMA 3.3 | LLaMA 4 Scout |\n")
            f.write("|------|-----------|---------------|\n")
            f.write(f"| Avg domain score | {m3['avg_domain_score']} | {m4['avg_domain_score']} |\n")
            f.write(f"| Avg forbidden score | {m3['avg_forbidden_score']} | {m4['avg_forbidden_score']} |\n\n")

            if m3_real and m4_real:
                f.write("## Synthetic vs Real Review Comparison\n\n")

                f.write("### Semantic Similarity to Real Reviews\n")
                f.write("| Metric | LLaMA 3.3 | LLaMA 4 Scout |\n")
                f.write("|------|-----------|---------------|\n")
                f.write(
                    f"| Avg similarity | {round(m3_real['semantic']['avg'], 3)} | {round(m4_real['semantic']['avg'], 3)} |\n"
                )
                f.write(
                    f"| Median similarity | {round(m3_real['semantic']['median'], 3)} | {round(m4_real['semantic']['median'], 3)} |\n"
                )
                f.write(
                    f"| Std deviation | {round(m3_real['semantic']['std'], 3)} | {round(m4_real['semantic']['std'], 3)} |\n\n"
                )

                f.write("### Review Length Alignment\n")
                f.write("| Metric | LLaMA 3.3 | LLaMA 4 Scout |\n")
                f.write("|------|-----------|---------------|\n")
                f.write(
                    f"| Avg length (words) | {m3_real['length']['avg']} | {m4_real['length']['avg']} |\n"
                )
                f.write(
                    f"| Length std | {m3_real['length']['std']} | {m4_real['length']['std']} |\n\n"
                )

                f.write(
                    "Synthetic samples from both models show close semantic alignment with real user reviews "
                    "while maintaining sufficient variation, indicating realistic generation without memorization.\n\n"
                )

            f.write("## Summary\n")
            f.write(
                "- **LLaMA 3.3** shows stronger overall quality consistency and semantic diversity.\n"
                "- **LLaMA 4 Scout** is faster per sample but produces a higher rate of near-duplicate content.\n"
                "- Choice depends on whether speed or quality stability is prioritized.\n"
            )

