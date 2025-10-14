#!/usr/bin/env python3
"""
V2 Format Benchmark

Comprehensive comparison of all session-ctx formats:
- V1 Standard (pretty JSON)
- V1 Minified
- V1 Optimized (single-letter keys)
- V2 Layered (array-based with string table)

Tests with realistic data to show actual token savings.
"""

import json
from pathlib import Path
from typing import Dict, Any, List
import sys

try:
    import tiktoken
    HAS_TIKTOKEN = True
except ImportError:
    HAS_TIKTOKEN = False

from optimized_json import OptimizedJSONContext
from v2_layered_format import V2LayeredEncoder, V2LayeredDecoder


def count_tokens(text: str, model: str = "gpt-4") -> int:
    """Count tokens using tiktoken or approximation"""
    if not HAS_TIKTOKEN:
        return len(text) // 4
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


def generate_realistic_data(num_sessions: int = 5) -> Dict[str, Any]:
    """Generate realistic multi-session test data"""
    data = {
        "v": "1.0",
        "project": "ai-powered-analytics-platform",
        "created": "2025-01-01T10:00:00Z",
        "updated": "2025-01-15T16:30:00Z",
        "sessions": []
    }

    goals = [
        "setup_backend_infrastructure",
        "implement_user_authentication_system",
        "build_data_ingestion_pipeline",
        "create_analytics_dashboard",
        "add_real_time_processing",
        "implement_machine_learning_models",
        "build_api_gateway",
        "add_caching_and_optimization",
        "implement_monitoring_alerting",
        "create_admin_management_panel"
    ]

    tech_decisions = [
        {
            "what": "nextjs_react_framework",
            "why": "server_side_rendering_fast_development_great_dx_strong_ecosystem",
            "alt": ["vue_nuxt", "svelte_kit", "angular"]
        },
        {
            "what": "postgresql_with_timescaledb",
            "why": "time_series_data_relational_integrity_proven_scalability",
            "alt": ["mongodb", "cassandra", "mysql_with_clickhouse"]
        },
        {
            "what": "fastapi_python_backend",
            "why": "async_support_type_hints_auto_docs_high_performance",
            "alt": ["django", "flask", "express_nodejs"]
        },
        {
            "what": "redis_distributed_cache",
            "why": "in_memory_speed_pub_sub_support_data_structures",
            "alt": ["memcached", "hazelcast", "in_process_cache"]
        },
        {
            "what": "jwt_oauth2_authentication",
            "why": "stateless_industry_standard_mobile_friendly_scalable",
            "alt": ["session_based_auth", "saml", "passwordless"]
        },
        {
            "what": "docker_kubernetes_deployment",
            "why": "container_orchestration_auto_scaling_cloud_native_best_practices",
            "alt": ["docker_swarm", "nomad", "bare_metal_systemd"]
        },
        {
            "what": "apache_kafka_event_streaming",
            "why": "high_throughput_fault_tolerant_real_time_processing_proven_scale",
            "alt": ["rabbitmq", "pulsar", "aws_kinesis"]
        },
        {
            "what": "prometheus_grafana_monitoring",
            "why": "time_series_metrics_powerful_visualization_alerting_open_source",
            "alt": ["datadog", "new_relic", "elastic_apm"]
        }
    ]

    for i in range(num_sessions):
        session = {
            "id": f"s{i+1}",
            "start": f"2025-01-{i+1:02d}T09:00:00Z",
            "end": f"2025-01-{i+1:02d}T18:30:00Z" if i < num_sessions - 1 else None,
            "goal": goals[i % len(goals)],
            "state": "completed" if i < num_sessions - 1 else "in_progress",
            "decisions": [],
            "files": {},
            "patterns": {},
            "blockers": [],
            "next": [],
            "kv": {}
        }

        # Add 2-5 decisions per session
        num_decisions = min(2 + (i % 4), 5)
        for j in range(num_decisions):
            tech = tech_decisions[(i * 3 + j) % len(tech_decisions)].copy()
            decision = {
                "id": f"d{i*10+j+1}",
                "what": tech["what"],
                "why": tech["why"],
                "alt": tech["alt"],
                "impact": [
                    f"src/backend/services/{tech['what']}.py",
                    f"src/frontend/components/{tech['what']}.tsx",
                    f"config/{tech['what']}.yaml",
                    f"tests/integration/test_{tech['what']}.py"
                ]
            }
            session["decisions"].append(decision)

        # Add 4-8 files per session
        num_files = min(4 + i, 8)
        file_types = [
            ("src/backend/api/routes/users.py", "created", "user_management_crud_endpoints"),
            ("src/backend/api/routes/analytics.py", "created", "analytics_data_endpoints"),
            ("src/backend/services/auth.py", "created", "authentication_authorization_logic"),
            ("src/backend/services/data_processor.py", "created", "data_transformation_processing"),
            ("src/backend/models/user.py", "created", "user_database_model"),
            ("src/backend/models/analytics_event.py", "created", "analytics_event_schema"),
            ("src/frontend/pages/dashboard.tsx", "created", "main_dashboard_interface"),
            ("src/frontend/components/charts/LineChart.tsx", "created", "time_series_visualization"),
            ("src/frontend/components/auth/LoginForm.tsx", "created", "user_authentication_form"),
            ("config/database.yaml", "created", "database_connection_configuration"),
            ("config/redis.yaml", "created", "cache_configuration"),
            ("docker-compose.yml", "modified", "container_orchestration_setup"),
        ]

        for j in range(num_files):
            file_spec = file_types[j % len(file_types)]
            session["files"][file_spec[0]] = {
                "action": file_spec[1],
                "role": file_spec[2],
                "deps": [
                    "fastapi",
                    "sqlalchemy",
                    "pydantic",
                    "redis",
                    "jwt"
                ][:((j % 3) + 2)],
                "status": "complete" if j < num_files - 1 else "partial"
            }

        # Add patterns
        session["patterns"] = {
            "api_structure": "layered_architecture_with_dependency_injection",
            "error_handling": "custom_exceptions_with_error_codes_and_structured_logging",
            "testing_strategy": "unit_tests_integration_tests_e2e_with_pytest",
            "authentication_flow": "jwt_access_refresh_tokens_httponly_cookies",
            "data_validation": "pydantic_models_with_strict_type_checking"
        }

        # Add blockers for some sessions
        if i % 3 == 0 and session["state"] == "in_progress":
            session["blockers"].append({
                "id": f"b{i+1}",
                "desc": "waiting_for_security_review_of_authentication_implementation",
                "status": "open"
            })

        # Add next steps for in-progress sessions
        if session["state"] == "in_progress":
            session["next"] = [
                "complete_unit_test_coverage_for_auth_module",
                "implement_rate_limiting_on_api_endpoints",
                "add_request_response_logging_middleware",
                "update_api_documentation_with_examples",
                "perform_load_testing_and_optimize_queries"
            ]

        # Add KV data
        session["kv"] = {
            "python_version": "3.11",
            "node_version": "20.x",
            "package_manager": "pnpm",
            "ci_cd_platform": "github_actions",
            "cloud_provider": "aws",
            "deployment_region": "us-east-1"
        }

        data["sessions"].append(session)

    return data


def test_format(name: str, json_str: str) -> Dict[str, Any]:
    """Test a format and return metrics"""
    return {
        'name': name,
        'bytes': len(json_str.encode('utf-8')),
        'chars': len(json_str),
        'tokens_gpt4': count_tokens(json_str, "gpt-4"),
        'tokens_gpt35': count_tokens(json_str, "gpt-3.5-turbo"),
    }


def print_comparison(results: List[Dict[str, Any]], num_sessions: int):
    """Print detailed comparison table"""

    print("\n" + "=" * 100)
    print(f"SESSION-CTX FORMAT BENCHMARK ({num_sessions} sessions)")
    print("=" * 100)

    if not HAS_TIKTOKEN:
        print("\n⚠️  Using approximate token counts (install tiktoken for exact counts)")

    print(f"\n{'Format':<30} {'Size (KB)':<15} {'Tokens (GPT-4)':<20} {'Tokens (GPT-3.5)':<20}")
    print("-" * 100)

    baseline = results[0]

    for result in results:
        size_kb = result['bytes'] / 1024
        size_pct = (result['bytes'] / baseline['bytes']) * 100
        tok4_pct = (result['tokens_gpt4'] / baseline['tokens_gpt4']) * 100
        tok35_pct = (result['tokens_gpt35'] / baseline['tokens_gpt35']) * 100

        print(f"{result['name']:<30} "
              f"{size_kb:>6.2f} ({size_pct:>5.1f}%)   "
              f"{result['tokens_gpt4']:>6} ({tok4_pct:>5.1f}%)      "
              f"{result['tokens_gpt35']:>6} ({tok35_pct:>5.1f}%)")

    # Detailed savings comparison
    print("\n" + "=" * 100)
    print("TOKEN SAVINGS COMPARISON (vs V1 Standard)")
    print("-" * 100)
    print(f"{'Format':<30} {'Bytes Saved':<20} {'GPT-4 Tokens':<20} {'GPT-3.5 Tokens':<20}")
    print("-" * 100)

    for result in results[1:]:  # Skip baseline
        bytes_saved = baseline['bytes'] - result['bytes']
        bytes_pct = ((baseline['bytes'] - result['bytes']) / baseline['bytes']) * 100

        tok4_saved = baseline['tokens_gpt4'] - result['tokens_gpt4']
        tok4_pct = ((baseline['tokens_gpt4'] - result['tokens_gpt4']) / baseline['tokens_gpt4']) * 100

        tok35_saved = baseline['tokens_gpt35'] - result['tokens_gpt35']
        tok35_pct = ((baseline['tokens_gpt35'] - result['tokens_gpt35']) / baseline['tokens_gpt35']) * 100

        print(f"{result['name']:<30} "
              f"{bytes_saved:>6} ({bytes_pct:>5.1f}%)   "
              f"{tok4_saved:>6} ({tok4_pct:>5.1f}%)      "
              f"{tok35_saved:>6} ({tok35_pct:>5.1f}%)")

    # Cost analysis
    print("\n" + "=" * 100)
    print("COST ANALYSIS (Input tokens, per 100 reads)")
    print("-" * 100)

    # Cost per 1K tokens: GPT-4: $0.01, GPT-3.5: $0.0005
    gpt4_rate = 0.00001
    gpt35_rate = 0.0000005

    print(f"{'Format':<30} {'GPT-4 (100 reads)':<25} {'GPT-3.5 (100 reads)':<25}")
    print("-" * 100)

    for result in results:
        cost_gpt4 = result['tokens_gpt4'] * gpt4_rate * 100
        cost_gpt35 = result['tokens_gpt35'] * gpt35_rate * 100
        print(f"{result['name']:<30} ${cost_gpt4:>8.4f}                  ${cost_gpt35:>8.4f}")

    # Savings over 1000 reads
    print("\n" + "=" * 100)
    print("PROJECTED SAVINGS OVER 1,000 READS (vs V1 Standard)")
    print("-" * 100)

    for result in results[1:]:
        tok4_saved = baseline['tokens_gpt4'] - result['tokens_gpt4']
        tok35_saved = baseline['tokens_gpt35'] - result['tokens_gpt35']

        cost4_saved = tok4_saved * gpt4_rate * 1000
        cost35_saved = tok35_saved * gpt35_rate * 1000

        print(f"\n{result['name']}:")
        print(f"  GPT-4:   ${cost4_saved:.2f}")
        print(f"  GPT-3.5: ${cost35_saved:.2f}")

    print("\n" + "=" * 100)


def main():
    """Run comprehensive benchmark"""

    num_sessions = 5
    if len(sys.argv) > 1:
        try:
            num_sessions = int(sys.argv[1])
        except ValueError:
            print("Usage: python v2_benchmark.py [num_sessions]")
            sys.exit(1)

    print(f"\nGenerating test data with {num_sessions} sessions...")
    data = generate_realistic_data(num_sessions)

    results = []

    # 1. V1 Standard (pretty JSON)
    v1_pretty = json.dumps(data, indent=2)
    results.append(test_format("V1 Standard (2-space indent)", v1_pretty))

    # 2. V1 Minified
    v1_mini = json.dumps(data, separators=(',', ':'))
    results.append(test_format("V1 Minified", v1_mini))

    # 3. V1 Optimized (single-letter keys)
    optimizer = OptimizedJSONContext()
    v1_opt = optimizer.optimize(data)
    v1_opt_str = json.dumps(v1_opt, separators=(',', ':'))
    results.append(test_format("V1 Optimized (abbrev keys)", v1_opt_str))

    # 4. V2 Layered (array-based)
    encoder = V2LayeredEncoder()
    v2_data = encoder.encode(data)
    v2_str = json.dumps(v2_data, separators=(',', ':'))
    results.append(test_format("V2 Layered (array + strings)", v2_str))

    # Print results
    print_comparison(results, num_sessions)

    # Save samples
    samples_dir = Path("benchmark_samples")
    samples_dir.mkdir(exist_ok=True)

    with open(samples_dir / "v1_standard.json", 'w') as f:
        f.write(v1_pretty)

    with open(samples_dir / "v1_minified.json", 'w') as f:
        f.write(v1_mini)

    with open(samples_dir / "v1_optimized.json", 'w') as f:
        f.write(v1_opt_str)

    with open(samples_dir / "v2_layered.json", 'w') as f:
        f.write(v2_str)

    # Also save pretty V2 for inspection
    with open(samples_dir / "v2_layered_pretty.json", 'w') as f:
        json.dump(v2_data, f, indent=2)

    print(f"\nSample files saved to: {samples_dir}/")
    print("  - v1_standard.json")
    print("  - v1_minified.json")
    print("  - v1_optimized.json")
    print("  - v2_layered.json")
    print("  - v2_layered_pretty.json")

    print("\nBenchmark complete!")


if __name__ == "__main__":
    main()
