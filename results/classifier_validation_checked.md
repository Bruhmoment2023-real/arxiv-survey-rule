# Classifier validation (rules v1.0 against 400 hand labels)

Labels: labels_checked.csv (first-pass labels after the author's non-blind check; see checks/). Labeller: AI assistant, first pass, blind to id, date, category and classifier output. All 400 labels were then checked against the full text with the first-pass label visible (non-blind); data/labels/label_changes_checked.csv lists the changes.

Population stratum sizes (CS papers on the 57 random days): `{"strict|pre": 469, "strict|post": 93, "broad_only|pre": 457, "broad_only|post": 203, "neither|pre": 13672, "neither|post": 4885}`

## Positive class = main: S or P

### Raw counts in each sampled stratum

| stratum | period | labelled | positive | share positive (Wilson 95%) |
|---|---|---|---|---|
| strict | pre | 50 | 42 | 0.840 (0.715-0.917) |
| strict | post | 50 | 39 | 0.780 (0.648-0.872) |
| broad_only | pre | 40 | 10 | 0.250 (0.142-0.402) |
| broad_only | post | 40 | 7 | 0.175 (0.087-0.320) |
| neither | pre | 110 | 3 | 0.027 (0.009-0.077) |
| neither | post | 110 | 2 | 0.018 (0.005-0.064) |

### Precision, recall and prevalence (stratum-weighted; bootstrap 95% intervals)

| measure | period | precision | recall | true prevalence of S/P among CS papers |
|---|---|---|---|---|
| strict | pre | 0.840 (0.740-0.940) | 0.447 (0.288-0.783) | 0.0604 (0.0348-0.0943) |
| strict | post | 0.780 (0.660-0.880) | 0.368 (0.210-0.746) | 0.0380 (0.0186-0.0657) |
| strict | pooled | 0.830 (0.740-0.913) | 0.433 (0.295-0.666) | 0.0545 (0.0354-0.0796) |
| strict | post minus pre, precision | -0.060 (-0.220 to +0.100) | | |
| strict | post minus pre, recall | -0.079 (-0.425 to +0.326) | | |
| broad | pre | 0.549 (0.467-0.634) | 0.577 (0.374-1.000) | 0.0604 (0.0350-0.0925) |
| broad | post | 0.365 (0.284-0.457) | 0.549 (0.313-1.000) | 0.0380 (0.0185-0.0653) |
| broad | pooled | 0.504 (0.439-0.572) | 0.572 (0.389-0.880) | 0.0545 (0.0349-0.0797) |
| broad | post minus pre, precision | -0.184 (-0.302 to -0.059) | | |
| broad | post minus pre, recall | -0.028 (-0.470 to +0.510) | | |

## Positive class = sensitivity: S, P or M

### Raw counts in each sampled stratum

| stratum | period | labelled | positive | share positive (Wilson 95%) |
|---|---|---|---|---|
| strict | pre | 50 | 43 | 0.860 (0.738-0.930) |
| strict | post | 50 | 41 | 0.820 (0.692-0.902) |
| broad_only | pre | 40 | 11 | 0.275 (0.161-0.428) |
| broad_only | post | 40 | 7 | 0.175 (0.087-0.320) |
| neither | pre | 110 | 3 | 0.027 (0.009-0.077) |
| neither | post | 110 | 2 | 0.018 (0.005-0.064) |

### Precision, recall and prevalence (stratum-weighted; bootstrap 95% intervals)

| measure | period | precision | recall | true prevalence of S/P among CS papers |
|---|---|---|---|---|
| strict | pre | 0.860 (0.760-0.960) | 0.447 (0.291-0.755) | 0.0618 (0.0365-0.0946) |
| strict | post | 0.820 (0.700-0.920) | 0.380 (0.218-0.759) | 0.0387 (0.0192-0.0665) |
| strict | pooled | 0.853 (0.763-0.930) | 0.435 (0.300-0.658) | 0.0557 (0.0367-0.0806) |
| strict | post minus pre, precision | -0.040 (-0.180 to +0.100) | | |
| strict | post minus pre, recall | -0.067 (-0.403 to +0.333) | | |
| broad | pre | 0.571 (0.489-0.655) | 0.587 (0.381-1.000) | 0.0618 (0.0367-0.0946) |
| broad | post | 0.378 (0.294-0.470) | 0.557 (0.320-1.000) | 0.0387 (0.0192-0.0654) |
| broad | pooled | 0.524 (0.459-0.592) | 0.581 (0.403-0.881) | 0.0557 (0.0360-0.0804) |
| broad | post minus pre, precision | -0.194 (-0.312 to -0.077) | | |
| broad | post minus pre, recall | -0.029 (-0.462 to +0.507) | | |

## How hand-labelled S/P papers were caught (unweighted sample counts)

| period | stratum | true S | true P |
|---|---|---|---|
| pre | strict | 37 | 5 |
| pre | broad_only | 7 | 3 |
| pre | neither | 2 | 1 |
| post | strict | 32 | 7 |
| post | broad_only | 2 | 5 |
| post | neither | 0 | 2 |
