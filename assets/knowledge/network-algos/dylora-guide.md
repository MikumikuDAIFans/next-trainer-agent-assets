# DyLoRA guide (two distinct entry points — do not conflate them)

- Version: `2026-08-30`
- Scope: the two different DyLoRA routes exposed by the workbench (native `networks.dylora` module vs LyCORIS `algo=dylora`), their separate field contracts, availability per page, and what "train once, use many ranks" actually implies here.
- Evidence status: L1 project contract (schema shared blocks + lora-master module union + support-matrix adapter lists).
- Aliases / 检索关键词: dylora, dylokr, dynamic lora, unit, dylora_unit, networks.dylora, 多rank

## The two entries (L1)

| Entry | How to select | Contract fields | Pages |
|---|---|---|---|
| Native DyLoRA module | `network_module = networks.dylora` | `dylora_unit` (min 1 = slowest; docs suggest 4/8/12/16) serialized as `unit=` | SD 1.x/2.x, SDXL (`lora-master.ts` module union; matrix DyLoRA entries) |
| LyCORIS DyLoRA algo | `network_module = lycoris.kohya`, `lycoris_algo = dylora` | LyCORIS block fields (`conv_dim`, `conv_alpha`, dropout, train_norm) | SD 1.x/2.x, SDXL, Flux (`shared.ts` LYCORIS_MAIN union) |

They are different implementations reached through different fields; "which DyLoRA did I pick" must always be answered by the module + algo pair, never by the word DyLoRA alone. Flux has the LyCORIS route only (`networks.dylora` is not in the Flux module union).

## What DyLoRA does (method context, official paper — L1 public)

DyLoRA trains a structured low-rank adapter from which **smaller-rank subspaces of the same trained weights can be extracted at inference** (rank-nesting during training), rather than training N separate LoRAs. The official paper is arXiv:2210.07558 (registered source `dylora-paper`). This product exposes the trainer modules; extraction/slicing at inference is not a workbench feature — there is no "export dim slice" UI in the audited contract, so plan downstream use accordingly.

## Practical reading (contract-derived, no measured numbers)

- `dylora_unit` trades training speed (unit=1 minimum slices, slowest) vs slice granularity; documented suggestion 4/8/12/16.
- No shipped DyLoRA preset and no measured DyLoRA-vs-LoRA run exists in this staging evidence: any "DyLoRA needs higher LR / more steps" claim is L3, not KB fact.
- Availability ≠ recommendation: matrix lists DyLoRA under SD15/SDXL (native + LyCORIS) and Flux (LyCORIS) as adapter availability under those pages' support level, with per-page validator as authority.

## Sources

- https://github.com/wochenlong/lora-scripts-next branch `feat/pi-agent-plugin`: `mikazuki/schema/lora-master.ts`, `mikazuki/schema/shared.ts`, `frontend/src/training/params.ts`.
- DyLoRA paper: https://arxiv.org/abs/2210.07558 (method; not product parameter evidence).
- Frozen support matrix (staging artifact `01_训练器能力盘点/support-matrix.json`).

## Boundaries

- Do not promise multi-rank inference export from the workbench — the audited product surface trains DyLoRA checkpoints but provides no slice-export flow.
- Do not confuse with T-LoRA (timestep-dynamic rank, Anima-only) — `tlora-anima-guide.md`.
- No Anima/Krea/Fast DyLoRA path exists; asking for one is an unsupported request.
