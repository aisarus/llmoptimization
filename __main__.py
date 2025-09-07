import argparse
from .cost import estimate_cost, Pricing
from .text_stats import count_tokens, split_into_chunks

def main():
    p = argparse.ArgumentParser(prog="efmcalc", description="Token & cost estimator")
    p.add_argument("--prompt", required=True, help="input text")
    p.add_argument("--resp", type=int, default=0, help="expected output tokens")
    p.add_argument("--in1k", type=float, default=0.5, help="USD per 1k input tokens")
    p.add_argument("--out1k", type=float, default=1.5, help="USD per 1k output tokens")
    p.add_argument("--chunk", type=int, default=0, help="optional chunk size; 0 = skip")
    args = p.parse_args()

    total_tokens, price = estimate_cost(args.prompt, args.resp, Pricing(args.in1k, args.out1k))
    print(f"tokens_total={total_tokens} price_usd={price}")
    if args.chunk > 0:
        for i, c in enumerate(split_into_chunks(args.prompt, args.chunk), 1):
            print(f"[chunk {i}] {c}")

if __name__ == "__main__":
    main()
