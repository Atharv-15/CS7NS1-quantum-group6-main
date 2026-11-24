# import json

# from simulator import run_one_hop, run_two_hop, run_variant_scenario
# from policy import make_policy

# P = json.load(open("variant_params.json"))
# T = P["grading"]["sim_time_ms"]
# seed = P["grading"]["seed"]

# print("----------------------One hop----------------------")
# r1 = run_one_hop(P, T, seed)
# print("one-hop:", r1, "| target rate", P["reference"]["expected"]["one_hop_rate"])
# print("same again?", run_one_hop(P, T, seed) == r1)

# print("----------------------Two hop----------------------")
# r2 = run_two_hop(P, T, seed)
# print("two-hop:", r2, "| target rate", P["reference"]["expected"]["two_hop_rate"],
#       "F", P["reference"]["expected"]["two_hop_fidelity"])
# print("same again?", run_two_hop(P, T, seed) == r2)

# print("----------------------Variant----------------------")
# print("target rate:", P["slo"]["min_rate"])
# print("target fidelity:", P["slo"]["min_fidelity"])
# print("max latency:", P["slo"]["max_p95_latency_ms"])
# print("seed:", seed)
# r3 = run_variant_scenario(P, T, seed, make_policy(P))
# print(r3)
# for s in P["grading"]["held_out_seeds"]:
#       print("seed:", s)
#       print(run_variant_scenario(P, T, s, make_policy(P)))

import json

from simulator import run_one_hop, run_two_hop, run_variant_scenario
from policy import make_policy
from experiments import run_sensitivity


P = json.load(open("variant_params.json"))
T = P["grading"]["sim_time_ms"]
seed = P["grading"]["seed"]


# One-hop reference validation

print("\n----------------------One hop----------------------")

r1 = run_one_hop(P, T, seed)

print(
    "one-hop:",
    r1,
    "| target rate",
    P["reference"]["expected"]["one_hop_rate"]
)

print(
    "same again?",
    run_one_hop(P, T, seed) == r1
)


# ============================================================
# Two-hop reference validation
# ============================================================

print("\n----------------------Two hop----------------------")

r2 = run_two_hop(P, T, seed)

print(
    "two-hop:",
    r2,
    "| target rate",
    P["reference"]["expected"]["two_hop_rate"],
    "F",
    P["reference"]["expected"]["two_hop_fidelity"]
)

print(
    "same again?",
    run_two_hop(P, T, seed) == r2
)


# ============================================================
# Variant / SLO validation
# ============================================================

print("\n----------------------Variant----------------------")

print("target rate:", P["slo"]["min_rate"])
print("target fidelity:", P["slo"]["min_fidelity"])
print("max latency:", P["slo"]["max_p95_latency_ms"])
print("seed:", seed)

r3 = run_variant_scenario(
    P,
    T,
    seed,
    make_policy(P)
)

print("result:", r3)


# ============================================================
# Held-out seed robustness
# ============================================================

print("\n----------------------Held-out seeds----------------------")

for s in P["grading"]["held_out_seeds"]:
    result = run_variant_scenario(
        P,
        T,
        s,
        make_policy(P)
    )

    print("seed:", s)
    print(result)


# ============================================================
# Sensitivity experiment
# ============================================================

print("\n----------------------Sensitivity experiment----------------------")

exp = P["experiment"]
sensitivity = run_sensitivity(P, exp["seeds"])

print(json.dumps(sensitivity, indent=2))


# ============================================================
# Final summary
# ============================================================

print("\n======================SUMMARY======================")

print("\nOne-hop:")
print(r1)

print("\nTwo-hop:")
print(r2)

print("\nVariant:")
print(r3)

print("\nSensitivity:")
for point in sensitivity["points"]:
    print(
        f"T2={point['t2_ms']} ms | "
        f"rate={point['rate_mean']:.4f} ± "
        f"{point['rate_ci95']:.4f} | "
        f"n={point['n_seeds']}"
    )

print("\nexperiment_results.json written successfully.")