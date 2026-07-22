# AlphaRadar Architecture

Status: LOCKED BASELINE  
Architecture Version: 1.0  
Established: Sprint E9.5  
Repository: wancupie-netizen/AlphaRadar

---

## 1. Purpose

AlphaRadar is an adaptive intelligence system that:

1. observes market conditions,
2. detects signals,
3. interprets market behaviour,
4. produces explainable decisions,
5. records outcomes and learning,
6. builds historical experience,
7. presents adaptive dashboard intelligence.

The system must remain deterministic, explainable,
testable and maintainable.

---

## 2. Architecture Principle

AlphaRadar follows this dependency direction:

```text
Delivery
   ↓
Application
   ↓
Domain / Adaptive Contracts
   ↓
Infrastructure Implementations


# Sprint E9.5 — Architecture Lock

Audit awal mendapati repository belum mempunyai dokumen ADR atau architecture rasmi. Jadi sprint ini akan menghasilkan:

```text
Module 01  Architecture Constitution
Module 02  Artifact Ownership ADR
Module 03  Folder Responsibility ADR
Module 04  Dependency Rules
Module 05  Engineering SOP
Module 06  Architecture Verification
```

Kita mulakan dengan dokumen induk.

Runner kini secara rasmi bertindak sebagai production orchestrator, termasuk Dashboard Engine, tetapi tidak membuat keputusan atau mengakses business rules.  Adaptive Dashboard Service menerima `DashboardRequest`, membaca history dan menghasilkan `DashboardCard`.  Collection Service pula hanya menerima koleksi request dan mengekalkan susunannya.

---

# Module 01 — Architecture Constitution

## Root Folder

```text
AlphaRadar/
```

## File Baru

```text
docs/architecture/AlphaRadar_Architecture.md
```

## Full File

````markdown
# AlphaRadar Architecture

Status: LOCKED BASELINE  
Architecture Version: 1.0  
Established: Sprint E9.5  
Repository: wancupie-netizen/AlphaRadar

---

## 1. Purpose

AlphaRadar is an adaptive intelligence system that:

1. observes market conditions,
2. detects signals,
3. interprets market behaviour,
4. produces explainable decisions,
5. records outcomes and learning,
6. builds historical experience,
7. presents adaptive dashboard intelligence.

The system must remain deterministic, explainable,
testable and maintainable.

---

## 2. Architecture Principle

AlphaRadar follows this dependency direction:

```text
Delivery
   ↓
Application
   ↓
Domain / Adaptive Contracts
   ↓
Infrastructure Implementations
````

Business decisions must not depend on:

* API frameworks,
* databases,
* dashboard presentation,
* schedulers,
* external market providers.

---

## 3. Production Flow

The official production flow is:

```text
Market Provider
      ↓
Market Normalization
      ↓
Observation
      ↓
Signal Detection
      ↓
Interpretation
      ↓
DecisionArtifact
      ↓
Knowledge Fingerprint
      ↓
Intelligence Persistence
      ↓
DashboardRequest
      ↓
Adaptive Dashboard
      ↓
Lifecycle
      ↓
Outcome
      ↓
Learning
      ↓
Knowledge
      ↓
Production Result
```

The Production Runner coordinates this flow.

The Runner must not:

* detect signals,
* interpret markets,
* make trading decisions,
* implement serialization rules,
* contain domain business rules.

---

## 4. Folder Responsibilities

### `core/`

Owns stable domain artifacts and domain-level models.

Examples:

* `DecisionArtifact`
* `KnowledgeArtifact`
* `LearningArtifact`
* `OutcomeArtifact`
* `MarketSnapshot`
* domain enums

Rules:

* immutable where practical,
* no database access,
* no API dependency,
* no scheduler dependency,
* no presentation logic.

---

### `scanner/`

Owns the production intelligence engine and
market-scanning implementation.

Examples:

* market acquisition,
* normalization,
* observation,
* signal detection,
* interpretation,
* decision execution,
* lifecycle execution,
* serialization,
* persistence adapters,
* Production Runner.

Rules:

* engines may build Core artifacts,
* Runner performs orchestration only,
* domain decisions remain inside engines,
* persistence logic must remain isolated in stores.

---

### `adaptive/`

Owns adaptive intelligence contracts and behaviour.

Examples:

* ExperienceArtifact,
* EvidenceArtifact,
* HistorySummary,
* DashboardRequest,
* DashboardCard,
* experience compilation,
* history aggregation,
* dashboard builders.

Rules:

* does not make the original trading decision,
* does not access external market providers,
* does not control the Production Runner,
* adaptive output must be derived from Core decisions
  and historical experience.

---

### `application/`

Owns use-case orchestration.

Examples:

* Adaptive Dashboard Service,
* Dashboard Collection Service,
* token query services,
* assemblers,
* DTO mapping.

Rules:

* coordinates domain and adaptive modules,
* does not contain market decision logic,
* does not duplicate domain calculations,
* receives and returns explicit contracts,
* must not accept primitive argument collections where
  a formal request artifact already exists.

---

### `api/`

Owns the external HTTP delivery boundary.

Rules:

* validates transport input,
* invokes Application services,
* converts results into API responses,
* contains no market intelligence logic,
* contains no direct database business workflow.

---

### `pulse/`

Owns operational job tracking.

Examples:

* job start,
* job finish,
* duration,
* execution status.

It must not influence trading decisions.

---

### `scheduler/`

Owns scheduled execution.

It may invoke Production Runner but must not contain
scanner or decision logic.

---

### `validation/`

Owns engineering validation and regression workflows.

Validation scripts must use current package paths and
current artifact contracts.

---

### `tests/`

Owns automated unit, contract and integration tests.

Tests must:

* be safe during pytest collection,
* avoid production side effects,
* use package-qualified imports,
* reflect current contracts,
* test one responsibility clearly.

---

## 5. Artifact Ownership

| Artifact           | Owner                                       |
| ------------------ | ------------------------------------------- |
| DecisionArtifact   | `core/artifacts/decision_artifact.py`       |
| OutcomeArtifact    | `core/artifacts/outcome_artifact.py`        |
| LearningArtifact   | `core/artifacts/learning_artifact.py`       |
| KnowledgeArtifact  | `core/artifacts/knowledge_artifact.py`      |
| ExperienceArtifact | `adaptive/artifacts/experience_artifact.py` |
| EvidenceArtifact   | `adaptive/artifacts/evidence_artifact.py`   |
| HistorySummary     | `adaptive/history/history_summary.py`       |
| DashboardRequest   | `adaptive/dashboard/dashboard_request.py`   |
| DashboardCard      | `adaptive/dashboard/dashboard_card.py`      |
| Lifecycle Package  | `scanner/lifecycle_engine.py`               |

Artifact ownership means:

* the owner defines the contract,
* builders may construct the artifact,
* services may coordinate it,
* consumers may read it,
* consumers must not redefine it.

---

## 6. Dashboard Ownership

The official Dashboard flow is:

```text
DecisionArtifact
      ↓
DashboardRequestBuilder
      ↓
DashboardRequest
      ↓
AdaptiveDashboardService
      ↓
HistoryRepository
      ↓
HistorySummary
      ↓
DashboardBuilder
      ↓
DashboardCard
```

For multiple tokens:

```text
Iterable[DashboardRequest]
      ↓
DashboardCollectionService
      ↓
list[DashboardCard]
```

The Collection Service must not reconstruct
DashboardRequest fields.

---

## 7. Fingerprint Ownership

AlphaRadar currently contains two distinct fingerprint
concepts.

### Operational Intelligence Fingerprint

Location:

```text
scanner/knowledge_fingerprint.py
```

Purpose:

* derived from an Intelligence Package,
* identifies decision and interpretation state,
* used by Intelligence persistence,
* used for Adaptive history lookup,
* built once by Production Runner.

### Learning Fingerprint

Location:

```text
core/knowledge/fingerprint.py
```

Purpose:

* derived from LearningArtifact collections,
* belongs to knowledge aggregation,
* currently uses a placeholder implementation.

These two fingerprints must not be treated as the same
contract.

A future ADR may rename them to remove semantic ambiguity.
Until that ADR is approved, their current responsibilities
remain separate.

---

## 8. Dependency Rules

Allowed:

```text
api → application
application → adaptive
application → core
application → scanner contracts
adaptive → core
scanner → core
scheduler → scanner runner
```

Disallowed:

```text
core → scanner
core → application
core → api
adaptive → api
adaptive → scheduler
scanner engines → api
domain artifacts → databases
```

Circular imports are prohibited.

---

## 9. Request Contract Rule

Whenever a formal request artifact exists, Application
services must receive that request artifact.

Example:

```python
build_adaptive_dashboard(
    request: DashboardRequest,
)
```

Not:

```python
build_adaptive_dashboard(
    token=...,
    decision=...,
    confidence=...,
    fingerprint=...,
)
```

This prevents contract drift and primitive obsession.

---

## 10. Persistence Rule

Persistence flow must remain explicit:

```text
Artifact
   ↓
Serializer
   ↓
Payload
   ↓
Store
```

Stores must not:

* construct domain decisions,
* infer missing business values,
* mutate immutable artifacts,
* silently change artifact contracts.

---

## 11. Time Rule

New timestamps must be timezone-aware UTC values.

Preferred:

```python
datetime.now(timezone.utc)
```

Deprecated for new code:

```python
datetime.utcnow()
```

Existing usages may be migrated incrementally through
dedicated refactoring modules.

---

## 12. Engineering Change Rule

Every architecture-sensitive change must follow:

```text
Issue
  ↓
Repository Audit
  ↓
Dependency Audit
  ↓
Root Cause
  ↓
Architecture Decision
  ↓
Full File or Full Section Replacement
  ↓
Targeted Test
  ↓
Regression Test
  ↓
PASS
  ↓
Commit
  ↓
LOCK
```

No architecture contract is considered locked until its
tests pass and the change is committed.

---

## 13. Current Locked Contracts

The following contracts are locked:

* DecisionArtifact
* DashboardRequest
* DashboardRequestBuilder
* AdaptiveDashboardService
* DashboardCard
* DashboardCollectionService
* Module 04C Production Runner integration

Changes to these contracts require a new ADR.

---

## 14. Legacy Code Policy

Legacy modules must not be deleted merely because they fail
current tests.

Each legacy module must first be classified as:

* migrate,
* replace,
* archive,
* delete.

Deletion requires evidence that no active production path,
test, import or consumer depends on the module.

---

## 15. Definition of Done

A module is complete only when:

* ownership is clear,
* contracts are explicit,
* dependency direction is valid,
* targeted tests pass,
* relevant regression tests pass,
* no production side effects occur during test collection,
* changes are committed,
* status is marked LOCKED.
