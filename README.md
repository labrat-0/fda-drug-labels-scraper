# FDA Drug Labels Scraper

> **Extract FDA drug labeling data from openFDA -- indications, dosage, warnings, interactions, and more. No API key required.**

Search and retrieve structured drug label information from the FDA's openFDA database. Get comprehensive labeling data for prescription drugs, OTC medications, biologics, and more.

---

## What does it do?

FDA Drug Labels Scraper queries the openFDA Drug Labeling API and returns structured data about FDA-approved drug labels. It extracts labeling sections including indications, dosage, contraindications, warnings, adverse reactions, drug interactions, and pharmacology into clean, normalized JSON. Returns consistent output -- ready for analysis, pharma pipelines, or consumption by AI agents via MCP.

## 👥 Who Uses This

### 💊 Pharma Competitive Intelligence Teams

You need to know what's on a competitor's label — which indications they've claimed, what warnings they carry, what dosage regimens are approved. FDA drug labels are the ground truth for what a drug is officially approved to do. This actor pulls the full structured label so you can compare across products without manual PDF review.

```json
{
    "mode": "search_labels",
    "query": "GLP-1 obesity",
    "productType": "HUMAN PRESCRIPTION DRUG",
    "maxResults": 50
}
```

Use the `indications_and_usage`, `warnings_and_precautions`, and `contraindications` fields for head-to-head label comparisons. Combine with FDA Adverse Events for a full safety profile picture.

---

### 🔬 Pharmacovigilance and Drug Safety Teams

You're monitoring boxed warnings, contraindications, and adverse reactions in drug labels — either for your own products or for safety surveillance across a therapeutic area. Label text changes are regulatory events worth tracking.

```json
{
    "mode": "search_labels",
    "query": "metformin",
    "productType": "HUMAN PRESCRIPTION DRUG",
    "maxResults": 100
}
```

Pull `boxed_warning`, `warnings`, `adverse_reactions`, and `drug_interactions` fields. Schedule runs to detect label updates over time — a new boxed warning or contraindication is a material change for any downstream user of that data.

---

### 🏗️ Healthcare App and Platform Developers

You're building a drug interaction checker, a clinical decision support tool, a patient information app, or a formulary management system. FDA label data is authoritative, public domain, and structured — ideal as a backend data source without licensing fees.

```json
{
    "mode": "get_label",
    "applicationNumber": "NDA021977"
}
```

The `drug_interactions`, `dosage_and_administration`, `contraindications`, and `warnings_and_precautions` fields map directly to the display sections most clinical apps need. No licensing, no subscription — FDA data is public domain.

---

### 📋 Regulatory Affairs and Medical Writers

You need to reference competitor labels for regulatory submissions, prepare label comparisons for advisory committees, or track how labels in your therapeutic area evolve over time. Pulling 50 labels by indication keyword takes seconds instead of hours on DailyMed.

```json
{
    "mode": "search_labels",
    "query": "PCSK9 inhibitor hyperlipidemia",
    "productType": "HUMAN PRESCRIPTION DRUG",
    "maxResults": 20
}
```

Export to CSV for tabular comparison of warnings, contraindications, and dosing across approved products in a class.

---

### 🤖 AI/LLM Engineers and Medical AI Builders

You're grounding a medical AI assistant in authoritative drug information — not hallucinated text, but the actual FDA-approved label. Drug label data as a RAG source or MCP tool gives your agent access to dosing, interactions, and warnings at query time.

**MCP tool config:**

```json
{
    "mcpServers": {
        "fda-drug-labels": {
            "url": "https://mcp.apify.com?tools=labrat011/fda-drug-labels-scraper",
            "headers": {
                "Authorization": "Bearer <APIFY_TOKEN>"
            }
        }
    }
}
```

Combine with Clinical Trials Scraper and PubMed Scraper in the same MCP config to give your agent the full FDA + literature + trial data stack.

---

---

## Input

Choose a scraping mode and provide your search filters.

### Mode 1: Search Labels

Search for drug labels by keyword, drug name, active ingredient, or manufacturer.

```json
{
    "mode": "search_labels",
    "query": "diabetes",
    "productType": "HUMAN PRESCRIPTION DRUG",
    "maxResults": 100
}
```

Search by active ingredient:

```json
{
    "mode": "search_labels",
    "activeIngredient": "metformin",
    "maxResults": 50
}
```

### Mode 2: Get Label

Look up a specific drug label by its Set ID.

```json
{
    "mode": "get_label",
    "setId": "7f5c842e-2f3a-4b1c-9d8e-1234567890ab"
}
```

### Mode 3: Search by Drug

Search labels by drug/brand name or active ingredient.

```json
{
    "mode": "search_by_drug",
    "drugName": "Lipitor",
    "maxResults": 10
}
```

```json
{
    "mode": "search_by_drug",
    "activeIngredient": "atorvastatin",
    "maxResults": 25
}
```

### Mode 4: Search by Manufacturer

Find all drug labels from a specific manufacturer.

```json
{
    "mode": "search_by_manufacturer",
    "manufacturer": "Pfizer",
    "maxResults": 100
}
```

---

## Output

Each drug label record includes:

| Field | Description |
|-------|-------------|
| `set_id` | FDA Set ID (unique identifier) |
| `brand_name` | Brand/trade name |
| `generic_name` | Generic drug name |
| `manufacturer_name` | Manufacturer or labeler |
| `product_type` | Type (prescription, OTC, etc.) |
| `route` | Routes of administration |
| `substance_name` | Active ingredients |
| `product_ndc` | NDC codes |
| `indications_and_usage` | Approved indications |
| `dosage_and_administration` | Dosing instructions |
| `contraindications` | When not to use |
| `warnings_and_cautions` | Safety warnings |
| `boxed_warning` | Black box warnings |
| `adverse_reactions` | Side effects |
| `drug_interactions` | Interaction information |
| `clinical_pharmacology` | How the drug works |
| `mechanism_of_action` | Mechanism details |
| `pharmacokinetics` | Absorption, distribution, metabolism |
| `pregnancy` | Pregnancy information |
| `label_url` | Link to full label on DailyMed |

### Example output

```json
{
    "schema_version": "1.0",
    "type": "drug_label",
    "set_id": "7f5c842e-2f3a-4b1c-9d8e-1234567890ab",
    "brand_name": "LIPITOR",
    "generic_name": "ATORVASTATIN CALCIUM",
    "manufacturer_name": "Pfizer Laboratories Div Pfizer Inc",
    "product_type": "HUMAN PRESCRIPTION DRUG",
    "route": ["ORAL"],
    "substance_name": ["ATORVASTATIN CALCIUM"],
    "indications_and_usage": ["Therapy with LIPITOR should be a component of multiple-risk-factor intervention..."],
    "contraindications": ["Active liver disease or unexplained persistent elevations of serum transaminases..."],
    "boxed_warning": [],
    "adverse_reactions": ["The following serious adverse reactions are discussed in greater detail..."],
    "drug_interactions": ["Strong CYP3A4 Inhibitors: Atorvastatin is metabolized by CYP3A4..."],
    "label_url": "https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=7f5c842e-2f3a-4b1c-9d8e-1234567890ab"
}
```

---

## Filters

| Filter | Description | Example |
|--------|-------------|---------|
| `query` | General search term | `"headache"` |
| `drugName` | Brand name | `"Advil"` |
| `activeIngredient` | Active ingredient | `"ibuprofen"` |
| `manufacturer` | Company name | `"Johnson & Johnson"` |
| `productType` | Product category | `"HUMAN PRESCRIPTION DRUG"` |
| `route` | Administration route | `"ORAL"`, `"INTRAVENOUS"` |

### Product types

- `HUMAN PRESCRIPTION DRUG`
- `HUMAN OTC DRUG`
- `PLASMA DERIVATIVE`
- `VACCINE`
- `CELLULAR THERAPY`
- `STANDARDIZED ALLERGENIC`
- `NON-STANDARDIZED ALLERGENIC`

### Can I combine filters?

Yes. All filters are AND-combined. For example, search for oral prescription drugs containing metformin from a specific manufacturer.

---

## Integrations

### Apify API

```bash
curl "https://api.apify.com/v2/acts/labrat011~fda-drug-labels-scraper/runs" \
  -X POST \
  -H "Authorization: Bearer <APIFY_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "search_by_drug",
    "drugName": "Humira",
    "maxResults": 10
  }'
```

### Python

```python
from apify_client import ApifyClient

client = ApifyClient("<APIFY_TOKEN>")

run = client.actor("labrat011/fda-drug-labels-scraper").call(run_input={
    "mode": "search_labels",
    "activeIngredient": "adalimumab",
    "maxResults": 25
})

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(f"{item['brand_name']}: {item['indications_and_usage'][0][:100]}...")
```

### JavaScript

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<APIFY_TOKEN>' });

const run = await client.actor('labrat011/fda-drug-labels-scraper').call({
    mode: 'search_by_manufacturer',
    manufacturer: 'AbbVie',
    maxResults: 50
});

const { items } = await client.dataset(run.defaultDatasetId).listItems();
items.forEach(item => {
    console.log(`${item.brand_name} - ${item.generic_name}`);
});
```

---

## MCP Integration

This actor works as an MCP tool through Apify's hosted MCP server. No custom server needed.

- **Endpoint:** `https://mcp.apify.com?tools=labrat011/fda-drug-labels-scraper`
- **Auth:** `Authorization: Bearer <APIFY_TOKEN>`
- **Transport:** Streamable HTTP
- **Works with:** Claude Desktop, Cursor, VS Code, Windsurf, Warp, Gemini CLI

**Example MCP config (Claude Desktop / Cursor):**

```json
{
    "mcpServers": {
        "fda-drug-labels-scraper": {
            "url": "https://mcp.apify.com?tools=labrat011/fda-drug-labels-scraper",
            "headers": {
                "Authorization": "Bearer <APIFY_TOKEN>"
            }
        }
    }
}
```

AI agents can use this actor to search drug labels, look up drug information, check interactions, and retrieve safety data -- all as a callable MCP tool.

---

## Limits and pricing

- **Free tier:** 25 results per run
- **Paid tier:** Up to 1,000 results per run
- **Rate limiting:** Built-in rate limiting respects openFDA API limits
- **No API key required:** Uses the public openFDA API

---

## FAQ

### What data source does this use?

This actor queries the [openFDA Drug Labeling API](https://open.fda.gov/apis/drug/label/), which contains drug labels submitted to the FDA in Structured Product Labeling (SPL) format. The data is updated weekly.

### Is the data up to date?

The openFDA database is updated weekly with new and revised drug labels. The `effective_time` field indicates when each label was last updated.

### Can I search for OTC drugs?

Yes. Use `productType: "HUMAN OTC DRUG"` to filter for over-the-counter medications. OTC labels include additional fields like `purpose`, `do_not_use`, `ask_doctor`, and `stop_use`.

### What's the difference between brand_name and generic_name?

`brand_name` is the trade name (e.g., "Advil"), while `generic_name` is the nonproprietary name (e.g., "ibuprofen"). Some labels may have multiple brand names for the same generic.

### How do I find drug interactions?

The `drug_interactions` field contains interaction information from the label. Search for a specific drug and examine this field, or use the general `query` search with interaction-related terms.

### Is this data official?

Yes. This data comes directly from the FDA's openFDA API, which contains official drug labeling submitted to the FDA. However, labels may not always reflect the most current information -- always verify critical information with official FDA sources.

---

## 🔗 Related Actors

| Actor | What it does | Pairs well when... |
|-------|-------------|---------------------|
| [FDA Adverse Events Scraper](https://apify.com/labrat011/fda-adverse-events-scraper) | FAERS post-market safety reports | Cross-reference label warnings with real-world adverse event signals |
| [FDA Orange Book Scraper](https://apify.com/labrat011/fda-orange-book-scraper) | Patent, exclusivity, and generic data | Check approval and patent status for labeled drugs |
| [Clinical Trials Scraper](https://apify.com/labrat011/clinical-trials-scraper) | ClinicalTrials.gov study data | Find active trials for drugs or conditions in the label |
| [PubMed Scraper](https://apify.com/labrat011/pubmed-scraper) | 35M+ biomedical abstracts from NCBI | Find supporting literature for label claims and safety data |
| [NPI Provider Contact Finder](https://apify.com/labrat011/npi-provider-contact-finder) | Healthcare provider directory | Find prescribers for drugs in a specific therapeutic area |

---

## Resources

- [openFDA Drug Labeling API](https://open.fda.gov/apis/drug/label/)
- [DailyMed](https://dailymed.nlm.nih.gov/) -- Full drug labels with images
- [FDA Drug Databases](https://www.fda.gov/drugs/drug-approvals-and-databases)
- [Apify Documentation](https://docs.apify.com/)

---

## License

This actor is provided under the MIT License. The underlying data is from the FDA and is in the public domain.
