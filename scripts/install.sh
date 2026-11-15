#!/usr/bin/env bash
# Установка Strategist CLI (pfs): подтягивает все три репозитория проекта
# и ставит pfs как глобальную команду. Всё автоматически, с проверкой.
#
#   1. materials (приватный) → knowledge/   карты знаний, шаблоны, рубрики
#   2. site (публичный)      → site/        стратегproduct.ru — локальная копия
#   3. этот репозиторий (код) → pfs (uv tool install -e . или venv + symlink)
#   4. проверка: pfs doctor + наличие INDEX.md/index.html
set -euo pipefail
# корень репозитория — каталогом выше scripts/ (работает и для ./scripts/install.sh,
# и для bash scripts/install.sh, и для запуска из другого каталога)
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

BASE_REPO="https://github.com/Fighter90/product-factory-strategist-base.git"
SITE_REPO="https://github.com/Fighter90/product-factory-strategist-site.git"

step() { printf "\n→ %s\n" "$*"; }
ok()   { printf "✓ %s\n" "$*"; }
fail() { printf "✗ ОШИБКА: %s\n" "$*" >&2; exit 1; }

# ---------- 1. Материалы агента (приватный репозиторий) ----------
step "1/4 Материалы агента: product-factory-strategist-base (приватный)"
if [ -f knowledge/INDEX.md ]; then
  ok "knowledge/ уже на месте (обновить: cd knowledge && git pull)"
else
  git clone --depth 1 "$BASE_REPO" knowledge 2>&1 | grep -v "^Cloning" || true
  [ -f knowledge/INDEX.md ] || fail "база не подтянулась. Нужен доступ к приватному
репозиторию product-factory-strategist-base — приглашение выдаёт владелец
(GitHub → репозиторий → Settings → Collaborators)."
  ok "knowledge/ подтянута (100 карт RU + 100 EN, шаблоны, рубрики)"
fi

# ---------- 2. Сайт (публичный репозиторий) ----------
step "2/4 Сайт: product-factory-strategist-site (публичный)"
if [ -f site/index.html ]; then
  ok "site/ уже на месте (обновить: cd site && git pull)"
else
  git clone --depth 1 "$SITE_REPO" site
  [ -f site/index.html ] || fail "сайт не подтянулся"
  ok "site/ подтянут (strategyproduct.ru — локальная копия)"
fi

# ---------- 3. Установка pfs как глобальной команды ----------
step "3/4 Установка pfs"
if command -v uv >/dev/null 2>&1; then
  echo "→ uv tool install -e . (editable: обновления main подхватываются сами)"
  uv tool install -e . --force
elif command -v python3 >/dev/null 2>&1; then
  echo "→ uv не найден: venv ~/.pfs-venv + symlink в ~/.local/bin"
  python3 -m venv ~/.pfs-venv
  ~/.pfs-venv/bin/pip install --upgrade pip >/dev/null
  ~/.pfs-venv/bin/pip install -e .
  mkdir -p ~/.local/bin
  ln -sf ~/.pfs-venv/bin/pfs ~/.local/bin/pfs
  case ":$PATH:" in *":$HOME/.local/bin:"*) ;; *) echo "⚠ добавьте в PATH: export PATH=\"\$HOME/.local/bin:\$PATH\"";; esac
else
  fail "нужен uv (https://docs.astral.sh/uv/) или python3."
fi

# ---------- 4. Проверка установки ----------
step "4/4 Проверка"
FAILS=0
command -v pfs >/dev/null 2>&1 && ok "pfs — глобальная команда" || { echo "✗ pfs не в PATH"; FAILS=1; }
[ -f knowledge/INDEX.md ] && ok "база знаний: knowledge/INDEX.md на месте" || { echo "✗ нет knowledge/INDEX.md"; FAILS=1; }
[ -f site/index.html ] && ok "сайт: site/index.html на месте" || { echo "✗ нет site/index.html"; FAILS=1; }
python3 -c "import tools.pfs" >/dev/null 2>&1 && ok "tools.pfs импортируется" || { echo "✗ tools.pfs не импортируется"; FAILS=1; }
pfs doctor | tail -6 || true
[ "$FAILS" -eq 0 ] && echo "" && echo "✓ Установка завершена: все три репозитория на месте, pfs готов." \
  && echo "  Запуск: pfs new \"<название>\" \"<запрос>\"  ·  Сайт локально: open site/index.html" \
  || exit 1
echo ""
pfs --help | head -3
echo "Готово: pfs — глобальная команда. Проекты: <репо>/projects (или env PFS_PROJECTS_DIR)."
