# codex

This repository provides a simple script to extract meeting information from a Word document and submit the result to a Google Form.

## Requirements

- Python 3.11+
- [`python-docx`](https://python-docx.readthedocs.io/) for reading `.docx` files
- [`requests`](https://docs.python-requests.org/) for posting data to Google Forms

Install the dependencies with:

```bash
pip install python-docx requests
```

## Usage

```bash
python extract_meeting_minutes.py MEETING.docx FORM_URL \
  time=entry.12345 location=entry.23456 chair=entry.34567 \
  opinions=entry.45678 conclusion=entry.56789
```

- `MEETING.docx` is the Word file containing the meeting minutes.
- `FORM_URL` is the Google Form `formResponse` URL.
- Each `field=entry.id` pair maps a field in the meeting record to the corresponding Google Form entry ID.

The script searches the document text for lines starting with:

- `會議時間:` for the meeting time
- `會議地點:` for the location
- `主席:` for the chair
- `委員意見:` for committee opinions
- `會議結論:` for the conclusion

Adjust these keywords if your document uses different labels.
