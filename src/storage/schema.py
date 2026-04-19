from src.storage.database import get_connection
CREATE_AGENT_DECISIONS_TABLE = """
CREATE TABLE IF NOT EXISTS agent_decisions (
    decision_id INTEGER PRIMARY KEY,
    job_id INTEGER,
    agent_name TEXT NOT NULL,
    stage TEXT NOT NULL,
    decision_text TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id)
);
"""
CREATE_JOBS_TABLE = """
CREATE TABLE IF NOT EXISTS jobs (
    job_id INTEGER PRIMARY KEY,
    origin_url TEXT NOT NULL,
    max_depth INTEGER NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    started_at TEXT,
    completed_at TEXT,
    pages_discovered INTEGER NOT NULL DEFAULT 0,
    pages_crawled INTEGER NOT NULL DEFAULT 0,
    pages_indexed INTEGER NOT NULL DEFAULT 0,
    pages_failed INTEGER NOT NULL DEFAULT 0
);
"""

CREATE_PAGES_TABLE = """
CREATE TABLE IF NOT EXISTS pages (
    page_id INTEGER PRIMARY KEY,
    job_id INTEGER NOT NULL,
    page_url TEXT NOT NULL,
    origin_url TEXT NOT NULL,
    depth INTEGER NOT NULL,
    status TEXT NOT NULL,
    http_status INTEGER,
    title TEXT,
    content_text TEXT,
    content_hash TEXT,
    discovered_at TEXT,
    fetched_at TEXT,
    indexed_at TEXT,
    error_message TEXT,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id),
    UNIQUE (job_id, page_url)
);
"""

CREATE_VISITED_URLS_TABLE = """
CREATE TABLE IF NOT EXISTS visited_urls (
    job_id INTEGER NOT NULL,
    normalized_url TEXT NOT NULL,
    first_seen_depth INTEGER NOT NULL,
    seen_at TEXT NOT NULL,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id),
    UNIQUE (job_id, normalized_url)
);
"""

CREATE_TERMS_TABLE = """
CREATE TABLE IF NOT EXISTS terms (
    term_id INTEGER PRIMARY KEY,
    term_text TEXT NOT NULL UNIQUE
);
"""

CREATE_POSTINGS_TABLE = """
CREATE TABLE IF NOT EXISTS postings (
    term_id INTEGER NOT NULL,
    page_id INTEGER NOT NULL,
    term_frequency INTEGER NOT NULL,
    FOREIGN KEY (term_id) REFERENCES terms(term_id),
    FOREIGN KEY (page_id) REFERENCES pages(page_id),
    UNIQUE (term_id, page_id)
);
"""

CREATE_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);",
    "CREATE INDEX IF NOT EXISTS idx_pages_job_id ON pages(job_id);",
    "CREATE INDEX IF NOT EXISTS idx_pages_status ON pages(status);",
    "CREATE INDEX IF NOT EXISTS idx_terms_term_text ON terms(term_text);",
    "CREATE INDEX IF NOT EXISTS idx_postings_page_id ON postings(page_id);",    "CREATE INDEX IF NOT EXISTS idx_agent_decisions_job_id ON agent_decisions(job_id);",
]


def initialize_schema() -> None:
    with get_connection() as conn:
        conn.execute(CREATE_JOBS_TABLE)
        conn.execute(CREATE_PAGES_TABLE)
        conn.execute(CREATE_VISITED_URLS_TABLE)
        conn.execute(CREATE_TERMS_TABLE)
        conn.execute(CREATE_POSTINGS_TABLE)
        conn.execute(CREATE_AGENT_DECISIONS_TABLE)
        for statement in CREATE_INDEXES:
            conn.execute(statement)

        conn.commit()