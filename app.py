import os
import shutil
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

from flask import Flask, abort, jsonify, render_template, request, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.getenv('SECRET_KEY', 'change-me-in-production'),
    MAX_CONTENT_LENGTH=25 * 1024 * 1024,
)

ALLOWED_EXTENSIONS = {
    'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx'
}
ALLOWED_MIME_TYPES = {
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-powerpoint',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
}


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def cleanup_temp_dir(path: str):
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)


def convert_office_to_pdf(input_path: str, output_dir: str):
    command = ['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', output_dir, input_path]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f'Conversion failed: {result.stderr or result.stdout}')

    filename = Path(input_path).stem
    pdf_path = os.path.join(output_dir, f'{filename}.pdf')
    if not os.path.exists(pdf_path):
        for file in os.listdir(output_dir):
            if file.lower().endswith('.pdf'):
                pdf_path = os.path.join(output_dir, file)
                break
    if not os.path.exists(pdf_path):
        raise FileNotFoundError('PDF output was not created.')
    return pdf_path


@app.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    response.headers['Content-Security-Policy'] = "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; connect-src 'self';"
    return response


@app.route('/')
def home():
    return render_template('index.html', page_title='SecureConvert | Convert Office files to PDF')


@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in request.'}), 400

    uploaded = request.files['file']
    if uploaded.filename == '':
        return jsonify({'error': 'No selected file.'}), 400

    filename = secure_filename(uploaded.filename)
    if not allowed_file(filename):
        return jsonify({'error': 'Unsupported file type. Please upload DOC, DOCX, PPT, PPTX, XLS, or XLSX.'}), 400

    file_ext = filename.rsplit('.', 1)[1].lower()
    mime_guess = request.mimetype
    if mime_guess and mime_guess not in ALLOWED_MIME_TYPES:
        if file_ext not in {'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx'}:
            return jsonify({'error': 'Invalid file detected.'}), 400

    temp_dir = tempfile.mkdtemp(prefix='secureconvert_')
    try:
        input_path = os.path.join(temp_dir, filename)
        uploaded.save(input_path)

        pdf_path = convert_office_to_pdf(input_path, temp_dir)
        if not os.path.exists(pdf_path):
            raise FileNotFoundError('PDF file was not created.')

        download_name = f'{Path(filename).stem}.pdf'
        response = send_file(pdf_path, as_attachment=True, download_name=download_name)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500
    finally:
        cleanup_temp_dir(temp_dir)


@app.route('/docx-to-pdf')
def docx_to_pdf():
    return render_template('docx-to-pdf.html', page_title='DOCX to PDF')


@app.route('/pptx-to-pdf')
def pptx_to_pdf():
    return render_template('pptx-to-pdf.html', page_title='PPTX to PDF')


@app.route('/xlsx-to-pdf')
def xlsx_to_pdf():
    return render_template('xlsx-to-pdf.html', page_title='XLSX to PDF')


@app.route('/about')
def about():
    return render_template('about.html', page_title='About SecureConvert')


@app.route('/privacy')
def privacy():
    return render_template('privacy.html', page_title='Privacy Policy')


@app.route('/terms')
def terms():
    return render_template('terms.html', page_title='Terms of Service')


@app.route('/contact')
def contact():
    return render_template('contact.html', page_title='Contact')


@app.route('/faq')
def faq():
    return render_template('faq.html', page_title='FAQ')


@app.route('/blog/word-to-pdf')
def blog_word_to_pdf():
    return render_template('blog/word-to-pdf-guide.html', page_title='How to convert Word to PDF')


@app.route('/blog/ppt-to-pdf')
def blog_ppt_to_pdf():
    return render_template('blog/ppt-to-pdf-guide.html', page_title='How to convert PowerPoint to PDF')


@app.route('/blog/excel-to-pdf')
def blog_excel_to_pdf():
    return render_template('blog/excel-to-pdf-guide.html', page_title='How to convert Excel to PDF')


@app.route('/robots.txt')
def robots():
    return "User-agent: *\nAllow: /\nSitemap: https://secureconvert.eu/sitemap.xml\n", 200, {'Content-Type': 'text/plain; charset=utf-8'}


@app.route('/sitemap.xml')
def sitemap():
    routes = [
        '/', '/docx-to-pdf', '/pptx-to-pdf', '/xlsx-to-pdf', '/about', '/privacy', '/terms', '/contact', '/faq',
        '/blog/word-to-pdf', '/blog/ppt-to-pdf', '/blog/excel-to-pdf'
    ]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for route in routes:
        xml += f'  <url><loc>https://secureconvert.eu{route}</loc></url>\n'
    xml += '</urlset>\n'
    return xml, 200, {'Content-Type': 'application/xml; charset=utf-8'}


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', page_title='Page not found'), 404


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
