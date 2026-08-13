# ASPICE V4 Level 2 Internal Audit Report

## CppCheckDocker - Head of `main` at 2026-08-13

| Field | Value |
|:--------------|:------------|
| **Document ID** | CCD-AUD-2026-08-13-L2 |
| **Version** | v1.00 |
| **Date** | 2026-08-13 |
| **Author** | Dermot Murphy |
| **Reviewer** | Dermot Murphy |
| **Approver** | Dermot Murphy |
| **Status** | Released |
| **Classification** | Internal |
| **ASPICE Process** | SUP.1 - Quality Assurance (audit obligation); assesses all Level 2 processes |
| **Baseline audited** | `main` @ `1d394b4` (post-PR #27 merge; contains v2.21.1-r1, v2.21.1-r2, CR-21 records, CR-24 filter, CR-23 sweep) |

---

## Document Control

| Version | Date | Author | Change Description |
|:--------------|:------------|:------------|:--------------------|
| v1.00 | 2026-08-13 | Dermot Murphy | Initial issue - first formal ASPICE V4 Level 2 internal audit of the CppCheckDocker baseline; closes the CCD-DEV-002 corrective action for issue #28. |

---

## 1. Purpose

This document is the first formal internal audit of the CppCheckDocker ASPICE V4 baseline. It:

- Fulfils the time-boxed corrective action booked by [CCD-DEV-002 §6.1](CppCheckDocker_DEV002_Independent_QA_Audit_Deviation.md) (target 2026-11-11, executed 2026-08-13 - 90 days early).
- Assesses every process area defined in `documents/aspice/` against ASPICE PAM v4.0 Level 2 Process Attributes (PA 1.1, PA 2.1, PA 2.2).
- Identifies every finding that prevents a Fully Achieved rating on any process and opens a follow-up GitHub issue for each such finding.
- Provides an audit trail for the `Publish-Wiki` job to sync to the repository wiki.

## 2. Scope

Processes audited (13 in total, one per active ASPICE document under `documents/aspice/`):

| Process | Document | Included |
|:--------|:---------|:---------|
| MAN.3 - Project Management | CCD-MAN3-001 | Yes |
| ACQ.4 - Supplier Monitoring | CCD-ACQ4-001 | Yes |
| SPL.2 - Software Release | CCD-SPL2-001 | Yes |
| SUP.1 - Quality Assurance | CCD-SUP1-001 | Yes |
| SUP.8 - Configuration Management | CCD-SUP8-001 | Yes |
| SUP.9 - Problem Resolution | CCD-SUP9-001 | Yes |
| SUP.10 - Change Request Management | CCD-SUP9-001 (folded) | Yes |
| SWE.1 - SW Requirements | CCD-SWE1-001 | Yes |
| SWE.2 - SW Architectural Design | CCD-SWE2-001 | Yes |
| SWE.3 - SW Detailed Design | CCD-SWE3-001 | Yes |
| SWE.4 - SW Unit Verification | CCD-SWE4-001 | Yes |
| SWE.5 - SW Integration Test | CCD-SWE5-001 | Yes |
| SWE.6 - SW Qualification Test | CCD-SWE6-001 | Yes |

Cross-process artefacts inspected as evidence:

- CCD-RTM-001 (Master Traceability Matrix)
- CCD-DEV-001, CCD-DEV-002 (Process Deviation records)
- `documents/aspice/records/CCD-SVD-2.21.1-r1.md`, `CCD-SVD-2.21.1-r2.md`, `CCD-QTR-2.21.1-r1.md`, `CCD-QTR-2.21.1-r2.md` (release records)
- `.github/workflows/build.yml`, `.github/workflows/poll-cppcheck.yml`
- `.hadolint.yaml`, `.yamllint.yaml`, `.trivyignore`, `.pre-commit-config.yaml`
- `Dockerfile`, `.dockerignore`, `.gitattributes`
- GitHub PR / Actions history for the baseline commits

Out of scope:
- Upstream cppcheck source (SUP-001 supplier); treated as COTS per CCD-ACQ4-001
- Ubuntu base image (SUP-002 supplier); treated as COTS
- MISRA rule-texts file (SUP-003 supplier); treated as COTS

## 3. Method

Single-engineer audit conducted by Dermot Murphy in accordance with the compensating-control framework of [CCD-DEV-001](CppCheckDocker_DEV001_Single_Engineer_Role_Collapse_Deviation.md). The audit is self-conducted; the compensating controls (AI-assisted analytical challenge, PR review, CI gate stack, version-controlled audit trail, systematic self-review against clause intent) apply to the audit itself as they do to every other work product.

For each in-scope process:

1. Read the process-defining document at the audited commit.
2. Enumerate ASPICE base practices (BPs) implied by the process description.
3. Sample evidence: CI runs, release records, PRs, commits, and outputs the process would produce.
4. Rate PA 1.1, PA 2.1, PA 2.2 on the N/P/L/F scale (see §4).
5. Record each observation as a finding with severity (see §5) and cross-reference to the follow-up issue (if any).

## 4. Rating scale

Per ASPICE PAM v4.0 §4.3:

| Rating | Symbol | Achievement |
|:-------|:-------|:------------|
| Not achieved | N | 0% - 15% |
| Partially achieved | P | > 15% - 50% |
| Largely achieved | L | > 50% - 85% |
| Fully achieved | F | > 85% - 100% |

For Level 2 capability, every Process Attribute of every process in scope must be at least **L**; **F** is the target this audit uses to derive follow-up issues.

## 5. Finding severity

| Severity | Meaning |
|:---------|:--------|
| **Blocker** | Prevents a Fully Achieved rating on at least one PA of at least one process. Requires a follow-up GitHub issue. |
| **Improvement** | Does not block F today but is a documented quality-of-implementation gap the project should close. Optional follow-up. |
| **Observation** | Recorded for auditor awareness or as evidence of a passed check. No action required. |

## 6. Standing deviations applied

Two accepted deviations shape the ratings below. They are cited in the relevant PA cells rather than repeated as findings.

| Deviation | Effect |
|:----------|:-------|
| [CCD-DEV-001](CppCheckDocker_DEV001_Single_Engineer_Role_Collapse_Deviation.md) - Author = Reviewer = Approver | Applied to every PA 2.2 assessment. GP 2.2.3 (Review and Adjust Work Products) is rated in a "with compensating controls" mode. Permanent; retires only when a second reviewer joins. |
| [CCD-DEV-002](CppCheckDocker_DEV002_Independent_QA_Audit_Deviation.md) - No independent internal QA audit yet | Applied to SUP.1 PA 2.1 in the pre-audit baseline. **This audit closes the corrective action, so DEV-002 is scheduled for retirement in §11.** |

---

## 7. Per-process assessment

### 7.1 MAN.3 - Project Management  (CCD-MAN3-001 v1.03, Released)

**Base practices sampled:** project scope defined (§2), WBS defined (§4), roles defined (§3), lifecycle model defined (§5), schedule framework and milestones (§6), estimation basis (§7), risk register (§8), monitoring & control (§9), interfaces (§10).

| PA | Rating | Rationale |
|:---|:------:|:----------|
| PA 1.1 Process performance | **F** | Every base practice of MAN.3 has a section in CCD-MAN3-001 with concrete content (WBS-01..WBS-17; RSK-001..RSK-006; five documented milestones M1..M5). Evidence of monitoring: continuous CI status, PR history, ASPICE document version history. |
| PA 2.1 Performance management | **F** | Plan is defined and being followed. Schedule framework is documented and CR-driven; entry/exit criteria for milestones are explicit. No slippage against RSK-005 mitigation (documentation-first approach). |
| PA 2.2 Work product management | **L** | Document Control table maintained; version + date + status tracked. **Rated L due to [CCD-DEV-001]** - GP 2.2.3 review-independence not met, compensating controls apply. §3 explicitly cites the deviation. |

Findings: none.

### 7.2 ACQ.4 - Supplier Monitoring  (CCD-ACQ4-001 v1.02, Released)

**Base practices sampled:** supplier register (§3), monitoring cadence (§4), change-response procedure (§5), records location and retention (§6), supplier-change log (§7).

| PA | Rating | Rationale |
|:---|:------:|:----------|
| PA 1.1 Process performance | **F** | Three suppliers registered (SUP-001..SUP-003) with per-supplier consumed-via, change-detection method, evaluation criteria, bump procedure, withdrawal trigger, and contact. Automated monitoring via `.github/workflows/poll-cppcheck.yml` for SUP-001; per-CI-build digest capture for SUP-002. Supplier-change log has entries for all three baseline pins. |
| PA 2.1 Performance management | **F** | Cadence targets defined; evaluation criteria per supplier defined; CR process enforced before bump. |
| PA 2.2 Work product management | **L** | Document under version control; per-release SVD snapshots the supplier register (verified in `CCD-SVD-2.21.1-r1.md` §7). **Rated L due to [CCD-DEV-001]** for GP 2.2.3. |

Findings: none.

### 7.3 SPL.2 - Software Release  (CCD-SPL2-001 v1.02, Released; template CCD-SVD-001 v1.00 Draft)

**Base practices sampled:** release scope (§2), triggers and cadence (§3), entry criteria (§4), release procedure automated + manual (§5), exit criteria (§6), release records (§7), deprecation & withdrawal (§8).

| PA | Rating | Rationale |
|:---|:------:|:----------|
| PA 1.1 Process performance | **F** | Two releases executed (v2.21.1-r1, v2.21.1-r2). Both have populated SVD and QTR records under `documents/aspice/records/`. Automated flow proven by CI run <https://github.com/dermot-murphy/CppCheckDocker/actions/runs/31707301287>. `Release` job now includes the CR-24 paths-filter guard so non-image merges skip publish - documented in §5.1. |
| PA 2.1 Performance management | **F** | Entry criteria (§4, nine numbered items with evidence pointers) and exit criteria (§6, six items with objective evidence) are explicit and CI-enforced. |
| PA 2.2 Work product management | **L** | SVDs and QTRs committed to Git; template is Draft with a documented "instances under records/ are Released" rule (noted exception, correctly implemented). **Rated L due to [CCD-DEV-001]** for GP 2.2.3. |

Findings: none.

### 7.4 SUP.1 - Quality Assurance  (CCD-SUP1-001 v1.03, Released)

**Base practices sampled:** quality objectives (§2), quality gates (§3), code review process (§4), static analysis (§5), test adequacy (§6), non-conformance handling (§7), QA records (§8), ASPICE process compliance (§9), Process Deviations (§11).

| PA | Rating | Rationale |
|:---|:------:|:----------|
| PA 1.1 Process performance | **L** | Active gates (Build, Verify-Version, Run-Integration-Tests, Lint, Scan-Image, AllChecksPassed) proven on every PR in this baseline. QA records enumerated in §8 exist and are being produced. **Not F due to [FIND-A]** - the `Check-Image-Size` gate listed in §3 as Planned has no CI job and no manual execution record; SR-060 has no automated regression gate. |
| PA 2.1 Performance management | **L** | QA plan is defined and followed. Prior gap "no independent audit executed against the baseline" (CCD-DEV-002) is closed by THIS audit report. **Not F due to [FIND-B]** - §3 gate table has a labelling inconsistency: the hadolint gate is listed as `Lint-Dockerfile (Planned)` but the actual CI implementation names it `Lint (pre-commit)` and it is Active. An assessor reading the plan would flag the mismatch. |
| PA 2.2 Work product management | **L** | Document under version control; §11 correctly cites CCD-DEV-001 and CCD-DEV-002. **Rated L due to [CCD-DEV-001]** for GP 2.2.3. |

Findings: [FIND-A], [FIND-B]. Both Blocker.

### 7.5 SUP.8 - Configuration Management  (CCD-SUP8-001 v1.05, Released)

**Base practices sampled:** configuration items (§2), branching strategy (§3), versioning (§4), build environment (§5), document version control (§6), configuration audit (§7).

| PA | Rating | Rationale |
|:---|:------:|:----------|
| PA 1.1 Process performance | **L** | CI-001..CI-012 defined and each maps to a real controlled location. Branching strategy proven by every PR in the baseline. Image versioning `<v>-r<n>` proven by v2.21.1-r1, r2. Release job with paths-filter guard active per CR-24. **Not F due to [FIND-D]** - §7 Configuration Audit defines an obligation ("audit before each production release verifying published digest matches CI-produced digest") but there is no CI job that executes this check and no manual audit record has been filed for r1 or r2. Digest is captured in the SVD (implicit evidence) but not compared against CI-computed digest as a distinct step. |
| PA 2.1 Performance management | **F** | CI enforces PR + review before merge; branch protection rules in place. Wiki publication automated. Revision counter derived from tags (self-authoritative). |
| PA 2.2 Work product management | **L** | Every CI is under version control per the CI table. **Rated L due to [CCD-DEV-001]** for GP 2.2.3. |

Findings: [FIND-D]. Blocker.

### 7.6 SUP.9 - Problem Resolution & SUP.10 - Change Request Management  (CCD-SUP9-001 v1.01, Released)

**Base practices sampled:** problem classification & fields & lifecycle (§2.1-2.3), problem-report storage (§2.4), regression prevention (§2.5), CR triggers & fields & lifecycle (§3.1-3.3), document update policy (§3.4), CR storage (§3.5), upstream cppcheck bump flow (§3.6), impact chain (§4), process deviation records format (§5).

| PA | Rating | Rationale |
|:---|:------:|:----------|
| PA 1.1 Process performance | **L** | CR process executed for issues #4, #5, #6, #7, #9, #15, #21, #23, #24, #28. Each closed with an implementing PR. Regression-prevention step §2.5 executed for MISRA support (INT-040, QT-015 added). §5 process-deviation format defined and applied (CCD-DEV-001, CCD-DEV-002). **Not F due to [FIND-C]** - §2.4 and §3.5 mandate storage of PR and CR records as markdown files under `documents/reviews/`, but that directory does not exist and no markdown records have been filed. The activity has been captured entirely via GitHub Issues and PRs; the plan and the practice diverge. |
| PA 2.1 Performance management | **F** | Impact chain (§4) enforced by PR reviewer; document version policy (§3.4) evidenced by the ASPICE audit-readiness sweep bumping every affected doc's version. |
| PA 2.2 Work product management | **L** | This document, all CRs (as GitHub Issues + PRs), and all deviations are version-controlled. **Rated L due to [CCD-DEV-001]** for GP 2.2.3. |

Findings: [FIND-C]. Blocker.

### 7.7 SWE.1 - Software Requirements Analysis  (CCD-SWE1-001 v1.02, Released)

**Base practices sampled:** feature requirements (§5, FEAT-001..FEAT-011), image-build SRs (§6, SR-001..SR-010), cppcheck provisioning SRs (§7, SR-020..SR-029), runtime SRs (§8, SR-030..SR-036), security SRs (§9, SR-040..SR-044), reproducibility SRs (§10, SR-050..SR-054), performance SRs (§11, SR-060..SR-063), non-functional SRs (§12, NFR-001..NFR-009), traceability summary (§13).

| PA | Rating | Rationale |
|:---|:------:|:----------|
| PA 1.1 Process performance | **F** | 11 features and 40 Mandatory functional SRs plus 9 NFRs identified, uniquely IDed, and traced downstream via CCD-RTM-001. |
| PA 2.1 Performance management | **F** | SRS updated when features change (v1.01 added MISRA support with SR-028/SR-029); RTM v1.01 tracked the same change same-PR. |
| PA 2.2 Work product management | **L** | Document under version control; DC table maintained. **Rated L due to [CCD-DEV-001]** for GP 2.2.3. |

Findings: none.

### 7.8 SWE.2 - Software Architectural Design  (CCD-SWE2-001 v1.02, Released)

**Base practices sampled:** architectural elements ARC-IMG-*/ARC-BLD-*/ARC-RUN-*/ARC-INT-* traced from SRs.

| PA | Rating | Rationale |
|:---|:------:|:----------|
| PA 1.1 Process performance | **F** | Architecture elements enumerated per RTM §4 for every Mandatory SR. ARC-RUN-010 added same-PR when MISRA support was introduced. |
| PA 2.1 Performance management | **F** | Change-driven updates evidenced (v1.01 change note). |
| PA 2.2 Work product management | **L** | **Rated L due to [CCD-DEV-001]** for GP 2.2.3. |

Findings: none.

### 7.9 SWE.3 - Software Detailed Design  (CCD-SWE3-001 v1.02, Released)

**Base practices sampled:** detailed design sections §3.1..§3.5 traced from ARC elements; §4 dockerignore design; §5.5 image tagging design; §6.1 test harness design; §7 exit-code and output behaviour.

| PA | Rating | Rationale |
|:---|:------:|:----------|
| PA 1.1 Process performance | **F** | Detailed design covers every ARC element in RTM §4. §3.5 was added same-PR for MISRA support. |
| PA 2.1 Performance management | **F** | Change-driven updates evidenced. |
| PA 2.2 Work product management | **L** | **Rated L due to [CCD-DEV-001]** for GP 2.2.3. |

Findings: none.

### 7.10 SWE.4 - Software Unit Verification  (CCD-SWE4-001 v1.02, Released)

**Base practices sampled:** UVT-001..UVT-050 + UVT-060..UVT-061 (28 total). Test harness `test/unit/` scoped to image structure. Single-tier CI model per CCD-SUP1-001 §6.1.

| PA | Rating | Rationale |
|:---|:------:|:----------|
| PA 1.1 Process performance | **L** | Every Mandatory image-structure SR has at least one UVT; verified via CCD-RTM-001 §5.1 and by the r1 verification evidence in CCD-SVD-2.21.1-r1 §8. **Not F due to [FIND-E]** - §5 refers to a CI job `Run-Unit-Tests` which does not exist in `.github/workflows/build.yml`. The single-tier model folds UVT execution into `Verify-Version` + `Run-Integration-Tests` (per SUP.1 §6.1), but the SWE4 doc still cites the phantom job. |
| PA 2.1 Performance management | **L** | Test cases owned by SWE.4 and updated on change (UVT-060/UVT-061 added same-PR as MISRA support). **Not F due to [FIND-F]** - §2.5 Static Analysis Integration table marks hadolint and trivy as `(planned)` but both are Active per CCD-SUP1-001 §5.1/§5.2. Doc synchronization gap. |
| PA 2.2 Work product management | **L** | **Rated L due to [CCD-DEV-001]** for GP 2.2.3. |

Findings: [FIND-E], [FIND-F]. Both Blocker.

### 7.11 SWE.5 - Software Integration Test  (CCD-SWE5-001 v1.02, Released)

**Base practices sampled:** INT-001..INT-040 (24 cases across 5 phases); test harness `test/integration/run.sh`; CI job `Run-Integration-Tests`.

| PA | Rating | Rationale |
|:---|:------:|:----------|
| PA 1.1 Process performance | **F** | Integration test suite covers image + cppcheck + arguments + GHA-step-container. Phase 5 (Addons, INT-040) added same-PR as MISRA support. All passed on r1 (CCD-QTR-2.21.1-r1). |
| PA 2.1 Performance management | **F** | Phase order and time budget (< 3 min) defined; pass criteria per case; gating on develop/main. |
| PA 2.2 Work product management | **L** | **Rated L due to [CCD-DEV-001]** for GP 2.2.3. |

Findings: none.

### 7.12 SWE.6 - Software Qualification Test  (CCD-SWE6-001 v1.02, Released)

**Base practices sampled:** QT-001..QT-015 (15 cases); entry criteria; test-record fields; execution against pulled `<version>-r<rev>` image.

| PA | Rating | Rationale |
|:---|:------:|:----------|
| PA 1.1 Process performance | **F** | All 15 QT cases executed for r1 and r2 (CCD-QTR-2.21.1-r1, CCD-QTR-2.21.1-r2 - PASS 15/15 both times). |
| PA 2.1 Performance management | **F** | Entry criteria defined; test record fields defined; sign-off block filled. QTR filed per release. |
| PA 2.2 Work product management | **L** | QTR under version control; digest cited. **Rated L due to [CCD-DEV-001]** for GP 2.2.3. |

Findings: none.

---

## 8. Findings summary

Every finding preventing Fully Achieved on any PA of any process:

| ID | Severity | Process(es) affected | PA affected | Summary |
|:---|:---------|:---------------------|:------------|:--------|
| **FIND-A** | Blocker | SUP.1 | PA 1.1 | SR-060 (image size <= 200 MB) has no automated regression gate. CCD-SUP1-001 §3 lists `Check-Image-Size` as Planned. Current evidence is the informational `Record image size` step in `Build-Image` plus UVT-050 / QT-008 - none of which fail the build on a size overrun. |
| **FIND-B** | Blocker | SUP.1 | PA 2.1 | CCD-SUP1-001 §3 first row (NFR-001 hadolint gate) is labelled `Lint-Dockerfile (Planned)`, but the executing CI job is `Lint (pre-commit)` and it is Active. Cross-doc RTM §3a NFR-001 also names the planned job. Label mismatch will read as an unimplemented gate to an assessor. |
| **FIND-C** | Blocker | SUP.9 / SUP.10 | PA 1.1 | CCD-SUP9-001 §2.4 (PR records) and §3.5 (CR records) mandate storage of markdown records under `documents/reviews/`. The directory does not exist. Every CR and PR in the baseline was tracked via GitHub Issues + PRs instead. Plan and practice diverge. |
| **FIND-D** | Blocker | SUP.8 | PA 1.1 | CCD-SUP8-001 §7 defines a pre-release configuration audit ("published image digest matches the CI-produced digest") with no CI job or documented manual execution record. Digest is captured in the SVD but not distinctly compared as an audit step. |
| **FIND-E** | Blocker | SWE.4 | PA 1.1 | CCD-SWE4-001 §5 (and §2.4) cites a CI job `Run-Unit-Tests` that does not exist in `.github/workflows/build.yml`. The single-tier CI model (per CCD-SUP1-001 §6.1) is intentional; the doc's phantom-job reference must be reconciled with the actual implementation. |
| **FIND-F** | Blocker | SWE.4 | PA 2.1 | CCD-SWE4-001 §2.5 Static Analysis Integration table marks hadolint and trivy as `(planned)`; §2.5 body also says "once active". Both are Active per CCD-SUP1-001 §5.1 / §5.2 as of v1.01 / v1.02. Doc synchronization gap. |

Observations (no follow-up issue - recorded for auditor awareness):

| ID | Severity | Summary |
|:---|:---------|:--------|
| OBS-1 | Observation | `documents/aspice/audits/` directory referenced by CCD-DEV-002 §6 does not exist. This audit report is filed at top-level (`documents/aspice/CppCheckDocker_AUD_2026-08-13_ASPICE_L2_Audit.md`) so the existing `Publish-Wiki` job (which scans `documents/aspice/*.md` non-recursively) will pick it up. Recommend updating CCD-DEV-002 §6 wording to state "under `documents/aspice/`" or extending `Publish-Wiki` to include subdirectories - captured as OBS, not Blocker, because the audit obligation is met by this file. |
| OBS-2 | Observation | Standing deviation CCD-DEV-001 (role collapse) is applied to every PA 2.2 rating. Every PA 2.2 is therefore rated L. This is by design per the deviation's "Accepted with justification, permanent" disposition and is not a finding. |
| OBS-3 | Observation | NFR-006 (layer count kept low via combined RUN) has no automated check. Manual review only. Not a mandatory gate; consistent with CCD-RTM-001 §3a which classifies verification as "Review" only. |

## 9. Follow-up issues opened

One follow-up issue opened per Blocker in §8. Each issue cites this audit report by document ID and includes the finding text as its body. Issues are labelled `change-request` per CLAUDE.md workflow rules.

| Finding | Follow-up issue | Recommended branch |
|:--------|:----------------|:-------------------|
| FIND-A | [#29 - Automate image size regression gate](https://github.com/dermot-murphy/CppCheckDocker/issues/29) | `feature/CR-29-Automate_image_size_regression_gate` |
| FIND-B | [#30 - Correct SUP1 §3 hadolint gate label](https://github.com/dermot-murphy/CppCheckDocker/issues/30) | `feature/CR-30-Correct_SUP1_hadolint_gate_label` |
| FIND-C | [#31 - Reconcile SUP9 documents/reviews/ mandate](https://github.com/dermot-murphy/CppCheckDocker/issues/31) | `feature/CR-31-Reconcile_SUP9_reviews_dir_with_actual_practice` |
| FIND-D | [#32 - Automate SUP8 §7 configuration audit digest-match](https://github.com/dermot-murphy/CppCheckDocker/issues/32) | `feature/CR-32-Automate_SUP8_configuration_audit_digest_check` |
| FIND-E | [#33 - Remove SWE4 Run-Unit-Tests phantom job reference](https://github.com/dermot-murphy/CppCheckDocker/issues/33) | `feature/CR-33-Remove_SWE4_Run_Unit_Tests_phantom_job_reference` |
| FIND-F | [#34 - Sync SWE4 static-analysis table to Active](https://github.com/dermot-murphy/CppCheckDocker/issues/34) | `feature/CR-34-Sync_SWE4_static_analysis_table_to_active_status` |

## 10. Overall verdict

| Process | PA 1.1 | PA 2.1 | PA 2.2 | Overall (min of three) | Level 2 achieved? |
|:--------|:------:|:------:|:------:|:----------------------:|:-----------------:|
| MAN.3 | F | F | L | L | **Yes** |
| ACQ.4 | F | F | L | L | **Yes** |
| SPL.2 | F | F | L | L | **Yes** |
| SUP.1 | L | L | L | L | **Yes** |
| SUP.8 | L | F | L | L | **Yes** |
| SUP.9/10 | L | F | L | L | **Yes** |
| SWE.1 | F | F | L | L | **Yes** |
| SWE.2 | F | F | L | L | **Yes** |
| SWE.3 | F | F | L | L | **Yes** |
| SWE.4 | L | L | L | L | **Yes** |
| SWE.5 | F | F | L | L | **Yes** |
| SWE.6 | F | F | L | L | **Yes** |

**Bottom line:** every in-scope process is at **Largely Achieved (L)** or better on every PA. **ASPICE V4 Level 2 capability is achieved** across the baseline.

Every PA 2.2 is rated L (not F) exclusively because of the standing role-collapse deviation ([CCD-DEV-001]), which is permanently accepted. Closing FIND-A..FIND-F would raise every PA 1.1 and PA 2.1 currently rated L to F. PA 2.2 will remain at L for the lifetime of the project as single-engineer.

## 11. Retirement recommendation for CCD-DEV-002

Per [CCD-DEV-002 §6.2](CppCheckDocker_DEV002_Independent_QA_Audit_Deviation.md), the deviation retires when:

1. The first audit report exists under `documents/aspice/audits/` - **partially met.** Report filed at `documents/aspice/CppCheckDocker_AUD_2026-08-13_ASPICE_L2_Audit.md` (top level for wiki-publication reasons; see OBS-1). Recommend updating DEV-002 §6.2 wording to accept this location.
2. Any non-conformance findings have been dispositioned - **partially met.** Six Blocker findings (FIND-A..FIND-F) enumerated in §8 with follow-up issues opened in §9. Full closure waits on those issues resolving.
3. The next-audit date is entered in CCD-SUP1-001 and in DEV-002 as a superseding record - **pending.** Recommend annual cadence: next audit target 2027-08-13.

**Recommendation:** retire CCD-DEV-002 in a follow-up PR that (a) closes all six follow-up issues from §9, (b) updates DEV-002 §6.2 to accept the top-level audit location, (c) enters the 2027-08-13 next-audit date in CCD-SUP1-001, and (d) supersedes DEV-002 with a released "Deviation retired" record. **Not in scope of the current audit PR.**

## 12. Sign-Off

| Role | Name | Date | Signature/Approval |
|:-----|:-----|:-----|:-------------------|
| Author | Dermot Murphy | 2026-08-13 | Git commit authorship |
| Reviewer | Dermot Murphy | 2026-08-13 | Self-review under CCD-MAN3-001 §3 single-engineer clause; audit compensating controls per CCD-DEV-001 §5.2 |
| Approver | Dermot Murphy | 2026-08-13 | PR merge to `develop` on the CR-28 branch |

Per CCD-MAN3-001 §3 and CCD-DEV-001, for a single-engineer team the same individual fills all three roles; the process record (git commit + PR merge event + CI gate stack + AI-assisted analytical challenge during drafting) provides the auditable evidence.

## 13. Referenced Documents

| Document ID | Title | Version |
|:------------|:------|:--------|
| CCD-MAN3-001 | Project Management Plan | v1.03 |
| CCD-ACQ4-001 | Supplier Monitoring Plan | v1.02 |
| CCD-SPL2-001 | Software Release Plan | v1.02 |
| CCD-SUP1-001 | Software Quality Assurance Plan | v1.03 |
| CCD-SUP8-001 | Configuration Management Plan | v1.05 |
| CCD-SUP9-001 | Problem Resolution and Change Request Management Plan | v1.01 |
| CCD-SWE1-001 | Software Requirements Specification | v1.02 |
| CCD-SWE2-001 | Software Architectural Design Document | v1.02 |
| CCD-SWE3-001 | Software Detailed Design Document | v1.02 |
| CCD-SWE4-001 | Software Unit Verification Plan | v1.02 |
| CCD-SWE5-001 | Software Integration Test Plan | v1.02 |
| CCD-SWE6-001 | Software Qualification Test Specification | v1.02 |
| CCD-RTM-001 | Master Traceability Matrix | v1.05 |
| CCD-SVD-001 | Software Version Description (template) | v1.00 (Draft, template) |
| CCD-SVD-2.21.1-r1 | SVD instance for release v2.21.1-r1 | v1.00 |
| CCD-SVD-2.21.1-r2 | SVD instance for release v2.21.1-r2 | v1.00 |
| CCD-QTR-2.21.1-r1 | Qualification Test Record for v2.21.1-r1 | v1.00 |
| CCD-QTR-2.21.1-r2 | Qualification Test Record for v2.21.1-r2 | v1.00 |
| CCD-DEV-001 | Process Deviation - Author = Reviewer = Approver | v1.00 |
| CCD-DEV-002 | Process Deviation - No Independent Internal QA Audit Yet | v1.00 |
| ASPICE PAM v4.0 | Automotive SPICE Process Assessment Model | v4.0 |
| GitHub Issue #28 | Perform full ASPICE V4 Level 2 audit of head of main and file findings | - |

---

*End of CCD-AUD-2026-08-13-L2 v1.00*
