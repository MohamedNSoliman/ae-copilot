"""
Business case generator - creates one-pager business case with ROI in appendix.
"""

from datetime import datetime
from typing import Optional
from .schemas import ROIInputs, ROIOutputs, ExtractedSignals, CRMContext


def generate_business_case(
    company_name: str,
    roi_inputs: ROIInputs,
    roi_outputs: ROIOutputs,
    gong_signals: Optional[ExtractedSignals] = None,
    crm_context: Optional[CRMContext] = None
) -> str:
    """
    Generate a one-pager business case for Cursor adoption.
    
    Args:
        company_name: Company name
        roi_inputs: ROI calculation inputs
        roi_outputs: ROI calculation outputs
        gong_signals: Optional Gong signals
        crm_context: Optional CRM context
        
    Returns:
        Markdown-formatted business case
    """
    lines = []
    
    # Header
    lines.append("# Business Case: Cursor for Developer Productivity")
    lines.append("")
    lines.append(f"**Company:** {company_name}")
    lines.append(f"**Date:** {datetime.now().strftime('%B %d, %Y')}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Executive Summary
    lines.append("## Executive Summary")
    lines.append("")
    lines.append(f"Cursor delivers significant developer productivity gains for {company_name}, resulting in **${roi_outputs.net_annual_value:,.0f} in net annual value** with a payback period of **{roi_outputs.payback_months:.1f} months**.")
    lines.append("")
    
    # Business Impact
    lines.append("## Business Impact")
    lines.append("")
    lines.append("### Key Metrics")
    lines.append("")
    lines.append(f"- **Annual Cost Savings:** ${roi_outputs.annual_cost_saved:,.0f}")
    lines.append(f"- **Annual Hours Saved:** {roi_outputs.annual_hours_saved:,.0f} hours")
    lines.append(f"- **Net Annual Value:** ${roi_outputs.net_annual_value:,.0f}")
    lines.append(f"- **Payback Period:** {roi_outputs.payback_months:.1f} months")
    lines.append("")
    
    # Context (if available from Gong/CRM)
    if gong_signals or crm_context:
        lines.append("## Context")
        lines.append("")
        
        if crm_context:
            if crm_context.industry:
                lines.append(f"- **Industry:** {crm_context.industry}")
            if crm_context.employee_count:
                lines.append(f"- **Company Size:** {crm_context.employee_count:,} employees")
            if crm_context.region:
                lines.append(f"- **Region:** {crm_context.region}")
            lines.append("")
        
        if gong_signals:
            if gong_signals.pain_points:
                lines.append("### Identified Pain Points")
                for pain in gong_signals.pain_points:
                    lines.append(f"- {pain}")
                lines.append("")
            
            if gong_signals.current_tooling:
                lines.append("### Current Tooling")
                lines.append(f"- {', '.join(gong_signals.current_tooling)}")
                lines.append("")
            
            if gong_signals.buying_stage != "unaware":
                lines.append(f"### Buying Stage: {gong_signals.buying_stage.title()}")
                lines.append("")
    
    # Recommendation
    lines.append("## Recommendation")
    lines.append("")
    lines.append(f"Based on {roi_inputs.team_size_engineering} engineers saving {roi_inputs.hours_saved_per_engineer_per_week} hours per week with {roi_inputs.adoption_rate*100:.0f}% adoption, Cursor delivers immediate and measurable ROI.")
    lines.append("")
    lines.append("**Recommendation:** Proceed with Cursor implementation to capture ${:,.0f} in annual value.".format(roi_outputs.net_annual_value))
    lines.append("")
    
    # Next Steps
    lines.append("## Next Steps")
    lines.append("")
    lines.append("1. **Pilot Program:** Start with a small team to validate productivity gains")
    lines.append("2. **Expansion Plan:** Roll out to full engineering team based on pilot results")
    lines.append("3. **Success Metrics:** Track hours saved and developer satisfaction")
    lines.append("")
    
    # Appendix: Detailed ROI Analysis
    lines.append("---")
    lines.append("")
    lines.append("# Appendix: Detailed ROI Analysis")
    lines.append("")
    
    lines.append("## ROI Inputs")
    lines.append("")
    lines.append("| Parameter | Value |")
    lines.append("|-----------|-------|")
    lines.append(f"| Team Size (Engineering) | {roi_inputs.team_size_engineering} engineers |")
    lines.append(f"| Fully Loaded Cost per Engineer | ${roi_inputs.fully_loaded_cost_per_engineer:,.2f} |")
    lines.append(f"| Hours Saved per Engineer per Week | {roi_inputs.hours_saved_per_engineer_per_week} hours |")
    lines.append(f"| Adoption Rate | {roi_inputs.adoption_rate*100:.1f}% |")
    lines.append(f"| Weeks per Year | {roi_inputs.weeks_per_year} weeks |")
    lines.append(f"| Cursor Annual Cost | ${roi_inputs.cursor_annual_cost:,.2f} |")
    lines.append("")
    
    lines.append("## ROI Outputs")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| Annual Hours Saved | {roi_outputs.annual_hours_saved:,.2f} hours |")
    lines.append(f"| Annual Cost Saved | ${roi_outputs.annual_cost_saved:,.2f} |")
    lines.append(f"| Net Annual Value | ${roi_outputs.net_annual_value:,.2f} |")
    if roi_outputs.payback_months != float('inf'):
        lines.append(f"| Payback Period | {roi_outputs.payback_months:.2f} months |")
    else:
        lines.append(f"| Payback Period | N/A (no savings) |")
    lines.append("")
    
    # Calculation Methodology
    lines.append("## Calculation Methodology")
    lines.append("")
    lines.append("### Annual Hours Saved")
    lines.append("")
    lines.append("```")
    lines.append("Annual Hours Saved = Team Size × Hours Saved/Week × Adoption Rate × Weeks/Year")
    lines.append(f"                  = {roi_inputs.team_size_engineering} × {roi_inputs.hours_saved_per_engineer_per_week} × {roi_inputs.adoption_rate} × {roi_inputs.weeks_per_year}")
    lines.append(f"                  = {roi_outputs.annual_hours_saved:,.2f} hours")
    lines.append("```")
    lines.append("")
    
    lines.append("### Annual Cost Saved")
    lines.append("")
    lines.append("```")
    lines.append("Equivalent Engineers Saved = Annual Hours Saved / (Weeks/Year × 40 hours/week)")
    equivalent_engineers = roi_outputs.annual_hours_saved / (roi_inputs.weeks_per_year * 40)
    lines.append(f"                            = {roi_outputs.annual_hours_saved:,.2f} / ({roi_inputs.weeks_per_year} × 40)")
    lines.append(f"                            = {equivalent_engineers:.2f} engineers")
    lines.append("")
    lines.append("Annual Cost Saved = Equivalent Engineers Saved × Fully Loaded Cost/Engineer")
    lines.append(f"                  = {equivalent_engineers:.2f} × ${roi_inputs.fully_loaded_cost_per_engineer:,.2f}")
    lines.append(f"                  = ${roi_outputs.annual_cost_saved:,.2f}")
    lines.append("```")
    lines.append("")
    
    lines.append("### Net Annual Value")
    lines.append("")
    lines.append("```")
    lines.append("Net Annual Value = Annual Cost Saved - Cursor Annual Cost")
    lines.append(f"                  = ${roi_outputs.annual_cost_saved:,.2f} - ${roi_inputs.cursor_annual_cost:,.2f}")
    lines.append(f"                  = ${roi_outputs.net_annual_value:,.2f}")
    lines.append("```")
    lines.append("")
    
    if roi_outputs.payback_months != float('inf'):
        lines.append("### Payback Period")
        lines.append("")
        lines.append("```")
        lines.append("Payback Period (months) = (Cursor Annual Cost / Annual Cost Saved) × 12")
        lines.append(f"                         = (${roi_inputs.cursor_annual_cost:,.2f} / ${roi_outputs.annual_cost_saved:,.2f}) × 12")
        lines.append(f"                         = {roi_outputs.payback_months:.2f} months")
        lines.append("```")
        lines.append("")
    
    # Evidence (if from Gong)
    if gong_signals and gong_signals.evidence:
        lines.append("## Supporting Evidence")
        lines.append("")
        for ev in gong_signals.evidence:
            lines.append(f"### {ev.field_name.replace('_', ' ').title()}")
            lines.append("")
            if ev.timestamp_seconds:
                lines.append(f"*Timestamp: {ev.timestamp_seconds}s*")
            lines.append(f"> {ev.quote}")
            lines.append("")
    
    return "\n".join(lines)
