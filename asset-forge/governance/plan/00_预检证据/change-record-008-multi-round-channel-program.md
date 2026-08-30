# CR-008：多轮外部渠道整理与采集计划

- Date: `2026-08-30`
- Requested by: user
- Affected plan/stage/goal: new Stage 6 / G7 multi-round external channel program
- Trigger: user requests a reusable, broad, one-shot program for collecting as many external knowledge and template channels as practical.
- Previous state: Stage 5 bounded expansion with 16 catalog entries, 49 candidate knowledge docs, and 12 validator-proven candidate templates.
- New state: establish a catalog-driven multi-round process covering official repositories/docs, model papers, dataset/caption tooling, alternative trainers, and public metadata channels; run bounded rounds and append only auditable candidates.
- Risk delta: P1 scope drift and source duplication; P2 external revision drift, rate limits, and false cross-tool compatibility.
- User authorization: explicit for online public-source collection and staging only; formal migration remains unauthorized.

## Locked guardrails

1. All source discovery, requests, logs, extraction notes, candidates, and evidence remain under `E:\OpenSourceTeamWork\AgentAssets`.
2. Public anonymous HTTP only; no token/Cookie/login, no images, weights, private datasets, or long copyrighted text.
3. Each round has a request budget, 0.5-second spacing, 20-second timeout, response-size cap, and failure retention.
4. External tool configs never become Next Trainer templates by analogy. Templates require current route/schema/trainer/preset/validator proof, zero normalized diff, and a non-ok negative control.
5. Unknown remains unknown. Popularity/stars/downloads are discovery signals only.
6. Formal project and agent-assets trees remain read-only. No migration/sync/commit/push/build/package/release.

## Planned rounds

- Round 1: official trainer/model/algorithm repositories and docs.
- Round 2: dataset, caption, evaluation, and reproducibility tooling.
- Round 3: public model metadata and paper-level method evidence; no Civitai expansion unless separately authorized.
- Round 4: candidate synthesis, validator probing, deduplication, and migration preview refresh.
