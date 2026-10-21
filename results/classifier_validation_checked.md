# Classifier validation (rules v1.0 against 400 hand labels)

Labels: labels_checked.csv (first-pass labels after the author's non-blind check; see checks/). Labeller: AI assistant, first pass, blind to id, date, category and classifier output. A human second labeller is still needed (see 00-STATUS.md).

Population stratum sizes (CS papers on the 57 random days): `{"strict|pre": 469, "strict|post": 93, "broad_only|pre": 457, "broad_only|post": 203, "neither|pre": 13672, "neither|post": 4885}`

## Positive class = main: S or P

### Raw counts in each sampled stratum

| stratum | period | labelled | positive | share positive (Wilson 95%) |
|---|---|---|---|---|
| strict | pre | 50 | 43 | 0.860 (0.738-0.930) |
| strict | post | 50 | 39 | 0.780 (0.648-0.872) |
| broad_only | pre | 40 | 9 | 0.225 (0.123-0.375) |
| broad_only | post | 40 | 8 | 0.200 (0.105-0.348) |
| neither | pre | 110 | 3 | 0.027 (0.009-0.077) |
| neither | post | 110 | 1 | 0.009 (0.002-0.050) |

### Precision, recall and prevalence (stratum-weighted; bootstrap 95% intervals)

| measure | period | precision | recall | true prevalence of S/P among CS papers |
|---|---|---|---|---|
| strict | pre | 0.860 (0.760-0.940) | 0.459 (0.296-0.801) | 0.0602 (0.0344-0.0934) |
| strict | post | 0.780 (0.660-0.880) | 0.460 (0.267-0.763) | 0.0304 (0.0179-0.0521) |
| strict | pooled | 0.847 (0.760-0.924) | 0.459 (0.313-0.720) | 0.0524 (0.0332-0.0766) |
| strict | post minus pre, precision | -0.080 (-0.220 to +0.060) | | |
| strict | post minus pre, recall | +0.002 (-0.364 to +0.364) | | |
| broad | pre | 0.547 (0.469-0.629) | 0.576 (0.371-1.000) | 0.0602 (0.0345-0.0924) |
| broad | post | 0.382 (0.297-0.482) | 0.718 (0.426-1.000) | 0.0304 (0.0179-0.0506) |
| broad | pooled | 0.507 (0.442-0.573) | 0.597 (0.405-0.934) | 0.0524 (0.0333-0.0773) |
| broad | post minus pre, precision | -0.164 (-0.282 to -0.041) | | |
| broad | post minus pre, recall | +0.142 (-0.333 to +0.590) | | |

## Positive class = sensitivity: S, P or M

### Raw counts in each sampled stratum

| stratum | period | labelled | positive | share positive (Wilson 95%) |
|---|---|---|---|---|
| strict | pre | 50 | 43 | 0.860 (0.738-0.930) |
| strict | post | 50 | 41 | 0.820 (0.692-0.902) |
| broad_only | pre | 40 | 9 | 0.225 (0.123-0.375) |
| broad_only | post | 40 | 8 | 0.200 (0.105-0.348) |
| neither | pre | 110 | 3 | 0.027 (0.009-0.077) |
| neither | post | 110 | 1 | 0.009 (0.002-0.050) |

### Precision, recall and prevalence (stratum-weighted; bootstrap 95% intervals)

| measure | period | precision | recall | true prevalence of S/P among CS papers |
|---|---|---|---|---|
| strict | pre | 0.860 (0.760-0.960) | 0.459 (0.301-0.797) | 0.0602 (0.0344-0.0922) |
| strict | post | 0.820 (0.700-0.920) | 0.473 (0.283-0.781) | 0.0311 (0.0187-0.0506) |
| strict | pooled | 0.853 (0.763-0.930) | 0.461 (0.314-0.717) | 0.0526 (0.0337-0.0767) |
| strict | post minus pre, precision | -0.040 (-0.180 to +0.100) | | |
| strict | post minus pre, recall | +0.014 (-0.351 to +0.366) | | |
| broad | pre | 0.547 (0.469-0.626) | 0.576 (0.370-1.000) | 0.0602 (0.0352-0.0928) |
| broad | post | 0.395 (0.307-0.489) | 0.725 (0.440-1.000) | 0.0311 (0.0184-0.0510) |
| broad | pooled | 0.510 (0.448-0.576) | 0.599 (0.410-0.935) | 0.0526 (0.0338-0.0777) |
| broad | post minus pre, precision | -0.152 (-0.272 to -0.033) | | |
| broad | post minus pre, recall | +0.149 (-0.313 to +0.587) | | |

## How hand-labelled S/P papers were caught (unweighted sample counts)

| period | stratum | true S | true P |
|---|---|---|---|
| pre | strict | 38 | 5 |
| pre | broad_only | 6 | 3 |
| pre | neither | 1 | 2 |
| post | strict | 32 | 7 |
| post | broad_only | 2 | 6 |
| post | neither | 0 | 1 |
