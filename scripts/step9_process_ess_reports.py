"""
Step 9: Process ESS Reports (PDF, Excel, Word, CSV)
Extracts text from ESS reports and adds to knowledge base

Usage: python scripts/step9_process_ess_reports.py
"""

import os
import json
import pandas as pd
from datetime import datetime

# For PDF reading (install: pip install PyPDF2)
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    print("⚠ PyPDF2 not installed. PDF processing disabled.")
    print("Install with: pip install PyPDF2")
    PDF_AVAILABLE = False

# For Word reading (install: pip install python-docx)
try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    print("⚠ python-docx not installed. Word processing disabled.")
    print("Install with: pip install python-docx")
    DOCX_AVAILABLE = False


def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    if not PDF_AVAILABLE:
        return None
    
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
    except Exception as e:
        print(f"✗ Error reading PDF {pdf_path}: {e}")
        return None


def extract_text_from_docx(docx_path):
    """Extract text from Word document"""
    if not DOCX_AVAILABLE:
        return None
    
    try:
        doc = Document(docx_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        print(f"✗ Error reading DOCX {docx_path}: {e}")
        return None


def extract_data_from_excel(excel_path):
    """Extract data from Excel file"""
    try:
        # Read all sheets
        excel_file = pd.ExcelFile(excel_path)
        all_data = []
        
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(excel_path, sheet_name=sheet_name)
            
            # Convert to text representation
            text = f"Sheet: {sheet_name}\n"
            text += df.to_string(index=False)
            all_data.append(text)
        
        return "\n\n".join(all_data)
    except Exception as e:
        print(f"✗ Error reading Excel {excel_path}: {e}")
        return None


def extract_data_from_csv(csv_path):
    """Extract data from CSV file"""
    try:
        df = pd.read_csv(csv_path)
        return df.to_string(index=False)
    except Exception as e:
        print(f"✗ Error reading CSV {csv_path}: {e}")
        return None


def chunk_text(text, max_length=1000):
    """Split long text into chunks"""
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        current_length += len(word) + 1
        if current_length > max_length:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_length = len(word)
        else:
            current_chunk.append(word)
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks


def process_ess_reports(reports_dir="data/raw/ess_reports"):
    """Process all ESS reports and create documents"""
    
    print("=" * 60)
    print("PROCESSING ESS REPORTS")
    print("=" * 60)
    
    if not os.path.exists(reports_dir):
        print(f"✗ Directory not found: {reports_dir}")
        print(f"Creating directory...")
        os.makedirs(reports_dir)
        print(f"\n📁 Please add your ESS reports to: {reports_dir}")
        print("Supported formats: PDF, Excel (.xlsx), Word (.docx), CSV")
        return []
    
    documents = []
    files = os.listdir(reports_dir)
    
    if not files:
        print(f"\n⚠ No files found in {reports_dir}")
        print("Please add ESS reports (PDF, Excel, Word, CSV)")
        return []
    
    print(f"\nFound {len(files)} files")
    print("-" * 60)
    
    for filename in files:
        filepath = os.path.join(reports_dir, filename)
        
        if not os.path.isfile(filepath):
            continue
        
        print(f"\nProcessing: {filename}")
        
        # Detect file type and extract content
        text_content = None
        file_type = None
        
        if filename.endswith('.pdf'):
            file_type = "PDF Report"
            text_content = extract_text_from_pdf(filepath)
        
        elif filename.endswith('.xlsx') or filename.endswith('.xls'):
            file_type = "Excel Data"
            text_content = extract_data_from_excel(filepath)
        
        elif filename.endswith('.docx') or filename.endswith('.doc'):
            file_type = "Word Document"
            text_content = extract_text_from_docx(filepath)
        
        elif filename.endswith('.csv'):
            file_type = "CSV Data"
            text_content = extract_data_from_csv(filepath)
        
        else:
            print(f"  ⊘ Unsupported file type")
            continue
        
        if not text_content or len(text_content.strip()) < 100:
            print(f"  ✗ Could not extract content or content too short")
            continue
        
        # Detect report type from filename
        report_type = "General Report"
        if any(word in filename.lower() for word in ['weekly', 'week']):
            report_type = "Weekly Report"
        elif any(word in filename.lower() for word in ['monthly', 'month']):
            report_type = "Monthly Report"
        elif any(word in filename.lower() for word in ['quarterly', 'quarter', 'q1', 'q2', 'q3', 'q4']):
            report_type = "Quarterly Report"
        elif any(word in filename.lower() for word in ['annual', 'yearly', 'year']):
            report_type = "Annual Report"
        
        # Chunk long documents
        chunks = chunk_text(text_content, max_length=1000)
        
        print(f"  ✓ Extracted {len(text_content)} characters")
        print(f"  ✓ Split into {len(chunks)} chunks")
        print(f"  ✓ Type: {report_type}")
        
        # Create document for each chunk
        for i, chunk in enumerate(chunks, 1):
            doc = {
                'text': chunk,
                'metadata': {
                    'source': 'ESS',
                    'filename': filename,
                    'file_type': file_type,
                    'report_type': report_type,
                    'chunk': f"{i}/{len(chunks)}",
                    'processed_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            }
            documents.append(doc)
    
    print("\n" + "=" * 60)
    print(f"✓ PROCESSED {len(files)} FILES")
    print(f"✓ CREATED {len(documents)} DOCUMENT CHUNKS")
    print("=" * 60)
    
    return documents


def save_ess_documents(documents, output_file="data/processed/ess_documents.jsonl"):
    """Save ESS documents to JSONL file"""
    
    if not documents:
        print("\n⚠ No documents to save")
        return
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for doc in documents:
            f.write(json.dumps(doc, ensure_ascii=False) + '\n')
    
    print(f"\n✓ Saved {len(documents)} documents to {output_file}")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("STEP 9: PROCESS ESS REPORTS")
    print("=" * 60)
    
    # Check dependencies
    print("\nChecking dependencies...")
    if not PDF_AVAILABLE:
        print("⚠ Install PyPDF2 for PDF support: pip install PyPDF2")
    if not DOCX_AVAILABLE:
        print("⚠ Install python-docx for Word support: pip install python-docx")
    
    if not PDF_AVAILABLE and not DOCX_AVAILABLE:
        print("\n✗ Please install required packages:")
        print("  pip install PyPDF2 python-docx")
        exit(1)
    
    print("✓ Dependencies OK\n")
    
    # Process reports
    documents = process_ess_reports()
    
    # Save documents
    if documents:
        save_ess_documents(documents)
        
        print("\n" + "=" * 60)
        print("NEXT STEPS:")
        print("=" * 60)
        print("1. Run: python scripts/step10_rebuild_vector_db.py")
        print("   (This will add ESS reports to the existing database)")
        print("\n2. Run: python -m streamlit run app.py")
        print("   (Your chatbot will now include ESS reports!)")
        print("=" * 60)
    else:
        print("\n📁 Add ESS reports to: data/raw/ess_reports/")
        print("Then run this script again.")
