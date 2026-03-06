# FDA Drug Labels Scraper

> **Extract FDA drug labeling data from openFDA -- indications, dosage, warnings, interactions, and more. No API key required.**

Search and retrieve structured drug label information from the FDA's openFDA database. Get comprehensive labeling data for prescription drugs, OTC medications, biologics, and more.

---

## What does it do?

FDA Drug Labels Scraper queries the openFDA Drug Labeling API and returns structured data about FDA-approved drug labels. It extracts labeling sections including indications, dosage, contraindications, warnings, adverse reactions, drug interactions, and pharmacology into clean, normalized JSON. Returns consistent output -- ready for analysis, pharma pipelines, or consumption by AI agents via MCP.

**Use cases:**

- **Pharma competitive intelligence** -- analyze competitor drug labels, indications, and warnings
- **Drug safety monitoring** -- track boxed warnings, contraindications, and adverse reactions
- **Medical research** -- find drugs by indication, ingredient, or mechanism of action
- **Healthcare applications** -- build drug interaction checkers, dosage guides, or patient info tools
- **Regulatory compliance** -- monitor label changes and updates
- **AI agent tooling** -- expose as an MCP tool so AI agents can query drug information in real time

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

## Resources

- [openFDA Drug Labeling API](https://open.fda.gov/apis/drug/label/)
- [DailyMed](https://dailymed.nlm.nih.gov/) -- Full drug labels with images
- [FDA Drug Databases](https://www.fda.gov/drugs/drug-approvals-and-databases)
- [Apify Documentation](https://docs.apify.com/)

---

## License

This actor is provided under the MIT License. The underlying data is from the FDA and is in the public domain.
