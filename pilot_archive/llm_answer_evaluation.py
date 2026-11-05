#!/usr/bin/env python3

import argparse, csv, sys
from pathlib import Path
from collections import defaultdict

import matplotlib.pyplot as plt

GT_REQUIRED = ["Question_ID", "Temporal_Type", "Prompt_Question", "Ground_Truth_Answer", "Reference_Source", "Cutoff_Date"]
ANS_REQUIRED = ["Question_ID", "Model_ID", "Answer_Text", "Fully_Correct", "Hallucination", "Outdated", "Unresolved", "Abstention", "Annotation_Notes"]
BINARY = ["Fully_Correct", "Hallucination", "Outdated", "Unresolved", "Abstention"]

def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def validate(gt_path, ans_path):
    gt = read_csv(gt_path); ans = read_csv(ans_path)
    if not gt: raise ValueError("Ground-truth CSV has no questions.")
    if not ans: raise ValueError("Answers CSV has no annotated answer rows. Collect and annotate real model answers first.")
    with open(gt_path, encoding="utf-8-sig", newline="") as f: gt_fields = csv.DictReader(f).fieldnames or []
    with open(ans_path, encoding="utf-8-sig", newline="") as f: ans_fields = csv.DictReader(f).fieldnames or []
    missing = [x for x in GT_REQUIRED if x not in gt_fields]
    if missing: raise ValueError("Ground-truth file missing columns: " + ", ".join(missing))
    missing = [x for x in ANS_REQUIRED if x not in ans_fields]
    if missing: raise ValueError("Answers file missing columns: " + ", ".join(missing))
    gt_by_id = {r["Question_ID"]: r for r in gt}
    if len(gt_by_id) != len(gt): raise ValueError("Duplicate Question_ID in ground-truth file.")
    seen = set()
    for i, row in enumerate(ans, start=2):
        qid, model = row["Question_ID"].strip(), row["Model_ID"].strip()
        if qid not in gt_by_id: raise ValueError(f"Answers CSV row {i}: unknown Question_ID {qid!r}.")
        if not model: raise ValueError(f"Answers CSV row {i}: Model_ID is required.")
        key=(qid,model)
        if key in seen: raise ValueError(f"Duplicate answer for question/model pair {key}.")
        seen.add(key)
        if not row["Answer_Text"].strip(): raise ValueError(f"Answers CSV row {i}: Answer_Text is empty.")
        for col in BINARY:
            if row[col].strip() not in ("0","1"):
                raise ValueError(f"Answers CSV row {i}: {col} must be 0 or 1 after human annotation.")
            row[col]=int(row[col])
        if row["Fully_Correct"] and (row["Hallucination"] or row["Outdated"] or row["Unresolved"] or row["Abstention"]):
            raise ValueError(f"Answers CSV row {i}: Fully_Correct=1 conflicts with an error/abstention/unresolved label.")
        row["Temporal_Type"] = gt_by_id[qid]["Temporal_Type"]
    return gt, ans

def aggregate(rows, keys):
    groups=defaultdict(list)
    for r in rows: groups[tuple(r[k] for k in keys)].append(r)
    out=[]
    for group, items in sorted(groups.items()):
        n=len(items); row={k:v for k,v in zip(keys,group)}; row["N_Answers"]=n
        for col, label in [("Fully_Correct","Accuracy"),("Hallucination","Hallucination_Rate"),("Outdated","Outdated_Rate"),("Unresolved","Unresolved_Rate"),("Abstention","Abstention_Rate")]:
            count=sum(x[col] for x in items)
            row[label+"_N"]=count
            row[label]=round(count/n,4) if n else 0
        out.append(row)
    return out

def write_csv(path, rows):
    if not rows: return
    with open(path,"w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

def plot(summary, path):
    models=[r["Model_ID"] for r in summary if r.get("Temporal_Type","ALL")=="ALL"]
    if not models:
        print("Chart skipped: summary has no overall model rows."); return
    measures=[("Accuracy","Fully correct"),("Hallucination_Rate","Hallucination"),("Outdated_Rate","Outdated information")]
    x=list(range(len(models))); width=0.24
    fig, ax=plt.subplots(figsize=(10,5.8))
    for i,(key,label) in enumerate(measures):
        vals=[next((r[key] for r in summary if r.get("Model_ID")==m and r.get("Temporal_Type","ALL")=="ALL"),0) for m in models]
        ax.bar([v+(i-1)*width for v in x], vals, width=width, label=label)
    ax.set_xticks(x); ax.set_xticklabels(models, rotation=15, ha="right")
    ax.set_ylim(0,1); ax.set_ylabel("Proportion of annotated answers")
    ax.set_title("Pilot comparison of annotated LLM answers")
    ax.legend(); ax.grid(axis="y", alpha=.25); fig.tight_layout(); fig.savefig(path,dpi=180); plt.close(fig)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--ground-truth", required=True, help="CSV with questions and reference answers")
    p.add_argument("--answers", required=True, help="CSV with real model responses and completed human labels")
    p.add_argument("--outdir", default="analysis_output", help="Output folder")
    args=p.parse_args(); out=Path(args.outdir); out.mkdir(parents=True,exist_ok=True)
    try: gt, answers=validate(args.ground_truth,args.answers)
    except (ValueError, OSError) as e:
        print("INPUT ERROR:",e,file=sys.stderr); return 2
    overall=aggregate(answers,["Model_ID"])
    by_type=aggregate(answers,["Model_ID","Temporal_Type"])
    write_csv(out/"summary_by_model.csv",overall)
    write_csv(out/"summary_by_model_and_type.csv",by_type)
    plot(overall,out/"model_comparison.png")
    print(f"Ground-truth questions loaded: {len(gt)}")
    print(f"Real annotated answer rows analyzed: {len(answers)}")
    print(f"Models represented: {', '.join(sorted({r['Model_ID'] for r in answers}))}")
    print(f"Outputs saved in: {out.resolve()}")
    print("Rates are descriptive summaries of the submitted annotations, not automated fact-checking.")
    print("For a full 60-question design, extend/verify the dataset and collect the planned model answers before drawing general conclusions.")
    return 0
if __name__=="__main__": raise SystemExit(main())
