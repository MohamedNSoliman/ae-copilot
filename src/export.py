"""
Export functionality for Narrative Pack generation.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple
from .schemas import NarrativePack, ROIInputs, ROIOutputs, ExtractedSignals, CRMContext


def create_narrative_pack(
    roi_inputs: ROIInputs,
    roi_outputs: ROIOutputs,
    gong_signals: Optional[ExtractedSignals] = None,
    crm_context: Optional[CRMContext] = None,
    account_name: Optional[str] = None
) -> NarrativePack:
    """
    Create a narrative pack from all available data.
    
    Args:
        roi_inputs: ROI calculation inputs
        roi_outputs: ROI calculation outputs
        gong_signals: Extracted Gong signals (optional)
        crm_context: CRM context (optional)
        account_name: Account name for metadata
        
    Returns:
        NarrativePack ready for export
    """
    metadata = {
        "generated_at": datetime.now().isoformat(),
        "data_sources": [],
        "version": "1.0"
    }
    
    if gong_signals:
        metadata["data_sources"].append("gong")
    if crm_context:
        metadata["data_sources"].append("crm")
    if account_name:
        metadata["account_name"] = account_name
    
    return NarrativePack(
        roi_inputs=roi_inputs,
        roi_outputs=roi_outputs,
        gong_signals=gong_signals,
        crm_context=crm_context,
        metadata=metadata
    )


def export_narrative_pack(pack: NarrativePack, account_name: str, output_dir: Path = None) -> Tuple[Path, Path]:
    """
    Export narrative pack to JSON and Markdown files.
    
    Args:
        pack: NarrativePack to export
        account_name: Account name for filename
        output_dir: Output directory (defaults to outputs/)
        
    Returns:
        Tuple of (json_path, markdown_path)
    """
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "outputs"
    
    output_dir.mkdir(exist_ok=True)
    
    # Sanitize account name for filename
    safe_name = account_name.replace(" ", "_").replace("/", "_").lower()
    
    # Export JSON
    json_path = output_dir / f"{safe_name}_context.json"
    with open(json_path, 'w') as f:
        json.dump(pack.model_dump(), f, indent=2, default=str)
    
    # Export Markdown
    markdown_path = output_dir / f"{safe_name}_context.md"
    markdown_content = _generate_markdown(pack)
    with open(markdown_path, 'w') as f:
        f.write(markdown_content)
    
    return json_path, markdown_path


def _generate_markdown(pack: NarrativePack) -> str:
    """Generate human-readable Markdown from narrative pack."""
    lines = []
    
    lines.append("# Narrative Pack")
    lines.append("")
    lines.append(f"**Generated:** {pack.metadata.get('generated_at', 'Unknown')}")
    lines.append(f"**Data Sources:** {', '.join(pack.metadata.get('data_sources', [])) or 'None'}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # ROI Inputs
    lines.append("## ROI Inputs")
    lines.append("")
    lines.append(f"- **Team Size (Engineering):** {pack.roi_inputs.team_size_engineering}")
    lines.append(f"- **Fully Loaded Cost per Engineer:** ${pack.roi_inputs.fully_loaded_cost_per_engineer:,.2f}")
    lines.append(f"- **Hours Saved per Engineer per Week:** {pack.roi_inputs.hours_saved_per_engineer_per_week}")
    lines.append(f"- **Adoption Rate:** {pack.roi_inputs.adoption_rate * 100:.1f}%")
    lines.append(f"- **Weeks per Year:** {pack.roi_inputs.weeks_per_year}")
    lines.append(f"- **Cursor Annual Cost:** ${pack.roi_inputs.cursor_annual_cost:,.2f}")
    lines.append("")
    
    # ROI Outputs
    lines.append("## ROI Outputs")
    lines.append("")
    lines.append(f"- **Annual Hours Saved:** {pack.roi_outputs.annual_hours_saved:,.2f}")
    lines.append(f"- **Annual Cost Saved:** ${pack.roi_outputs.annual_cost_saved:,.2f}")
    lines.append(f"- **Net Annual Value:** ${pack.roi_outputs.net_annual_value:,.2f}")
    if pack.roi_outputs.payback_months != float('inf'):
        lines.append(f"- **Payback Period:** {pack.roi_outputs.payback_months:.2f} months")
    else:
        lines.append(f"- **Payback Period:** N/A (no savings)")
    lines.append("")
    
    # Gong Signals
    if pack.gong_signals:
        lines.append("---")
        lines.append("")
        lines.append("## Gong Signals")
        lines.append("")
        if pack.gong_signals.team_size_engineering:
            lines.append(f"- **Team Size:** {pack.gong_signals.team_size_engineering}")
        if pack.gong_signals.current_tooling:
            lines.append(f"- **Current Tooling:** {', '.join(pack.gong_signals.current_tooling)}")
        if pack.gong_signals.hours_saved_per_engineer_per_week:
            lines.append(f"- **Hours Saved per Week:** {pack.gong_signals.hours_saved_per_engineer_per_week}")
        if pack.gong_signals.pain_points:
            lines.append(f"- **Pain Points:** {', '.join(pack.gong_signals.pain_points)}")
        if pack.gong_signals.initiatives:
            lines.append(f"- **Initiatives:** {', '.join(pack.gong_signals.initiatives)}")
        lines.append(f"- **Buying Stage:** {pack.gong_signals.buying_stage}")
        if pack.gong_signals.notes:
            lines.append(f"- **Notes:** {pack.gong_signals.notes}")
        
        if pack.gong_signals.evidence:
            lines.append("")
            lines.append("### Evidence")
            lines.append("")
            for ev in pack.gong_signals.evidence:
                lines.append(f"- **{ev.field_name}** (timestamp: {ev.timestamp_seconds or 'N/A'}s):")
                lines.append(f"  > {ev.quote}")
                lines.append("")
        lines.append("")
    
    # CRM Context
    if pack.crm_context:
        lines.append("---")
        lines.append("")
        lines.append("## CRM Context")
        lines.append("")
        if pack.crm_context.account_name:
            lines.append(f"- **Account Name:** {pack.crm_context.account_name}")
        if pack.crm_context.domain:
            lines.append(f"- **Domain:** {pack.crm_context.domain}")
        if pack.crm_context.industry:
            lines.append(f"- **Industry:** {pack.crm_context.industry}")
        if pack.crm_context.employee_count:
            lines.append(f"- **Employee Count:** {pack.crm_context.employee_count:,}")
        if pack.crm_context.region:
            lines.append(f"- **Region:** {pack.crm_context.region}")
        
        if pack.crm_context.key_contacts:
            lines.append("")
            lines.append("### Key Contacts")
            lines.append("")
            for contact in pack.crm_context.key_contacts:
                lines.append(f"- **{contact.name or 'Unknown'}**")
                if contact.title:
                    lines.append(f"  - Title: {contact.title}")
                if contact.email:
                    lines.append(f"  - Email: {contact.email}")
                lines.append("")
        
        if pack.crm_context.opp_stage:
            lines.append("### Opportunity")
            lines.append("")
            lines.append(f"- **Stage:** {pack.crm_context.opp_stage}")
            if pack.crm_context.opp_amount:
                lines.append(f"- **Amount:** ${pack.crm_context.opp_amount:,.2f}")
            if pack.crm_context.opp_close_date:
                lines.append(f"- **Close Date:** {pack.crm_context.opp_close_date}")
            lines.append("")
        
        if pack.crm_context.last_activity_notes:
            lines.append("### Last Activity")
            lines.append("")
            lines.append(pack.crm_context.last_activity_notes)
            lines.append("")
    
    return "\n".join(lines)
