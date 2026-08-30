# Lumina 2 — current end-to-end breakage (boundary, not a workflow guide)

- Version: `2026-08-30`
- Scope: what the current product actually does when a user picks Lumina 2, and why no Lumina 2 training guide or template exists in this knowledge base.
- Evidence status: L1 project contract (frozen support matrix `lumina2-lora-currently-broken`, source commit `9cd2399`, re-verified unchanged up to `a1a5797`).
- Aliases / 检索关键词: lumina, lumina2, 不支持, 断链, lumina-lora, lumina2-lora, broken

## Observed contract state (L1)

| Layer | State | Evidence |
|---|---|---|
| Workbench module | registered (`modules.ts:42`) | frontend registers a Lumina 2 combo |
| Frontend forced value | wrong train-type value forced (`params.ts:43`) | frontend/src/training/params.ts |
| Schema | `lumina2-lora.ts` exists and declares LoRA/OFT/LyCORIS forms | mikazuki/schema/lumina2-lora.ts |
| Serialization | intended `lumina-lora` but `lumina2-lora` is what is serialized today | support-matrix entry `lumina2-lora-currently-broken` |
| Backend mapping | no working trainer mapping / backendEntrypoint is null | mikazuki/app/api.py:152-164, 845-849 |

Conclusion: the chain page → schema → serialized train type → trainer mapping is broken, so **Lumina 2 is not usable through the product today**, regardless of what the schema advertises.

## How to answer user questions

1. Do not produce a Lumina 2 dataset recipe, parameter table, or template. There is no L1 path that can run.
2. State the boundary: UI and schema exist, the backend contract does not close; this is tracked as unsupported in the frozen support matrix.
3. If a fix lands later (route/serialization/mapping changed in source), this document must be re-checked against `support-matrix.json` before any workflow guide is written.

## Observation notes (L2, non-causal)

The Stage 1 Civitai MVP sample queried the `Lumina 2` base-model stratum and received an empty public item list (`03_Civitai样本/raw/lumina2.json`, HTTP 200, 0 records). This only says the exploratory batch found no public LoRA records in that stratum; it is not evidence about the architecture or about product support.

## Sources

- Project contract: repository-relative evidence only: `frontend/src/training/modules.ts`, `frontend/src/training/params.ts`, `mikazuki/schema/lumina2-lora.ts`, `mikazuki/app/api.py` on branch `feat/pi-agent-plugin` (https://github.com/wochenlong/lora-scripts-next).
- Frozen matrix: `01_训练器能力盘点/support-matrix.json` entry `lumina2-lora-currently-broken` (staging artifact).
- L2 observation: `03_Civitai样本/raw/request-log.jsonl` stratum `lumina2` (staging artifact).

## Boundaries

- Not a workflow guide; nothing here may be reused as Lumina 2 "how to train" content.
- Support may change only with code evidence (new schema serialization + trainer mapping + validator path); until then keep every Lumina 2 request at "currently unsupported".
- Civitai empty-stratum observation must not be upgraded into a claim about Lumina 2's ecosystem.
