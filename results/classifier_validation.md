# Classifier validation (rules v1.0 against 400 hand labels)

Labeller: AI assistant, first pass, blind to id, date, category and classifier output. These are the first-pass labels; the checked labels are data/labels/labels_checked.csv.

Population stratum sizes (CS papers on the 57 random days): `{"strict|pre": 469, "strict|post": 93, "broad_only|pre": 457, "broad_only|post": 203, "neither|pre": 13672, "neither|post": 4885}`

## Positive class = main: S or P

### Raw counts in each sampled stratum

| stratum | period | labelled | positive | share positive (Wilson 95%) |
|---|---|---|---|---|
| strict | pre | 50 | 43 | 0.860 (0.738-0.930) |
| strict | post | 50 | 38 | 0.760 (0.626-0.857) |
| broad_only | pre | 40 | 9 | 0.225 (0.123-0.375) |
| broad_only | post | 40 | 8 | 0.200 (0.105-0.348) |
| neither | pre | 110 | 2 | 0.018 (0.005-0.064) |
| neither | post | 110 | 1 | 0.009 (0.002-0.050) |

### Precision, recall and prevalence (stratum-weighted; bootstrap 95% intervals)

| measure | period | precision | recall | true prevalence of S/P among CS papers |
|---|---|---|---|---|
| strict | pre | 0.860 (0.760-0.940) | 0.534 (0.345-0.849) | 0.0517 (0.0320-0.0795) |
| strict | post | 0.760 (0.640-0.880) | 0.454 (0.262-0.762) | 0.0301 (0.0176-0.0515) |
| strict | pooled | 0.843 (0.754-0.920) | 0.521 (0.358-0.775) | 0.0460 (0.0309-0.0669) |
| strict | post minus pre, precision | -0.100 (-0.260 to +0.060) | | |
| strict | post minus pre, recall | -0.080 (-0.455 to +0.296) | | |
| broad | pre | 0.547 (0.469-0.629) | 0.671 (0.441-1.000) | 0.0517 (0.0325-0.0780) |
| broad | post | 0.376 (0.289-0.477) | 0.715 (0.422-1.000) | 0.0301 (0.0176-0.0503) |
| broad | pooled | 0.505 (0.441-0.571) | 0.678 (0.465-1.000) | 0.0460 (0.0306-0.0668) |
| broad | post minus pre, precision | -0.171 (-0.289 to -0.044) | | |
| broad | post minus pre, recall | +0.044 (-0.447 to +0.513) | | |

## Positive class = sensitivity: S, P or M

### Raw counts in each sampled stratum

| stratum | period | labelled | positive | share positive (Wilson 95%) |
|---|---|---|---|---|
| strict | pre | 50 | 43 | 0.860 (0.738-0.930) |
| strict | post | 50 | 41 | 0.820 (0.692-0.902) |
| broad_only | pre | 40 | 9 | 0.225 (0.123-0.375) |
| broad_only | post | 40 | 8 | 0.200 (0.105-0.348) |
| neither | pre | 110 | 2 | 0.018 (0.005-0.064) |
| neither | post | 110 | 1 | 0.009 (0.002-0.050) |

### Precision, recall and prevalence (stratum-weighted; bootstrap 95% intervals)

| measure | period | precision | recall | true prevalence of S/P among CS papers |
|---|---|---|---|---|
| strict | pre | 0.860 (0.760-0.960) | 0.534 (0.348-0.841) | 0.0517 (0.0323-0.0793) |
| strict | post | 0.820 (0.700-0.920) | 0.473 (0.283-0.781) | 0.0311 (0.0187-0.0506) |
| strict | pooled | 0.853 (0.763-0.930) | 0.524 (0.363-0.771) | 0.0463 (0.0310-0.0671) |
| strict | post minus pre, precision | -0.040 (-0.180 to +0.100) | | |
| strict | post minus pre, recall | -0.062 (-0.419 to +0.302) | | |
| broad | pre | 0.547 (0.469-0.626) | 0.671 (0.437-1.000) | 0.0517 (0.0325-0.0792) |
| broad | post | 0.395 (0.307-0.489) | 0.725 (0.440-1.000) | 0.0311 (0.0184-0.0510) |
| broad | pooled | 0.510 (0.448-0.576) | 0.680 (0.470-1.000) | 0.0463 (0.0310-0.0672) |
| broad | post minus pre, precision | -0.152 (-0.272 to -0.033) | | |
| broad | post minus pre, recall | +0.054 (-0.429 to +0.512) | | |

## How hand-labelled S/P papers were caught (unweighted sample counts)

| period | stratum | true S | true P |
|---|---|---|---|
| pre | strict | 38 | 5 |
| pre | broad_only | 6 | 3 |
| pre | neither | 1 | 1 |
| post | strict | 31 | 7 |
| post | broad_only | 2 | 6 |
| post | neither | 0 | 1 |
