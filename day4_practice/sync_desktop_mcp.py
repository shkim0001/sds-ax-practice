# sync_desktop_mcp.py - Claude Code(~/.claude.json)의 MCP 서버를 Claude 데스크톱 앱 설정에 복사한다.
#
# 사용법 (Claude 앱을 완전히 종료한 상태에서 실행):
#   C:/Users/Admin/Desktop/sds-ax-practice/.venv/Scripts/python.exe sync_desktop_mcp.py
#   --dry-run : 파일을 바꾸지 않고 결과만 출력
#   --force   : Claude 실행 여부 검사를 건너뜀
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime

CODE_CONFIG = os.path.expanduser("~/.claude.json")
DESKTOP_CONFIG = os.path.join(
    os.environ["LOCALAPPDATA"], "Claude-Data", "claude_pzs8sxrjxfjjc", "claude_desktop_config.json"
)


def claude_running() -> bool:
    out = subprocess.run(
        ["tasklist", "/FI", "IMAGENAME eq claude.exe", "/NH"],
        capture_output=True, text=True, errors="ignore",
    ).stdout
    return "claude.exe" in out.lower()


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    if not dry_run and "--force" not in sys.argv and claude_running():
        print("Claude 앱이 실행 중입니다. 트레이 아이콘에서 완전히 종료한 뒤 다시 실행하세요.")
        print("(실행 중에 바꾸면 앱이 종료될 때 설정을 덮어씁니다.)")
        return 1

    with open(CODE_CONFIG, encoding="utf-8") as f:
        servers = json.load(f).get("mcpServers", {})
    if not servers:
        print(f"{CODE_CONFIG}에 mcpServers가 없습니다.")
        return 1

    with open(DESKTOP_CONFIG, encoding="utf-8") as f:
        desktop = json.load(f)

    merged = desktop.setdefault("mcpServers", {})
    for name, cfg in servers.items():
        merged[name] = {k: v for k, v in cfg.items() if k != "type"}  # 데스크톱 형식엔 type 불필요

    print("추가/갱신할 서버:", ", ".join(servers))
    print("결과 서버 목록:", ", ".join(merged))
    if dry_run:
        print("[dry-run] 파일은 바꾸지 않았습니다.")
        return 0

    backup = f"{DESKTOP_CONFIG}.bak-{datetime.now():%Y%m%d-%H%M%S}"
    shutil.copy2(DESKTOP_CONFIG, backup)
    with open(DESKTOP_CONFIG, "w", encoding="utf-8") as f:
        json.dump(desktop, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"저장 완료: {DESKTOP_CONFIG}")
    print(f"백업: {backup}")
    print("이제 Claude 앱을 실행하세요.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
