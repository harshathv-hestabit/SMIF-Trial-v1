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

## Latest Daily Audit: 2026-04-03 (New Relevance System / Client Processing)

- Audit scope: `src/app/modules/MAS/logs/generate_insight/20260403*.log`
- Local audit date: `2026-04-03`
- Runs audited: `47`

### Executive Summary

- Total runs: `47`
- Verified: `21`
- Failed: `26`
- Total prompt tokens: `108,850`
- Total completion tokens: `73,267`
- Total tokens: `182,117`
- Total iterations: `107`
- Total LLM calls: `174`

The new relevance system is visible in prompts via `Grounded Relevance: direct|indirect`, but today’s logs do not show evidence of a major token-efficiency breakthrough yet. The system still spent `182,117` tokens in one day, all of it on repeated-news documents, and indirect-relevance cases remain highly failure-prone.

### Highest-Impact Findings

- Repeated news processing still accounts for all spend today: `182,117 / 182,117` tokens were on multi-client repeated news docs.
- `Grounded Relevance` now appears in prompts: `direct` had `33` runs, `20` verified, `13` failed, and `117,323` tokens; `indirect` had `14` runs, `1` verified, `13` failed, and `64,794` tokens.
- Indirect relevance is still a poor spend bucket: only `1` of `14` indirect runs verified.
- Most common precheck failures were `missing_no_direct_exposure_statement` (`20`), `too_long` (`17`), `empty_draft` (`2`), and `missing_direct_symbol_reference` (`1`).
- Verifier cost remains material: `insight_generator` used `103,718` tokens across `107` calls; `verifier` used `78,399` tokens across `67` calls.

### New Telemetry Gap

- All `47` runs logged an empty `agent_context_profile.profile`.
- Because of that, the old `news_symbol_overlap` / compact-profile telemetry is effectively absent from today’s logs.
- The historical overlap audit is therefore no longer comparable on `2026-04-03`; the meaningful routing signal today is `Grounded Relevance`, not `compact_counts.news_symbol_overlap`.

This is an auditability regression. The new relevance architecture may be better, but the logs no longer expose enough structured context to prove why a run was classified as direct vs indirect or how much compaction/filtering was achieved.

### News Documents With Highest Total Token Spend Today

| News Doc ID | Runs | Verified | Failed | Client IDs | Total Tokens |
|---|---:|---:|---:|---|---:|
| `51643306` | 5 | 1 | 4 | `311`, `3621`, `6269`, `8255`, `8917` | 24003 |
| `51632723` | 5 | 2 | 3 | `311`, `3621`, `8255`, `8917`, `9579` | 19328 |
| `51633652` | 3 | 1 | 2 | `311`, `3621`, `8917` | 13274 |
| `51633458` | 2 | 0 | 2 | `311`, `3621` | 12195 |
| `51636374` | 3 | 0 | 3 | `311`, `3621`, `642` | 11211 |
| `51633653` | 2 | 0 | 2 | `311`, `8917` | 10843 |
| `51633899` | 2 | 1 | 1 | `311`, `6269` | 10710 |
| `51637298` | 2 | 1 | 1 | `311`, `6269` | 9175 |
| `51644008` | 2 | 1 | 1 | `311`, `3621` | 8648 |
| `51635025` | 2 | 0 | 2 | `311`, `8917` | 8486 |
| `51636047` | 2 | 2 | 0 | `311`, `3621` | 7547 |
| `51639363` | 3 | 2 | 1 | `311`, `8255`, `8917` | 7529 |

### Most Expensive Individual Runs Today

| Log File | News Doc ID | Client ID | Status | Iterations | LLM Calls | Total Tokens |
|---|---|---|---|---:|---:|---:|
| `20260403T100050132725Z_6269_51633899.log` | `51633899` | `6269` | `failed` | 3 | 6 | 7128 |
| `20260403T100154515853Z_8255_51643306.log` | `51643306` | `8255` | `failed` | 3 | 5 | 7035 |
| `20260403T100040144504Z_6269_51637298.log` | `51637298` | `6269` | `failed` | 3 | 5 | 6729 |
| `20260403T100039195479Z_3621_51633458.log` | `51633458` | `3621` | `failed` | 3 | 6 | 6195 |
| `20260403T100044147927Z_311_51633458.log` | `51633458` | `311` | `failed` | 3 | 6 | 6000 |
| `20260403T100046418329Z_8917_51633653.log` | `51633653` | `8917` | `failed` | 3 | 5 | 5822 |
| `20260403T100224301375Z_9579_51632723.log` | `51632723` | `9579` | `failed` | 3 | 4 | 5680 |
| `20260403T100535613897Z_8917_51633652.log` | `51633652` | `8917` | `failed` | 3 | 5 | 5677 |
| `20260403T100039651601Z_3621_51644008.log` | `51644008` | `3621` | `failed` | 3 | 6 | 5363 |
| `20260403T100400437916Z_3621_51636047.log` | `51636047` | `3621` | `verified` | 3 | 5 | 5143 |
| `20260403T100139232489Z_311_51632723.log` | `51632723` | `311` | `failed` | 3 | 5 | 5090 |
| `20260403T100039266801Z_311_51633653.log` | `51633653` | `311` | `failed` | 3 | 5 | 5021 |

### Client Totals Today

| Client ID | Runs | Verified | Failed | Total Tokens |
|---|---:|---:|---:|---:|
| `311` | 19 | 11 | 8 | 66201 |
| `3621` | 11 | 5 | 6 | 39531 |
| `8917` | 9 | 3 | 6 | 35097 |
| `6269` | 3 | 1 | 2 | 17777 |
| `8255` | 3 | 1 | 2 | 13757 |
| `9579` | 1 | 0 | 1 | 5680 |
| `642` | 1 | 0 | 1 | 4074 |

### Grounded Relevance Breakdown

| Grounded Relevance | Runs | Verified | Failed | Total Tokens |
|---|---:|---:|---:|---:|
| `direct` | 33 | 20 | 13 | 117323 |
| `indirect` | 14 | 1 | 13 | 64794 |

This is the most useful new quality signal in today’s logs. The current indirect path is still too expensive relative to its success rate.

### Revision Compaction Status

- Verifier compaction events observed: `67`
- Full feedback chars total: `42,132`
- Compact payload chars total: `27,226`
- Estimated revision-guidance compaction savings: `35.38%`
- Compaction occurred in `64` of `67` verifier completions

The revision-guidance optimization is still working. It is not the bottleneck.

### Representative Findings From Sample Logs

- New prompts include `Grounded Relevance`, for example an indirect Nike downgrade case: [20260403T100039090274Z_311_51633960.log](/home/harshathvenkastesh/Desktop/SMIF/src/app/modules/MAS/logs/generate_insight/20260403T100039090274Z_311_51633960.log)
- The same run still failed after three iterations because the system could not produce a convincing portfolio-specific indirect insight.
- Another indirect tech-whale-activity case burned `5,677` tokens and still failed after three iterations: [20260403T100535613897Z_8917_51633652.log](/home/harshathvenkastesh/Desktop/SMIF/src/app/modules/MAS/logs/generate_insight/20260403T100535613897Z_8917_51633652.log)

### Architectural Read For The New System

- The new relevance architecture is surfacing a useful direct/indirect label.
- It does not yet show a token-efficiency win at the workflow level.
- The strongest signal today is negative: indirect runs are still entering expensive iterative generation and mostly failing.
- The loss of compact-profile telemetry makes it harder to validate whether the new client-processing architecture is actually filtering context better than the previous one.

### Recommended Next Focus

- Add explicit log fields for the new relevance pipeline output: matched holdings count, relevance reason, filtered holdings count, dropped holdings count, and compaction/selection char estimates.
- Route `indirect` relevance through a cheaper template or capped single-pass path instead of full iterative generation by default.
- Restore structured portfolio-compaction telemetry so token savings remain measurable after the architecture change.

## Latest Daily Audit Update: 2026-04-03 (Expanded Log Set)

- Audit scope: `src/app/modules/MAS/logs/generate_insight/20260403*.log`
- Snapshot type: full-day recompute after additional logs arrived
- Runs audited: `174`

### Executive Summary

- Total runs: `174`
- Verified: `90`
- Failed: `84`
- Total prompt tokens: `383,711`
- Total completion tokens: `253,850`
- Total tokens: `637,561`
- Total iterations: `386`
- Total LLM calls: `640`

Compared with the earlier `47`-run snapshot for `2026-04-03`, the newer logs strengthen the same conclusion: the new relevance architecture exposes a useful `direct`/`indirect` label, but it has not yet produced a workflow-level token-efficiency win.

### Highest-Impact Findings

- Repeated news processing still accounts for all spend today: `637,561 / 637,561` tokens were spent on repeated multi-client news documents.
- `Grounded Relevance` remains the most useful routing signal: `direct` had `104` runs, `78` verified, `26` failed, and `338,718` tokens; `indirect` had `70` runs, `12` verified, `58` failed, and `298,843` tokens.
- Indirect runs are still very low yield: only `12` of `70` verified while consuming nearly half of all tokens.
- Most common precheck failures were `missing_no_direct_exposure_statement` (`89`), `too_long` (`39`), `empty_draft` (`3`), and `missing_direct_symbol_reference` (`1`).
- Verifier cost remains material: `insight_generator` used `346,270` tokens across `386` calls; `verifier` used `291,291` tokens across `254` calls.

### Telemetry Status

- All `174` runs still logged an empty `agent_context_profile.profile`.
- The old compact-profile and overlap telemetry remains absent.
- This means the new system is currently less auditable than the earlier compaction-based pipeline, even if the underlying relevance classification may be better.

### News Documents With Highest Total Token Spend In The Expanded Snapshot

| News Doc ID | Runs | Verified | Failed | Client IDs | Total Tokens |
|---|---:|---:|---:|---|---:|
| `51632723` | 20 | 4 | 16 | `10572`, `10903`, `11234`, `1304`, `2959`, `311`, `3621`, `4283`, `4614`, `5938`, `6931`, `8255`, `8917`, `9579`, `9910` | 93872 |
| `51643306` | 15 | 7 | 8 | `10572`, `10903`, `1304`, `2959`, `311`, `3621`, `4283`, `4614`, `5938`, `6269`, `6931`, `8255`, `8917`, `9910` | 70505 |
| `51633658` | 13 | 5 | 8 | `10572`, `10903`, `11234`, `1304`, `311`, `5938`, `6269`, `6931`, `7262`, `8917`, `9910` | 52360 |
| `51633653` | 12 | 1 | 11 | `10572`, `10903`, `11234`, `1304`, `311`, `5938`, `6931`, `7262`, `8917`, `9910` | 44817 |
| `51636374` | 11 | 2 | 9 | `10572`, `10903`, `11234`, `1304`, `311`, `3621`, `5938`, `6269`, `642`, `6931`, `9910` | 35394 |
| `51633652` | 10 | 6 | 4 | `10903`, `311`, `3621`, `5938`, `6269`, `6931`, `7262`, `8917` | 33442 |
| `51633458` | 8 | 3 | 5 | `10903`, `311`, `3621`, `5938`, `6269`, `6931` | 32492 |
| `51643875` | 8 | 7 | 1 | `311`, `5938`, `6269`, `6931`, `8917`, `9910` | 27682 |
| `51644008` | 8 | 7 | 1 | `10903`, `311`, `3621`, `5938`, `6269`, `6931` | 26703 |
| `51637298` | 6 | 3 | 3 | `11234`, `311`, `6269`, `9910` | 25166 |
| `51633914` | 8 | 7 | 1 | `10903`, `311`, `3621`, `5938`, `6269`, `6931` | 25015 |
| `51639363` | 7 | 4 | 3 | `311`, `6931`, `8255`, `8917` | 24919 |
| `51633899` | 5 | 4 | 1 | `311`, `6269`, `9910` | 24112 |
| `51636047` | 8 | 8 | 0 | `10903`, `311`, `3621`, `5938`, `6269`, `6931` | 21862 |
| `51635025` | 6 | 1 | 5 | `11234`, `311`, `6931`, `8917` | 21756 |

### Most Expensive Individual Runs In The Expanded Snapshot

| Log File | News Doc ID | Client ID | Status | Iterations | LLM Calls | Total Tokens |
|---|---|---|---|---:|---:|---:|
| `20260403T105517790685Z_6269_51633658.log` | `51633658` | `6269` | `verified` | 3 | 6 | 8082 |
| `20260403T100050132725Z_6269_51633899.log` | `51633899` | `6269` | `failed` | 3 | 6 | 7128 |
| `20260403T110605426962Z_5938_51632723.log` | `51632723` | `5938` | `failed` | 3 | 5 | 7128 |
| `20260403T105527408926Z_311_51637298.log` | `51637298` | `311` | `failed` | 3 | 6 | 7078 |
| `20260403T100154515853Z_8255_51643306.log` | `51643306` | `8255` | `failed` | 3 | 5 | 7035 |
| `20260403T105634627749Z_311_51632723.log` | `51632723` | `311` | `failed` | 3 | 6 | 6832 |
| `20260403T100040144504Z_6269_51637298.log` | `51637298` | `6269` | `failed` | 3 | 5 | 6729 |
| `20260403T105536417210Z_8917_51633658.log` | `51633658` | `8917` | `failed` | 3 | 5 | 6386 |
| `20260403T110648647978Z_4614_51632723.log` | `51632723` | `4614` | `failed` | 3 | 5 | 6357 |
| `20260403T110433452651Z_10903_51633652.log` | `51633652` | `10903` | `failed` | 3 | 5 | 6255 |
| `20260403T100039195479Z_3621_51633458.log` | `51633458` | `3621` | `failed` | 3 | 6 | 6195 |
| `20260403T105711003376Z_6269_51633899.log` | `51633899` | `6269` | `verified` | 2 | 4 | 6055 |
| `20260403T100044147927Z_311_51633458.log` | `51633458` | `311` | `failed` | 3 | 6 | 6000 |
| `20260403T110634868149Z_4283_51632723.log` | `51632723` | `4283` | `failed` | 3 | 6 | 5954 |
| `20260403T100046418329Z_8917_51633653.log` | `51633653` | `8917` | `failed` | 3 | 5 | 5822 |

### Client Totals In The Expanded Snapshot

| Client ID | Runs | Verified | Failed | Total Tokens |
|---|---:|---:|---:|---:|
| `311` | 36 | 22 | 14 | 132604 |
| `6931` | 17 | 7 | 10 | 64677 |
| `3621` | 20 | 11 | 9 | 64186 |
| `8917` | 16 | 6 | 10 | 63354 |
| `6269` | 17 | 15 | 2 | 59083 |
| `5938` | 14 | 8 | 6 | 47031 |
| `10903` | 13 | 6 | 7 | 43063 |
| `9910` | 8 | 5 | 3 | 28186 |
| `8255` | 5 | 2 | 3 | 25052 |
| `1304` | 5 | 1 | 4 | 21972 |

### Grounded Relevance Breakdown

| Grounded Relevance | Runs | Verified | Failed | Total Tokens |
|---|---:|---:|---:|---:|
| `direct` | 104 | 78 | 26 | 338718 |
| `indirect` | 70 | 12 | 58 | 298843 |

The updated full-day snapshot makes the indirect problem clearer: `40.23%` of runs are indirect, but they account for `46.87%` of all tokens and have an `82.86%` failure rate.

### Revision Compaction Status

- Verifier compaction events observed: `254`
- Full feedback chars total: `163,355`
- Compact payload chars total: `103,719`
- Estimated revision-guidance compaction savings: `36.51%`
- Compaction occurred in `241` of `254` verifier completions

The revision-guidance optimization still holds up. The main problem remains routing and iteration cost, not feedback replay.

### Updated Architectural Read

- The new relevance architecture still looks directionally correct in one respect: `direct` runs verify much more often than `indirect` runs.
- The token-efficiency outcome is still weak because the system continues to send many indirect cases into expensive iterative generation.
- The auditability regression remains unresolved: every `agent_context_profile.profile` is empty, so the new client-processing architecture cannot currently be validated through logs the way the previous compaction pipeline could.

### Updated Next Focus

- Add an `indirect` fast path with a hard cap of one generation pass and no verifier loop unless a stronger escalation condition is met.
- Restore structured telemetry for the new client-processing output so logs show why holdings were selected, how many were dropped, and what compaction or selection savings were achieved.
- Add a daily dashboard metric for `indirect verified %`, `indirect tokens / total tokens`, and `tokens per news doc` so the new relevance system can be measured as an optimization, not just observed qualitatively.

## Latest Daily Audit: 2026-04-06

- Audit scope: `src/app/modules/MAS/logs/generate_insight/20260406*.log`
- Local audit date: `2026-04-06`
- Runs audited: `49`

### Executive Summary

- Total runs: `49`
- Verified: `39`
- Failed: `10`
- Total prompt tokens: `97,860`
- Total completion tokens: `61,654`
- Total tokens: `159,514`
- Total iterations: `79`
- Total LLM calls: `153`

This is the first recent log set that shows a real workflow improvement. Verification rate is much higher than the `2026-04-03` runs, route-level telemetry is richer, and precheck churn is much lower. The remaining issues are narrower: all runs still go through `full_loop`, verifier cost still exceeds generator cost, and `agent_context_profile.profile` is still empty.

### Highest-Impact Findings

- Verification rate improved to `39 / 49` (`79.59%`), with only `10` failures.
- Route telemetry is now present on every run: execution route is `full_loop` on all `49` runs, grounded relevance is `direct` on all `49` runs, and security type alignment is `True` on all `49` runs.
- Repeated news still dominates spend, but not absolutely: repeated-news tokens were `136,495` and single-news tokens were `23,019`.
- Average matched holdings per routed run: `11.2`
- Max matched holdings in a single run: `68`
- Matched symbols were non-empty in `45` runs and empty in `4` runs.
- Most common precheck failures were only `missing_no_direct_exposure_statement` (`4`) and `missing_direct_symbol_reference` (`1`).
- Verifier cost remains material: `insight_generator` used `71,762` tokens across `79` calls; `verifier` used `87,752` tokens across `74` calls.

### Important Route-Level Read

- The new routing system appears to be filtering out indirect/weak cases before they reach this workflow.
- That is likely the main reason the `2026-04-06` success rate is materially better than the `2026-04-03` runs.
- However, every routed case still goes to `full_loop`, so the architecture has not yet started converting routing confidence into cheaper execution modes.

### Telemetry Status

- Route-level logging is much better than on `2026-04-03`.
- `workflow_route_received` now records `execution_route`, `route_reason`, `grounded_relevance`, `matched_holdings_count`, `matched_symbols`, and `security_type_alignment`.
- But `agent_context_profile.profile` is still empty on all `49` runs, so compact-profile / filtering / compaction auditability is still missing.

### News Documents With Highest Total Token Spend Today

| News Doc ID | Runs | Verified | Failed | Client IDs | Total Tokens |
|---|---:|---:|---:|---|---:|
| `51649729` | 8 | 7 | 1 | `10903`, `311`, `3621`, `5938`, `6269`, `6931`, `8255`, `9910` | 22201 |
| `51650557` | 5 | 3 | 2 | `311`, `5938`, `6269`, `8917`, `9910` | 22043 |
| `51650423` | 5 | 4 | 1 | `10903`, `311`, `3621`, `5938`, `6269` | 16843 |
| `51644008` | 5 | 4 | 1 | `10903`, `311`, `3621`, `6269`, `6931` | 14423 |
| `51644811` | 2 | 1 | 1 | `311`, `6269` | 13132 |
| `51643875` | 3 | 2 | 1 | `311`, `6269`, `8917` | 11609 |
| `51637298` | 2 | 2 | 0 | `311`, `6269` | 9119 |
| `51644048` | 5 | 5 | 0 | `10903`, `311`, `3621`, `6269`, `6931` | 8545 |
| `51639363` | 2 | 1 | 1 | `8255`, `8917` | 7369 |
| `51651901` | 3 | 3 | 0 | `311`, `6269`, `9910` | 6233 |

### Most Expensive Individual Runs Today

| Log File | News Doc ID | Client ID | Status | Iterations | LLM Calls | Total Tokens |
|---|---|---|---|---:|---:|---:|
| `20260406T074746710786Z_311_51649729.log` | `51649729` | `311` | `failed` | 3 | 6 | 6791 |
| `20260406T074931716218Z_6269_51644811.log` | `51644811` | `6269` | `failed` | 3 | 6 | 6638 |
| `20260406T074845456199Z_311_51637298.log` | `51637298` | `311` | `verified` | 3 | 6 | 6623 |
| `20260406T074956876252Z_311_51644811.log` | `51644811` | `311` | `verified` | 3 | 6 | 6494 |
| `20260406T075009523071Z_311_51643875.log` | `51643875` | `311` | `failed` | 3 | 6 | 6385 |
| `20260406T075035841659Z_9910_51650557.log` | `51650557` | `9910` | `failed` | 3 | 6 | 6380 |
| `20260406T074749337519Z_3621_51650423.log` | `51650423` | `3621` | `failed` | 3 | 6 | 6064 |
| `20260406T074812639343Z_311_51644008.log` | `51644008` | `311` | `failed` | 3 | 6 | 6052 |
| `20260406T074937788044Z_8917_51639363.log` | `51639363` | `8917` | `failed` | 3 | 6 | 6045 |
| `20260406T074744596872Z_311_51650557.log` | `51650557` | `311` | `failed` | 3 | 5 | 5813 |

### Client Totals Today

| Client ID | Runs | Verified | Failed | Total Tokens |
|---|---:|---:|---:|---:|
| `311` | 10 | 6 | 4 | 49948 |
| `6269` | 12 | 11 | 1 | 36966 |
| `8917` | 5 | 3 | 2 | 21113 |
| `3621` | 6 | 4 | 2 | 16978 |
| `9910` | 3 | 2 | 1 | 9017 |
| `10903` | 4 | 4 | 0 | 9001 |
| `5938` | 4 | 4 | 0 | 8887 |
| `6931` | 3 | 3 | 0 | 4743 |
| `8255` | 2 | 2 | 0 | 2861 |

### Revision Compaction Status

- Verifier compaction events observed: `74`
- Full feedback chars total: `42,780`
- Compact payload chars total: `28,843`
- Estimated revision-guidance compaction savings: `32.58%`
- Compaction occurred in `68` of `74` verifier completions

The feedback-compaction layer is still working, but it is no longer the main story in this log set.

### Representative Findings From Sample Logs

- Route instrumentation is now much richer, for example: [20260406T074744596872Z_311_51650557.log](/home/harshathvenkastesh/Desktop/SMIF/src/app/modules/MAS/logs/generate_insight/20260406T074744596872Z_311_51650557.log)
- That sample also shows a remaining failure pattern: good direct grounding, but iterative outputs still drift into discretionary trade language that breaches `execution-only` constraints.
- Another notable edge case is a run classified as `direct` with `matched_holdings_count = 9` but `matched_symbols = []`: [20260406T075317164126Z_2959_51644811.log](/home/harshathvenkastesh/Desktop/SMIF/src/app/modules/MAS/logs/generate_insight/20260406T075317164126Z_2959_51644811.log)

### Architectural Read

- The new routing layer appears to be working better than the `2026-04-03` version because weak indirect cases are no longer dominating the day.
- The next optimization opportunity is execution-mode reduction, not just better routing labels.
- Right now, all `49` runs still take `full_loop`, so the system is still paying verifier and multi-iteration costs even after a direct/high-confidence route decision.
- The missing `agent_context_profile.profile` payload is still an observability gap.

### Recommended Next Focus

- Add a cheaper execution path for high-confidence `direct` routes, for example a single-pass generator followed by save if deterministic checks pass.
- Enforce execution-only constraints earlier so trade-suggestion language is blocked before verifier cycles are spent correcting it.
- Keep the new route telemetry, but restore compact-profile and filtering telemetry so relevance quality and token savings can both be audited.
