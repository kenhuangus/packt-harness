"""
Uploads MP3 and MP4 media files from packt-harness to Ken Huang's Google Drive.
Invokes gws directly with the isolated kenhuangus profile environment.
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Setup profile environment
CONFIG_DIR = Path.home() / ".config" / "gws-profiles" / "kenhuangus"
GWS_ENV = os.environ.copy()
GWS_ENV["GOOGLE_WORKSPACE_CLI_CONFIG_DIR"] = str(CONFIG_DIR)
GWS_ENV["GOOGLE_WORKSPACE_CLI_ACCOUNT"] = "kenhuangus@gmail.com"

GWS_EXE = shutil.which("gws")
if not GWS_EXE:
    appdata = os.environ.get("APPDATA")
    if appdata:
        for c in [
            Path(appdata) / "npm" / "node_modules" / "@googleworkspace" / "cli" / "bin" / "gws.exe",
            Path(appdata) / "npm" / "gws.cmd",
        ]:
            if c.exists():
                GWS_EXE = str(c)
                break
if not GWS_EXE:
    GWS_EXE = "gws"

MEDIA_FILES = [
    {
        "path": Path(r"C:\Users\kenhu\packt-harness\deep_research_agent\demo\deep_research_agent_demo.mp4"),
        "name": "deep_research_agent_demo.mp4",
        "mime": "video/mp4",
        "desc": "Autonomous Deep Research Agent 1080p Demo Video (3.87 mins, 19 stages)",
    },
    {
        "path": Path(r"C:\Users\kenhu\packt-harness\audio\packt_harness_complete_masterclass_1hr.mp3"),
        "name": "packt_harness_complete_masterclass_1hr.mp3",
        "mime": "audio/mpeg",
        "desc": "Complete 1-Hour Packt Harness Engineering Masterclass Audio",
    },
    {
        "path": Path(r"C:\Users\kenhu\packt-harness\deep_research_agent\demo\demo_narration.mp3"),
        "name": "demo_narration.mp3",
        "mime": "audio/mpeg",
        "desc": "Deep Research Agent Demo Narration Voiceover Audio",
    },
]


def run_gws(args: list[str]) -> dict:
    cmd = [GWS_EXE] + args
    res = subprocess.run(cmd, env=GWS_ENV, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"STDERR: {res.stderr}", file=sys.stderr)
        print(f"STDOUT: {res.stdout}", file=sys.stderr)
        raise RuntimeError(f"Command failed: {cmd}\nCode: {res.returncode}")
    
    # Parse json output from gws
    stdout = res.stdout.strip()
    # If there are preamble lines (like 'Using keyring backend: ...'), find the first '{'
    json_start = stdout.find("{")
    if json_start != -1:
        return json.loads(stdout[json_start:])
    return {}


def create_folder(name: str) -> str:
    print(f"[*] Creating folder '{name}' on Ken Huang's Google Drive...")
    meta = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
        "description": "Packt Harness Engineering Masterclass Media Files",
    }
    res = run_gws(["drive", "files", "create", "--json", json.dumps(meta)])
    folder_id = res["id"]
    print(f"  [OK] Created folder: {name} (ID: {folder_id})")
    return folder_id


def upload_file(info: dict, folder_id: str) -> dict:
    p = info["path"]
    size_mb = p.stat().st_size / (1024 * 1024)
    print(f"[*] Uploading '{info['name']}' ({size_mb:.2f} MB)...")
    
    meta = {
        "name": info["name"],
        "parents": [folder_id],
        "description": info["desc"],
    }
    
    res = run_gws([
        "drive", "files", "create",
        "--json", json.dumps(meta),
        "--upload", str(p),
        "--upload-content-type", info["mime"],
    ])
    
    file_id = res.get("id")
    web_link = f"https://drive.google.com/file/d/{file_id}/view"
    print(f"  [OK] Uploaded {info['name']} -> ID: {file_id}")
    print(f"       Direct Link: {web_link}")
    return {
        "name": info["name"],
        "id": file_id,
        "size_mb": size_mb,
        "web_link": web_link,
    }


def main():
    print("================================================================================")
    print("UPLOADING MP3 & MP4 MEDIA TO KEN HUANG'S GOOGLE DRIVE (kenhuangus@gmail.com)")
    print("================================================================================")
    
    folder_id = create_folder("Packt-Harness-Engineering-Media")
    folder_url = f"https://drive.google.com/drive/folders/{folder_id}"
    
    uploaded = []
    for item in MEDIA_FILES:
        res = upload_file(item, folder_id)
        uploaded.append(res)
        
    print("\n================================================================================")
    print("ALL MEDIA FILES SUCCESSFULLY UPLOADED TO GOOGLE DRIVE!")
    print(f"Google Drive Folder URL: {folder_url}")
    for u in uploaded:
        print(f"• {u['name']} ({u['size_mb']:.2f} MB): {u['web_link']}")
    print("================================================================================")


if __name__ == "__main__":
    main()
