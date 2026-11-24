# Strategi Release & Versioning — MyLaprak

> **Gate ACC Wajib:** JANGAN git commit/push/tag/release tanpa ACC Avin.
> Selesai = tulis working tree + request-review. Baru commit setelah Avin review+ACC.
> Format: `feat(scope): deskripsi`, 1 task = 1 commit atomik.
> 1 branch/repo, rebase/merge tanpa squash. History task dipertahankan.
> Notif: chat + Discord (`discord:myagent` / `#ruang-magang`).

---

## 1. Tooling: git-cliff

**Dipilih:** [`git-cliff`](https://github.com/orhun/git-cliff) — Rust CLI untuk generate CHANGELOG.md dari Conventional Commits + auto version bump.

**Alasan:**
- Single binary, cepat, zero-runtime deps
- Native support Conventional Commits + Keep a Changelog format
- Built-in version bumping (`--bumped-version`)
- Integrasi GitHub Actions trivial (`taiki-e/install-action@git-cliff`)
- Format output sinkron dengan CHANGELOG.md existing (Indonesia, emoji sections)

**File konfigurasi:** `cliff.toml` (root repo)

**Install lokal:**
```bash
# Windows (Scoop)
scoop install git-cliff

# macOS (Homebrew)
brew install git-cliff

# Linux / CI (cargo)
cargo install git-cliff
```

---

## 2. Commit Template

**Format:** `<type>(<scope>): <deskripsi>` — **Conventional Commits** (https://conventionalcommits.org)

| Type      | Arti                      | Version Bump |
|-----------|---------------------------|--------------|
| `feat`    | Fitur baru                | **MINOR**    |
| `fix`     | Perbaikan bug             | **PATCH**    |
| `perf`    | Perbaikan performa        | PATCH        |
| `docs`    | Dokumentasi               | — (no bump)  |
| `refactor`| Refactor non-breaking     | —            |
| `test`    | Test                      | —            |
| `chore`   | Maintenance, deps, build  | —*           |
| `ci`      | CI/CD workflow            | —            |
| `build`   | Build system              | —            |

> `chore(release):` di-skip oleh git-cliff (no bump, no changelog entry)

**Scope:** modul/fitur terdampak — contoh: `make-laprak`, `breakdown-matkul`, `parser`, `template`, `release`, `skills`

**Aktivasi template:**
```bash
git config commit.template .gitmessage
```

File: `.gitmessage` (root repo) — berisi template lengkap + daftar type/scope.

---

## 3. Branch Strategy

### Prinsip
- **1 branch kerja per repo** (nama bebas, mis. `dev` / `work/F5-release`)
- **Semua task bertumpuk di branch itu** — gak banyak cabang
- **1 task = 1 commit atomik** — format `feat(scope): deskripsi`
- **Integrasi ke `main`:** rebase/merge **tanpa squash** → history task dipertahankan
- **Proteksi `main`:** require PR review + CI quality gate (`.github/workflows/ci.yml`)

### Alur Kerja
```bash
# 0. PENTING: aktifkan commit template sekali
git config commit.template .gitmessage

# 1. Buat/switch branch kerja (sekali di awal)
git checkout -b work/F5-release

# 2. Kerjakan task → commit per task
#    STAGE EKSPLISIT — JANGAN pakai `git add -A` / `git add .`
#    (working tree berisi file dari task lain; `git add -A` menyatukan
#     semua task ke 1 commit → melanggar "1 task = 1 commit")
git add cliff.toml .gitmessage .github/workflows/release.yml docs/RELEASE.md
git commit -m "feat(release): auto versioning + changelog via git-cliff"

# 3. Task selesai → NOTIF chat + Discord → request review → ACC
# 4. Setelah ACC: push branch → PR ke main → rebase/merge (no squash)
git push origin work/F5-release
# PR create via GitHub UI / gh CLI
# Reviewer: review only
# Avin: ACC → merge (rebase/merge commit)
```

### Catatan
- **Stage eksplisit per task:** selalu `git add <file-task>` — jangan `git add -A`.
  Di MyLaprak ada file untracked/modified dari task lain (`skills/ICG-ContextGenerate/`,
  `skills/ICG-Renaming/`, `CHANGELOG.md`, modified `README.md`, `CONTRIBUTING.md`,
  `plugin.json`, dll.) yang harus masuk commit task-nya sendiri.
- Branch kerja **tidak di-force-push** setelah dishare
- Rebase lokal sebelum PR biar clean: `git rebase main`
- Merge ke `main` via GitHub PR → **Rebase and merge** (bukan Squash)

---

## 4. Release Workflow (`.github/workflows/release.yml`)

### Trigger
1. **Manual dispatch (utama — setelah ACC):**
   - `workflow_dispatch` dengan input:
     - `bump`: `auto` (default) | `patch` | `minor` | `major`
     - `dry_run`: `true`/`false` (default `false`)
2. **Fallback tag push:** `push` tag `v*` → generate changelog + release tanpa auto-bump

### Steps (ringkas)
1. Checkout full history (`fetch-depth: 0`)
2. Install git-cliff
3. **Determine version:**
   - Tag push: pakai tag yg di-push
   - Dispatch: `git cliff --bumped-version` (auto) atau `--bump <level>`
4. **Generate CHANGELOG.md** → `git cliff --tag <version> --output CHANGELOG.md`
5. **Commit CHANGELOG.md** (dispatch only) — push pakai `GITHUB_TOKEN` sehingga
   tidak memicu workflow lain (GitHub tidak jalankan workflow dari push GITHUB_TOKEN).
   Tidak pakai `[skip ci]` karena itu no-op di GitHub Actions.
6. **Create & push tag** (dispatch only)
7. **Build bundle** → `MyLaprak-<version>.zip` (skills/, plugin.json, README.md, CONTRIBUTING.md, CHANGELOG.md) → dilampirkan ke GitHub Release via `files:`
8. **Create GitHub Release** via `softprops/action-gh-release@v2` dengan body = generated changelog
9. **Notify Discord** via webhook secret `DISCORD_WEBHOOK_URL`

### Secrets Required
| Secret | Deskripsi |
|--------|-----------|
| `DISCORD_WEBHOOK_URL` | Webhook URL channel `#ruang-magang` (Discord) |

### Menjalankan Release (setelah ACC)
1. Buka GitHub Actions → `Release — Auto Version, Changelog, & GitHub Release`
2. Klik **Run workflow**
3. Pilih `bump` (default `auto`) + `dry_run: false`
4. Klik **Run workflow**
5. Workflow jalan → bundle dibuat → tag → release publish → Discord notif

---

## 5. Notification Flow

```
Task Selesai (working tree ready)
       │
       ▼
NOTIF: chat (kanban summary) + Discord (discord:myagent / #ruang-magang)
       │
       ▼
REVIEW by REVIEWER-MAGANG (review only)
       │
       ▼
ACC by Avin (Xte-1412)
       │
       ▼
COMMIT + PUSH + PR + MERGE (rebase/merge, no squash)
       │
       ▼
RELEASE WORKFLOW (manual dispatch) → tag + release + Discord
```

**Discord channels:**
- `discord:myagent` (channel ID: `1562854861559566407`)
- `#ruang-magang` (channel ID: `1574433487899992176`)

---

## 6. File Checklist per Repo

| File | Deskripsi |
|------|-----------|
| `cliff.toml` | git-cliff config (changelog format, commit parsers, bump rules) |
| `.github/workflows/release.yml` | Release workflow (auto version, changelog, bundle, release, Discord) |
| `.gitmessage` | Commit message template (format + type/scope guide) |
| `docs/RELEASE.md` | Dokumentasi ini |
| `.github/release.yml` | GitHub auto-label categories (existing, sinkron dengan changelog) |

---

## 7. Referensi
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Keep a Changelog (ID)](https://keepachangelog.com/id/1.0.0/)
- [SemVer (ID)](https://semver.org/lang/id/)
- [git-cliff](https://github.com/orhun/git-cliff)
- [softprops/action-gh-release](https://github.com/softprops/action-gh-release)

---

*Generated for F5 Release task. Dokumentasi ini adalah bagian dari working tree changes — belum di-commit (ACC gate).*