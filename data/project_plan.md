
### `docs/project_plan.md`
```markdown
# JustInsight Project Plan

## 🎯 Objectives
1. Build an end-to-end pipeline: ingestion → NLP → insights.
2. Provide interns hands-on experience with data engineering, NLP, and dashboarding.
3. Deliver a working demo by the end of Week 6.

---

## 🗓️ Roadmap & Milestones

| Week | Deliverable                                                   |
|:----:|:--------------------------------------------------------------|
| **1**                      |
|        | - PoC: ingest 10 articles from two sources                   |
| **2**    | - Normalize & store articles in DB                          |
|        | - Define JSON schema & loader                                |
| **3**    | - spaCy NER integration: PERSON, ORG, GPE                    |
|        | - Create entity-tagging API endpoint                         |
| **4**    | - Topic modeling (BERTopic/LDA)                              |
|        | - Topic-tagging API                                          |
| **5**    | - Fact extraction (OpenIE/transformer extractor)             |
|        | - Implement alert rules (spike detection)                   |
| **6**    | - Streamlit dashboard: search, filters, trend charts         |
|        | - Final demo & documentation                                 |

---

## 📦 Deliverables
- **Source Code**: Modular, documented Python packages
- **Data Samples**: Normalized JSON files
- **API**: Endpoints for ingestion, tagging, insights
- **Dashboard**: Interactive Streamlit app
- **Docs**: README, project plan, architecture diagram

## 🗂 Development Methodology

**Kanban (Continuous Flow)**
- **GitHub Project Board**: “JustInsight Kanban.”
- **Pull-based workflow**: Pull the highest-priority card into “To Do” when ready.
- **Continuous delivery**: Merge features as they complete; close cards when PRs are merged.


## ⚠️ Risks & Mitigations
- **API rate limits**: caching, source rotation
- **Extraction noise**: limit entity types initially
- **Timeline drift**: weekly demos & reviews