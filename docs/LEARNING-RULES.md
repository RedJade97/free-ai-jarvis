# Executable learning rules and their limits

The tool does not train a model. It retains evidence and applies a small, explicit set of comparisons. An optional assistant interprets those records. All formulas are implemented locally in [brain.py](../brain.py); no model decides the numeric outcome.

## Metrics

| Name | Formula / availability |
| --- | --- |
| `saves_per_1000` | 1,000 × saves / views, from the same observation |
| `shares_per_1000` | 1,000 × shares / views, from the same observation |
| `follows_per_1000` | 1,000 × follows / views, from the same observation |
| `retention_10s` | The observed retained fraction at exactly second 10; no interpolation |

Unknown counts or zero views produce unknown ratios. Retention differences use fractions: 0.05 means five percentage points. Other metric differences use their stated per-1,000 units.

## Eligibility and selection

Each lesson locks an instrument when imported: feature name, platform, distribution cohort, metric, target post age, age tolerance, minimum views, minimum group size, required difference and direction.

1. Use only matching platform/cohort and labelled features, within the age tolerance.
2. The first run uses observations at or after lesson creation and at or before the cutoff. After a qualified run, new observations must be strictly later than its cutoff.
3. Exclude every experiment used in a previous qualified run for that lesson. Sibling cuts and later snapshots cannot create new confirmations.
4. Choose one post per experiment by platform and post ID in lexical order, then its nearest-to-target-age observation; ties use timestamp and evidence ID. This deliberately avoids choosing the best-performing variant. Give each independent concept its own experiment ID and never split sibling cuts across experiments.
5. Check that chosen observation's views and metric. If missing or below the minimum, exclude it; do not substitute a better-performing sibling or another snapshot.
6. Compare feature-present and feature-absent groups. All selected and excluded IDs and reasons are saved. The tool cannot verify that your labels, concept grouping or timestamps are honest or scientifically independent.

The recommended starting gate is eight independent concepts per group and a predeclared reach threshold. Those are workflow conventions, not a power calculation or a universal guarantee of reliable conclusions.

## Results

Calculate the mean in each group and subtract the feature-absent mean from the feature-present mean. Reverse the sign when the instrument says lower is better.

- **Insufficient:** either group is smaller than the gate. This does not consume experiments or refresh confidence.
- **Supports:** the directed difference meets the positive threshold and still meets it after removing any one selected experiment in turn.
- **Contradicts:** the directed difference reaches the negative threshold.
- **Inconclusive:** neither threshold is met, or apparent support fails the leave-one-experiment-out check.

Qualified means any result with sufficient group sizes, including inconclusive. Qualified experiments are consumed for future retests of that lesson. Contradiction is conservatively recorded without requiring the positive-support robustness test; inspect individual results before interpreting it.

The run stores both the raw mean difference and the smallest directed difference from the leave-one-out check. For every run, the full evidence remains in the context export so you can inspect counterexamples, not just averages.

## Confidence history

Consecutive supporting runs with new qualifying evidence produce:

| Supporting runs | Status |
| --- | --- |
| 0 or 1 | hunch |
| 2 | likely |
| 3 or more | supported (provisional) |

A qualified inconclusive result resets the streak to hunch. A contradiction resets it to contradicted. Later support can start a new streak without erasing earlier results or changing the original claim. These labels are **not calibrated probabilities** and do not establish causation.

After 30 days without a qualified retest, likely/supported lessons become `needs retest`. After 90 days, any lesson becomes `stale`. Dates use the retest cutoff, so running an empty job does not make old evidence fresh.

Runs are immutable. Reusing the same run ID and cutoff returns its saved result. A new run requires a later cutoff. Only new observations and independent experiments can add confirmations.

## Human checks that remain essential

The software cannot establish random assignment, control confounders, verify truthful media labels, certify original-to-cut maps, calculate causal effects or determine whether your audience has changed. There are no p-values, confidence intervals, multiple-testing adjustments or automated causal claims.

Changing what a feature means requires a new lesson, with its relationship to the old claim recorded in your notes. Never lower a gate or rewrite the claim after seeing results and present it as the original test. The software rejects changes to existing records; keep corrections transparent as described in [the data guide](DATA-FORMAT.md).

Reports contain the current full inventory and run history. `report --as-of` changes confidence-age evaluation; it is not a historical database snapshot. For historical records, save dated exports or restore a dated private backup.
