#!/usr/bin/env python3
"""
Benchmark different session context formats

This script compares JSON, optimized JSON, and MessagePack formats
for size, parsing speed, and token efficiency.
"""

import json
import time
from pathlib import Path
from typing import Dict, Any
import sys

try:
    import msgpack
    HAS_MSGPACK = True
except ImportError:
    HAS_MSGPACK = False

from optimized_json import OptimizedJSONContext


def estimate_tokens(text: str) -> int:
    """Rough token estimate (4 chars per token)"""
    return len(text) // 4


def benchmark_json_pretty(data: Dict[str, Any]) -> Dict[str, Any]:
    """Benchmark pretty JSON"""
    # Serialize
    start = time.time()
    serialized = json.dumps(data, indent=2)
    serialize_time = time.time() - start

    # Deserialize
    start = time.time()
    _ = json.loads(serialized)
    deserialize_time = time.time() - start

    return {
        'format': 'JSON (pretty)',
        'size_bytes': len(serialized),
        'size_kb': round(len(serialized) / 1024, 2),
        'tokens': estimate_tokens(serialized),
        'serialize_ms': round(serialize_time * 1000, 2),
        'deserialize_ms': round(deserialize_time * 1000, 2)
    }


def benchmark_json_minified(data: Dict[str, Any]) -> Dict[str, Any]:
    """Benchmark minified JSON"""
    # Serialize
    start = time.time()
    serialized = json.dumps(data, separators=(',', ':'))
    serialize_time = time.time() - start

    # Deserialize
    start = time.time()
    _ = json.loads(serialized)
    deserialize_time = time.time() - start

    return {
        'format': 'JSON (minified)',
        'size_bytes': len(serialized),
        'size_kb': round(len(serialized) / 1024, 2),
        'tokens': estimate_tokens(serialized),
        'serialize_ms': round(serialize_time * 1000, 2),
        'deserialize_ms': round(deserialize_time * 1000, 2)
    }


def benchmark_optimized_json(data: Dict[str, Any]) -> Dict[str, Any]:
    """Benchmark optimized JSON"""
    optimizer = OptimizedJSONContext()

    # Optimize
    start = time.time()
    optimized = optimizer.optimize(data)
    serialized = json.dumps(optimized, separators=(',', ':'))
    serialize_time = time.time() - start

    # Normalize
    start = time.time()
    _ = optimizer.normalize(json.loads(serialized))
    deserialize_time = time.time() - start

    return {
        'format': 'JSON (optimized)',
        'size_bytes': len(serialized),
        'size_kb': round(len(serialized) / 1024, 2),
        'tokens': estimate_tokens(serialized),
        'serialize_ms': round(serialize_time * 1000, 2),
        'deserialize_ms': round(deserialize_time * 1000, 2)
    }


def benchmark_messagepack(data: Dict[str, Any]) -> Dict[str, Any]:
    """Benchmark MessagePack"""
    if not HAS_MSGPACK:
        return {'format': 'MessagePack', 'error': 'Not installed (pip install msgpack)'}

    # Serialize
    start = time.time()
    serialized = msgpack.packb(data, use_bin_type=True)
    serialize_time = time.time() - start

    # Deserialize
    start = time.time()
    _ = msgpack.unpackb(serialized, raw=False)
    deserialize_time = time.time() - start

    return {
        'format': 'MessagePack',
        'size_bytes': len(serialized),
        'size_kb': round(len(serialized) / 1024, 2),
        'tokens': 'N/A (binary)',
        'serialize_ms': round(serialize_time * 1000, 2),
        'deserialize_ms': round(deserialize_time * 1000, 2)
    }


def print_results(results: list):
    """Print benchmark results in a table"""
    print("\n" + "=" * 80)
    print("BENCHMARK RESULTS")
    print("=" * 80)

    # Header
    print(f"\n{'Format':<20} {'Size':<12} {'Tokens':<10} {'Serialize':<12} {'Deserialize':<12}")
    print("-" * 80)

    baseline_size = results[0]['size_bytes']
    baseline_tokens = results[0]['tokens']

    for result in results:
        if 'error' in result:
            print(f"{result['format']:<20} {result['error']}")
            continue

        # Calculate percentages
        size_pct = (result['size_bytes'] / baseline_size) * 100
        if isinstance(result['tokens'], int):
            token_pct = (result['tokens'] / baseline_tokens) * 100
            tokens_str = f"{result['tokens']} ({token_pct:.0f}%)"
        else:
            tokens_str = result['tokens']

        print(f"{result['format']:<20} "
              f"{result['size_kb']} KB ({size_pct:.0f}%)  "
              f"{tokens_str:<10} "
              f"{result['serialize_ms']} ms     "
              f"{result['deserialize_ms']} ms")

    print("\n" + "=" * 80)

    # Savings summary
    if len(results) >= 3:
        opt_result = results[2]  # Optimized JSON
        size_saved = baseline_size - opt_result['size_bytes']
        size_saved_pct = (size_saved / baseline_size) * 100

        if isinstance(opt_result['tokens'], int):
            tokens_saved = baseline_tokens - opt_result['tokens']
            tokens_saved_pct = (tokens_saved / baseline_tokens) * 100

            print(f"\n💡 Optimized JSON saves:")
            print(f"   - {size_saved_pct:.1f}% size ({size_saved} bytes)")
            print(f"   - {tokens_saved_pct:.1f}% tokens ({tokens_saved} tokens)")
            print(f"   - ~${tokens_saved * 0.00001:.4f} per read (GPT-4 prices)")


def main():
    """Run benchmarks"""
    # Load sample data
    sample_file = Path("../examples/02_multi_session.json")
    if not sample_file.exists():
        sample_file = Path("examples/02_multi_session.json")

    if not sample_file.exists():
        print("Error: Sample file not found. Run from repo root or experimental/ directory.")
        sys.exit(1)

    with open(sample_file, 'r') as f:
        data = json.load(f)

    print("Running benchmarks on sample session context...")
    print(f"Sessions: {len(data.get('sessions', []))}")

    # Run benchmarks
    results = [
        benchmark_json_pretty(data),
        benchmark_json_minified(data),
        benchmark_optimized_json(data),
        benchmark_messagepack(data),
    ]

    print_results(results)

    print("\n📊 Recommendation for LLM agents: Use Optimized JSON")
    print("   - Best token efficiency")
    print("   - Native LLM compatibility")
    print("   - Significant cost savings")


if __name__ == "__main__":
    main()
