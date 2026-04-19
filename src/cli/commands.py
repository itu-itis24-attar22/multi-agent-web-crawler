from src.core.config import DB_PATH, DEFAULT_FRONTIER_MAXSIZE
from src.core.indexing_service import run_indexing_job, get_indexing_job_summary
from src.crawler.frontier import Frontier
from src.crawler.worker import process_crawl_item
from src.models.crawl_item import CrawlItem
from src.storage.schema import initialize_schema
from src.storage.job_repository import create_job, list_jobs, get_job
from src.storage.page_repository import add_visited_url, list_pages_for_job
from src.search.query_processor import search_query
from src.storage.agent_repository import list_agent_decisions

def init_db_command() -> None:
    initialize_schema()
    print(f"Database initialized successfully at: {DB_PATH}")


def hello_command() -> None:
    print("Crawler project skeleton is set up correctly.")


def create_sample_job_command(origin_url: str, max_depth: int) -> None:
    job_id = create_job(origin_url=origin_url, max_depth=max_depth)
    print(f"Created job {job_id} for origin={origin_url}, max_depth={max_depth}")


def list_jobs_command() -> None:
    jobs = list_jobs()

    if not jobs:
        print("No jobs found.")
        return

    for job in jobs:
        print(
            f"[job_id={job['job_id']}] "
            f"origin={job['origin_url']} "
            f"max_depth={job['max_depth']} "
            f"status={job['status']} "
            f"discovered={job['pages_discovered']} "
            f"crawled={job['pages_crawled']} "
            f"indexed={job['pages_indexed']} "
            f"failed={job['pages_failed']}"
        )


def test_single_crawl_command(origin_url: str, max_depth: int) -> None:
    job_id = create_job(origin_url=origin_url, max_depth=max_depth, status="running")

    add_visited_url(job_id=job_id, normalized_url=origin_url, first_seen_depth=0)

    frontier = Frontier(maxsize=DEFAULT_FRONTIER_MAXSIZE)
    frontier.put(
        CrawlItem(
            job_id=job_id,
            url=origin_url,
            origin_url=origin_url,
            depth=0,
        )
    )

    item = frontier.get()
    process_crawl_item(frontier=frontier, item=item, max_depth=max_depth)
    frontier.task_done()

    pages = list_pages_for_job(job_id)
    job = get_job(job_id)

    print(f"Test crawl completed for job {job_id}")
    print(f"Pages stored: {len(pages)}")
    print(f"Discovered counter: {job['pages_discovered']}")
    print(f"Crawled counter: {job['pages_crawled']}")
    print(f"Indexed counter: {job['pages_indexed']}")
    print(f"Failed counter: {job['pages_failed']}")

    for page in pages:
        print(
            f"- depth={page['depth']} status={page['status']} url={page['page_url']}"
        )

    print(f"Frontier size after processing: {frontier.qsize()}")


def index_command(origin_url: str, max_depth: int) -> None:
    job_id, runtime_status = run_indexing_job(
        origin_url=origin_url,
        max_depth=max_depth,
    )
    job = get_indexing_job_summary(job_id)

    print(f"Indexing completed for job {job_id}")
    print(f"Origin: {job['origin_url']}")
    print(f"Max depth: {job['max_depth']}")
    print(f"Status: {job['status']}")
    print(f"Discovered: {job['pages_discovered']}")
    print(f"Crawled: {job['pages_crawled']}")
    print(f"Indexed: {job['pages_indexed']}")
    print(f"Failed: {job['pages_failed']}")
    print()

    print("Runtime status:")
    print(f"  Frontier size: {runtime_status['frontier_size']}/{runtime_status['frontier_maxsize']}")
    print(f"  Active workers: {runtime_status['active_workers']}")
    print(f"  Total enqueued: {runtime_status['total_enqueued']}")
    print(f"  Total dequeued: {runtime_status['total_dequeued']}")
    print(f"  Back pressure events: {runtime_status['back_pressure_events']}")
    print(f"  Pressure state: {runtime_status['pressure_state']}")
        
def search_command(query: str, limit: int = 20, job_id: int | None = None) -> None:
    results = search_query(query, limit=limit, job_id=job_id)

    if not results:
        print("No results found.")
        return

    scope_text = f" for job_id={job_id}" if job_id is not None else ""
    print(f"Found {len(results)} results{scope_text}:\n")

    for i, result in enumerate(results, start=1):
        print(f"{i}. URL: {result.relevant_url}")
        print(f"   Origin: {result.origin_url}")
        print(f"   Depth: {result.depth}")
        print(f"   Score: {result.score}")
        print()
        
def job_status_command(job_id: int) -> None:
    job = get_job(job_id)

    if not job:
        print(f"No job found with job_id={job_id}")
        return

    print(f"Job ID: {job['job_id']}")
    print(f"Origin: {job['origin_url']}")
    print(f"Max depth: {job['max_depth']}")
    print(f"Status: {job['status']}")
    print(f"Created at: {job['created_at']}")
    print(f"Started at: {job['started_at']}")
    print(f"Completed at: {job['completed_at']}")
    print(f"Discovered: {job['pages_discovered']}")
    print(f"Crawled: {job['pages_crawled']}")
    print(f"Indexed: {job['pages_indexed']}")
    print(f"Failed: {job['pages_failed']}")
    
def pages_command(job_id: int) -> None:
    pages = list_pages_for_job(job_id)

    if not pages:
        print(f"No pages found for job_id={job_id}")
        return

    print(f"Pages for job {job_id}:\n")

    for page in pages:
        print(f"Page ID: {page['page_id']}")
        print(f"  URL: {page['page_url']}")
        print(f"  Origin: {page['origin_url']}")
        print(f"  Depth: {page['depth']}")
        print(f"  Status: {page['status']}")
        print(f"  HTTP status: {page['http_status']}")
        print(f"  Title: {page['title']}")
        print()

def agent_decisions_command(job_id: int | None = None) -> None:
    decisions = list_agent_decisions(job_id=job_id)

    if not decisions:
        if job_id is None:
            print("No agent decisions found.")
        else:
            print(f"No agent decisions found for job_id={job_id}")
        return

    if job_id is None:
        print("Agent decisions:\n")
    else:
        print(f"Agent decisions for job {job_id}:\n")

    for decision in decisions:
        print(f"[{decision['decision_id']}] {decision['agent_name']} ({decision['stage']})")
        print(f"  job_id: {decision['job_id']}")
        print(f"  time: {decision['created_at']}")
        print(f"  decision: {decision['decision_text']}")
        print()
        