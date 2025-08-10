from pathlib import Path

NARRATION_DIR = Path(__file__).parent / "narration"

def load_script(script_name: str) -> str:
    """
    Load narration text from a .txt file in the narration directory.
    """
    script_path = NARRATION_DIR / f"{script_name}.txt"
    if not script_path.exists():
        raise FileNotFoundError(f"Script not found: {script_path}")
    
    with open(script_path, "r", encoding="utf-8") as f:
        return f.read().strip()

def list_scripts() -> list:
    """
    List all available .txt scripts in the narration directory.
    """
    return [p.stem for p in NARRATION_DIR.glob("*.txt")]
