# RESponder

AI-assisted workflow automation tool for parsing, categorizing, and responding to real estate inquiries.

The project demonstrates practical LLM integration for business process automation, combining email ingestion, structured information extraction, and automated response drafting.

---

## Features

- Automatic email retrieval via OAuth2
- AI-powered inquiry parsing
- Structured information extraction
- Automated response generation
- CSV export and logging
- Configurable workflow pipeline
- Real estate lead triaging

---

## Example Workflow

Incoming client email
↓
Email retrieval via OAuth2
↓
OpenAI-powered parsing and classification
↓
Structured extraction of inquiry details
↓
Response drafting
↓
CSV export / logging

---

## Example Input

```txt
Hello, I’m interested in the property on Westheimer.
My budget is around $450k and I’m hoping to move within 2 months.
Could you send more details?
```

## Example Parsed Output

```json
{
  "intent": "property_inquiry",
  "budget": 450000,
  "timeline": "2 months",
  "location": "Westheimer"
}
```

---

## Tech Stack

- Python
- OpenAI API
- OAuth2
- CSV / JSON pipelines
- Logging & workflow automation

---

## File Structure

### `aouth2_get.py`
Retrieves emails using OAuth2 authentication.

### `aouth2_send.py`
Handles automated response delivery.

### `openai_API.py`
Processes email content using OpenAI models for extraction and response generation.

### `module_out_csv.py`
Exports structured data into CSV format.

### `config.json`
Stores runtime configuration and API settings.

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Usage

Run the email ingestion workflow:

```bash
python aouth2_get.py
```

Check generated logs for workflow status and processing errors.

---

## Motivation

This project explores how LLM-powered workflow automation can reduce repetitive administrative work for small businesses while preserving human oversight for client communication.

---

## Future Improvements

- CRM integrations
- Queue-based asynchronous processing
- Multi-agent orchestration
- Cloud deployment
- Human-in-the-loop approval workflows
- Dashboard & analytics

---

## Disclaimer

This repository is intended as a technical demonstration and workflow automation prototype.
