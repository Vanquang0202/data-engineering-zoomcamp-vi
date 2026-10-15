# DE legacy/current image rollout

Scope: every local Markdown image reference in the assigned module directories
and cohort Markdown paths (`cohorts/2022`, `cohorts/2024`, `cohorts/2025`,
`cohorts/2026`, and `cohorts/2027/02-workflow-orchestration`).

The initial inventory contains 94 local references to 92 unique source paths.
The audit includes video thumbnails, exact Airflow/UI captures, explanatory
diagrams, workshop assets, and homework evidence. The 2022 IAM reference
originally used the wrong relative path; it is corrected to the existing
repository-root source in a focused commit.

Imagegen capability was available and the skill was read in full. Imagegen was
used only for the bounded incremental-loading decision tree after inspecting
the source and verifying every required label and branch. Exact UI, code,
URL, numeric, logo, and plot-like assets remain deterministic or unchanged.

## Accepted image changes

### Incremental-loading decision tree

- Source: `cohorts/2024/workshops/dlt_resources/incremental_loading.png`
- Reference: `cohorts/2024/workshops/dlt_resources/data_ingestion_workshop.md`
- Disposition: `crop/replace`, score 11/12. The tree teaches the choice among
  append, replace, and merge/upsert; the generated replacement preserves all
  labels, branch directions, and outcomes while making the typography and
  lines crisp.
- Method: built-in imagegen edit after local inspection; no face, camera tile,
  browser chrome, cursor, watermark, or extra component was present or added.
- Required invariants checked: `Is it stateful data?`, `NO`/`YES` branch order,
  `Can you request it incrementally?`, and the exact three dispositions.
- Replacement: `incremental_loading-imagegen.png`

### Homework dataset evidence

- Source: `02-workflow-orchestration/images/homework.png` (the identical
  original is also preserved in the 2025 and 2027 cohort image directories).
- References: the 2025, 2026, and 2027 workflow-orchestration homework files.
- Disposition: `crop/replace`, score 10/12. The screenshot uniquely shows the
  yellow and green 2021 assets that the assignment asks learners to ingest;
  it complements the written assignment with concrete filenames and sizes.
- Method: deterministic crop of each side after local inspection. Removed the
  browser address bars and reaction controls while preserving the exact
  filenames, sizes, dates, highlighted 2021 rows, and purple teaching notes.
- Crop: left pane `820x750+0+25`, right pane `820x760+824+25`, padded and
  appended to `1640x760`.
- Replacement: `02-workflow-orchestration/images/homework-cropped.png`
- No imagegen: exact UI text, filenames, dates, and numeric sizes are the
  source of truth.

### 2022 IAM search screen

- Source: `images/aws/iam.png`
- Reference: `cohorts/2022/week_2_data_ingestion/transfer_service/README.md`
- Disposition: `keep`, score 8/12. The screenshot directly supports the
  instruction to search for IAM before creating an access key, and its exact
  AWS labels are readable. The original relative reference was broken and was
  corrected to `../../../../images/aws/iam.png`.
- Method: retained exact source; no imagegen because this is a live UI whose
  labels are the source of truth. The source contains no face or camera tile.

## Final inventory and disposition

- 94 local Markdown image references were audited.
- The initial inventory had 92 unique path strings: 91 existing source files
  plus the broken IAM path. After the focused repairs and the shared homework
  replacement, the active references use 91 unique, resolving source paths.
- Retained: 94 references. Removed: 0. No image failed the instructional or
  navigation-value hard gates.
- Content changes: 1 imagegen replacement, 1 deterministic crop reused by 3
  references, and 1 repaired relative path. The remaining 89 references keep
  their original pixels and source assets.
- Originals remain in place, including both duplicate homework originals and
  the original incremental-loading diagram.

### Video-thumbnail inventory

All 80 thumbnail references were inspected in a contact sheet. They are
navigation assets linking to the corresponding videos, so the presenter faces,
play buttons, and designed thumbnail graphics are intentional rather than
unwanted webcam/capture overlays. They were retained at 8/12 as navigation
images (the surrounding lesson heading and linked video provide the caption
and context), with no imagegen or deterministic rewrite.

| Scope | References / unique sources | Source dimensions | Disposition |
| --- | ---: | --- | --- |
| `01-docker-terraform/**` (including `docker-sql`) | 8 / 8 | 480x360 JPEG | keep, video navigation |
| `02-workflow-orchestration/**` | 16 / 16 | 480x360 JPEG | keep, video navigation |
| `05-data-platforms/**` | 10 / 10 | 480x360 JPEG | keep, video navigation |
| `06-batch/**` | 16 / 16 | 480x360 JPEG | keep, video navigation |
| `cohorts/2024` workflow/workshop Markdown | 17 / 17 | 480x360 JPEG | keep, video navigation |
| `cohorts/2025` workflow/workshop Markdown | 13 / 13 | 480x360 JPEG | keep, video navigation |

The inventory paths are the `thumbnail-*.jpg` files referenced by those exact
Markdown scopes; no unreferenced thumbnails were changed.

### Instructional-image inventory

| Active source | Refs | Score | Decision and method |
| --- | ---: | ---: | --- |
| `cohorts/2022/week_2_data_ingestion/airflow/docs/arch-diag-airflow.png` | 1 | 12/12 | Keep. Clean architecture diagram with exact component relationships and readable labels. |
| `cohorts/2022/week_2_data_ingestion/airflow/docs/gcs_ingestion_dag.png` | 1 | 10/12 | Keep. Exact Airflow graph state is the teaching evidence; labels and task arrows are clear, with no webcam or browser chrome. |
| `images/aws/iam.png` | 1 | 8/12 | Keep exact UI. It demonstrates searching for IAM; only the broken Markdown path was repaired. |
| `cohorts/2022/week_3_data_warehouse/airflow/docs/gcs_2_bq_dag_graph_view.png` | 1 | 10/12 | Keep. Exact Airflow graph showing yellow/green branches and task relationships. |
| `cohorts/2022/week_3_data_warehouse/airflow/docs/gcs_2_bq_dag_tree_view.png` | 1 | 9/12 | Keep. Exact tree-view execution state; compact but legible at source resolution. |
| `cohorts/2024/workshops/dlt_resources/incremental_loading-imagegen.png` | 1 | 11/12 | Accepted imagegen replacement; see the accepted-change record above. |
| `02-workflow-orchestration/images/homework-cropped.png` | 3 | 10/12 | Accepted deterministic crop; see the accepted-change record above. |
| `cohorts/2025/04-analytics-engineering/homework_q2.png` | 1 | 11/12 | Keep. Crisp lineage/data-flow diagram; exact project labels and relationships are readable. |
| `cohorts/2025/workshops/dlt/img/pipes.jpg` | 1 | 10/12 | Keep. Crisp pipeline overview with a clear collect/ingest/store/compute/consume flow and required product labels. |
| `cohorts/2025/workshops/dlt/img/Rest_API.png` | 1 | 11/12 | Keep. Clean explanatory API-challenges diagram; authentication, pagination, memory, and rate-limit relationships are readable. |
| `cohorts/2025/workshops/dlt/img/dlt.png` | 2 | 11/12 | Keep. Crisp dlt source/normalize/load mapping with exact product logos and labels; do not entrust these to imagegen. |

### Method totals

- Imagegen: 1 bounded explanatory decision tree, inspected before and after;
  all exact labels and branch directions passed review.
- Deterministic: 1 exact UI screenshot crop, reused by 3 homework references;
  browser address bars and reaction controls were removed without changing
  filenames, dates, sizes, highlights, or teaching annotations.
- Retained unchanged: 80 video thumbnails and 9 other instructional sources,
  plus the IAM source after its path repair.
- Removed: none. Every retained image contributes either navigational value,
  exact technical evidence, or a distinct explanatory relationship.

## Validation

- The source inventory was rerun after the edits: 94 local references, 91
  unique active paths, 0 missing paths.
- `git diff --check` passes for every focused commit and the final audit state.
- The generated and cropped assets were inspected with `view_image` at source
  resolution; originals were not overwritten.

## Limitations

- Airflow and AWS images preserve exact historical UI labels and dates because
  those pixels are the instructional evidence; they were not regenerated.
- The homework crop preserves the original purple annotations because they
  explain which 2021 assets the learner must ingest. Only browser framing and
  reaction controls were removed.
- Video-thumbnail faces are intentional presenter artwork/navigation content,
  not recording webcam tiles; removing them would damage the video-link role.
- The imagegen decision tree uses a clean white background rather than the
  source's transparent canvas; all text and relationships remain unchanged.
