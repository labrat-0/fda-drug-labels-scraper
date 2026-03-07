"""Core scraping logic for FDA Drug Labels Scraper.

All 4 modes: search_labels, get_label (by set_id), search_by_drug, search_by_manufacturer.
"""

from __future__ import annotations

import logging
from typing import Any, AsyncGenerator
from urllib.parse import quote

import httpx

from .models import DrugLabelRecord, ScraperInput
from .utils import BASE_URL, RateLimiter, build_headers, fetch_json

logger = logging.getLogger(__name__)


def _safe_list(val: Any) -> list[str]:
    """Ensure we always return a list of strings."""
    if val is None:
        return []
    if isinstance(val, list):
        return [str(v) for v in val if v]
    return [str(val)] if val else []


def _safe_str(val: Any) -> str:
    """Ensure we always return a string."""
    if val is None:
        return ""
    if isinstance(val, list):
        return val[0] if val else ""
    return str(val)


def _extract_label(raw: dict[str, Any]) -> DrugLabelRecord:
    """Parse an openFDA drug label API response into a DrugLabelRecord."""
    openfda = raw.get("openfda", {}) or {}

    # Identification
    set_id = _safe_str(raw.get("set_id"))
    label_id = _safe_str(raw.get("id"))
    version = _safe_str(raw.get("version"))
    effective_time = _safe_str(raw.get("effective_time"))

    # Product info from openfda
    brand_name = _safe_str(openfda.get("brand_name"))
    generic_name = _safe_str(openfda.get("generic_name"))
    manufacturer_name = _safe_str(openfda.get("manufacturer_name"))
    product_type = _safe_str(openfda.get("product_type"))
    route = _safe_list(openfda.get("route"))
    substance_name = _safe_list(openfda.get("substance_name"))
    product_ndc = _safe_list(openfda.get("product_ndc"))
    package_ndc = _safe_list(openfda.get("package_ndc"))
    application_number = _safe_str(openfda.get("application_number"))

    # Marketing status - handle both string and list
    marketing_status_raw = openfda.get("marketing_status")
    if isinstance(marketing_status_raw, list):
        marketing_status = marketing_status_raw[0] if marketing_status_raw else ""
    else:
        marketing_status = _safe_str(marketing_status_raw)

    # Labeling sections
    indications_and_usage = _safe_list(raw.get("indications_and_usage"))
    dosage_and_administration = _safe_list(raw.get("dosage_and_administration"))
    dosage_forms_and_strengths = _safe_list(raw.get("dosage_forms_and_strengths"))
    contraindications = _safe_list(raw.get("contraindications"))
    warnings_and_cautions = _safe_list(raw.get("warnings_and_cautions"))
    warnings = _safe_list(raw.get("warnings"))
    boxed_warning = _safe_list(raw.get("boxed_warning"))
    adverse_reactions = _safe_list(raw.get("adverse_reactions"))
    drug_interactions = _safe_list(raw.get("drug_interactions"))
    overdosage = _safe_list(raw.get("overdosage"))
    description = _safe_list(raw.get("description"))
    clinical_pharmacology = _safe_list(raw.get("clinical_pharmacology"))
    mechanism_of_action = _safe_list(raw.get("mechanism_of_action"))
    pharmacodynamics = _safe_list(raw.get("pharmacodynamics"))
    pharmacokinetics = _safe_list(raw.get("pharmacokinetics"))
    pregnancy = _safe_list(raw.get("pregnancy"))
    pediatric_use = _safe_list(raw.get("pediatric_use"))
    geriatric_use = _safe_list(raw.get("geriatric_use"))
    how_supplied = _safe_list(raw.get("how_supplied"))
    storage_and_handling = _safe_list(raw.get("storage_and_handling"))
    active_ingredient = _safe_list(raw.get("active_ingredient"))
    inactive_ingredient = _safe_list(raw.get("inactive_ingredient"))
    purpose = _safe_list(raw.get("purpose"))

    # OTC specific
    do_not_use = _safe_list(raw.get("do_not_use"))
    ask_doctor = _safe_list(raw.get("ask_doctor"))
    stop_use = _safe_list(raw.get("stop_use"))
    keep_out_of_reach_of_children = _safe_list(raw.get("keep_out_of_reach_of_children"))

    # Controlled substance
    controlled_substance = _safe_list(raw.get("controlled_substance"))
    abuse = _safe_list(raw.get("abuse"))
    dependence = _safe_list(raw.get("dependence"))

    # Build label URL
    label_url = f"https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid={set_id}" if set_id else ""

    return DrugLabelRecord(
        set_id=set_id,
        id=label_id,
        version=version,
        effective_time=effective_time,
        brand_name=brand_name,
        generic_name=generic_name,
        manufacturer_name=manufacturer_name,
        product_type=product_type,
        route=route,
        substance_name=substance_name,
        product_ndc=product_ndc,
        package_ndc=package_ndc,
        marketing_status=marketing_status,
        application_number=application_number,
        indications_and_usage=indications_and_usage,
        dosage_and_administration=dosage_and_administration,
        dosage_forms_and_strengths=dosage_forms_and_strengths,
        contraindications=contraindications,
        warnings_and_cautions=warnings_and_cautions,
        warnings=warnings,
        boxed_warning=boxed_warning,
        adverse_reactions=adverse_reactions,
        drug_interactions=drug_interactions,
        overdosage=overdosage,
        description=description,
        clinical_pharmacology=clinical_pharmacology,
        mechanism_of_action=mechanism_of_action,
        pharmacodynamics=pharmacodynamics,
        pharmacokinetics=pharmacokinetics,
        pregnancy=pregnancy,
        pediatric_use=pediatric_use,
        geriatric_use=geriatric_use,
        how_supplied=how_supplied,
        storage_and_handling=storage_and_handling,
        active_ingredient=active_ingredient,
        inactive_ingredient=inactive_ingredient,
        purpose=purpose,
        do_not_use=do_not_use,
        ask_doctor=ask_doctor,
        stop_use=stop_use,
        keep_out_of_reach_of_children=keep_out_of_reach_of_children,
        controlled_substance=controlled_substance,
        abuse=abuse,
        dependence=dependence,
        label_url=label_url,
    )


class FDADrugLabelsScraper:
    """Async scraper for openFDA drug labels."""

    def __init__(
        self,
        client: httpx.AsyncClient,
        rate_limiter: RateLimiter,
        config: ScraperInput,
    ) -> None:
        self.client = client
        self.rate_limiter = rate_limiter
        self.config = config
        self.headers = build_headers()
        self.timeout = float(config.timeout_secs)
        self.retries = config.max_retries

    async def scrape(self) -> AsyncGenerator[dict[str, Any], None]:
        if self.config.mode.value == "get_label":
            async for item in self._get_label():
                yield item
        elif self.config.mode.value == "search_by_drug":
            async for item in self._search_by_drug():
                yield item
        elif self.config.mode.value == "search_by_manufacturer":
            async for item in self._search_by_manufacturer():
                yield item
        else:
            async for item in self._search_labels():
                yield item

    def _build_search_query(self, terms: list[tuple[str, str]]) -> str:
        """Build openFDA search query from field:value pairs."""
        parts = []
        for field, value in terms:
            if value:
                # Escape special characters and quote multi-word values
                escaped = value.replace('"', '\\"')
                if " " in escaped:
                    parts.append(f'{field}:"{escaped}"')
                else:
                    parts.append(f"{field}:{escaped}")
        return "+AND+".join(parts)

    async def _search_labels(self) -> AsyncGenerator[dict[str, Any], None]:
        """Search drug labels with various filters."""
        terms: list[tuple[str, str]] = []
        general_search = None

        if self.config.query:
            # General search - just use the query term directly
            query_escaped = self.config.query.replace('"', '\\"')
            if " " in query_escaped:
                general_search = f'"{query_escaped}"'
            else:
                general_search = query_escaped

        # Build additional filter terms
        if self.config.drug_name:
            terms.append(("openfda.brand_name", self.config.drug_name))
        if self.config.active_ingredient:
            terms.append(("openfda.substance_name", self.config.active_ingredient))
        if self.config.manufacturer:
            terms.append(("openfda.manufacturer_name", self.config.manufacturer))
        if self.config.product_type:
            terms.append(("openfda.product_type", self.config.product_type))
        if self.config.route:
            terms.append(("openfda.route", self.config.route))

        # Construct search query
        if general_search and terms:
            search_query = f"{general_search}+AND+{self._build_search_query(terms)}"
        elif general_search:
            search_query = general_search
        elif terms:
            search_query = self._build_search_query(terms)
        else:
            search_query = ""

        async for item in self._paginate_search(search_query):
            yield item

    async def _get_label(self) -> AsyncGenerator[dict[str, Any], None]:
        """Get a specific drug label by set_id."""
        set_id = self.config.set_id.strip()
        search_query = f'set_id:"{set_id}"'

        params = {
            "search": search_query,
            "limit": 1,
        }

        data = await fetch_json(
            self.client,
            BASE_URL,
            self.rate_limiter,
            self.headers,
            max_retries=self.retries,
            timeout=self.timeout,
            params=params,
        )

        if not data or not isinstance(data, dict):
            logger.warning(f"No label found for set_id: {set_id}")
            return

        results = data.get("results", [])
        if not results:
            logger.warning(f"No label found for set_id: {set_id}")
            return

        record = _extract_label(results[0])
        yield record.model_dump()

    async def _search_by_drug(self) -> AsyncGenerator[dict[str, Any], None]:
        """Search labels by drug name or active ingredient."""
        terms: list[tuple[str, str]] = []

        if self.config.drug_name:
            terms.append(("openfda.brand_name", self.config.drug_name))
        if self.config.active_ingredient:
            terms.append(("openfda.substance_name", self.config.active_ingredient))

        if not terms:
            return

        search_query = self._build_search_query(terms)
        async for item in self._paginate_search(search_query):
            yield item

    async def _search_by_manufacturer(self) -> AsyncGenerator[dict[str, Any], None]:
        """Search labels by manufacturer name."""
        if not self.config.manufacturer:
            return

        search_query = self._build_search_query([
            ("openfda.manufacturer_name", self.config.manufacturer)
        ])

        async for item in self._paginate_search(search_query):
            yield item

    async def _paginate_search(
        self, search_query: str
    ) -> AsyncGenerator[dict[str, Any], None]:
        """Paginate through search results."""
        logger.info(f"Searching with query: '{search_query}'")
        
        if not search_query or search_query.strip() == "":
            logger.warning("Empty search query - no results will be returned")
            return
            
        skip = 0
        limit = min(100, self.config.max_results)  # openFDA max per request is 100
        total_yielded = 0

        while total_yielded < self.config.max_results:
            params = {
                "search": search_query,
                "limit": limit,
                "skip": skip,
            }

            data = await fetch_json(
                self.client,
                BASE_URL,
                self.rate_limiter,
                self.headers,
                max_retries=self.retries,
                timeout=self.timeout,
                params=params,
            )

            if not data or not isinstance(data, dict):
                break

            results = data.get("results", [])
            if not results:
                break

            for raw_label in results:
                if total_yielded >= self.config.max_results:
                    break
                record = _extract_label(raw_label)
                yield record.model_dump()
                total_yielded += 1

            # Check if there are more results
            meta = data.get("meta", {})
            total_available = meta.get("results", {}).get("total", 0)

            skip += len(results)
            if skip >= total_available:
                break

            # Adjust limit for next page
            remaining = self.config.max_results - total_yielded
            limit = min(100, remaining)
