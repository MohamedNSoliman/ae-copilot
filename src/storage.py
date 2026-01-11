"""
Storage module for ROI calculators and business cases with versioning.
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict
from .schemas import ROIInputs, ROIOutputs, ExtractedSignals, CRMContext


def sanitize_filename(name: str) -> str:
    """Sanitize company name for use as filename."""
    sanitized = re.sub(r'[^\w\s-]', '', name)
    sanitized = re.sub(r'[-\s]+', '-', sanitized)
    sanitized = sanitized.strip('-')
    return sanitized if sanitized else "company"


def get_next_version(company_dir: Path, company_name: str, file_type: str = "roi") -> int:
    """
    Get the next version number for a company's files.
    
    Args:
        company_dir: Path to the company's directory
        company_name: Sanitized company name
        file_type: "roi" or "business_case"
        
    Returns:
        Next version number (1 if no existing versions)
    """
    if not company_dir.exists():
        return 1
    
    # Pattern depends on file type
    if file_type == "roi":
        pattern = f"{company_name}-v*.json"
    else:
        pattern = f"{company_name}-v*.md"
    
    existing_files = list(company_dir.glob(pattern))
    
    if not existing_files:
        return 1
    
    # Extract version numbers
    versions = []
    version_pattern = re.compile(rf"{re.escape(company_name)}-v(\d+)\.(json|md)")
    
    for file in existing_files:
        match = version_pattern.match(file.name)
        if match:
            versions.append(int(match.group(1)))
    
    if not versions:
        return 1
    
    return max(versions) + 1


def save_roi_calculator(
    company_name: str,
    roi_inputs: ROIInputs,
    roi_outputs: ROIOutputs,
    gong_signals: Optional[ExtractedSignals] = None,
    crm_context: Optional[CRMContext] = None
) -> Path:
    """
    Save ROI calculator with versioning.
    
    Args:
        company_name: Company name
        roi_inputs: ROI inputs
        roi_outputs: ROI outputs
        gong_signals: Optional Gong signals
        crm_context: Optional CRM context
        
    Returns:
        Path to saved file
    """
    outputs_dir = Path("outputs") / "roi_calculators"
    outputs_dir.mkdir(parents=True, exist_ok=True)
    
    sanitized_company = sanitize_filename(company_name)
    company_dir = outputs_dir / sanitized_company
    company_dir.mkdir(exist_ok=True)
    
    version = get_next_version(company_dir, sanitized_company, "roi")
    filename = f"{sanitized_company}-v{version}.json"
    file_path = company_dir / filename
    
    # Prepare data for saving
    data = {
        "company_name": company_name,
        "version": version,
        "created_at": datetime.now().isoformat(),
        "roi_inputs": roi_inputs.model_dump(),
        "roi_outputs": roi_outputs.model_dump(),
        "gong_signals": gong_signals.model_dump() if gong_signals else None,
        "crm_context": crm_context.model_dump() if crm_context else None
    }
    
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2, default=str)
    
    return file_path


def save_business_case(
    company_name: str,
    business_case_content: str,
    version: Optional[int] = None
) -> Path:
    """
    Save business case with versioning.
    
    Args:
        company_name: Company name
        business_case_content: Markdown content
        version: Optional version number (auto-incremented if not provided)
        
    Returns:
        Path to saved file
    """
    outputs_dir = Path("outputs") / "business_cases"
    outputs_dir.mkdir(parents=True, exist_ok=True)
    
    sanitized_company = sanitize_filename(company_name)
    company_dir = outputs_dir / sanitized_company
    company_dir.mkdir(exist_ok=True)
    
    if version is None:
        version = get_next_version(company_dir, sanitized_company, "business_case")
    
    filename = f"{sanitized_company}-v{version}.md"
    file_path = company_dir / filename
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(business_case_content)
    
    return file_path


def get_roi_calculators(company_name: Optional[str] = None) -> List[Dict]:
    """
    Get list of saved ROI calculators.
    
    Args:
        company_name: Optional company name to filter by
        
    Returns:
        List of ROI calculator metadata
    """
    roi_dir = Path("outputs") / "roi_calculators"
    
    if not roi_dir.exists():
        return []
    
    calculators = []
    
    if company_name:
        # Get calculators for specific company
        sanitized = sanitize_filename(company_name)
        company_dir = roi_dir / sanitized
        if company_dir.exists():
            for file in sorted(company_dir.glob("*.json"), reverse=True):
                try:
                    with open(file, 'r') as f:
                        data = json.load(f)
                    calculators.append({
                        "company": data.get("company_name", company_name),
                        "version": data.get("version", 1),
                        "created_at": data.get("created_at", ""),
                        "file_path": str(file),
                        "roi_outputs": data.get("roi_outputs", {})
                    })
                except Exception:
                    continue
    else:
        # Get all calculators
        for company_dir in roi_dir.iterdir():
            if company_dir.is_dir():
                for file in sorted(company_dir.glob("*.json"), reverse=True):
                    try:
                        with open(file, 'r') as f:
                            data = json.load(f)
                        calculators.append({
                            "company": data.get("company_name", company_dir.name),
                            "version": data.get("version", 1),
                            "created_at": data.get("created_at", ""),
                            "file_path": str(file),
                            "roi_outputs": data.get("roi_outputs", {})
                        })
                    except Exception:
                        continue
    
    return calculators


def get_business_cases(company_name: Optional[str] = None) -> List[Dict]:
    """
    Get list of saved business cases.
    
    Args:
        company_name: Optional company name to filter by
        
    Returns:
        List of business case metadata
    """
    cases_dir = Path("outputs") / "business_cases"
    
    if not cases_dir.exists():
        return []
    
    cases = []
    
    if company_name:
        # Get cases for specific company
        sanitized = sanitize_filename(company_name)
        company_dir = cases_dir / sanitized
        if company_dir.exists():
            for file in sorted(company_dir.glob("*.md"), reverse=True):
                try:
                    # Extract version from filename
                    match = re.match(rf"{re.escape(sanitized)}-v(\d+)\.md", file.name)
                    version = int(match.group(1)) if match else 1
                    
                    stat = file.stat()
                    cases.append({
                        "company": company_name,
                        "version": version,
                        "created_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        "file_path": str(file)
                    })
                except Exception:
                    continue
    else:
        # Get all cases
        for company_dir in cases_dir.iterdir():
            if company_dir.is_dir():
                for file in sorted(company_dir.glob("*.md"), reverse=True):
                    try:
                        # Extract company and version from filename
                        match = re.match(r"(.+)-v(\d+)\.md", file.name)
                        if match:
                            company = match.group(1).replace("-", " ")
                            version = int(match.group(2))
                            
                            stat = file.stat()
                            cases.append({
                                "company": company,
                                "version": version,
                                "created_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                                "file_path": str(file)
                            })
                    except Exception:
                        continue
    
    return cases


def load_roi_calculator(file_path: str) -> Dict:
    """
    Load ROI calculator from file.
    
    Args:
        file_path: Path to ROI calculator JSON file
        
    Returns:
        Dictionary with ROI data
    """
    with open(file_path, 'r') as f:
        return json.load(f)


def load_business_case(file_path: str) -> str:
    """
    Load business case from file.
    
    Args:
        file_path: Path to business case Markdown file
        
    Returns:
        Business case content as string
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def get_companies() -> List[str]:
    """Get list of all companies with saved ROI calculators or business cases."""
    companies = set()
    
    # From ROI calculators
    roi_dir = Path("outputs") / "roi_calculators"
    if roi_dir.exists():
        for company_dir in roi_dir.iterdir():
            if company_dir.is_dir():
                # Try to get company name from first file
                for file in company_dir.glob("*.json"):
                    try:
                        with open(file, 'r') as f:
                            data = json.load(f)
                            companies.add(data.get("company_name", company_dir.name))
                            break
                    except Exception:
                        companies.add(company_dir.name.replace("-", " "))
                        break
    
    # From business cases
    cases_dir = Path("outputs") / "business_cases"
    if cases_dir.exists():
        for company_dir in cases_dir.iterdir():
            if company_dir.is_dir():
                companies.add(company_dir.name.replace("-", " "))
    
    return sorted(list(companies))
