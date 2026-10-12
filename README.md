# SecureConvert

Privacy-first document conversion website for Europe.

## Features
- DOCX/DOC to PDF
- PPTX/PPT to PDF
- XLSX/XLS to PDF
- No login required
- No user tracking
- Temporary file cleanup
- Ad-ready layout
- Privacy-first design

## Local Setup

### 1. Install LibreOffice

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install libreoffice
```

**macOS:**
```bash
brew install libreoffice
```

**Windows:** Download and install from https://www.libreoffice.org/

### 2. Clone and setup

```bash
git clone https://github.com/Cipher-96/secureconvert.git
cd secureconvert
```

### 3. Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the app

```bash
flask run --host 0.0.0.0 --port 5000
```

### 6. Open in browser

http://localhost:5000

## Project Structure

```
secureconvert/
├── app.py                 # Main Flask app
├── requirements.txt       # Python dependencies
├── templates/
│   ├── base.html         # Layout template
│   ├── index.html        # Home page / converter
│   ├── docx-to-pdf.html  # SEO page
│   ├── pptx-to-pdf.html  # SEO page
│   ├── xlsx-to-pdf.html  # SEO page
│   ├── about.html
│   ├── privacy.html
│   ├── terms.html
│   ├── contact.html
│   ├── faq.html
│   ├── 404.html
│   └── blog/
│       ├── word-to-pdf-guide.html
│       ├── ppt-to-pdf-guide.html
│       └── excel-to-pdf-guide.html
├── static/
│   ├── css/
│   │   └── style.css    # Dark hacker theme
│   └── js/
│       └── app.js       # Upload and conversion logic
```

## How it works

1. User uploads a DOCX/PPTX/XLSX file
2. Flask receives the file and validates it
3. LibreOffice converts to PDF
4. PDF is sent to user for download
5. Temporary files are deleted automatically
6. No user data is stored

## Security features

- Input validation
- File type checking
- Secure filename handling
- Temporary file auto-cleanup
- Security headers
- No database queries
- No personal data collection

## Privacy

This project is GDPR compliant and privacy-first:
- No login required
- No user tracking
- No cookies for tracking
- Temporary files are deleted after conversion
- No personal data stored

## Deployment

### Deploy on Render

1. Push code to GitHub
2. Create account on render.com
3. Connect GitHub repo
4. Add build command: `pip install -r requirements.txt`
5. Add start command: `gunicorn app:app`
6. Add LibreOffice system package
7. Deploy

### Deploy on Railway

1. Push code to GitHub
2. Create account on railway.app
3. Connect GitHub repo
4. Railway auto-detects Python
5. Add environment: `PORT=5000`
6. Deploy

## Monetization

- Google AdSense ads on pages
- Premium features can be added later
- Affiliate links to office tools

## Email

Support: xcipher214@gmail.com

## License

MIT
