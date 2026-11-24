"""Director Engine — Pass 1 visual census & git-context narrative planning.

S2-SecurityFix:
- SEC-01: `allow_git_context` opt-in flag; without it commit subjects are never
  loaded into `git_timeline` and never reach the Gemini prompt.
  `repo_path` is resolved and contained under `allowed_root` (defaults to
  workspace_root.parent, override via `--repo-root`) — defense-in-depth
  against arbitrary repo read (review round 1, MAJOR #2).
- SEC-09: subprocess exceptions are caught specifically; all log messages
  redacted via `redact()`.
"""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

from rich.console import Console

from src.security import PathValidationError, redact, resolve_under_root

console = Console()


class DirectorEngine:
    """Plan screenshot narrative, optionally using *redacted* git commit subjects."""

    def __init__(
        self,
        repo_path: str | None = None,
        allow_git_context: bool = False,
        allowed_root: str | Path | None = None,
    ):
        self.allow_git_context = allow_git_context
        self.allowed_root = Path(allowed_root).resolve() if allowed_root else None
        self.git_timeline: list[dict[str, Any]] = []

        if repo_path:
            if self.allowed_root:
                # Contain repo_path under allowed_root (defense-in-depth, MAJOR #2)
                try:
                    resolved = resolve_under_root(self.allowed_root, repo_path, must_exist=True)
                except PathValidationError as exc:
                    console.print(f"[yellow]⚠️ Repo path rejected: {redact(str(exc))}[/yellow]")
                    self.repo_path = None
                    self.allow_git_context = False
                    return
            else:
                resolved = Path(repo_path).resolve()
                if not resolved.exists():
                    console.print(f"[yellow]⚠️ Repo path does not exist: {redact(repo_path)}[/yellow]")
                    self.repo_path = None
                    self.allow_git_context = False
                    return
            self.repo_path = str(resolved)
            if self.allow_git_context:
                self._load_git_timeline()
            else:
                console.print(
                    "[dim]ℹ️ Git context disabled (pass --allow-git-context to opt in).[/dim]"
                )
        else:
            self.repo_path = None

    def _load_git_timeline(self) -> None:
        """Extract git commit history with timestamps and redacted subjects."""
        try:
            cmd = [
                "git", "-C", self.repo_path,
                "log", "--pretty=format:%h|%ad|%s", "--date=iso", "-n", "50",
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            for line in result.stdout.strip().split("\n"):
                if not line:
                    continue
                parts = line.split("|", 2)
                if len(parts) != 3:
                    continue
                commit_hash, date_str, subject = parts
                try:
                    dt = datetime.fromisoformat(date_str.strip())
                except ValueError:
                    continue
                self.git_timeline.append({
                    "hash": commit_hash,
                    "time": dt,
                    "subject": redact(subject.strip()),
                })
            console.print(
                f"[green]✅ Loaded {len(self.git_timeline)} git commits for narrative alignment.[/green]"
            )
        except (subprocess.CalledProcessError, OSError, UnicodeDecodeError) as exc:
            console.print(
                f"[yellow]⚠️ Could not load git timeline: {redact(str(exc))}[/yellow]"
            )

    def get_nearest_commit(self, file_mtime: datetime) -> str:
        """Return the redacted commit subject preceding `file_mtime`."""
        if not self.git_timeline:
            return "General development progress"
        for commit in self.git_timeline:
            if commit["time"] <= file_mtime:
                return commit["subject"]
        return self.git_timeline[-1]["subject"]

    def plan_narrative(
        self, screenshots_dir: str, draft_inisiasi_path: str | None = None
    ) -> List[Dict[str, Any]]:
        """Pass 1: visual census & narrative planning."""
        img_dir = Path(screenshots_dir)
        files = []
        for f in img_dir.glob("*.png"):
            mtime = datetime.fromtimestamp(f.stat().st_mtime).astimezone()
            files.append({
                "path": f,
                "name": f.name,
                "stem": f.stem,
                "mtime": mtime,
                "is_numeric": f.stem.isdigit(),
                "numeric_val": int(f.stem) if f.stem.isdigit() else 9999,
            })

        numeric_files = sorted(
            [f for f in files if f["is_numeric"]], key=lambda x: x["numeric_val"]
        )
        timestamp_files = sorted(
            [f for f in files if not f["is_numeric"]], key=lambda x: x["mtime"]
        )
        all_ordered = numeric_files + timestamp_files

        console.print(
            f"[bold cyan]🎬 Director Mode: Planning narrative for "
            f"{len(all_ordered)} screenshots...[/bold cyan]"
        )

        planned_items = []
        for idx, item in enumerate(all_ordered, start=1):
            planned_items.append({
                "index": idx,
                "original_name": item["name"],
                "path": item["path"],
                "mtime": item["mtime"],
                "git_context": self.get_nearest_commit(item["mtime"]),
            })
        return planned_items