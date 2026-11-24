"""ImageContext-Generator CLI entrypoint.

S2-SecurityFix: every path from the CLI is validated through the shared
`resolve_under_root()` helper and the course/pertemuan allowlists BEFORE any
filesystem write (SEC-02/03/04/07).
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

import typer
import yaml
from rich.console import Console
from rich.table import Table

from src.knowledge_manager import KnowledgeManager
from src.security import (
    PathValidationError,
    redact,
    resolve_under_root,
    validate_course_id,
    validate_segment,
)
from src.vision_engine import VisionEngine
from src.director import DirectorEngine
from src.context_engine import ContextEngine, AccRequiredError
from src.renaming_engine import (
    build_renaming_plan,
    RenamingPlan,
    extract_module_steps,
    list_screenshots,
)

app = typer.Typer(help="ImageContext-Generator: Generate inisiasi.txt from lab screenshots")
console = Console()


def _load_environment() -> None:
    """Load .env ONLY at the entrypoint (SEC-05) — never at module import."""
    from dotenv import load_dotenv

    dotenv_path = Path(__file__).resolve().parents[1] / ".env"
    load_dotenv(dotenv_path=dotenv_path if dotenv_path.exists() else None)


def _fail(exc: Exception) -> None:
    """Print a redacted validation error and exit non-zero."""
    console.print(f"[red]❌ {redact(str(exc))}[/red]")
    raise typer.Exit(2)


def _prepare(
    course: str,
    pertemuan: str,
    workspace_root: str,
) -> tuple[str, str, Path, Path]:
    """Validate all user-supplied path segments before any FS operation."""
    try:
        course_id = validate_course_id(course)
        meeting = validate_segment(pertemuan, "pertemuan")
        root = resolve_under_root(Path.cwd(), workspace_root, must_exist=True)
        screenshots_dir = resolve_under_root(
            root, root / course_id.upper() / "screenshots" / meeting, must_exist=False
        )
        return course_id, meeting, root, screenshots_dir
    except (PathValidationError, FileNotFoundError, OSError) as exc:
        _fail(exc)


def _resolve_output(root: Path, course_id: str, meeting: str, output: str | None, suffix: str) -> Path:
    """Resolve output under workspace root, rejecting traversal and non-.txt files."""
    try:
        if output:
            return resolve_under_root(root, output, suffix=".txt")
        return resolve_under_root(
            root,
            root / course_id.upper() / "inisiasi" / f"{meeting}{suffix}",
            suffix=".txt",
        )
    except (PathValidationError, OSError) as exc:
        _fail(exc)


def _require_screenshots(screenshots_dir: Path) -> None:
    if not screenshots_dir.exists():
        _fail(FileNotFoundError(f"Directory not found: {screenshots_dir}"))


def _make_director(
    repo_path: str | None,
    allow_git_context: bool,
    root: Path,
    repo_root: str | None = None,
) -> DirectorEngine:
    """Build DirectorEngine with explicit consent + repo_path containment (SEC-01)."""
    # SEC-01 point 1: repo must be contained under an allowed root. Default to
    # the parent of workspace (where practice repos normally live); users can
    # widen it explicitly with --repo-root.
    allowed_root = Path(repo_root).resolve() if repo_root else root.parent
    if repo_path and allow_git_context:
        console.print(
            f"[yellow]⚠️ OPT-IN: commit subject dari repo di dalam {allowed_root} "
            "akan dibaca dan dikirim ke Gemini saat generate-director. "
            "Pastikan tidak ada kredensial di pesan commit.[/yellow]"
        )
    return DirectorEngine(
        repo_path=repo_path,
        allow_git_context=allow_git_context,
        allowed_root=allowed_root,
    )


@app.command()
def scan(
    course: str = typer.Option(..., "--course", "-c", help="Course ID (e.g., kepl, ppg)"),
    pertemuan: str = typer.Option(..., "--pertemuan", "-p", help="Pertemuan folder name (e.g., Per4)"),
    workspace_root: str = typer.Option("workspace", "--workspace", "-w", help="Workspace root directory"),
):
    """Scan and list screenshots in a pertemuan folder"""
    course_id, meeting, _root, screenshots_dir = _prepare(course, pertemuan, workspace_root)
    _require_screenshots(screenshots_dir)

    images = sorted(
        [f for f in screenshots_dir.glob("*.png") if f.stem.isdigit()],
        key=lambda x: int(x.stem),
    )

    table = Table(title=f"Screenshots in {course_id.upper()}/{meeting}")
    table.add_column("#", style="cyan")
    table.add_column("Filename", style="green")
    table.add_column("Size", style="yellow")

    for img in images:
        stat = img.stat()
        size_mb = stat.st_size / (1024 * 1024)
        table.add_row(img.stem, img.name, f"{size_mb:.2f} MB")

    console.print(table)
    console.print(f"\nTotal: {len(images)} images")


@app.command()
def generate(
    course: str = typer.Option(..., "--course", "-c", help="Course ID (e.g., kepl, ppg)"),
    pertemuan: str = typer.Option(..., "--pertemuan", "-p", help="Pertemuan folder name (e.g., Per4)"),
    workspace_root: str = typer.Option("workspace", "--workspace", "-w", help="Workspace root directory"),
    knowledge_dir: str = typer.Option("knowledge/courses", "--knowledge", "-k", help="Knowledge base directory"),
    reference_dir: str = typer.Option(None, "--reference-dir", "-r", help="Optional reference directory with PDF materials"),
):
    """Generate inisiasi.txt from screenshots using Vision AI + knowledge base"""
    course_id, meeting, root, screenshots_dir = _prepare(course, pertemuan, workspace_root)
    output_file = _resolve_output(root, course_id, meeting, None, ".txt")
    _require_screenshots(screenshots_dir)

    km = KnowledgeManager(knowledge_dir, allowed_root=root, reference_root=Path.cwd())
    ve = VisionEngine()

    result = ve.generate_course_inisiasi(
        course_id=course_id,
        screenshots_dir=str(screenshots_dir),
        knowledge_manager=km,
        output_file=str(output_file),
        reference_dir=reference_dir,
    )

    if result["errors"] > 0:
        console.print(f"[yellow]⚠️ Completed with {result['errors']} errors[/yellow]")
    else:
        console.print("[green]✅ Generation completed successfully![/green]")


@app.command()
def list_courses(
    knowledge_dir: str = typer.Option("knowledge/courses", "--knowledge", "-k", help="Knowledge base directory"),
):
    """List available course configurations"""
    km = KnowledgeManager(knowledge_dir)
    configs = list(Path(knowledge_dir).glob("*.yaml"))

    table = Table(title="Available Courses")
    table.add_column("Course ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Code", style="yellow")
    table.add_column("Semester", style="magenta")

    for cfg in configs:
        try:
            course = km.load_course_config(cfg.stem)
            table.add_row(
                cfg.stem,
                course.get("course_name", ""),
                course.get("code", ""),
                str(course.get("semester", "")),
            )
        except (PathValidationError, FileNotFoundError, OSError, yaml.YAMLError) as exc:
            console.print(f"[yellow]⚠️ Skip {cfg.name}: {redact(str(exc))}[/yellow]")
            table.add_row(cfg.stem, "Error loading", "", "")

    console.print(table)


@app.command()
def plan(
    course: str = typer.Option(..., "--course", "-c", help="Course ID (e.g., kepl, ppg)"),
    pertemuan: str = typer.Option(..., "--pertemuan", "-p", help="Pertemuan folder name (e.g., Per4, UTS)"),
    repo_path: str = typer.Option(None, "--repo", "-r", help="Path to project repository for git timeline matching"),
    repo_root: str = typer.Option(None, "--repo-root", help="Containment root for --repo (default: workspace parent)"),
    workspace_root: str = typer.Option("workspace", "--workspace", "-w", help="Workspace root directory"),
    allow_git_context: bool = typer.Option(
        False, "--allow-git-context",
        help="OPT-IN: allow commit subjects to be used as (redacted) vision context",
    ),
):
    """Director Mode: Plan screenshot order and match against Git commits"""
    _course_id, meeting, root, screenshots_dir = _prepare(course, pertemuan, workspace_root)
    _require_screenshots(screenshots_dir)

    director = _make_director(repo_path, allow_git_context, root, repo_root)
    plan_items = director.plan_narrative(str(screenshots_dir))

    table = Table(title=f"🎬 Director Plan for {meeting}")
    table.add_column("#", style="cyan", justify="right")
    table.add_column("Filename", style="green")
    table.add_column("Mod Time", style="yellow")
    table.add_column("Aligned Git Context", style="magenta")

    for item in plan_items[:25]:
        table.add_row(
            str(item["index"]),
            item["original_name"],
            item["mtime"].strftime("%Y-%m-%d %H:%M:%S"),
            item["git_context"][:60] + "..." if len(item["git_context"]) > 60 else item["git_context"],
        )

    console.print(table)
    if len(plan_items) > 25:
        console.print(f"[dim]... and {len(plan_items) - 25} more screenshots[/dim]")
        console.print(f"\n[bold green]Total planned:[/bold green] {len(plan_items)} screenshots.")


@app.command()
def organize(
    course: str = typer.Option(..., "--course", "-c", help="Course ID (e.g., kepl, ppg)"),
    pertemuan: str = typer.Option(..., "--pertemuan", "-p", help="Pertemuan folder name (e.g., UTS)"),
    repo_path: str = typer.Option(None, "--repo", "-r", help="Path to project repository for git timeline matching"),
    repo_root: str = typer.Option(None, "--repo-root", help="Containment root for --repo (default: workspace parent)"),
    workspace_root: str = typer.Option("workspace", "--workspace", "-w", help="Workspace root directory"),
    copy: bool = typer.Option(True, "--copy/--rename", help="Copy files to a new 'organized' folder or rename in place (default: copy)"),
    allow_git_context: bool = typer.Option(
        False, "--allow-git-context",
        help="OPT-IN: allow commit subjects to be used as (redacted) vision context",
    ),
):
    """Director Mode: Organize screenshots into 1.png, 2.png, ... based on narrative plan"""
    _course_id, meeting, root, screenshots_dir = _prepare(course, pertemuan, workspace_root)
    _require_screenshots(screenshots_dir)

    director = _make_director(repo_path, allow_git_context, root, repo_root)
    plan_items = director.plan_narrative(str(screenshots_dir))

    try:
        target_dir = screenshots_dir if not copy else resolve_under_root(
            root, screenshots_dir.parent / f"{meeting}_organized", must_exist=False
        )
    except PathValidationError as exc:
        _fail(exc)
    target_dir.mkdir(parents=True, exist_ok=True)

    console.print(f"\n[bold yellow]📦 Organizing {len(plan_items)} images to {target_dir.name}...[/bold yellow]")

    for item in plan_items:
        src = item["path"]
        ext = src.suffix
        dest = target_dir / f"{item['index']}{ext}"

        if copy:
            shutil.copy2(src, dest)
        else:
            src.rename(dest)

    console.print(f"[green]✅ Successfully organized into {target_dir}[/green]")


@app.command()
def generate_director(
    course: str = typer.Option(..., "--course", "-c", help="Course ID (e.g., kepl, ppg)"),
    pertemuan: str = typer.Option(..., "--pertemuan", "-p", help="Pertemuan folder name (e.g., UTS)"),
    repo_path: str = typer.Option(None, "--repo", "-r", help="Path to project repository for git timeline matching"),
    repo_root: str = typer.Option(None, "--repo-root", help="Containment root for --repo (default: workspace parent)"),
    output: str = typer.Option(None, "--output", "-o", help="Custom output file path (must stay under workspace root)"),
    workspace_root: str = typer.Option("workspace", "--workspace", "-w", help="Workspace root directory"),
    knowledge_dir: str = typer.Option("knowledge/courses", "--knowledge", "-k", help="Knowledge base directory"),
    reference_dir: str = typer.Option(None, "--reference-dir", "-r", help="Optional reference directory with PDF materials"),
    allow_git_context: bool = typer.Option(
        False, "--allow-git-context",
        help="OPT-IN: allow commit subjects to be used as (redacted) vision context",
    ),
):
    """Director Mode: Plan and generate inisiasi.txt using multimodal vision + Git timeline"""
    course_id, meeting, root, screenshots_dir = _prepare(course, pertemuan, workspace_root)
    output_file = _resolve_output(root, course_id, meeting, output, "_director.txt")
    _require_screenshots(screenshots_dir)

    director = _make_director(repo_path, allow_git_context, root, repo_root)
    plan_items = director.plan_narrative(str(screenshots_dir))

    km = KnowledgeManager(knowledge_dir, allowed_root=root, reference_root=Path.cwd())
    ve = VisionEngine()

    ve.generate_director_inisiasi(
        plan_items=plan_items,
        course_id=course_id,
        knowledge_manager=km,
        output_file=str(output_file),
        reference_dir=reference_dir,
    )


@app.command()
def rename(
    course: str = typer.Option(..., "--course", "-c", help="Course ID (e.g., kepl, ppg)"),
    pertemuan: str = typer.Option(..., "--pertemuan", "-p", help="Pertemuan folder name (e.g., Per4)"),
    workspace_root: str = typer.Option("workspace", "--workspace", "-w", help="Workspace root directory"),
    reference_dir: str = typer.Option(None, "--reference-dir", "-r", help="Optional reference directory with PDF/PPTX materials"),
    output_dir: str = typer.Option(None, "--output-dir", "-o", help="Output directory for renamed images (default: <workspace>/<COURSE>/gambar/<Pertemuan>)"),
    source_subdir: str = typer.Option(".", "--source-subdir", help="Subdirectory under pertemuan for raw screenshots (default: current folder)"),
):
    """
    F1 Renaming Engine: Rename screenshots to canonical names (1.png, 1a.png, T1.png, ...)
    based on module step order from PDF/PPTX reference and vision classification.

    Pipeline: extract steps → classify screenshots → dedup → assign names → ACC gate → write.

    Without --reference-dir or if classification fails, falls back to mtime ordering.
    """
    from src.vision_engine import VisionEngine

    course_id, meeting, root, screenshots_dir = _prepare(course, pertemuan, workspace_root)
    screenshots_dir = resolve_under_root(
        root, screenshots_dir / source_subdir, must_exist=False
    )
    _require_screenshots(screenshots_dir)

    if output_dir:
        out_dir = resolve_under_root(root, output_dir, must_exist=False)
    else:
        out_dir = resolve_under_root(
            root, root / course_id.upper() / "gambar" / meeting, must_exist=False
        )

    ref_dir = None
    if reference_dir:
        ref_dir = resolve_under_root(root, reference_dir, must_exist=True)

    # Build plan (classifier uses VisionEngine if reference exists)
    classifier = None
    if ref_dir:
        from PIL import Image as PILImage
        ve = VisionEngine()
        def _classify(img: Path, steps):
            # Ask vision to match screenshot to step
            prompt = (
                "Klasifikasikan screenshot ini ke salah satu step berikut (hanya angka 1-N, 0 jika tidak cocok):\n"
                + "\n".join(f"{i}. {s.title}" for i, s in enumerate(steps, 1))
                + "\n\nBalas HANYA angka (misal: 3)."
            )
            try:
                with PILImage.open(str(img)) as pil_img:
                    resp = ve.model.generate_content(
                        [prompt, pil_img],
                        generation_config={"temperature": 0.0, "max_output_tokens": 10},
                    )
                text = (resp.text or "").strip()
                m = re.search(r"\d+", text)
                idx = int(m.group()) if m else 0
                return idx, 1.0 if 1 <= idx <= len(steps) else 0.0
            except Exception:
                return 0, 0.0
        classifier = _classify

    plan: RenamingPlan = build_renaming_plan(
        source_dir=str(screenshots_dir),
        reference_dir=str(ref_dir) if ref_dir else None,
        output_dir=str(out_dir),
        classifier=classifier,
    )

    if plan.is_empty:
        console.print("[yellow]No screenshots found to rename.[/yellow]")
        return

    # Display ACC table
    table = Table(title=f"🔄 Renaming Plan ({plan.mode}) — ACC Required")
    table.add_column("#", style="cyan", justify="right")
    table.add_column("Source", style="green")
    table.add_column("Final Name", style="yellow")
    table.add_column("Step", style="magenta")
    table.add_column("Conf", style="blue", justify="right")

    for i, (src, final, step_label, conf) in enumerate(plan.summary_rows(), 1):
        table.add_row(str(i), src, final, step_label, conf)

    console.print(table)
    console.print(f"\nDuplicates removed: {len(plan.duplicates)}")
    console.print(f"Unmatched: {len(plan.unmatched)}")

    # ACC gate: always require confirmation
    if not typer.confirm("\n[bold yellow]Approve and write renamed images?[/bold yellow]"):
        console.print("[red]❌ Aborted by user.[/red]")
        raise typer.Exit(1)

    report = plan.commit()
    console.print(f"\n[green]✅ Renaming complete! {len(plan.mappings)} images written to {out_dir}[/green]")
    console.print(f"[dim]Report: {report}[/dim]")


@app.command()
def generate_context(
    course: str = typer.Option(..., "--course", "-c", help="Course ID (e.g., kepl, ppg)"),
    pertemuan: str = typer.Option(..., "--pertemuan", "-p", help="Pertemuan folder name (e.g., Per4, UTS)"),
    workspace_root: str = typer.Option("workspace", "--workspace", "-w", help="Workspace root directory"),
    module_summary: str = typer.Option(None, "--module-summary", help="Brief module summary for Pass 1 planning"),
    course_context: str = typer.Option(None, "--course-context", help="Additional course context for Pass 2"),
    output: str = typer.Option(None, "--output", "-o", help="Custom output file path (must stay under workspace root)"),
):
    """
    F2 ICG-ContextGenerate: Two-pass enriched context generation.

    Pass 1: Visual census of all screenshots -> narrative plan (sections, order, pairs).
    Pass 2: Per-image enriched context (type=, group=, @section) -> pending inisiasi.txt.

    ACC gate: pending file is written first. User must approve before final inisiasi.txt.
    Automatically resumes from .icg_cache/pending_inisiasi.txt if interrupted.
    """
    course_id, meeting, root, screenshots_dir = _prepare(course, pertemuan, workspace_root)
    _require_screenshots(screenshots_dir)

    output_file = _resolve_output(root, course_id, meeting, output, "_context.txt")
    pending_file = root / ".icg_cache" / "pending_inisiasi.txt"

    ve = VisionEngine()
    engine = ContextEngine(ve.model)

    image_paths = sorted(
        [p for p in screenshots_dir.glob("*.png")],
        key=lambda p: sort_image_name(p.name),
    )
    if not image_paths:
        console.print("[yellow]No screenshots found.[/yellow]")
        return

    console.print(f"\n[bold blue]📸 Found {len(image_paths)} screenshots[/bold blue]")

    # Pass 1: Visual Census
    module_summ = module_summary or f"Praktikum {course_id.upper()} {meeting}"
    console.print("[bold yellow]🔍 Pass 1: Visual Census & Narrative Planning...[/bold yellow]")
    plan = engine.visual_census(image_paths, module_summ)

    console.print(f"  Sections: {[f'{s.id}={s.title}' for s in plan.sections]}")
    console.print(f"  Order: {plan.order}")
    console.print(f"  Pairs: {plan.pairs}")

    # Pass 2: Generate Context (with auto-save to pending)
    ctx = course_context or f"Mata kuliah: {course_id.upper()}, Pertemuan: {meeting}"
    console.print("[bold yellow]🧠 Pass 2: Enriched Context Generation...[/bold yellow]")

    result = engine.generate_pending(
        image_paths=image_paths,
        plan=plan,
        course_context=ctx,
        pending_path=pending_file,
        course=course_id.upper(),
        meeting=meeting,
    )

    console.print(f"[green]✅ Pending saved: {pending_file}[/green]")
    console.print(f"  Generated: {result['generated']}/{result['total']} images")

    # ACC Gate — require explicit user approval before final write
    console.print("\n[bold yellow]⚠️ ACC Required: Approve to write final inisiasi.txt[/bold yellow]")
    console.print(f"  Pending file: {pending_file}")
    console.print(f"  Final file:   {output_file}")

    if typer.confirm("\nApprove and write final inisiasi.txt?"):
        try:
            engine.commit_pending(pending_file, output_file, approved=True)
            console.print(f"[green]✅ Final inisiasi.txt written to {output_file}[/green]")
        except AccRequiredError:
            console.print("[red]❌ ACC denied[/red]")
            raise typer.Exit(1)
    else:
        console.print(
            "[yellow]⚠️ ACC not given. Pending preserved at .icg_cache/pending_inisiasi.txt[/yellow]"
        )


def main() -> None:
    """Entrypoint — .env is loaded here, not on import (SEC-05)."""
    _load_environment()
    app()


if __name__ == "__main__":
    main()
