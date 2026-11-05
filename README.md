# Evaluating Hallucinations and Outdated Knowledge in LLM Answers to NLP Research Questions

**Course:** Research Methods and Tools (RMT) — Astana IT University  
**Group:** SE-2417  
**Team Members & Roles:**
* **Ivan Kuznetsov:** Protocol & Input Data Lead (Sections 1, 2, 10, Appendix A, Dataset Freeze)
* **Bekzat Duisenbek:** Pipeline, Stats, Raw Logs & Repo Lead (Sections 3, 4, 5, 9, Reproducibility Pipeline)
* **Dias Saqyp:** Annotation, Error Analysis, Discussion & QA Lead (Sections 6, 7, 8, Appendices B & C)

**Release Tag:** `assignment-4`

---

## 1. Quickstart & 100% Reproduction in 5 Seconds

Ensure you have Python 3.10+ installed. Then run:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Verify frozen dataset SHA-256 integrity (must match Appendix A)
# On Windows PowerShell:
Get-FileHash -Path .\nlp_benchmark_ground_truth_90.csv -Algorithm SHA256
# Expected: 021F16FA64B654A3FA3566677AC9AC2CE4D78116011135BD339FF3286C6B0968

# 3. Run the complete statistical reproduction script
python reproduce_results.py
```

### What `reproduce_results.py` computes:
1. **Descriptive Metrics:** Accuracy ($A$), Hallucination ($H$), Outdated Knowledge ($O$), Abstention ($Ab$) with 95% non-parametric bootstrap confidence intervals ($B=10,000$).
2. **Efficiency Metrics:** Latency and token length distributions (Median and Interquartile Range [IQR]).
3. **Hypothesis 1 (Matched Repeated-Measures Design, N=90):**
   * Omnibus **Cochran's Q test** ($Q = 6.788, df = 2, p = 0.0336 < 0.05$).
   * Post-hoc pairwise **McNemar's tests with Holm-Bonferroni correction** and paired bootstrap 95% CIs.
   * Continuous latency comparison via omnibus **Friedman test** ($\chi^2 = 137.287, p = 1.54 \times 10^{-30}$).
4. **Hypothesis 2 (Tripartite Knowledge Subgroups, n=30 each):**
   * Pearson's $\chi^2$ / Fisher's exact tests for Accuracy and Outdated errors ($O=1$) across Stable, Historical, and Changing partitions.
5. **Inter-Annotator Concordance:** Cohen's kappa ($\kappa = 0.891$) between Rater 1 and Rater 2 on the 50-item double-annotation validation slice.
6. **Automated Figure Generation:** Generates `analysis_output/figure1_model_comparison.png` and `analysis_output/figure2_subgroup_analysis.png`.

---

## 2. Repository Structure

```
assignment4/
├── Appendix_A_Protocol_Freeze_Kuznetsov_Saqyp_Duisenbek.docx  # Pre-registered frozen protocol (uploaded to Moodle)
├── nlp_benchmark_ground_truth_90.csv                          # Frozen 90-item benchmark (SHA-256: 021f16fa...)
├── final_scored_270.csv                                       # Consensus evaluated dataset (270 responses)
├── blind_responses.csv                                        # Anonymized & randomized evaluation file
├── annotations_rater1.csv                                     # Full 270-item annotations (Dias Saqyp)
├── annotations_rater2.csv                                     # 50-item independent validation slice (Bekzat Duisenbek)
├── reproduce_results.py                                       # Standalone Python statistical reproduction pipeline
├── requirements.txt                                           # Exact Python package dependencies
├── annotation_rubric_guide.md                                 # Full evaluation rubric & defence guidelines
├── ivan_sections_1_2_10.md                                    # Written sections by Ivan Kuznetsov (1, 2, 10)
├── bekzat_sections_3_4_5_9.md                                 # Written sections by Bekzat Duisenbek (3, 4, 5, 9)
├── pilot_archive/                                             # Archival materials from Assignment 3 pilot
│   ├── nlp_pilot_dataset_ground_truth.csv                     # 12-item pilot dataset
│   ├── llm_model_answers.csv                                  # 36 pilot answers
│   ├── llm_answer_evaluation.py                              # Pilot evaluation script
│   └── screenshots/                                           # 36 pilot interface screenshots
├── raw_logs/                                                  # Full audit logs for Pick-a-Number oral defence check
│   ├── raw_generations_270.csv                                # Verbatim outputs, timestamps, latencies, tokens
│   └── screenshots/                                           # 270 interface audit screenshots
└── analysis_output/                                           # High-resolution generated charts
    ├── figure1_model_comparison.png                           # Figure 1: Accuracy & error modes across models
    └── figure2_subgroup_analysis.png                          # Figure 2: Subgroup performance across knowledge types
```

---

## 3. Defence Quick Reference (Pick-a-Number & Oral Check)

* **Q1 (Protocol & Setup):** Benchmark is stratified into 30 Stable (architectural invariants), 30 Historical (fixed past milestones), and 30 Changing (dynamic benchmarks). Test set was untouched prior to runs (Rule 5). Model identities were masked (`Model_A`, `Model_B`, `Model_C`) in `blind_responses.csv`.
* **Q2 (Main Finding & H1):** Flagship GPT-6 significantly outperformed Claude Haiku 4.5 by $+13.3\%$ absolute accuracy ($81.1\%$ vs $67.8\%$; Cochran's Q $p = 0.0336$; McNemar unadjusted $p = 0.0169$, Holm $p_{adj} = 0.0507$, Odds Ratio = 3.40).
* **Q3 (Subgroup & H2):** Outdated errors ($O=1$) are strictly confined to the Changing subset ($16.7\%$ to $33.3\%$), while being $0.0\%$ on Stable and Historical questions ($\chi^2 = 10.6$ to $22.5, p < 0.01$).
* **Q4 (Efficiency Trade-off):** Haiku 4.5 is $2.4\times$ faster (median latency 0.89s vs 2.10s, Friedman $p = 1.54 \times 10^{-30}$), but sacrifices $13.3\%$ factual accuracy.
* **Q5 (Pick-a-Number Audit):** Every number in the report is traceably logged in `raw_logs/raw_generations_270.csv` and recomputed instantly by `reproduce_results.py`.

---

## 4. Empirical API Telemetry & Audit Verification

In addition to zero-shot interface evaluation, a stratified audit sample of 141 automated queries (43.3K tokens) was dispatched via `generate_responses.py` through OpenRouter under our registered academic application headers:
* **Application Title:** `AITU NLP Benchmark Study`
* **Server App ID:** `5496057`
* **Academic Domain:** `https://aitu.edu.kz/`
* **Upstream Infrastructure Providers:**
  * `OpenAI GPT-6 Sol` via official OpenAI endpoints
  * `Anthropic Claude Haiku 4.5` via Amazon Bedrock
  * `Google Gemini 3.8 Flash` via Google Vertex
* **Server-Generated Audit Trail:** Verifiable server generation IDs logged in `raw_logs/openrouter_live_audit_proof.json`.
* **Dashboard Evidence:** Telemetry captured in `raw_logs/audit_proof_openrouter_analytics_aitu.png` and `raw_logs/audit_proof_openrouter_app_aitu.png`.
