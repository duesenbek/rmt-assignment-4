# Assignment 4: Technical Pipeline, Results, and Reproducibility

**Student:** Bekzat Duisenbek (SE-2417)  
**Assigned Roles:** Pipeline, Stats, Raw Logs & Repo Lead  
**Assigned Report Sections:** Section 3, Section 4, Section 5, Section 9  
**Team Members:** Ivan Kuznetsov (Protocol & Data Lead), Dias Saqyp (Annotation & QA Lead), Bekzat Duisenbek (Tech & Pipeline Lead)  
**Project:** Evaluating Hallucinations and Outdated Knowledge in LLM Answers to NLP Research Questions  
**Evaluated Models:** OpenAI GPT-6, Anthropic Claude Haiku 4.5, Google Gemini 3.8 Flash  
**Test Set Cryptographic SHA-256 Hash:** `021f16fa64b654a3fa3566677ac9ac2ce4d78116011135bd339ff3286c6b0968`

---

## Section 3: Deviations from the Frozen Protocol

The experiment followed the pre-registered protocol without modifications. The Experiment Protocol Freeze Form (Appendix A) was formally uploaded to Moodle on 4 November 2026 at 22:40 UTC+5, locking the 90-item benchmark with cryptographic hash SHA-256: `021f16fa64b654a3fa3566677ac9ac2ce4d78116011135bd339ff3286c6b0968`.

Following instructor feedback from Assignment 3, we transitioned from the preliminary two-class taxonomy to a three-category benchmark: 30 Stable Facts, 30 Historical Facts, and 30 Changing Facts. This division isolates temporal knowledge decay on dynamic leaderboards from static historical recall. In line with course policy (Rule 1 / Rule 9), the study was conducted by our approved three-member team (Ivan Kuznetsov, Dias Saqyp, Bekzat Duisenbek) with designated individual responsibilities across protocol design, technical data collection, and independent annotation. All 270 zero-shot inference queries adhered strictly to the frozen execution parameters, prompt structure, and evaluation rubric.

*(Word count: 131 words — Target limit: 100–150 words)*

---

## Section 4: Final Experimental Setup

We evaluated three frontier large language models: OpenAI GPT-6 (flagship reasoning baseline), Anthropic Claude Haiku 4.5 (lightweight edge baseline), and Google Gemini 3.8 Flash (fast multimodal baseline). Testing occurred on 4 November 2026 across 90 standardized NLP research questions, yielding 270 independent zero-shot queries.

To guarantee zero-shot conditions and isolate internal parametric memory, each question was submitted into a newly initialized chat session. This eliminated conversational memory carryover and context window pollution. Web search, browsing plug-ins, and external tools were explicitly disabled in each interface settings. Where parametric isolation could not be audited via backend telemetry, disabling retrieval toggles was verified by two team members prior to query submission.

Prompts used a fixed template without preliminary dialogue or few-shot exemplars: *"Answer the following factual question about NLP research as accurately and concisely as possible. Give the direct answer and, if useful, one brief explanation. Do not use web browsing or external retrieval. If you do not know the answer or cannot determine whether it is current, state that uncertainty rather than guessing."*

Raw text outputs were captured verbatim without truncation. Wall-clock response latency was logged in seconds from prompt dispatch to final token generation, and output token counts were recorded. To prevent evaluation bias, responses were blinded and randomly ordered: model names were masked as `Model_A`, `Model_B`, and `Model_C` in `blind_responses.csv` before human evaluation. All 270 responses were evaluated by Dias Saqyp (Rater 1) using the deterministic decision rubric. Bekzat Duisenbek (Rater 2) independently evaluated a stratified random slice of 50 responses to assess inter-annotator agreement. Discrepancies were resolved through joint consensus against primary peer-reviewed literature and official model technical reports.

*(Word count: 271 words — Target limit: 250–350 words, excluding table)*

### Table 1. Final Experimental Setup Summary

| Experimental Dimension | Specification / Value | Methodological Justification |
| :--- | :--- | :--- |
| **Evaluated Models** | • OpenAI GPT-6<br>• Anthropic Claude Haiku 4.5<br>• Google Gemini 3.8 Flash | Comparative spectrum: flagship reasoning model, fast edge model, and high-throughput multimodal model. |
| **Benchmark Composition** | 90 balanced items:<br>• 30 Stable Facts ($S01$–$S30$)<br>• 30 Historical Facts ($H01$–$H30$)<br>• 30 Changing Facts ($C01$–$C30$) | Stratified to isolate mathematical invariants and historical milestones from dynamic post-2024 benchmark drift. |
| **Test-Set Integrity** | SHA-256 = `021f16fa64b654a3fa3566677ac9ac2ce4d78116011135bd339ff3286c6b0968` | Frozen prior to runs; untouched test set compliance (Rule 5). |
| **Interaction Mode** | Zero-shot single-turn prompting in fresh sessions | Prevents multi-turn contextual leakage and prompt priming. |
| **Retrieval Control** | Integrated web search and retrieval plug-ins disabled | Restricts evaluation strictly to frozen parametric weights. |
| **Timing & Logging** | Wall-clock latency (seconds), output token count, interface screenshots | Captures operational efficiency and provides audit trail (`raw_logs/`). |
| **Blinding & Scoring** | Double-blind masking (`Model_A`, `Model_B`, `Model_C`); Cohen's $\kappa$ evaluation on 50 items | Eliminates annotator brand preconceptions; verifies measurement reliability. |

---

## Section 5: Main Results

Table 2 presents the overall descriptive metrics for all evaluated models across the 90 benchmark items. OpenAI GPT-6 achieved the highest overall factual accuracy at 81.1% (95% bootstrap CI: [73.3%, 88.9%]), followed by Google Gemini 3.8 Flash at 72.2% (95% CI: [63.3%, 81.1%]), and Anthropic Claude Haiku 4.5 at 67.8% (95% CI: [57.8%, 76.7%]). Error breakdowns revealed that Claude Haiku 4.5 exhibited both the highest hallucination rate (15.6% [8.9%, 23.3%]) and outdated knowledge rate (11.1% [5.6%, 17.8%]), whereas GPT-6 maintained the lowest failure rates (7.8% hallucination, 5.6% outdated). Epistemic abstentions remained low across all three models (5.6% to 6.7%), demonstrating that models preferred asserting unverified claims over expressing uncertainty.

To test Hypothesis 1 regarding between-model accuracy differences under our matched repeated-measures design, we conducted Cochran's Q test across the 90 items. The omnibus test demonstrated a statistically significant overall difference in accuracy across the three models ($Q = 6.788$, $df = 2$, $p = 0.0336 < 0.05$). Post-hoc pairwise McNemar tests with Holm-Bonferroni correction indicated that GPT-6 outperformed Claude Haiku 4.5 with an absolute accuracy margin of $\Delta A = +13.3\%$ (paired 95% bootstrap CI: [+3.3%, +23.3%], 17 vs 5 discordant pairs, Odds Ratio = 3.40, unadjusted $p = 0.0169$, Holm-adjusted $p = 0.0507$). While the family-wise adjusted $p$-value sits right on the $\alpha = 0.05$ threshold due to conservative penalization over three comparisons, the practical effect size ($\Delta A > 10\%$) demonstrates a substantial operational advantage for the flagship model. Contrasts between GPT-6 and Gemini 3.8 Flash ($\Delta A = +8.9\%$ [0.0%, +18.9%], OR = 2.33, raw $p = 0.1153$, $p_{adj} = 0.2306$) and between Gemini 3.8 Flash and Claude Haiku 4.5 ($\Delta A = +4.4\%$ [-6.7%, +14.4%], OR = 1.40, raw $p = 0.5413$, $p_{adj} = 0.5413$) did not achieve statistical significance.

Regarding continuous efficiency, wall-clock generation latency differed drastically across architectures. A non-parametric Friedman test confirmed significant latency variance ($\chi^2 = 137.287$, $p = 1.54 \times 10^{-30}$). Claude Haiku 4.5 proved fastest with a median latency of 0.89 seconds (IQR: [0.77s, 1.03s]), followed by Gemini 3.8 Flash at 1.13 seconds (IQR: [0.90s, 1.27s]), whereas GPT-6 required 2.10 seconds (IQR: [1.81s, 2.43s]). Median output lengths ranged from 104 tokens for Gemini to 154 tokens for GPT-6. Inter-annotator agreement between Rater 1 and Rater 2 on the 50-item double-annotation validation sample yielded Cohen's $\kappa = 0.891$, confirming almost perfect agreement. Figure 1 illustrates overall accuracy and error mode distributions, while Figure 2 depicts subgroup performance across knowledge types.

*(Word count: 407 words — Target limit: 400–600 words, excluding tables)*

### Table 2. Overall Performance and Efficiency across Evaluated Frontier LLMs (N = 90 items per model)

| Model Name | Factual Accuracy ($A$) [95% Bootstrap CI] | Hallucination Rate ($H$) [95% Bootstrap CI] | Outdated Rate ($O$) [95% Bootstrap CI] | Abstention Rate ($Ab$) | Latency (Seconds) Median [IQR] | Output Tokens Median [IQR] |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **OpenAI GPT-6** | **81.1%** [73.3% – 88.9%] | **7.8%** [2.2% – 13.3%] | **5.6%** [1.1% – 11.1%] | 5.6% | 2.10 s [1.81 – 2.43 s] | 154 [137 – 174] |
| **Google Gemini 3.8 Flash** | **72.2%** [63.3% – 81.1%] | **12.2%** [5.6% – 18.9%] | **8.9%** [3.3% – 15.6%] | 6.7% | 1.13 s [0.90 – 1.27 s] | 104 [85 – 122] |
| **Anthropic Claude Haiku 4.5** | **67.8%** [57.8% – 76.7%] | **15.6%** [8.9% – 23.3%] | **11.1%** [5.6% – 17.8%] | 5.6% | 0.89 s [0.77 – 1.03 s] | 125 [109 – 138] |

### Table 3. Hypothesis 1: Post-Hoc Pairwise McNemar Tests with Holm-Bonferroni Correction (Matched Pairs, N = 90)

| Contrast Pair | Absolute Difference ($\Delta A$) [Paired 95% Bootstrap CI] | Discordant Pairs ($b / c$) | Odds Ratio ($OR$) | Unadjusted $p$-value | Holm-Adjusted $p$-value | Statistically Significant ($\alpha = 0.05$) | Practical Substantial Difference ($\Delta A \ge 10\%$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **GPT-6 vs Claude Haiku 4.5** | **+13.3%** [+3.3%, +23.3%] | 17 / 5 | 3.40 | 0.0169 | 0.0507 | Boundary ($p_{adj} \approx 0.05$) | **YES** ($\Delta A = +13.3\%$) |
| **GPT-6 vs Gemini 3.8 Flash** | **+8.9%** [0.0%, +18.9%] | 14 / 6 | 2.33 | 0.1153 | 0.2306 | NO | NO |
| **Gemini 3.8 Flash vs Claude Haiku 4.5** | **+4.4%** [-6.7%, +14.4%] | 14 / 10 | 1.40 | 0.5413 | 0.5413 | NO | NO |

*Omnibus Cochran's Q test: $Q = 6.788$, $df = 2$, $p = 0.0336$ (Statistically significant overall accuracy difference).*  
*Continuous Latency Friedman test: $\chi^2 = 137.287$, $df = 2$, $p = 1.54 \times 10^{-30}$ (Significant latency separation across architectures).*

---

## Section 9: Reproducibility Statement and Repository Link

The complete benchmark data, raw logs, evaluation scripts, and replication code are published in our public GitHub repository: `https://github.com/duesenbek/rmt-assignment-4` under the official release tag `assignment-4`. 

The repository contains the untouched test dataset `nlp_benchmark_ground_truth_90.csv`, whose SHA-256 checksum (`021f16fa64b654a3fa3566677ac9ac2ce4d78116011135bd339ff3286c6b0968`) matches the frozen protocol registered in Appendix A. It also includes `raw_logs/raw_generations_270.csv` with verbatim model responses, interface screenshots, and per-query timestamps, alongside double-blind annotation files and the replication script `reproduce_results.py`. Running `python reproduce_results.py` under standard Python 3.10+ environments with dependencies installed from `requirements.txt` recomputes all reported descriptive metrics, 10,000-sample bootstrap confidence intervals, Cochran's Q test, McNemar-Holm pairwise contrasts, subgroup Chi-Square tests, and generation latency distributions, regenerating both analytical charts in `analysis_output/` within five seconds without network dependencies.

*(Word count: 114 words — Target limit: 100–150 words)*
