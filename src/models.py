"""Pydantic models for FDA Drug Labels Scraper."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ScrapingMode(str, Enum):
    SEARCH_LABELS = "search_labels"
    GET_LABEL = "get_label"
    SEARCH_BY_DRUG = "search_by_drug"
    SEARCH_BY_MANUFACTURER = "search_by_manufacturer"


class ScraperInput(BaseModel):
    mode: ScrapingMode = ScrapingMode.SEARCH_LABELS
    query: str = ""
    set_id: str = ""
    drug_name: str = ""
    active_ingredient: str = ""
    manufacturer: str = ""
    product_type: str = ""
    route: str = ""
    marketing_status: str = ""
    max_results: int = 100
    request_interval_secs: float = 0.2
    timeout_secs: int = 30
    max_retries: int = 5

    @classmethod
    def from_actor_input(cls, raw: dict[str, Any]) -> ScraperInput:
        return cls(
            mode=raw.get("mode", ScrapingMode.SEARCH_LABELS),
            query=raw.get("query", ""),
            set_id=raw.get("setId", "") or raw.get("set_id", ""),
            drug_name=raw.get("drugName", "") or raw.get("drug_name", ""),
            active_ingredient=raw.get("activeIngredient", "") or raw.get("active_ingredient", ""),
            manufacturer=raw.get("manufacturer", ""),
            product_type=raw.get("productType", "") or raw.get("product_type", ""),
            route=raw.get("route", ""),
            marketing_status=raw.get("marketingStatus", "") or raw.get("marketing_status", ""),
            max_results=raw.get("maxResults", 100),
            request_interval_secs=raw.get("requestIntervalSecs", 0.2),
            timeout_secs=raw.get("timeoutSecs", 30),
            max_retries=raw.get("maxRetries", 5),
        )

    def validate_for_mode(self) -> str | None:
        if self.mode == ScrapingMode.GET_LABEL:
            if not self.set_id:
                return "Provide a Set ID (e.g., 'a1b2c3d4-e5f6-7890-abcd-ef1234567890') for get_label mode."
        if self.mode == ScrapingMode.SEARCH_BY_DRUG:
            if not (self.drug_name or self.active_ingredient):
                return "Provide a drug name or active ingredient for search_by_drug mode."
        if self.mode == ScrapingMode.SEARCH_BY_MANUFACTURER:
            if not self.manufacturer:
                return "Provide a manufacturer name for search_by_manufacturer mode."
        if self.mode == ScrapingMode.SEARCH_LABELS:
            if not (self.query or self.drug_name or self.active_ingredient or self.manufacturer):
                return "Provide at least one of: query, drug name, active ingredient, or manufacturer for search_labels."
        return None


class DrugLabelRecord(BaseModel):
    """Normalized FDA drug label record."""

    schema_version: str = "1.0"
    type: str = "drug_label"

    # Identification
    set_id: str = ""
    id: str = ""
    version: str = ""
    effective_time: str = ""

    # Product info
    brand_name: str = ""
    generic_name: str = ""
    manufacturer_name: str = ""
    product_type: str = ""
    route: list[str] = Field(default_factory=list)
    substance_name: list[str] = Field(default_factory=list)
    product_ndc: list[str] = Field(default_factory=list)
    package_ndc: list[str] = Field(default_factory=list)
    marketing_status: str = ""
    application_number: str = ""

    # Labeling sections
    indications_and_usage: list[str] = Field(default_factory=list)
    dosage_and_administration: list[str] = Field(default_factory=list)
    dosage_forms_and_strengths: list[str] = Field(default_factory=list)
    contraindications: list[str] = Field(default_factory=list)
    warnings_and_cautions: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    boxed_warning: list[str] = Field(default_factory=list)
    adverse_reactions: list[str] = Field(default_factory=list)
    drug_interactions: list[str] = Field(default_factory=list)
    overdosage: list[str] = Field(default_factory=list)
    description: list[str] = Field(default_factory=list)
    clinical_pharmacology: list[str] = Field(default_factory=list)
    mechanism_of_action: list[str] = Field(default_factory=list)
    pharmacodynamics: list[str] = Field(default_factory=list)
    pharmacokinetics: list[str] = Field(default_factory=list)
    pregnancy: list[str] = Field(default_factory=list)
    pediatric_use: list[str] = Field(default_factory=list)
    geriatric_use: list[str] = Field(default_factory=list)
    how_supplied: list[str] = Field(default_factory=list)
    storage_and_handling: list[str] = Field(default_factory=list)
    active_ingredient: list[str] = Field(default_factory=list)
    inactive_ingredient: list[str] = Field(default_factory=list)
    purpose: list[str] = Field(default_factory=list)

    # OTC specific
    do_not_use: list[str] = Field(default_factory=list)
    ask_doctor: list[str] = Field(default_factory=list)
    stop_use: list[str] = Field(default_factory=list)
    keep_out_of_reach_of_children: list[str] = Field(default_factory=list)

    # Controlled substance
    controlled_substance: list[str] = Field(default_factory=list)
    abuse: list[str] = Field(default_factory=list)
    dependence: list[str] = Field(default_factory=list)

    # URLs
    label_url: str = ""
