"""
Configuration management for literature lookup.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, Optional
import os
import yaml


@dataclass
class ZoteroConfig:
    """Zotero configuration"""
    available: bool = True
    default_collection: Optional[str] = None
    prefer_semantic_search: bool = True
    semantic_limit: int = 10


@dataclass
class ResearchLookupConfig:
    """Research-Lookup configuration"""
    available: bool = field(default=False)  # Auto-detect
    fallback_on_empty: bool = True  # Only fallback when 0 results


@dataclass
class ValidationConfig:
    """Validation configuration"""
    validate_local: bool = True
    validate_external: bool = True
    verify_doi_for_external: bool = True


@dataclass
class LookupConfig:
    """Complete lookup configuration"""
    zotero: ZoteroConfig = field(default_factory=ZoteroConfig)
    research_lookup: ResearchLookupConfig = field(default_factory=ResearchLookupConfig)
    validation: ValidationConfig = field(default_factory=ValidationConfig)
    output_format: Literal["unified", "native"] = "unified"

    @classmethod
    def from_env(cls) -> "LookupConfig":
        """Create config from environment variables"""
        return cls(
            research_lookup=ResearchLookupConfig(
                available=bool(os.getenv("OPENROUTER_API_KEY"))
            )
        )

    @classmethod
    def from_file(cls, path: Path) -> "LookupConfig":
        """Create config from YAML file"""
        with open(path) as f:
            data = yaml.safe_load(f) or {}

        zotero_data = data.get("zotero", {})
        rl_data = data.get("research_lookup", {})
        val_data = data.get("validation", {})

        return cls(
            zotero=ZoteroConfig(
                available=zotero_data.get("available", True),
                default_collection=zotero_data.get("default_collection"),
                prefer_semantic_search=zotero_data.get(
                    "prefer_semantic_search", True
                ),
                semantic_limit=zotero_data.get("semantic_limit", 10),
            ),
            research_lookup=ResearchLookupConfig(
                available=False,  # Always auto-detect from env
                fallback_on_empty=rl_data.get("fallback_on_empty", True),
            ),
            validation=ValidationConfig(
                validate_local=val_data.get("validate_local", True),
                validate_external=val_data.get("validate_external", True),
                verify_doi_for_external=val_data.get(
                    "verify_doi_for_external", True
                ),
            ),
            output_format=data.get("output_format", "unified"),
        )

    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> "LookupConfig":
        """Load config (file first, env fallback)"""
        if config_path and config_path.exists():
            return cls.from_file(config_path)
        return cls.from_env()

    @property
    def use_fallback(self) -> bool:
        """Whether fallback should be attempted"""
        rl = self.research_lookup
        return rl.available and rl.fallback_on_empty


def load_config(config_path: Optional[str] = None) -> LookupConfig:
    """Load configuration from file or environment"""
    path = Path(config_path) if config_path else None
    return LookupConfig.load(path)
