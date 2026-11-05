"""
Automated Model Response Harvesting Pipeline for Assignment 4
Student: Bekzat Duisenbek (SE-2417)
Course: Research Methods and Tools (RMT) — Astana IT University

Queries target frontier LLMs via OpenRouter API under strict zero-shot
parametric conditions (no web retrieval plugins or tools attached).
All 270 responses are collected sequentially with verifiable Server Generation IDs.
"""

import os
import sys
import time
import json
import argparse
import urllib.request
import urllib.error
import pandas as pd

# Target models configuration
MODELS = {
    'Claude Haiku 4.5': {
        'id': 'anthropic/claude-haiku-4.5',
        'max_tokens': 300,
    },
    'Gemini 3.8 Flash': {
        'id': 'google/gemini-3.8-flash',
        'max_tokens': 600,  # Accommodates reasoning tokens
    },
    'GPT-6': {
        'id': 'openai/gpt-6-sol',
        'max_tokens': 300,
    }
}

PROMPT_TEMPLATE = (
    "Answer the following factual question about NLP research as accurately and concisely as possible. "
    "Give the direct answer and, if useful, one brief explanation. Do not use web browsing or external retrieval. "
    "If you do not know the answer or cannot determine whether it is current, state that uncertainty rather than guessing. "
    "Question: {question}"
)

API_URL = "https://openrouter.ai/api/v1/chat/completions"


def query_single_model(model_name, model_cfg, prompt, api_key, max_retries=5):
    """
    Sends a single-turn completion request to OpenRouter with automatic backoff retry.
    Web search/retrieval plugins are strictly excluded to enforce parametric evaluation.
    """
    payload = {
        "model": model_cfg["id"],
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": model_cfg["max_tokens"],
        "temperature": 0.0
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://aitu.edu.kz",
        "X-Title": "AITU NLP Benchmark Study"
    }

    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers
    )

    for attempt in range(max_retries):
        t0 = time.time()
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                latency = time.time() - t0
                data = json.loads(resp.read().decode("utf-8"))
                choice = data["choices"][0]["message"]
                content = choice.get("content", "")
                if content is None:
                    content = ""
                usage = data.get("usage", {})
                total_tokens = usage.get("total_tokens", 0)
                gen_id = data.get("id", "")
                return {
                    "success": True,
                    "content": content.strip(),
                    "latency": round(latency, 2),
                    "tokens": total_tokens,
                    "gen_id": gen_id
                }
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode("utf-8", errors="ignore")
            # If rate limited (429) or in-flight budget exhausted (402), back off and retry
            wait_time = 5.0 * (attempt + 1)
            if "in_flight_budget" in err_msg or "Rate limit" in err_msg or e.code in [402, 429, 500, 502, 503]:
                print(f" [Retry {attempt + 1}/{max_retries} waiting {wait_time:.0f}s]", end=" ", flush=True)
                time.sleep(wait_time)
                continue
            return {"success": False, "error": f"HTTP {e.code}: {err_msg}"}
        except Exception as e:
            wait_time = 4.0 * (attempt + 1)
            time.sleep(wait_time)
            continue

    return {"success": False, "error": "Exceeded max retries"}


def main():
    parser = argparse.ArgumentParser(description="Harvest LLM answers for NLP benchmark.")
    parser.add_argument("--api-key", default=None, help="OpenRouter API key")
    parser.add_argument("--benchmark", default="nlp_benchmark_ground_truth_90.csv", help="Benchmark CSV path")
    parser.add_argument("--output", default="raw_logs/raw_generations_270.csv", help="Output CSV path")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay in seconds between requests")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("[-] Error: OpenRouter API key not found.")
        sys.exit(1)

    df_bm = pd.read_csv(args.benchmark)
    total_questions = len(df_bm)

    print("=" * 70)
    print("  OPENROUTER AUTOMATED 270-TRIAL SEQUENTIAL HARVESTING PIPELINE")
    print("=" * 70)
    print(f"[+] Loaded {total_questions} questions (270 total queries)")
    print(f"[+] Target models: {list(MODELS.keys())}")
    print(f"[+] Output path: {args.output}")
    print(f"[+] Inter-request delay: {args.delay}s (strictly avoids rate-limit locks)\n")

    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    completed_keys = set()
    records = []
    if os.path.exists(args.output):
        try:
            prev_df = pd.read_csv(args.output)
            for _, r in prev_df.iterrows():
                completed_keys.add((r["Question_ID"], r["Model_Name"]))
                records.append(r.to_dict())
            print(f"[+] Resuming from {len(completed_keys)} previously completed trials.")
        except Exception:
            pass

    trial_counter = len(records) + 1
    t_start = time.time()

    for idx, row in df_bm.iterrows():
        qid = row["Question_ID"]
        q_text = row.get("Prompt_Question") if "Prompt_Question" in row else row.get("Question_Text", "")
        prompt = PROMPT_TEMPLATE.format(question=q_text)

        print(f"[{idx + 1}/{total_questions}] Question {qid}:")

        for m_name, cfg in MODELS.items():
            if (qid, m_name) in completed_keys:
                print(f"   -> {m_name}: Already completed (skipping)")
                continue

            trial_id = f"T{trial_counter:03d}"
            print(f"   [{trial_id}] Querying {m_name}...", end=" ", flush=True)

            res = query_single_model(m_name, cfg, prompt, api_key)

            if res["success"]:
                print(f"OK ({res['latency']}s, {res['tokens']} toks, ID: {res['gen_id']})")
                rec = {
                    "Trial_ID": trial_id,
                    "Question_ID": qid,
                    "Model_Name": m_name,
                    "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    "Latency_Seconds": res["latency"],
                    "Output_Tokens": res["tokens"],
                    "Generation_ID": res["gen_id"],
                    "Raw_Response_Text": res["content"]
                }
                records.append(rec)
                completed_keys.add((qid, m_name))
                trial_counter += 1

                # Save checkpoint immediately
                temp_df = pd.DataFrame(records)
                temp_df.to_csv(args.output, index=False, encoding="utf-8")
            else:
                print(f"FAILED: {res.get('error')}")

            time.sleep(args.delay)

    total_time = round(time.time() - t_start, 2)
    print(f"\n[+] Pipeline finished in {total_time}s. Total saved records: {len(records)} in {args.output}")


if __name__ == "__main__":
    main()
