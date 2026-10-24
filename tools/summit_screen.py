"""Local screen that imitates Summit's difficulty check.

Each attempt is one independent headless Claude Code run: the figure goes in as an image block and the
stem as text in a single user message (no image block when --image is omitted), no tools, a plain solver system prompt, the chosen model and
reasoning effort. The JSON result gives the stop reason, the output tokens (thinking included) and the
answer text. An attempt is a cut-off when it stops on max_tokens or gives no FINAL ANSWER line, or when
its output tokens exceed --cap (so one uncapped batch can be rescored at any cap afterwards).

Usage:
  python3 summit_screen.py --label v11 --stem stem.txt --image image.png --key 27 --n 5 \
      [--model claude-opus-5-5] [--effort high] [--cap 64000] [--out results.jsonl]
"""
import argparse, base64, json, os, re, subprocess, sys, time, pathlib, concurrent.futures as cf

CLAUDE = os.environ.get("CLAUDE_CODE_EXECPATH", "claude")
SYSTEM = ("You are an expert solving a graduate-level problem. The problem refers to the attached figure. "
          "Work the problem out carefully and completely, then end your reply with one line of the form "
          "FINAL ANSWER: <answer>.")

def attempt(args, i):
    content = []
    if args.image:   # text-only tasks (Summit opened them for Math and Bio/Medicine on 2026-10-24) pass no image
        img = base64.b64encode(pathlib.Path(args.image).read_bytes()).decode()
        content.append({"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": img}})
    content.append({"type": "text", "text": pathlib.Path(args.stem).read_text()})
    msg = {"type": "user", "message": {"role": "user", "content": content}}
    system = SYSTEM if args.image else SYSTEM.replace("The problem refers to the attached figure. ", "")
    cmd = [CLAUDE, "-p", "--model", args.model, "--effort", args.effort, "--system-prompt", system,
           "--tools", "", "--input-format", "stream-json", "--output-format", "stream-json", "--verbose", "--max-turns", "1"]
    env = dict(os.environ)
    if args.hard_cap: env["CLAUDE_CODE_MAX_OUTPUT_TOKENS"] = str(args.hard_cap)
    t0 = time.time()
    try:
        p = subprocess.run(cmd, input=json.dumps(msg) + "\n", capture_output=True, text=True, env=env, timeout=args.timeout)
    except subprocess.TimeoutExpired:
        return dict(label=args.label, attempt=i, stop="timeout", out_tokens=10**9, thinking=None, seconds=args.timeout, answer=None, error=False, tail="killed at timeout: still thinking past the Summit-size budget")
    dt = time.time() - t0
    d = None
    for line in p.stdout.splitlines():
        try: j = json.loads(line)
        except Exception: continue
        if j.get("type") == "result": d = j
    if d is None: d = {"result": "", "stop_reason": "run_error", "is_error": True, "stderr": p.stderr[-500:]}
    mu = (d.get("modelUsage") or {}).get(args.model, {})
    out_tok = mu.get("outputTokens") or (d.get("usage") or {}).get("output_tokens", 0)
    text = d.get("result") or ""
    m = re.findall(r"FINAL ANSWER:\s*\$?([^\n$]*)", text)
    ans = m[-1].strip().rstrip(".") if m else None
    return dict(label=args.label, attempt=i, stop=d.get("stop_reason"), out_tokens=out_tok,
                thinking=mu.get("thinkingTokens"), seconds=round(dt), answer=ans, error=d.get("is_error"),
                tail=text[-400:])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True); ap.add_argument("--stem", required=True); ap.add_argument("--image", default="", help="omit for a text-only task")
    ap.add_argument("--key", required=True); ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--model", default="claude-opus-5-5"); ap.add_argument("--effort", default="max")
    ap.add_argument("--cap", type=int, default=128000, help="score attempts above this many output tokens as cut-offs")
    ap.add_argument("--hard-cap", type=int, default=0, help="set CLAUDE_CODE_MAX_OUTPUT_TOKENS for the run")
    ap.add_argument("--timeout", type=int, default=600); ap.add_argument("--out", default="screen_results.jsonl")
    args = ap.parse_args()
    res = []
    with cf.ThreadPoolExecutor(args.n) as ex:
        for fut in cf.as_completed([ex.submit(attempt, args, i) for i in range(1, args.n + 1)]):
            r = fut.result(); res.append(r)
            with open(args.out, "a") as f: f.write(json.dumps(r) + "\n")
            print(f"done #{r['attempt']} {r['seconds']}s answer={r['answer']}", flush=True)
    ok = cut = 0
    for r in res:
        if r["stop"] == "run_error":
            print(f"{r['label']} #{r['attempt']}: RUN ERROR, not counted"); continue
        is_cut = r["stop"] == "max_tokens" or r["answer"] is None or (args.cap and r["out_tokens"] > args.cap)
        def norm(a):
            a = a.replace(" ", "").replace("\u2212", "-").replace("$", "").rstrip(".")
            try: return float(a)
            except ValueError: return a
        right = (not is_cut) and norm(r["answer"]) == norm(args.key)
        ok += right; cut += is_cut
        print(f"{r['label']} #{r['attempt']}: answer={r['answer']} stop={r['stop']} out_tokens={r['out_tokens']} thinking={r['thinking']} {r['seconds']}s {'CUT' if is_cut else ('RIGHT' if right else 'WRONG')}")
    print(f"{args.label}: correct {ok}/{args.n}, cut-offs {cut}" + (f" (cap {args.cap})" if args.cap else ""))

if __name__ == "__main__":
    main()
