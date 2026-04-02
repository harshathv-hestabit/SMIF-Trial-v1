# Token Benchmark by Phase, News Document, and Client (Totals Only)

- Generated at (UTC): 2026-04-01T11:13:02.458170+00:00
- Log scope: `src/app/modules/MAS/logs/generate_insight/*.log`
- Metric mode: **Totals only** (no averages)

## Phase Classification

- `pre baseline`: no `agent_context_profile` event in log
- `stage 1`: has `agent_context_profile`, but no populated compaction savings profile, and no precheck
- `stage 1.1`: has populated compaction savings profile, and no precheck
- `stage 2`: has `insight_precheck_completed` events

## Columns

- `Runs`: Completed workflow count
- `Verified` / `Failed`: Workflow terminal status counts
- `Iterations Total`: Sum of workflow iterations
- `LLM Calls Total`: Sum of `token_usage.calls` lengths
- `Prompt/Completion/Total Tokens`: Sums from `workflow_completed.payload.token_usage`
- `Precheck Events Total` / `Precheck Failed Total`: Stage-2 gate counts (0 in earlier phases)

## Pre Baseline

- Log files in phase: **52**
- Phase Totals: Runs=40, Verified=27, Failed=13, Iterations Total=84, LLM Calls Total=168, Prompt Tokens Total=339095, Completion Tokens Total=61011, Total Tokens Total=400106, Precheck Events Total=0, Precheck Failed Total=0

### News Document `51589649`

- News Totals: Runs=1, Verified=1, Failed=0, Iterations Total=1, LLM Calls Total=2, Prompt Tokens Total=5887, Completion Tokens Total=1429, Total Tokens Total=7316, Precheck Events Total=0, Precheck Failed Total=0

| Client ID | Runs | Verified | Failed | Iterations Total | LLM Calls Total | Prompt Tokens Total | Completion Tokens Total | Total Tokens Total | Precheck Events Total | Precheck Failed Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `311` | 1 | 1 | 0 | 1 | 2 | 5887 | 1429 | 7316 | 0 | 0 |

### News Document `51590064`

- News Totals: Runs=2, Verified=2, Failed=0, Iterations Total=3, LLM Calls Total=6, Prompt Tokens Total=19068, Completion Tokens Total=1233, Total Tokens Total=20301, Precheck Events Total=0, Precheck Failed Total=0

| Client ID | Runs | Verified | Failed | Iterations Total | LLM Calls Total | Prompt Tokens Total | Completion Tokens Total | Total Tokens Total | Precheck Events Total | Precheck Failed Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `6269` | 1 | 1 | 0 | 2 | 4 | 14093 | 799 | 14892 | 0 | 0 |
| `8255` | 1 | 1 | 0 | 1 | 2 | 4975 | 434 | 5409 | 0 | 0 |

### News Document `51590557`

- News Totals: Runs=2, Verified=0, Failed=2, Iterations Total=6, LLM Calls Total=12, Prompt Tokens Total=23696, Completion Tokens Total=3724, Total Tokens Total=27420, Precheck Events Total=0, Precheck Failed Total=0

| Client ID | Runs | Verified | Failed | Iterations Total | LLM Calls Total | Prompt Tokens Total | Completion Tokens Total | Total Tokens Total | Precheck Events Total | Precheck Failed Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `311` | 1 | 0 | 1 | 3 | 6 | 17794 | 1762 | 19556 | 0 | 0 |
| `642` | 1 | 0 | 1 | 3 | 6 | 5902 | 1962 | 7864 | 0 | 0 |

### News Document `51590777`

- News Totals: Runs=7, Verified=4, Failed=3, Iterations Total=17, LLM Calls Total=34, Prompt Tokens Total=70667, Completion Tokens Total=11068, Total Tokens Total=81735, Precheck Events Total=0, Precheck Failed Total=0

| Client ID | Runs | Verified | Failed | Iterations Total | LLM Calls Total | Prompt Tokens Total | Completion Tokens Total | Total Tokens Total | Precheck Events Total | Precheck Failed Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `3621` | 1 | 1 | 0 | 1 | 2 | 1416 | 1333 | 2749 | 0 | 0 |
| `4945` | 1 | 0 | 1 | 3 | 6 | 3539 | 1202 | 4741 | 0 | 0 |
| `6269` | 1 | 0 | 1 | 3 | 6 | 21556 | 1974 | 23530 | 0 | 0 |
| `642` | 1 | 1 | 0 | 1 | 2 | 1957 | 288 | 2245 | 0 | 0 |
| `8255` | 1 | 0 | 1 | 3 | 6 | 15685 | 2813 | 18498 | 0 | 0 |
| `8917` | 1 | 1 | 0 | 3 | 6 | 15585 | 1479 | 17064 | 0 | 0 |
| `9579` | 1 | 1 | 0 | 3 | 6 | 10929 | 1979 | 12908 | 0 | 0 |

### News Document `51591372`

- News Totals: Runs=2, Verified=2, Failed=0, Iterations Total=4, LLM Calls Total=8, Prompt Tokens Total=18831, Completion Tokens Total=2924, Total Tokens Total=21755, Precheck Events Total=0, Precheck Failed Total=0

| Client ID | Runs | Verified | Failed | Iterations Total | LLM Calls Total | Prompt Tokens Total | Completion Tokens Total | Total Tokens Total | Precheck Events Total | Precheck Failed Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `311` | 1 | 1 | 0 | 3 | 6 | 17657 | 2326 | 19983 | 0 | 0 |
| `3621` | 1 | 1 | 0 | 1 | 2 | 1174 | 598 | 1772 | 0 | 0 |

### News Document `51591382`

- News Totals: Runs=5, Verified=3, Failed=2, Iterations Total=14, LLM Calls Total=28, Prompt Tokens Total=67934, Completion Tokens Total=10224, Total Tokens Total=78158, Precheck Events Total=0, Precheck Failed Total=0

| Client ID | Runs | Verified | Failed | Iterations Total | LLM Calls Total | Prompt Tokens Total | Completion Tokens Total | Total Tokens Total | Precheck Events Total | Precheck Failed Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `311` | 1 | 0 | 1 | 3 | 6 | 17766 | 1975 | 19741 | 0 | 0 |
| `6269` | 1 | 0 | 1 | 3 | 6 | 21319 | 2317 | 23636 | 0 | 0 |
| `642` | 1 | 1 | 0 | 3 | 6 | 6093 | 1381 | 7474 | 0 | 0 |
| `8255` | 1 | 1 | 0 | 3 | 6 | 15465 | 2549 | 18014 | 0 | 0 |
| `9579` | 1 | 1 | 0 | 2 | 4 | 7291 | 2002 | 9293 | 0 | 0 |

### News Document `51591434`

- News Totals: Runs=7, Verified=4, Failed=3, Iterations Total=15, LLM Calls Total=30, Prompt Tokens Total=49424, Completion Tokens Total=12340, Total Tokens Total=61764, Precheck Events Total=0, Precheck Failed Total=0

| Client ID | Runs | Verified | Failed | Iterations Total | LLM Calls Total | Prompt Tokens Total | Completion Tokens Total | Total Tokens Total | Precheck Events Total | Precheck Failed Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `3621` | 1 | 0 | 1 | 3 | 6 | 4263 | 2585 | 6848 | 0 | 0 |
| `4945` | 1 | 1 | 0 | 1 | 2 | 1155 | 982 | 2137 | 0 | 0 |
| `6269` | 1 | 1 | 0 | 1 | 2 | 7102 | 575 | 7677 | 0 | 0 |
| `642` | 1 | 0 | 1 | 3 | 6 | 5892 | 1701 | 7593 | 0 | 0 |
| `8255` | 1 | 1 | 0 | 3 | 6 | 15406 | 2173 | 17579 | 0 | 0 |
| `8917` | 1 | 1 | 0 | 1 | 2 | 5149 | 1278 | 6427 | 0 | 0 |
| `9579` | 1 | 0 | 1 | 3 | 6 | 10457 | 3046 | 13503 | 0 | 0 |

### News Document `51591676`

- News Totals: Runs=2, Verified=2, Failed=0, Iterations Total=3, LLM Calls Total=6, Prompt Tokens Total=17063, Completion Tokens Total=2042, Total Tokens Total=19105, Precheck Events Total=0, Precheck Failed Total=0

| Client ID | Runs | Verified | Failed | Iterations Total | LLM Calls Total | Prompt Tokens Total | Completion Tokens Total | Total Tokens Total | Precheck Events Total | Precheck Failed Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `6269` | 1 | 1 | 0 | 1 | 2 | 7095 | 828 | 7923 | 0 | 0 |
| `8917` | 1 | 1 | 0 | 2 | 4 | 9968 | 1214 | 11182 | 0 | 0 |

### News Document `51591719`

- News Totals: Runs=4, Verified=2, Failed=2, Iterations Total=8, LLM Calls Total=16, Prompt Tokens Total=21549, Completion Tokens Total=5096, Total Tokens Total=26645, Precheck Events Total=0, Precheck Failed Total=0

| Client ID | Runs | Verified | Failed | Iterations Total | LLM Calls Total | Prompt Tokens Total | Completion Tokens Total | Total Tokens Total | Precheck Events Total | Precheck Failed Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `4945` | 1 | 0 | 1 | 3 | 6 | 3491 | 2405 | 5896 | 0 | 0 |
| `6269` | 1 | 1 | 0 | 1 | 2 | 6938 | 515 | 7453 | 0 | 0 |
| `642` | 1 | 0 | 1 | 3 | 6 | 6065 | 1334 | 7399 | 0 | 0 |
| `8255` | 1 | 1 | 0 | 1 | 2 | 5055 | 842 | 5897 | 0 | 0 |

### News Document `51591846`

- News Totals: Runs=8, Verified=7, Failed=1, Iterations Total=13, LLM Calls Total=26, Prompt Tokens Total=44976, Completion Tokens Total=10931, Total Tokens Total=55907, Precheck Events Total=0, Precheck Failed Total=0

| Client ID | Runs | Verified | Failed | Iterations Total | LLM Calls Total | Prompt Tokens Total | Completion Tokens Total | Total Tokens Total | Precheck Events Total | Precheck Failed Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `10241` | 1 | 1 | 0 | 2 | 4 | 3222 | 828 | 4050 | 0 | 0 |
| `3621` | 1 | 1 | 0 | 1 | 2 | 1654 | 1140 | 2794 | 0 | 0 |
| `4945` | 1 | 0 | 1 | 3 | 6 | 4379 | 1408 | 5787 | 0 | 0 |
| `6269` | 1 | 1 | 0 | 2 | 4 | 14765 | 992 | 15757 | 0 | 0 |
| `642` | 1 | 1 | 0 | 1 | 2 | 2334 | 1535 | 3869 | 0 | 0 |
| `8255` | 1 | 1 | 0 | 1 | 2 | 5425 | 1033 | 6458 | 0 | 0 |
| `8917` | 1 | 1 | 0 | 1 | 2 | 5346 | 1321 | 6667 | 0 | 0 |
| `9579` | 1 | 1 | 0 | 2 | 4 | 7851 | 2674 | 10525 | 0 | 0 |

## Stage 1

- Log files in phase: **26**
- Phase Totals: Runs=16, Verified=13, Failed=3, Iterations Total=29, LLM Calls Total=58, Prompt Tokens Total=23271, Completion Tokens Total=18037, Total Tokens Total=41308, Precheck Events Total=0, Precheck Failed Total=0

### News Document `51591719`

- News Totals: Runs=1, Verified=0, Failed=1, Iterations Total=3, LLM Calls Total=6, Prompt Tokens Total=2390, Completion Tokens Total=1644, Total Tokens Total=4034, Precheck Events Total=0, Precheck Failed Total=0

| Client ID | Runs | Verified | Failed | Iterations Total | LLM Calls Total | Prompt Tokens Total | Completion Tokens Total | Total Tokens Total | Precheck Events Total | Precheck Failed Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `8255` | 1 | 0 | 1 | 3 | 6 | 2390 | 1644 | 4034 | 0 | 0 |

### News Document `51591887`

- News Totals: Runs=2, Verified=2, Failed=0, Iterations Total=3, LLM Calls Total=6, Prompt Tokens Total=2535, Completion Tokens Total=1776, Total Tokens Total=4311, Precheck Events Total=0, Precheck Failed Total=0

| Client ID | Runs | Verified | Failed | Iterations Total | LLM Calls Total | Prompt Tokens Total | Completion Tokens Total | Total Tokens Total | Precheck Events Total | Precheck Failed Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `4945` | 1 | 1 | 0 | 1 | 2 | 751 | 492 | 1243 | 0 | 0 |
| `8917` | 1 | 1 | 0 | 2 | 4 | 1784 | 1284 | 3068 | 0 | 0 |

### News Document `51592105`

- News Totals: Runs=4, Verified=4, Failed=0, Iterations Total=7, LLM Calls Total=14, Prompt Tokens Total=5712, Completion Tokens Total=5291, Total Tokens Total=11003, Precheck Events Total=0, Precheck Failed Total=0

| Client ID | Runs | Verified | Failed | Iterations Total | LLM Calls Total | Prompt Tokens Total | Completion Tokens Total | Total Tokens Total | Precheck Events Total | Precheck Failed Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `3621` | 1 | 1 | 0 | 2 | 4 | 1564 | 1649 | 3213 | 0 | 0 |
| `4945` | 1 | 1 | 0 | 2 | 4 | 1766 | 1750 | 3516 | 0 | 0 |
| `6269` | 1 | 1 | 0 | 2 | 4 | 1604 | 1497 | 3101 | 0 | 0 |
| `8255` | 1 | 1 | 0 | 1 | 2 | 778 | 395 | 1173 | 0 | 0 |

### News Document `51592157`

- News Totals: Runs=3, Verified=2, Failed=1, Iterations Total=7, LLM Calls Total=14, Prompt Tokens Total=4958, Completion Tokens Total=3431, Total Tokens Total=8389, Precheck Events Total=0, Precheck Failed Total=0

| Client ID | Runs | Verified | Failed | Iterations Total | LLM Calls Total | Prompt Tokens Total | Completion Tokens Total | Total Tokens Total | Precheck Events Total | Precheck Failed Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `3621` | 1 | 1 | 0 | 2 | 4 | 1372 | 892 | 2264 | 0 | 0 |
| `642` | 1 | 1 | 0 | 2 | 4 | 1425 | 1000 | 2425 | 0 | 0 |
| `8255` | 1 | 0 | 1 | 3 | 6 | 2161 | 1539 | 3700 | 0 | 0 |

### News Document `51592177`

- News Totals: Runs=4, Verified=3, Failed=1, Iterations Total=7, LLM Calls Total=14, Prompt Tokens Total=5994, Completion Tokens Total=5076, Total Tokens Total=11070, Precheck Events Total=0, Precheck Failed Total=0

| Client ID | Runs | Verified | Failed | Iterations Total | LLM Calls Total | Prompt Tokens Total | Completion Tokens Total | Total Tokens Total | Precheck Events Total | Precheck Failed Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `6269` | 1 | 0 | 1 | 3 | 6 | 2705 | 1749 | 4454 | 0 | 0 |
| `642` | 1 | 1 | 0 | 1 | 2 | 818 | 1407 | 2225 | 0 | 0 |
| `8255` | 1 | 1 | 0 | 2 | 4 | 1762 | 1774 | 3536 | 0 | 0 |
| `8917` | 1 | 1 | 0 | 1 | 2 | 709 | 146 | 855 | 0 | 0 |

### News Document `51592597`

- News Totals: Runs=2, Verified=2, Failed=0, Iterations Total=2, LLM Calls Total=4, Prompt Tokens Total=1682, Completion Tokens Total=819, Total Tokens Total=2501, Precheck Events Total=0, Precheck Failed Total=0

| Client ID | Runs | Verified | Failed | Iterations Total | LLM Calls Total | Prompt Tokens Total | Completion Tokens Total | Total Tokens Total | Precheck Events Total | Precheck Failed Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `642` | 1 | 1 | 0 | 1 | 2 | 888 | 619 | 1507 | 0 | 0 |
| `8255` | 1 | 1 | 0 | 1 | 2 | 794 | 200 | 994 | 0 | 0 |

## Stage 1.1

- Log files in phase: **16**
- Phase Totals: Runs=5, Verified=5, Failed=0, Iterations Total=7, LLM Calls Total=14, Prompt Tokens Total=8084, Completion Tokens Total=2075, Total Tokens Total=10159, Precheck Events Total=0, Precheck Failed Total=0

### News Document `51592177`

- News Totals: Runs=1, Verified=1, Failed=0, Iterations Total=2, LLM Calls Total=4, Prompt Tokens Total=2521, Completion Tokens Total=386, Total Tokens Total=2907, Precheck Events Total=0, Precheck Failed Total=0

| Client ID | Runs | Verified | Failed | Iterations Total | LLM Calls Total | Prompt Tokens Total | Completion Tokens Total | Total Tokens Total | Precheck Events Total | Precheck Failed Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `8917` | 1 | 1 | 0 | 2 | 4 | 2521 | 386 | 2907 | 0 | 0 |

### News Document `51592597`

- News Totals: Runs=3, Verified=3, Failed=0, Iterations Total=4, LLM Calls Total=8, Prompt Tokens Total=4627, Completion Tokens Total=1477, Total Tokens Total=6104, Precheck Events Total=0, Precheck Failed Total=0

| Client ID | Runs | Verified | Failed | Iterations Total | LLM Calls Total | Prompt Tokens Total | Completion Tokens Total | Total Tokens Total | Precheck Events Total | Precheck Failed Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `311` | 1 | 1 | 0 | 1 | 2 | 1260 | 170 | 1430 | 0 | 0 |
| `642` | 1 | 1 | 0 | 1 | 2 | 1096 | 492 | 1588 | 0 | 0 |
| `8255` | 1 | 1 | 0 | 2 | 4 | 2271 | 815 | 3086 | 0 | 0 |

### News Document `51592959`

- News Totals: Runs=1, Verified=1, Failed=0, Iterations Total=1, LLM Calls Total=2, Prompt Tokens Total=936, Completion Tokens Total=212, Total Tokens Total=1148, Precheck Events Total=0, Precheck Failed Total=0

| Client ID | Runs | Verified | Failed | Iterations Total | LLM Calls Total | Prompt Tokens Total | Completion Tokens Total | Total Tokens Total | Precheck Events Total | Precheck Failed Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `3621` | 1 | 1 | 0 | 1 | 2 | 936 | 212 | 1148 | 0 | 0 |

## Stage 2

- Log files in phase: **30**
- Phase Totals: Runs=21, Verified=9, Failed=12, Iterations Total=49, LLM Calls Total=80, Prompt Tokens Total=37255, Completion Tokens Total=12291, Total Tokens Total=49546, Precheck Events Total=49, Precheck Failed Total=18

### News Document `51592105`

- News Totals: Runs=2, Verified=1, Failed=1, Iterations Total=4, LLM Calls Total=6, Prompt Tokens Total=2685, Completion Tokens Total=665, Total Tokens Total=3350, Precheck Events Total=4, Precheck Failed Total=2

| Client ID | Runs | Verified | Failed | Iterations Total | LLM Calls Total | Prompt Tokens Total | Completion Tokens Total | Total Tokens Total | Precheck Events Total | Precheck Failed Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `4945` | 1 | 1 | 0 | 1 | 2 | 767 | 197 | 964 | 1 | 0 |
| `8255` | 1 | 0 | 1 | 3 | 4 | 1918 | 468 | 2386 | 3 | 2 |

### News Document `51592157`

- News Totals: Runs=2, Verified=1, Failed=1, Iterations Total=4, LLM Calls Total=7, Prompt Tokens Total=2995, Completion Tokens Total=720, Total Tokens Total=3715, Precheck Events Total=4, Precheck Failed Total=1

| Client ID | Runs | Verified | Failed | Iterations Total | LLM Calls Total | Prompt Tokens Total | Completion Tokens Total | Total Tokens Total | Precheck Events Total | Precheck Failed Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `3621` | 1 | 1 | 0 | 1 | 2 | 785 | 174 | 959 | 1 | 0 |
| `8255` | 1 | 0 | 1 | 3 | 5 | 2210 | 546 | 2756 | 3 | 1 |

### News Document `51592177`

- News Totals: Runs=3, Verified=1, Failed=2, Iterations Total=8, LLM Calls Total=12, Prompt Tokens Total=6342, Completion Tokens Total=1322, Total Tokens Total=7664, Precheck Events Total=8, Precheck Failed Total=4

| Client ID | Runs | Verified | Failed | Iterations Total | LLM Calls Total | Prompt Tokens Total | Completion Tokens Total | Total Tokens Total | Precheck Events Total | Precheck Failed Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `6269` | 1 | 0 | 1 | 3 | 5 | 2478 | 577 | 3055 | 3 | 1 |
| `8255` | 1 | 0 | 1 | 3 | 4 | 2045 | 453 | 2498 | 3 | 2 |
| `8917` | 1 | 1 | 0 | 2 | 3 | 1819 | 292 | 2111 | 2 | 1 |

### News Document `51592959`

- News Totals: Runs=4, Verified=2, Failed=2, Iterations Total=8, LLM Calls Total=14, Prompt Tokens Total=7035, Completion Tokens Total=1789, Total Tokens Total=8824, Precheck Events Total=8, Precheck Failed Total=2

| Client ID | Runs | Verified | Failed | Iterations Total | LLM Calls Total | Prompt Tokens Total | Completion Tokens Total | Total Tokens Total | Precheck Events Total | Precheck Failed Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `3621` | 1 | 0 | 1 | 3 | 6 | 3084 | 909 | 3993 | 3 | 0 |
| `4945` | 1 | 1 | 0 | 1 | 2 | 804 | 188 | 992 | 1 | 0 |
| `6269` | 1 | 1 | 0 | 1 | 2 | 1132 | 259 | 1391 | 1 | 0 |
| `8255` | 1 | 0 | 1 | 3 | 4 | 2015 | 433 | 2448 | 3 | 2 |

### News Document `51593269`

- News Totals: Runs=5, Verified=1, Failed=4, Iterations Total=13, LLM Calls Total=19, Prompt Tokens Total=9350, Completion Tokens Total=4384, Total Tokens Total=13734, Precheck Events Total=13, Precheck Failed Total=7

| Client ID | Runs | Verified | Failed | Iterations Total | LLM Calls Total | Prompt Tokens Total | Completion Tokens Total | Total Tokens Total | Precheck Events Total | Precheck Failed Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `311` | 1 | 0 | 1 | 3 | 3 | 1544 | 934 | 2478 | 3 | 3 |
| `4945` | 1 | 0 | 1 | 3 | 4 | 1596 | 1907 | 3503 | 3 | 2 |
| `642` | 1 | 0 | 1 | 3 | 5 | 2209 | 538 | 2747 | 3 | 1 |
| `8255` | 1 | 1 | 0 | 1 | 2 | 1043 | 496 | 1539 | 1 | 0 |
| `8917` | 1 | 0 | 1 | 3 | 5 | 2958 | 509 | 3467 | 3 | 1 |

### News Document `51593388`

- News Totals: Runs=5, Verified=3, Failed=2, Iterations Total=12, LLM Calls Total=22, Prompt Tokens Total=8848, Completion Tokens Total=3411, Total Tokens Total=12259, Precheck Events Total=12, Precheck Failed Total=2

| Client ID | Runs | Verified | Failed | Iterations Total | LLM Calls Total | Prompt Tokens Total | Completion Tokens Total | Total Tokens Total | Precheck Events Total | Precheck Failed Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `10241` | 1 | 0 | 1 | 3 | 5 | 1805 | 835 | 2640 | 3 | 1 |
| `3621` | 1 | 1 | 0 | 2 | 4 | 1605 | 390 | 1995 | 2 | 0 |
| `4945` | 1 | 1 | 0 | 2 | 4 | 1598 | 933 | 2531 | 2 | 0 |
| `642` | 1 | 0 | 1 | 3 | 5 | 1997 | 481 | 2478 | 3 | 1 |
| `8255` | 1 | 1 | 0 | 2 | 4 | 1843 | 772 | 2615 | 2 | 0 |

## Latest Daily Audit: 2026-04-02

- Audit scope: `src/app/modules/MAS/logs/generate_insight/20260402*.log`
- Local audit date: `2026-04-02`
- Runs audited: `32`

### Executive Summary

- Total runs today: `32`
- Verified: `14`
- Failed: `18`
- Total prompt tokens: `87,031`
- Total completion tokens: `61,432`
- Total tokens: `148,463`
- Total iterations: `80`
- Total LLM calls: `136`

The main token problem is no longer raw verifier feedback replay. The current dominant waste is repeated per-client reasoning over the same news item, combined with repeated failures on no-direct-overlap cases and security-type misreads.

### Highest-Impact Findings

- `10` runs had `news_symbol_overlap = 0`; only `1` verified and `9` failed, consuming `40,118` total tokens.
- Repeated news processing dominates spend: repeated news docs consumed `138,078 / 148,463` tokens, about `93%` of today’s total.
- Verifier cost remains high: `insight_generator` used `79,543` tokens across `80` calls; `verifier` used `68,920` tokens across `56` calls.
- Most common precheck failures were `missing_no_direct_exposure_statement` (`13`), `too_long` (`7`), and `missing_direct_symbol_reference` (`4`).

### News Documents With Highest Total Token Spend Today

| News Doc ID | Runs | Verified | Failed | Client IDs | Total Tokens |
|---|---:|---:|---:|---|---:|
| `51613814` | 3 | 0 | 3 | `311`, `6269`, `8917` | 22269 |
| `51617921` | 3 | 1 | 2 | `311`, `6269`, `8917` | 17773 |
| `51615449` | 3 | 3 | 0 | `311`, `6269`, `8917` | 17345 |
| `51618792` | 4 | 1 | 3 | `311`, `3621`, `642`, `8255` | 16650 |
| `51617026` | 3 | 2 | 1 | `311`, `6269`, `8917` | 16513 |
| `51618508` | 3 | 2 | 1 | `311`, `3621`, `6269` | 13182 |
| `51618226` | 3 | 0 | 3 | `311`, `3621`, `642` | 11953 |
| `51617187` | 3 | 0 | 3 | `642`, `8255`, `8917` | 11515 |
| `51617517` | 2 | 1 | 1 | `311`, `6269` | 6421 |
| `51619236` | 1 | 0 | 1 | `311` | 6360 |

### Most Expensive Individual Runs Today

| Log File | News Doc ID | Client ID | Status | Iterations | LLM Calls | Total Tokens |
|---|---|---|---|---:|---:|---:|
| `20260402T101044923749Z_311_51613814.log` | `51613814` | `311` | `failed` | 3 | 6 | 8509 |
| `20260402T101129133106Z_311_51617026.log` | `51617026` | `311` | `verified` | 3 | 6 | 8208 |
| `20260402T101057394085Z_6269_51613814.log` | `51613814` | `6269` | `failed` | 3 | 6 | 7221 |
| `20260402T101158350126Z_311_51615449.log` | `51615449` | `311` | `verified` | 3 | 6 | 7214 |
| `20260402T101054885240Z_311_51617921.log` | `51617921` | `311` | `verified` | 3 | 6 | 6948 |
| `20260402T101212297318Z_8917_51613814.log` | `51613814` | `8917` | `failed` | 3 | 5 | 6539 |
| `20260402T101335397812Z_8917_51617026.log` | `51617026` | `8917` | `failed` | 3 | 5 | 6391 |
| `20260402T101042852749Z_311_51619236.log` | `51619236` | `311` | `failed` | 3 | 6 | 6360 |
| `20260402T101241057943Z_311_51618508.log` | `51618508` | `311` | `failed` | 3 | 6 | 6318 |
| `20260402T101044916685Z_6269_51617921.log` | `51617921` | `6269` | `failed` | 3 | 4 | 5845 |

### Overlap Analysis

| News Symbol Overlap Count | Runs | Verified | Failed | Total Tokens |
|---|---:|---:|---:|---:|
| `0` | 10 | 1 | 9 | 40118 |
| `1` | 12 | 7 | 5 | 52119 |
| `2` | 7 | 6 | 1 | 34136 |
| `3` | 2 | 0 | 2 | 13581 |
| `4` | 1 | 0 | 1 | 8509 |

Zero-overlap runs are currently a poor use of tokens unless they are handled by a much cheaper deterministic or template-driven path.

### Revision Compaction Status

- Verifier compaction events observed: `56`
- Full feedback chars total: `36,578`
- Compact payload chars total: `24,119`
- Estimated revision-guidance compaction savings: `34.06%`
- Compaction occurred in `48` of `56` verifier completions

This confirms the structured revision-guidance change is helping, but it is no longer the biggest remaining waste source.

### Representative Problem Cases

- No-direct-overlap control failure and repeated precheck churn: [20260402T101404565126Z_8255_51618792.log](/home/harshathvenkastesh/Desktop/SMIF/src/app/modules/MAS/logs/generate_insight/20260402T101404565126Z_8255_51618792.log)
- Security-type misread causing three full iterations before failure: [20260402T101042852749Z_311_51619236.log](/home/harshathvenkastesh/Desktop/SMIF/src/app/modules/MAS/logs/generate_insight/20260402T101042852749Z_311_51619236.log)

### Current Architectural Read

- The portfolio compaction layer is working and visibly cuts prompt size.
- Structured verifier guidance is working and reduces loop bloat.
- The dominant unresolved issue is still architectural duplication: the same news is being reasoned about repeatedly for multiple clients, low-relevance/no-direct-overlap cases are still allowed into expensive iterative loops, and security-type awareness is not strong enough before generation.

### Recommended Next Focus

- Add a cheap per-news analysis cache that is reused across clients.
- Add a deterministic zero-overlap path that avoids full iterative generation unless a minimum relevance bar is met.
- Add security-type aware preprocessing so issuer debt is not treated like equity exposure during generation.

## Latest Daily Audit Update: 2026-04-02 (Newer Log Set)

- Audit scope: `src/app/modules/MAS/logs/generate_insight/20260402*.log`
- Snapshot type: full-day recompute after newer logs arrived
- Runs audited: `122`

### Executive Summary

- Total runs: `122`
- Verified: `59`
- Failed: `63`
- Total prompt tokens: `298,922`
- Total completion tokens: `219,581`
- Total tokens: `518,503`
- Total iterations: `293`
- Total LLM calls: `499`

The additional logs did not change the architectural conclusion. The dominant waste is still duplicated per-news reasoning across clients, with zero-overlap cases and repeated regeneration loops consuming a disproportionate share of spend.

### Highest-Impact Findings

- Repeated news processing consumed `512,069 / 518,503` tokens, about `98.76%` of the full-day total.
- Zero-overlap runs remain the worst bucket: `44` runs, only `10` verified and `34` failed, consuming `178,213` tokens.
- Verifier cost remains substantial: `insight_generator` used `283,461` tokens across `293` calls; `verifier` used `235,042` tokens across `206` calls.
- Most common precheck failures were `missing_no_direct_exposure_statement` (`47`), `too_long` (`26`), `missing_direct_symbol_reference` (`13`), and `empty_draft` (`1`).

### News Documents With Highest Total Token Spend In The Updated Full-Day Snapshot

| News Doc ID | Runs | Verified | Failed | Client IDs | Total Tokens |
|---|---:|---:|---:|---|---:|
| `51618792` | 14 | 1 | 13 | `10572`, `10903`, `11234`, `1304`, `311`, `3621`, `5938`, `642`, `6931`, `8255`, `9910` | 61081 |
| `51618226` | 13 | 3 | 10 | `10572`, `10903`, `11234`, `1304`, `311`, `3621`, `5938`, `642`, `6931`, `9910` | 49379 |
| `51617921` | 8 | 4 | 4 | `311`, `5938`, `6269`, `8917`, `9910` | 41710 |
| `51617026` | 8 | 5 | 3 | `311`, `5938`, `6269`, `8917`, `9910` | 39410 |
| `51617707` | 10 | 3 | 7 | `10572`, `10903`, `1304`, `2959`, `4283`, `4614`, `5938`, `8255`, `9910` | 38383 |
| `51618934` | 6 | 3 | 3 | `11234`, `311`, `6931`, `8255`, `8917`, `9910` | 37424 |
| `51613814` | 6 | 2 | 4 | `311`, `5938`, `6269`, `6931`, `8917`, `9910` | 37096 |
| `51615449` | 7 | 5 | 2 | `311`, `5938`, `6269`, `8917` | 35682 |
| `51619236` | 8 | 6 | 2 | `10903`, `311`, `3621`, `5938`, `6269`, `6931`, `9910` | 32887 |
| `51618508` | 9 | 7 | 2 | `10903`, `311`, `3621`, `5938`, `6269`, `6931` | 30001 |
| `51617517` | 5 | 2 | 3 | `311`, `6269`, `9910` | 23376 |
| `51620263` | 6 | 4 | 2 | `10903`, `311`, `3621`, `5938`, `6269`, `6931` | 22303 |

### Most Expensive Individual Runs In The Updated Snapshot

| Log File | News Doc ID | Client ID | Status | Iterations | LLM Calls | Total Tokens |
|---|---|---|---|---:|---:|---:|
| `20260402T103838493138Z_8917_51618934.log` | `51618934` | `8917` | `failed` | 3 | 5 | 9074 |
| `20260402T101044923749Z_311_51613814.log` | `51613814` | `311` | `failed` | 3 | 6 | 8509 |
| `20260402T101129133106Z_311_51617026.log` | `51617026` | `311` | `verified` | 3 | 6 | 8208 |
| `20260402T104054714460Z_6269_51617517.log` | `51617517` | `6269` | `failed` | 3 | 6 | 7619 |
| `20260402T104111584638Z_311_51617921.log` | `51617921` | `311` | `failed` | 3 | 6 | 7306 |
| `20260402T101057394085Z_6269_51613814.log` | `51613814` | `6269` | `failed` | 3 | 6 | 7221 |
| `20260402T101158350126Z_311_51615449.log` | `51615449` | `311` | `verified` | 3 | 6 | 7214 |
| `20260402T103839343316Z_6269_51619236.log` | `51619236` | `6269` | `verified` | 3 | 6 | 7062 |
| `20260402T101054885240Z_311_51617921.log` | `51617921` | `311` | `verified` | 3 | 6 | 6948 |
| `20260402T103837496367Z_311_51618934.log` | `51618934` | `311` | `failed` | 3 | 6 | 6940 |
| `20260402T104313751269Z_8917_51617026.log` | `51617026` | `8917` | `failed` | 3 | 5 | 6891 |
| `20260402T103836461353Z_6269_51620263.log` | `51620263` | `6269` | `failed` | 3 | 6 | 6734 |

### Client Totals In The Updated Snapshot

| Client ID | Runs | Verified | Failed | Total Tokens |
|---|---:|---:|---:|---:|
| `311` | 21 | 8 | 13 | 112161 |
| `6269` | 19 | 14 | 5 | 85666 |
| `8917` | 10 | 4 | 6 | 56001 |
| `9910` | 10 | 4 | 6 | 40109 |
| `6931` | 9 | 5 | 4 | 36249 |
| `5938` | 11 | 6 | 5 | 35584 |
| `8255` | 8 | 4 | 4 | 30931 |
| `3621` | 9 | 4 | 5 | 26541 |
| `642` | 6 | 2 | 4 | 22914 |
| `10903` | 7 | 4 | 3 | 22027 |

### Overlap Analysis

| News Symbol Overlap Count | Runs | Verified | Failed | Total Tokens |
|---|---:|---:|---:|---:|
| `0` | 44 | 10 | 34 | 178213 |
| `1` | 54 | 32 | 22 | 218524 |
| `2` | 19 | 16 | 3 | 87273 |
| `3` | 4 | 1 | 3 | 25984 |
| `4` | 1 | 0 | 1 | 8509 |

The zero-overlap bucket is still an obvious candidate for a cheaper deterministic path or an early exit policy.

### Revision Compaction Status

- Verifier compaction events observed: `206`
- Full feedback chars total: `128,330`
- Compact payload chars total: `85,584`
- Estimated revision-guidance compaction savings: `33.31%`
- Compaction occurred in `187` of `206` verifier completions

The compaction layer is still working, but it is now clearly a secondary optimization. The first-order waste is repeated reasoning and failed iteration churn.

### Updated Architectural Read

- The compaction work is still holding up under higher volume.
- Prompt replay from full verifier prose is no longer the main issue.
- The dominant waste pattern is now more obvious at scale: the same news docs are being reasoned about repeatedly across many clients, zero-overlap cases are still allowed to spend thousands of tokens each, and the loop still burns multiple iterations on controllable format and framing failures.

### Updated Next Focus

- Introduce reusable per-news analysis objects so repeated news does not restart reasoning from scratch for each client.
- Add a zero-overlap fast path with deterministic phrasing and stricter routing before iterative LLM generation starts.
- Strengthen preprocessing for security type and mandate constraints so the generator is not asked to infer these late in the loop.
