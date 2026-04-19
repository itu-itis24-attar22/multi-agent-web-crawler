from flask import Flask, render_template, request, redirect, url_for

from src.core.background_jobs import background_job_manager
from src.search.query_processor import search_query
from src.storage.job_repository import list_jobs, get_job
from src.storage.page_repository import list_pages_for_job
from src.storage.agent_repository import list_agent_decisions

app = Flask(__name__, template_folder="templates")


@app.route("/")
def dashboard():
    jobs = list_jobs()
    runtime = {
        job["job_id"]: background_job_manager.get_runtime_status(job["job_id"])
        for job in jobs
    }
    running = {
        job["job_id"]: background_job_manager.is_running(job["job_id"])
        for job in jobs
    }
    recent_decisions = list_agent_decisions()[:10]
    
    return render_template(
        "dashboard.html",
        jobs=jobs,
        runtime=runtime,
        running=running,
        recent_decisions=recent_decisions,
    )


@app.route("/start-index", methods=["POST"])
def start_index():
    origin_url = request.form.get("origin_url", "").strip()
    max_depth = int(request.form.get("max_depth", "1"))

    job_id = background_job_manager.start_index_job(
        origin_url=origin_url,
        max_depth=max_depth,
    )
    return redirect(url_for("job_detail", job_id=job_id))


@app.route("/job/<int:job_id>")
def job_detail(job_id: int):
    job = get_job(job_id)
    if not job:
        return f"No job found with job_id={job_id}", 404

    runtime = background_job_manager.get_runtime_status(job_id)
    running = background_job_manager.is_running(job_id)
    error = background_job_manager.get_error(job_id)
    pages = list_pages_for_job(job_id)
    decisions = list_agent_decisions(job_id=job_id)
    
    return render_template(
        "job_detail.html",
        job=job,
        runtime=runtime,
        running=running,
        error=error,
        pages=pages,
        decisions=decisions,
    )


@app.route("/search")
def search_page():
    query = request.args.get("q", "").strip()
    limit = int(request.args.get("limit", "20"))
    job_id_raw = request.args.get("job_id", "").strip()
    job_id = int(job_id_raw) if job_id_raw else None

    results = search_query(query, limit=limit, job_id=job_id) if query else []

    return render_template(
        "search.html",
        query=query,
        limit=limit,
        job_id=job_id_raw,
        results=results,
    )


def run_ui(host: str = "127.0.0.1", port: int = 5000) -> None:
    app.run(host=host, port=port, debug=False, use_reloader=False)