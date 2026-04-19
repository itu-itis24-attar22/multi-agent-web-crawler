# Agent Prompt Pack

This document provides examples of prompts used to guide each AI agent during development.

---

## Product Requirements Agent

Prompt:
"Read the assignment and convert it into clear product requirements, constraints, assumptions, and acceptance criteria for a crawler and search system."

---

## System Architecture Agent

Prompt:
"Design a single-machine architecture for a crawler and search engine supporting depth-limited indexing, duplicate prevention, back pressure, and concurrent search."

---

## Crawl & Indexing Agent

Prompt:
"Design the crawling pipeline including frontier management, URL normalization, duplicate prevention, and incremental indexing."

---

## Search & Retrieval Agent

Prompt:
"Design a search system using an inverted index and returning results as `(relevant_url, origin_url, depth)` with simple ranking."

---

## Persistence & Operations Agent

Prompt:
"Design a local database schema and runtime state tracking system for a crawler using SQLite."

---

## QA / Review Agent

Prompt:
"Review the system against the assignment and identify missing features, risks, and improvements."