"""Shared helpers for exporting/reconstructing FPL LAB web data chunks."""
from __future__ import annotations
import hashlib, json, shutil
from pathlib import Path

SAFE_ASSET_LIMIT = 24 * 1024 * 1024
HEAVY_KEYS = {"snapshots", "playerMatch", "eventPlayer", "events"}


def compact_json(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()[:12]


def load_data_js(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    prefix = "window.FPL_V2="
    if not raw.startswith(prefix) or not raw.rstrip().endswith(";"):
        raise ValueError("data.js is not in the expected window.FPL_V2=<json>; format")
    payload = raw[len(prefix):].rstrip()[:-1]
    data = json.loads(payload)
    if not isinstance(data, dict) or not data.get("teams") or not data.get("gws"):
        raise ValueError("data.js is missing required FPL LAB data")
    return data


def nested_week(source: dict, gw: int) -> dict:
    key = str(gw)
    out = {}
    for entity_id, weeks in source.items():
        if isinstance(weeks, dict) and key in weeks:
            out[str(entity_id)] = {key: weeks[key]}
    return out


def _write_hashed_json(out_dir: Path, stem: str, payload: dict) -> dict:
    raw = compact_json(payload)
    if len(raw) > SAFE_ASSET_LIMIT:
        raise ValueError(f"Generated asset {stem}.json is too large: {len(raw):,} bytes")
    name = f"{stem}.{digest(raw)}.json"
    (out_dir / name).write_bytes(raw)
    return {"file": name, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def export_web_data(data_or_path, out_dir: Path) -> dict:
    data = load_data_js(Path(data_or_path)) if not isinstance(data_or_path, dict) else data_or_path
    out_dir = Path(out_dir)
    temp = out_dir.with_name(out_dir.name + ".tmp")
    if temp.exists(): shutil.rmtree(temp)
    temp.mkdir(parents=True)

    core = {k: v for k, v in data.items() if k not in HEAVY_KEYS}
    core_ref = _write_hashed_json(temp, "core", core)
    gw_refs = []
    for gw in sorted(int(x) for x in data["gws"]):
        payload = {
            "gw": gw,
            "snapshots": nested_week(data.get("snapshots", {}), gw),
            "playerMatch": nested_week(data.get("playerMatch", {}), gw),
            "eventPlayer": nested_week(data.get("eventPlayer", {}), gw),
            "events": [e for e in data.get("events", []) if int(e[0]) == gw],
        }
        ref = _write_hashed_json(temp, f"gw-{gw:02d}", payload)
        ref["gw"] = gw
        gw_refs.append(ref)

    fingerprint = digest(compact_json({"core": core_ref, "gameweeks": gw_refs}))
    manifest = {
        "schema": 1,
        "build": fingerprint,
        "season": data.get("season"),
        "core": core_ref,
        "gameweeks": gw_refs,
        "totals": {
            "players": len(data.get("players", [])),
            "fixtures": len(data.get("fixtures", [])),
            "events": len(data.get("events", [])),
        },
    }
    (temp / "manifest.json").write_bytes(compact_json(manifest))
    if out_dir.exists(): shutil.rmtree(out_dir)
    temp.rename(out_dir)
    return manifest


def reconstruct_web_data(data_dir: Path) -> tuple[dict, dict]:
    data_dir = Path(data_dir)
    manifest = json.loads((data_dir / "manifest.json").read_text(encoding="utf-8"))
    core_path = data_dir / manifest["core"]["file"]
    core_raw = core_path.read_bytes()
    if hashlib.sha256(core_raw).hexdigest() != manifest["core"].get("sha256"):
        raise ValueError("Core dataset checksum mismatch")
    core = json.loads(core_raw)
    core["snapshots"] = {}; core["playerMatch"] = {}; core["eventPlayer"] = {}; core["events"] = []

    def merge(dst, source):
        for pid, weeks in source.items(): dst.setdefault(pid, {}).update(weeks)

    for item in sorted(manifest["gameweeks"], key=lambda x: int(x["gw"])):
        path = data_dir / item["file"]
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != item.get("sha256"):
            raise ValueError(f"Gameweek {item['gw']} dataset checksum mismatch")
        chunk = json.loads(raw)
        merge(core["snapshots"], chunk.get("snapshots", {}))
        merge(core["playerMatch"], chunk.get("playerMatch", {}))
        merge(core["eventPlayer"], chunk.get("eventPlayer", {}))
        core["events"].extend(chunk.get("events", []))
    return core, manifest
