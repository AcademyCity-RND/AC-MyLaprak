"""Vision engine — Gemini multimodal inference for inisiasi.txt generation.

S2-SecurityFix changes:
- SEC-05: `load_dotenv()` removed from module import; API key read from env
  at construction time only, never stored on `self`.
- SEC-09: broad `except Exception` replaced with specific google API/PIL/OSError
  catches; all log messages passed through `redact()`.
- SEC-10: LLM output lines validated by `sanitize_ai_line()` before formatting.
- F0: indentation error in generate_director_inisiasi fixed.
"""
from __future__ import annotations

import os
import re
from pathlib import Path
from typing import List, Dict, Any

import google.genai.errors as genai_errors
from google import genai
from PIL import Image, UnidentifiedImageError
from rich.console import Console

from src.security import redact, sanitize_ai_line

console = Console()


def _clean_ai_response_line(text: str) -> str:
    """Remove any leading index prefix from AI response line."""
    pattern = r"^\s*\d+(?:\.png)?\s*(?:[.)]\s*)?(?:\|\s*)?"
    return re.sub(pattern, "", text.strip())


class _LegacyModelShim:
    """Expose legacy ``model.generate_content(contents, generation_config=...)``
    on top of google-genai 3.x, keeping every existing call site and mock intact.
    """

    def __init__(self, client: "genai.Client", model_name: str):
        self._client = client
        self._model_name = model_name

    def generate_content(self, contents, generation_config=None, **kwargs):
        call_kwargs = {"model": self._model_name, "contents": contents}
        if generation_config is not None:
            call_kwargs["config"] = generation_config
        call_kwargs.update(kwargs)
        return self._client.models.generate_content(**call_kwargs)


class VisionEngine:
    """Gemini Vision wrapper. API key is read from GOOGLE_API_KEY at init."""

    _DEFAULT_MODEL = "models/gemini-3.1-flash-lite"

    def __init__(self, api_key: str | None = None, model_name: str | None = None):
        key = api_key or os.environ.get("GOOGLE_API_KEY")
        if not key:
            console.print("[red]❌ Error: GOOGLE_API_KEY not found![/red]")
            raise ValueError("Google API key is required")
        self._client = genai.Client(api_key=key)
        self.model_name = model_name or self._DEFAULT_MODEL
        self.model = _LegacyModelShim(self._client, self.model_name)

    def __repr__(self) -> str:
        return f"VisionEngine(model={self.model_name!r})"

    def __str__(self) -> str:
        return self.__repr__()

    def analyze_image_with_context(
        self,
        image_path: str,
        git_context: str,
        general_context: str = "",
        planned_index: int | None = None,
    ) -> str:
        """Analyze a single image with specific git commit context."""
        try:
            with Image.open(image_path) as img:
                index_hint = (
                    f" (urutan ke-{planned_index} dalam narasi)" if planned_index else ""
                )
                prompt = f"""
Git Commit Context: {git_context}
General Context: {general_context}{index_hint}

Berdasarkan gambar ini, buat satu baris format inisiasi (TANPA nomor indeks di depan):
{{label}} | Konteks: {{context}} | Arah: {{direction}}

Aturan penting:
- Utamakan APA YANG NYATA TERLIHAT DI GAMBAR (GUI/terminal/browser/editor).
- Gunakan Git Commit Context hanya sebagai pendukung topik/alur, BUKAN menggantikan fakta gambar.
- label: Judul singkat gambar (maksimal 50 karakter)
- Konteks: Penjelasan teknis apa yang benar-benar tampak di layar
- Arah: Arah pembahasan/evaluasi teknis
- Bahasa Indonesia, teknis tapi ringkas, langsung esens.
- Output HANYA satu baris format: Label | Konteks: ... | Arah: ...
"""
                response = self.model.generate_content([img, prompt])
                return response.text.strip() if response.text else ""
        except (OSError, UnidentifiedImageError, genai_errors.APIError, ValueError) as exc:
            console.print(
                f"[yellow]⚠️ Error analyzing {image_path}: {redact(str(exc))}[/yellow]"
            )
            return ""

    @staticmethod
    def _sort_stem(stem: str):
        if stem.isdigit():
            return (0, int(stem), 0)
        match = re.match(r"^(\d+)([a-z]+)$", stem)
        if match:
            return (1, int(match.group(1)), match.group(2))
        if stem.startswith("T") and stem[1:].isdigit():
            return (2, int(stem[1:]), 0)
        match = re.match(r"^T(\d+)-(\d+)([a-z]?)$", stem)
        if match:
            return (3, int(match.group(1)), int(match.group(2)))
        return (9, stem, 0)

    def generate_course_inisiasi(
        self,
        course_id: str,
        screenshots_dir: str,
        knowledge_manager: "KnowledgeManager",
        output_file: str,
        reference_dir: str | None = None,
        resume: bool = True,
    ) -> Dict[str, Any]:
        """Generate inisiasi.txt for all screenshots in a pertemuan folder."""
        # Auto-discover reference dir: workspace/<COURSE>/_reference
        if reference_dir is None:
            img_path = Path(screenshots_dir)
            candidate = img_path.parent.parent / "_reference"
            if candidate.is_dir():
                reference_dir = str(candidate)

        console.print(
            f"\n[bold magenta]🎯 Running Generate Mode for {course_id}...[/bold magenta]"
        )
        course_context = knowledge_manager.build_course_context(
            course_id, reference_dir=reference_dir
        )
        out_path = Path(output_file)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        img_dir = Path(screenshots_dir)
        image_files = sorted(
            [f for f in img_dir.glob("*.png")], key=lambda f: self._sort_stem(f.stem)
        )
        total = len(image_files)

        if total == 0:
            console.print("[yellow]⚠️ Tidak ada screenshot (*.png) ditemukan.[/yellow]")
            return {"total": 0, "generated": 0, "errors": 0}

        completed_map: dict[str, str] = {}
        if resume:
            # Harvest both out_path and temp_path; later (newer) source wins
            # so a partially-written temp file is never discarded on resume.
            sources = [p for p in (out_path, out_path.with_suffix(".tmp")) if p.exists()]
            for src in sorted(sources, key=lambda p: p.stat().st_mtime):
                for line in src.read_text(encoding="utf-8").splitlines():
                    if line.startswith("#") or not line.strip():
                        continue
                    parts = line.split("|", 1)
                    if parts and ".png" in parts[0]:
                        stem = parts[0].replace(".png", "").strip()
                        completed_map[stem] = line

        header = (
            "# ========================================================\n"
            "# FORMAT INISIASI UTS - GENERATE MODE\n"
            "# ========================================================"
        )
        temp_path = out_path.with_suffix(".tmp")
        if not temp_path.exists() or not completed_map:
            temp_path.write_text(header + "\n", encoding="utf-8")

        all_results = dict(completed_map)
        generated = 0
        errors = 0

        for idx, path in enumerate(image_files, 1):
            stem = path.stem
            if stem in completed_map:
                generated += 1
                continue

            result_line = self.analyze_image_with_context(
                str(path), git_context="", general_context=course_context, planned_index=idx
            )

            cleaned = _clean_ai_response_line(result_line) if result_line else ""
            safe_line = sanitize_ai_line(cleaned)
            if safe_line:
                all_results[stem] = f"{stem}.png | {safe_line}"
                generated += 1
            else:
                has_ref = "REFERENSI MATERI" in course_context
                ref_note = "referensi materi dimasukkan ke prompt" if has_ref else "tanpa referensi materi"
                all_results[stem] = (
                    f"{stem}.png | Dokumentasi Teknis {stem} | "
                    f"Konteks: ({ref_note}) | "
                    "Arah: Evaluasi praktikum"
                )
                errors += 1

            sorted_lines = [
                all_results[k] for k in sorted(all_results.keys(), key=self._sort_stem)
            ]
            temp_path.write_text(
                header + "\n" + "\n".join(sorted_lines)
                + "\n# ========================================================\n",
                encoding="utf-8",
            )

        if temp_path.exists():
            import shutil

            shutil.move(str(temp_path), str(out_path))

        return {"total": total, "generated": generated, "errors": errors}

    def generate_director_inisiasi(
        self,
        plan_items: List[Dict[str, Any]],
        course_id: str,
        knowledge_manager: "KnowledgeManager",
        output_file: str,
        reference_dir: str | None = None,
        resume: bool = True,
    ) -> Dict[str, Any]:
        """Generate inisiasi.txt using Director Mode planned items and git context."""
        console.print(
            f"\n[bold magenta]🎬 Running Director Mode Generation for {course_id}...[/bold magenta]"
        )
        course_context = knowledge_manager.build_course_context(course_id, reference_dir=reference_dir)
        out_path = Path(output_file)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        total = len(plan_items)
        generated = 0
        errors = 0

        completed_indices: dict[int, str] = {}
        if resume and out_path.exists():
            for line in out_path.read_text(encoding="utf-8").splitlines():
                if line.startswith("#") or not line.strip():
                    continue
                parts = line.split("|", 1)
                if parts and ".png" in parts[0]:
                    try:
                        idx_num = int(parts[0].replace(".png", "").strip())
                        completed_indices[idx_num] = line
                    except ValueError:
                        pass

        header = (
            "# ========================================================\n"
            "# FORMAT INISIASI UTS - DIRECTOR MODE\n"
            "# ========================================================"
        )
        temp_path = out_path.with_suffix(".tmp")
        if not temp_path.exists() or not completed_indices:
            temp_path.write_text(header + "\n", encoding="utf-8")

        all_results = dict(completed_indices)

        for idx, item in enumerate(plan_items, 1):
            if idx in completed_indices:
                generated += 1
                continue

            path = item["path"]
            git_ctx = item["git_context"]

            result_line = self.analyze_image_with_context(
                str(path), git_context=git_ctx, general_context=course_context,
                planned_index=idx,
            )

            cleaned = _clean_ai_response_line(result_line) if result_line else ""
            safe_line = sanitize_ai_line(cleaned)
            if safe_line:
                all_results[idx] = f"{idx}.png | {safe_line}"
                generated += 1
            else:
                all_results[idx] = (
                    f"{idx}.png | Dokumentasi Teknis {idx} | "
                    f"Konteks: {redact(str(git_ctx))} | Arah: Evaluasi UTS"
                )
                errors += 1

            sorted_lines = [all_results[k] for k in sorted(all_results.keys())]
            temp_path.write_text(
                header + "\n" + "\n".join(sorted_lines)
                + "\n# ========================================================\n",
                encoding="utf-8",
            )

        if temp_path.exists():
            import shutil

            shutil.move(str(temp_path), str(out_path))

        return {"total": total, "generated": generated, "errors": errors}