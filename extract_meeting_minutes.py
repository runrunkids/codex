import re
import sys
from dataclasses import dataclass
from typing import Optional

# External dependencies
try:
    from docx import Document
except ImportError:  # pragma: no cover - docx not installed
    Document = None

try:
    import requests
except ImportError:  # pragma: no cover - requests not installed
    requests = None


@dataclass
class MeetingRecord:
    time: Optional[str] = None
    location: Optional[str] = None
    chair: Optional[str] = None
    opinions: Optional[str] = None
    conclusion: Optional[str] = None


def load_docx_text(path: str) -> str:
    """Load text from a docx file."""
    if Document is None:
        raise ImportError("python-docx must be installed to read .docx files")
    document = Document(path)
    return "\n".join(para.text for para in document.paragraphs)


def parse_meeting_record(text: str) -> MeetingRecord:
    """Extract meeting fields from text using simple regex patterns."""
    record = MeetingRecord()
    patterns = {
        'time': r"會議時間[:：]\s*(.*)",
        'location': r"會議地點[:：]\s*(.*)",
        'chair': r"主席[:：]\s*(.*)",
        'opinions': r"委員意見[:：]\s*(.*)",
        'conclusion': r"會議結論[:：]\s*(.*)",
    }
    for field, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            setattr(record, field, match.group(1).strip())
    return record


def submit_to_google_form(form_url: str, entry_mapping: dict, record: MeetingRecord) -> None:
    """Submit the meeting record to a Google Form."""
    if requests is None:
        raise ImportError("The requests package is required to submit to Google Forms")

    payload = {}
    for field, entry in entry_mapping.items():
        value = getattr(record, field)
        if value is not None:
            payload[entry] = value

    response = requests.post(form_url, data=payload)
    response.raise_for_status()


def main(docx_path: str, form_url: str, entry_mapping: dict) -> None:
    text = load_docx_text(docx_path)
    record = parse_meeting_record(text)
    submit_to_google_form(form_url, entry_mapping, record)


if __name__ == "__main__":  # pragma: no cover - simple CLI
    if len(sys.argv) < 3:
        print("Usage: python extract_meeting_minutes.py <docx-path> <form-url> [field=entry...]")
        sys.exit(1)
    docx_path = sys.argv[1]
    form_url = sys.argv[2]
    mapping = {}
    for item in sys.argv[3:]:
        if '=' in item:
            key, value = item.split('=', 1)
            mapping[key] = value
    main(docx_path, form_url, mapping)
