#!/usr/bin/env python3
"""
Token Conservation Test

This script measures actual token usage for different session-ctx formats
using real tokenizers (tiktoken for GPT models, approximation for others).

Install: pip install tiktoken
"""

import json
from pathlib import Path
from typing import Dict, Any
import sys

try:
    import tiktoken
    HAS_TIKTOKEN = True
except ImportError:
    HAS_TIKTOKEN = False
    print("WARNING: tiktoken not installed. Using approximation.")
    print("Install with: pip install tiktoken")
    print()

from optimized_json import OptimizedJSONContext


def count_tokens_gpt(text: str, model: str = "gpt-4") -> int:
    """Count tokens using OpenAI's tiktoken"""
    if not HAS_TIKTOKEN:
        # Rough approximation: 1 token ≈ 4 characters
        return len(text) // 4

    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


def count_tokens_claude(text: str) -> int:
    """Approximate token count for Claude (similar to GPT)"""
    if HAS_TIKTOKEN:
        # Claude uses similar tokenization to GPT
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))
    return len(text) // 4


def test_format(data: Dict[str, Any], format_name: str, json_str: str) -> Dict[str, Any]:
    """Test a specific format and return metrics"""

    # Count tokens for different models
    gpt4_tokens = count_tokens_gpt(json_str, "gpt-4")
    gpt35_tokens = count_tokens_gpt(json_str, "gpt-3.5-turbo")
    claude_tokens = count_tokens_claude(json_str)

    return {
        'format': format_name,
        'size_bytes': len(json_str.encode('utf-8')),
        'size_kb': round(len(json_str.encode('utf-8')) / 1024, 2),
        'tokens_gpt4': gpt4_tokens,
        'tokens_gpt35': gpt35_tokens,
        'tokens_claude': claude_tokens,
        'cost_gpt4_input': gpt4_tokens * 0.00001,  # $0.01 per 1K tokens
        'cost_gpt35_input': gpt35_tokens * 0.0000005,  # $0.0005 per 1K tokens
        'cost_claude_input': claude_tokens * 0.000003,  # $0.003 per 1K tokens
    }


def print_results(results: list, sessions: int):
    """Print detailed comparison results"""

    print("\n" + "=" * 90)
    print(f"TOKEN CONSERVATION TEST RESULTS ({sessions} sessions)")
    print("=" * 90)

    if not HAS_TIKTOKEN:
        print("\n⚠️  Using approximate token counts (install tiktoken for exact counts)")

    # Size and token comparison
    print(f"\n{'Format':<25} {'Size':<15} {'GPT-4':<15} {'GPT-3.5':<15} {'Claude':<15}")
    print("-" * 90)

    baseline = results[0]

    for result in results:
        size_pct = (result['size_bytes'] / baseline['size_bytes']) * 100
        gpt4_pct = (result['tokens_gpt4'] / baseline['tokens_gpt4']) * 100
        gpt35_pct = (result['tokens_gpt35'] / baseline['tokens_gpt35']) * 100
        claude_pct = (result['tokens_claude'] / baseline['tokens_claude']) * 100

        print(f"{result['format']:<25} "
              f"{result['size_kb']:>6.2f} KB ({size_pct:>5.1f}%)  "
              f"{result['tokens_gpt4']:>6} ({gpt4_pct:>5.1f}%)  "
              f"{result['tokens_gpt35']:>6} ({gpt35_pct:>5.1f}%)  "
              f"{result['tokens_claude']:>6} ({claude_pct:>5.1f}%)")

    # Cost comparison
    print("\n" + "=" * 90)
    print("COST PER CONTEXT READ (Input tokens only)")
    print("-" * 90)
    print(f"{'Format':<25} {'GPT-4':<20} {'GPT-3.5':<20} {'Claude':<20}")
    print("-" * 90)

    for result in results:
        print(f"{result['format']:<25} "
              f"${result['cost_gpt4_input']:.6f}         "
              f"${result['cost_gpt35_input']:.6f}         "
              f"${result['cost_claude_input']:.6f}")

    # Savings summary
    print("\n" + "=" * 90)
    print("SAVINGS WITH OPTIMIZED JSON")
    print("-" * 90)

    if len(results) >= 3:
        opt_result = results[2]  # Optimized JSON

        size_saved = baseline['size_bytes'] - opt_result['size_bytes']
        size_saved_pct = ((baseline['size_bytes'] - opt_result['size_bytes']) / baseline['size_bytes']) * 100

        gpt4_saved = baseline['tokens_gpt4'] - opt_result['tokens_gpt4']
        gpt4_saved_pct = ((baseline['tokens_gpt4'] - opt_result['tokens_gpt4']) / baseline['tokens_gpt4']) * 100

        gpt35_saved = baseline['tokens_gpt35'] - opt_result['tokens_gpt35']
        gpt35_saved_pct = ((baseline['tokens_gpt35'] - opt_result['tokens_gpt35']) / baseline['tokens_gpt35']) * 100

        claude_saved = baseline['tokens_claude'] - opt_result['tokens_claude']
        claude_saved_pct = ((baseline['tokens_claude'] - opt_result['tokens_claude']) / baseline['tokens_claude']) * 100

        cost_gpt4_saved = baseline['cost_gpt4_input'] - opt_result['cost_gpt4_input']
        cost_gpt35_saved = baseline['cost_gpt35_input'] - opt_result['cost_gpt35_input']
        cost_claude_saved = baseline['cost_claude_input'] - opt_result['cost_claude_input']

        print(f"\nSize Reduction:")
        print(f"   {size_saved:,} bytes saved ({size_saved_pct:.1f}% reduction)")

        print(f"\nToken Reduction:")
        print(f"   GPT-4:     {gpt4_saved:,} tokens ({gpt4_saved_pct:.1f}% reduction)")
        print(f"   GPT-3.5:   {gpt35_saved:,} tokens ({gpt35_saved_pct:.1f}% reduction)")
        print(f"   Claude:    {claude_saved:,} tokens ({claude_saved_pct:.1f}% reduction)")

        print(f"\nCost Savings per Read:")
        print(f"   GPT-4:     ${cost_gpt4_saved:.6f} ({gpt4_saved_pct:.1f}%)")
        print(f"   GPT-3.5:   ${cost_gpt35_saved:.6f} ({gpt35_saved_pct:.1f}%)")
        print(f"   Claude:    ${cost_claude_saved:.6f} ({claude_saved_pct:.1f}%)")

        # Extrapolate to 100 reads
        print(f"\nCost Savings over 100 Reads:")
        print(f"   GPT-4:     ${cost_gpt4_saved * 100:.4f}")
        print(f"   GPT-3.5:   ${cost_gpt35_saved * 100:.4f}")
        print(f"   Claude:    ${cost_claude_saved * 100:.4f}")

    print("\n" + "=" * 90)


def generate_test_data(num_sessions: int = 5) -> Dict[str, Any]:
    """Generate realistic test data with variable number of sessions"""
    data = {
        "v": "1.0",
        "project": "ecommerce-platform",
        "created": "2025-01-01T10:00:00Z",
        "updated": "2025-01-15T16:30:00Z",
        "sessions": []
    }

    goals = [
        "setup_project_structure",
        "implement_user_authentication",
        "build_product_catalog",
        "add_shopping_cart",
        "integrate_payment_processing",
        "implement_order_management",
        "add_admin_dashboard",
        "optimize_database_queries",
        "implement_caching_layer",
        "add_search_functionality"
    ]

    decisions_pool = [
        {"what": "react_framework", "why": "component_based_fast_ecosystem", "alt": ["vue", "angular"]},
        {"what": "postgresql_database", "why": "relational_reliable_acid", "alt": ["mongodb", "mysql"]},
        {"what": "jwt_authentication", "why": "stateless_scalable_standard", "alt": ["session_based", "oauth_only"]},
        {"what": "redis_cache", "why": "fast_in_memory_simple_api", "alt": ["memcached", "in_process"]},
        {"what": "stripe_payments", "why": "trusted_full_featured_good_docs", "alt": ["paypal", "square"]},
        {"what": "docker_containers", "why": "consistent_env_easy_deploy", "alt": ["vm", "bare_metal"]},
        {"what": "nginx_proxy", "why": "battle_tested_performant", "alt": ["apache", "caddy"]},
        {"what": "typescript", "why": "type_safety_better_dx_scalable", "alt": ["javascript"]},
    ]

    for i in range(num_sessions):
        session = {
            "id": f"s{i+1}",
            "start": f"2025-01-{i+1:02d}T10:00:00Z",
            "end": f"2025-01-{i+1:02d}T18:00:00Z" if i < num_sessions - 1 else None,
            "goal": goals[i % len(goals)],
            "state": "completed" if i < num_sessions - 1 else "in_progress",
            "decisions": [],
            "files": {},
            "patterns": {},
            "blockers": [],
            "next": [],
            "kv": {}
        }

        # Add 2-4 decisions per session
        num_decisions = min(2 + i, 4)
        for j in range(num_decisions):
            decision = decisions_pool[(i + j) % len(decisions_pool)].copy()
            decision["id"] = f"d{i*10+j+1}"
            decision["impact"] = [f"src/components/module{j}.tsx", f"src/services/service{j}.ts"]
            session["decisions"].append(decision)

        # Add 3-6 files per session
        num_files = min(3 + i, 6)
        for j in range(num_files):
            file_path = f"src/modules/module{i}/component{j}.tsx"
            session["files"][file_path] = {
                "action": "created" if j == 0 else "modified",
                "role": f"handles_{goals[i % len(goals)]}_logic",
                "deps": ["react", "redux"] if j % 2 == 0 else ["axios", "lodash"],
                "status": "complete"
            }

        # Add patterns
        session["patterns"] = {
            "component_structure": "container_presentation_pattern",
            "state_management": "redux_toolkit_with_rtk_query",
            "api_calls": "axios_with_interceptors"
        }

        # Add next steps for in-progress sessions
        if session["state"] == "in_progress":
            session["next"] = [
                "write_unit_tests",
                "add_integration_tests",
                "update_documentation",
                "perform_code_review"
            ]

        # Add KV data
        session["kv"] = {
            "node_version": "20.x",
            "package_manager": "pnpm",
            "ci_cd": "github_actions"
        }

        data["sessions"].append(session)

    return data


def main():
    """Run token conservation tests"""

    # Allow custom session count
    num_sessions = 5
    if len(sys.argv) > 1:
        try:
            num_sessions = int(sys.argv[1])
        except ValueError:
            print("Usage: python token_conservation_test.py [num_sessions]")
            print("Example: python token_conservation_test.py 10")
            sys.exit(1)

    print(f"\nGenerating test data with {num_sessions} sessions...")
    data = generate_test_data(num_sessions)

    # Test different formats
    results = []

    # 1. Pretty JSON
    json_pretty = json.dumps(data, indent=2)
    results.append(test_format(data, "JSON (pretty, 2-space)", json_pretty))

    # 2. Minified JSON
    json_minified = json.dumps(data, separators=(',', ':'))
    results.append(test_format(data, "JSON (minified)", json_minified))

    # 3. Optimized JSON
    optimizer = OptimizedJSONContext()
    optimized_data = optimizer.optimize(data)
    json_optimized = json.dumps(optimized_data, separators=(',', ':'))
    results.append(test_format(optimized_data, "JSON (optimized)", json_optimized))

    # Print results
    print_results(results, num_sessions)

    # Save samples for inspection
    samples_dir = Path("token_test_samples")
    samples_dir.mkdir(exist_ok=True)

    with open(samples_dir / "01_pretty.json", 'w') as f:
        f.write(json_pretty)

    with open(samples_dir / "02_minified.json", 'w') as f:
        f.write(json_minified)

    with open(samples_dir / "03_optimized.json", 'w') as f:
        f.write(json_optimized)

    print(f"\nSample files saved to: {samples_dir}/")
    print("   - 01_pretty.json")
    print("   - 02_minified.json")
    print("   - 03_optimized.json")

    print("\nTest complete!")


if __name__ == "__main__":
    main()
