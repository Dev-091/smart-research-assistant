import json
from copy import deepcopy
from pathlib import Path

from config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    EMBEDDING_MODEL,
    FAISS_STORAGE_PATH,
    GROQ_MODEL,
    MAX_TOKENS,
    TEMPERATURE,
    TOP_K,
)


SETTINGS_PATH = Path(FAISS_STORAGE_PATH) / "app_settings.json"
SETTINGS_SCHEMA = {
    "retrieval": {
        "top_k": TOP_K,
    },
    "chunking": {
        "chunk_size": CHUNK_SIZE,
        "chunk_overlap": CHUNK_OVERLAP,
    },
    "models": {
        "embedding_model": EMBEDDING_MODEL,
        "llm_model": GROQ_MODEL,
    },
    "generation": {
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
    },
}
SETTINGS_OPTIONS = {
    "embedding_models": [
        "sentence-transformers/all-MiniLM-L6-v2",
        "sentence-transformers/all-mpnet-base-v2",
    ],
    "llm_models": [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "mixtral-8x7b-32768",
    ],
}


class AppSettingsService:
    def __init__(self, settings_path=SETTINGS_PATH):
        self.settings_path = Path(settings_path)
        self.settings_path.parent.mkdir(parents=True, exist_ok=True)

    def get_defaults(self):
        return deepcopy(SETTINGS_SCHEMA)

    def load_settings(self):
        defaults = self.get_defaults()
        if not self.settings_path.exists():
            return defaults

        try:
            saved_settings = json.loads(self.settings_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return defaults

        return self._merge_settings(defaults, saved_settings)

    def save_settings(self, settings):
        normalized = self._normalize_settings(settings)
        self.settings_path.write_text(json.dumps(normalized, indent=2), encoding="utf-8")
        return normalized

    def get_options(self):
        return deepcopy(SETTINGS_OPTIONS)

    def _merge_settings(self, defaults, saved_settings):
        merged = deepcopy(defaults)
        for section, values in saved_settings.items():
            if section in merged and isinstance(values, dict):
                merged[section].update(values)
        return self._normalize_settings(merged)

    def _normalize_settings(self, settings):
        normalized = deepcopy(settings)
        chunk_size = int(normalized["chunking"]["chunk_size"])
        chunk_overlap = int(normalized["chunking"]["chunk_overlap"])
        normalized["retrieval"]["top_k"] = max(1, int(normalized["retrieval"]["top_k"]))
        normalized["chunking"]["chunk_size"] = max(100, chunk_size)
        normalized["chunking"]["chunk_overlap"] = max(0, min(chunk_overlap, normalized["chunking"]["chunk_size"] - 1))
        normalized["generation"]["temperature"] = float(normalized["generation"]["temperature"])
        normalized["generation"]["max_tokens"] = max(64, int(normalized["generation"]["max_tokens"]))
        return normalized
