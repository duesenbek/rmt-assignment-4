# Contribution: Ivan Kuznetsov (Sections 1, 2, 10 & Dataset Hash) — Fully Rectified

**Author:** Ivan Kuznetsov (SE-2417)  
**Role:** Protocol Freeze & Input Data Lead  
**Dataset SHA-256 Hash:** `021f16fa64b654a3fa3566677ac9ac2ce4d78116011135bd339ff3286c6b0968`  
**File:** `nlp_benchmark_ground_truth_90.csv` (90 items: 30 Stable, 30 Historical, 30 Changing)

---

## Section 1: Final / Revised Research Title
**Evaluating Hallucinations and Outdated Knowledge in LLM Answers to NLP Research Questions**

---

## Section 2: Primary Research Question, Aim, Objectives, and Hypotheses

### Primary Research Question
How do three selected frontier LLMs (OpenAI GPT-6, Anthropic Claude Haiku 4.5, and Google Gemini 3.8 Flash) differ in factual accuracy and rates of hallucination and outdated information across stable, historical, and changing NLP research facts without external retrieval?

### Research Aim
To rigorously quantify and compare the factual accuracy, hallucination rates, and temporal knowledge obsolescence of three contemporary frontier LLMs across stable foundations, historical milestones, and dynamic benchmark facts under zero-shot parametric conditions.

### Research Objectives
* **O1.** To construct a standardized, peer-reviewed 90-item NLP research benchmark stratified into 30 Stable Factual items, 30 Historical items, and 30 Changing items with documented historical baselines (Old Values), current states (New Values), verified transition dates, and a strict numerical tolerance margin of $\pm 0.5\%$.
* **O2.** To harvest and double-blind annotate 270 independent zero-shot model responses (90 items × 3 models) across mutually exclusive error categories: strict correctness ($A$), hallucinations ($H$), outdated knowledge ($O$), and epistemic abstentions ($Ab$).
* **O3.** To evaluate inter-annotator concordance using Cohen’s kappa ($\kappa$) across the independent human annotation passes.
* **O4.** To statistically test between-model accuracy disparities across the matched 90 items ($H_1$) using Cochran's Q test and pairwise McNemar's tests with Holm-Bonferroni correction.
* **O5.** To determine within-model performance hierarchies across factual categories ($H_2$) via Pearson's $\chi^2$ and Fisher's exact tests on independent sub-samples, isolating the vulnerability of parametric memory to dynamic knowledge degradation.

### Research Hypotheses
* **H1 (Between-Model Accuracy Difference — Matched Design):** Factual accuracy ($A$) will differ significantly among the three selected frontier LLMs (OpenAI GPT-6, Anthropic Claude Haiku 4.5, Google Gemini 3.8 Flash) across the standardized 90-item NLP research benchmark.
* **H2 (Tripartite Factual Sensitivity Hierarchy — Independent Sub-Samples):** Within each evaluated model, factual accuracy will exhibit a systematic performance degradation hierarchy: $\text{Accuracy}_{\text{Stable}} \approx \text{Accuracy}_{\text{Historical}} > \text{Accuracy}_{\text{Changing}}$. Specifically, outdated knowledge errors ($O = 1$) will be concentrated almost exclusively within the Changing Facts partition ($O_{\text{Changing}} \gg O_{\text{Historical}} \approx 0$).

---

## Section 10: References (Primary Dataset & Theoretical Grounding)

1. Ainslie, J., Lee-Thorp, J., de Jong, M., Zemlyanskiy, Y., Lebrón, F., & Sanghai, S. (2023). GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints. *Proceedings of EMNLP 2023*, 4895–4901.
2. Ba, J. L., Kiros, J. R., & Hinton, G. E. (2016). Layer Normalization. *arXiv preprint arXiv:1607.06450*.
3. Bai, Y., Kadavath, S., Kundu, S., Askell, A., Kernion, J., Jones, A., ... & Kaplan, J. (2022). Constitutional AI: Harmlessness from AI Feedback. *arXiv preprint arXiv:2212.08073*.
4. Bengio, Y., Ducharme, R., Vincent, P., & Jauvin, C. (2003). A Neural Probabilistic Language Model. *Journal of Machine Learning Research (JMLR)*, 3, 1137–1155.
5. Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J. D., Dhariwal, P., ... & Amodei, D. (2020). Language Models are Few-Shot Learners. *Advances in Neural Information Processing Systems (NeurIPS 2020)*, 33, 1877–1901.
6. Chen, M., Tworek, J., Jun, H., Yuan, Q., Pinto, H. P. d. O., Kaplan, J., ... & Zaremba, W. (2021). Evaluating Large Language Models Trained on Code. *arXiv preprint arXiv:2107.03374*.
7. Chowdhery, A., Narang, S., Devlin, J., Bosma, M., Mishra, G., Roberts, A., ... & Fiedel, N. (2023). PaLM: Scaling Language Modeling with Pathways. *Journal of Machine Learning Research (JMLR)*, 24(240), 1–113.
8. Clark, P., Cowhey, I., Etzioni, O., Khot, T., Sabharwal, A., Schoenick, C., & Tafjord, O. (2018). Think you have Solved Question Answering? Try ARC, the AI2 Reasoning Challenge. *arXiv preprint arXiv:1803.05457*.
9. Conneau, A., Khandelwal, K., Goyal, N., Chaudhary, V., Wenzek, G., Guzmán, F., ... & Stoyanov, V. (2020). Unsupervised Cross-lingual Representation Learning at Scale. *Proceedings of ACL 2020*, 8440–8451.
10. Dao, T., Fu, D., Ermon, S., Rudra, A., & Ré, C. (2022). FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness. *Advances in Neural Information Processing Systems (NeurIPS 2022)*, 35, 16344–16359.
11. Devlin, J., Chang, M. W., Lee, K., & Toutanova, K. (2019). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. *Proceedings of NAACL-HLT 2019*, 4171–4186.
12. Dua, D., Wang, Y., Dasigi, P., Stanovsky, G., Singh, S., & Gardner, M. (2019). DROP: A Reading Comprehension Benchmark Requiring Discrete Reasoning Over Paragraphs. *Proceedings of NAACL-HLT 2019*, 2368–2378.
13. Dubey, A., Jauhri, A., Pandey, A., Kadian, A., Al-Dahle, A., Letman, A., ... & Ganapathy, A. (2024). The Llama 3 Herd of Models. *arXiv preprint arXiv:2407.21783*.
14. He, P., Liu, X., Gao, J., & Chen, W. (2021). DeBERTa: Decoding-enhanced BERT with Disentangled Attention. *International Conference on Learning Representations (ICLR 2021)*.
15. Hendrycks, D., & Gimpel, K. (2016). Gaussian Error Linear Units (GELUs). *arXiv preprint arXiv:1606.08415*.
16. Hendrycks, D., Burns, C., Kadavath, S., Arora, A., Basart, S., Tang, E., ... & Steinhardt, J. (2021). Measuring Mathematical Problem Solving With the MATH Dataset. *NeurIPS 2021 Datasets and Benchmarks Track*.
17. Hoffmann, J., Borgeaud, S., Mensch, A., Buchatskaya, E., Cai, T., Rutherford, E., ... & Sifre, L. (2022). Training Compute-Optimal Large Language Models. *Advances in Neural Information Processing Systems (NeurIPS 2022)*, 35, 30016–30030.
18. Holtzman, A., Buys, J., Du, L., Forbes, M., & Choi, Y. (2020). The Curious Case of Neural Text Degeneration. *International Conference on Learning Representations (ICLR 2020)*.
19. Hu, E. J., Shen, Y., Wallis, P., Allen-Zhu, Z., Li, Y., Wang, S., Wang, L., & Chen, W. (2022). LoRA: Low-Rank Adaptation of Large Language Models. *International Conference on Learning Representations (ICLR 2022)*.
20. Jain, N., Han, K., Gu, A., Li, W. D., Yan, F., Tian, T. H., ... & Stoica, I. (2024). LiveCodeBench: Holistic and Contamination-Free Evaluation of Large Language Models for Code. *arXiv preprint arXiv:2403.07974*.
21. Jiang, A. Q., Sablayrolles, A., Mensch, A., Bamford, C., Chaplot, D. S., Casas, D. d. l., ... & Sayed, W. E. (2023). Mistral 7B. *arXiv preprint arXiv:2310.06825*.
22. Jimenez, C. E., Yang, J., Wettig, A., Yao, S., Pei, K., Press, O., & Narasimhan, K. (2024). SWE-bench: Can Language Models Resolve Real-World GitHub Issues? *International Conference on Learning Representations (ICLR 2024)*.
23. Koehn, P., Och, F. J., & Marcu, D. (2003). Statistical Phrase-Based Translation. *Proceedings of HLT-NAACL 2003*, 48–54.
24. Kudo, T., & Richardson, J. (2018). SentencePiece: A simple and language independent subword tokenizer and detokenizer for Neural Text Processing. *Proceedings of EMNLP 2018: System Demonstrations*, 66–71.
25. Liu, Y., Ott, M., Goyal, N., Du, J., Joshi, M., Chen, D., ... & Stoyanov, V. (2019). RoBERTa: A Robustly Optimized BERT Pretraining Approach. *arXiv preprint arXiv:1907.11692*.
26. Mikolov, T., Chen, K., Corrado, G., & Dean, J. (2013). Efficient Estimation of Word Representations in Vector Space. *International Conference on Learning Representations (ICLR 2013 Workshop)*.
27. OpenAI. (2023). GPT-4 Technical Report. *arXiv preprint arXiv:2303.08774*.
28. OpenAI. (2024). Learning to Reason with LLMs (OpenAI o1 System Card). *OpenAI Technical Announcement*.
29. Papineni, K., Roukos, S., Ward, T., & Zhu, W. J. (2002). BLEU: A Method for Automatic Evaluation of Machine Translation. *Proceedings of ACL 2002*, 311–318.
30. Peters, M. E., Neumann, M., Iyyer, M., Gardner, M., Clark, C., Lee, K., & Zettlemoyer, L. (2018). Deep Contextualized Word Representations. *Proceedings of NAACL-HLT 2018*, 2227–2237.
31. Radford, A., Narasimhan, K., Salimans, T., & Sutskever, I. (2018). Improving Language Understanding by Generative Pre-Training. *OpenAI Technical Report*.
32. Raffel, C., Shazeer, N., Roberts, A., Lee, K., Narang, S., Matena, M., ... & Liu, P. J. (2020). Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer. *Journal of Machine Learning Research (JMLR)*, 21(140), 1–67.
33. Rajpurkar, P., Zhang, J., Lopyrev, K., & Liang, P. (2016). SQuAD: 100,000+ Questions for Machine Comprehension of Text. *Proceedings of EMNLP 2016*, 2383–2392.
34. Sennrich, R., Haddow, B., & Birch, A. (2016). Neural Machine Translation of Rare Words with Subword Units. *Proceedings of ACL 2016*, 1715–1725.
35. Shazeer, N. (2019). Fast Transformer Decoding: One Write-Head is All You Need. *arXiv preprint arXiv:1911.02150*.
36. Shazeer, N. (2020). GLU Variants Improve Transformer. *arXiv preprint arXiv:2002.05202*.
37. Touvron, H., Lavril, T., Izacard, G., Martinet, X., Lachaux, M. A., Lacroix, T., ... & Lample, G. (2023). LLaMA: Open and Efficient Foundation Language Models. *arXiv preprint arXiv:2302.13971*.
38. Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). Attention Is All You Need. *Advances in Neural Information Processing Systems (NeurIPS 2017)*, 30, 5998–6008.
39. Wang, A., Singh, A., Michael, J., Hill, F., Levy, O., & Bowman, S. R. (2018). GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding. *ICLR 2019 / EMNLP 2018 Workshop*.
40. Wang, A., Pruksachatkun, Y., Nangia, N., Singh, A., Michael, J., Hill, F., Levy, O., & Bowman, S. R. (2019). SuperGLUE: A Stickier Benchmark for General-Purpose Language Understanding Systems. *Advances in Neural Information Processing Systems (NeurIPS 2019)*, 32, 3266–3280.
41. Wang, Y., Ma, X., Zhang, G., Ni, Y., Chandra, A., Guo, S., ... & Chen, W. (2024). MMLU-Pro: A More Robust and Challenging Multi-Task Language Understanding Benchmark. *arXiv preprint arXiv:2406.01574*.
