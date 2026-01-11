"""
Pydantic schemas for AE Copilot data models.
"""

from datetime import datetime
from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class ROIInputs(BaseModel):
    """Inputs for ROI calculation."""
    team_size_engineering: int = Field(ge=1, description="Number of engineers on the team")
    fully_loaded_cost_per_engineer: float = Field(default=220000.0, ge=0, description="Fully loaded cost per engineer per year")
    hours_saved_per_engineer_per_week: float = Field(ge=0, description="Hours saved per engineer per week")
    adoption_rate: float = Field(default=0.7, ge=0, le=1, description="Adoption rate (0-1)")
    weeks_per_year: int = Field(default=48, ge=1, le=52, description="Working weeks per year")
    cursor_annual_cost: float = Field(ge=0, description="Annual cost of Cursor")


class ROIOutputs(BaseModel):
    """Outputs from ROI calculation."""
    annual_hours_saved: float = Field(description="Total annual hours saved")
    annual_cost_saved: float = Field(description="Total annual cost saved")
    net_annual_value: float = Field(description="Net annual value (savings - cost)")
    payback_months: float = Field(description="Payback period in months")


class EvidenceQuote(BaseModel):
    """Evidence quote with timestamp."""
    field_name: str = Field(description="Field name this evidence supports")
    quote: str = Field(description="Quote from transcript")
    timestamp_seconds: Optional[int] = Field(None, description="Timestamp in seconds")


class ExtractedSignals(BaseModel):
    """Structured signals extracted from Gong transcript."""
    team_size_engineering: Optional[int] = Field(None, description="Engineering team size if mentioned")
    current_tooling: List[str] = Field(default_factory=list, description="Current tools mentioned")
    hours_saved_per_engineer_per_week: Optional[float] = Field(None, description="Hours saved if explicitly stated")
    pain_points: List[str] = Field(default_factory=list, description="Pain points mentioned")
    initiatives: List[str] = Field(default_factory=list, description="Initiatives or projects mentioned")
    buying_stage: Literal["unaware", "exploring", "evaluating", "procurement"] = Field(
        default="unaware", 
        description="Buying stage"
    )
    notes: Optional[str] = Field(None, description="Additional notes")
    evidence: List[EvidenceQuote] = Field(default_factory=list, description="Evidence quotes with timestamps")


class CRMContact(BaseModel):
    """CRM contact information."""
    name: Optional[str] = None
    title: Optional[str] = None
    email: Optional[str] = None


class CRMContext(BaseModel):
    """CRM account and contact context."""
    account_name: Optional[str] = None
    domain: Optional[str] = None
    industry: Optional[str] = None
    employee_count: Optional[int] = None
    region: Optional[str] = None
    key_contacts: List[CRMContact] = Field(default_factory=list)
    opp_stage: Optional[str] = None
    opp_amount: Optional[float] = None
    opp_close_date: Optional[str] = None
    last_activity_notes: Optional[str] = None


class NarrativePack(BaseModel):
    """Complete narrative pack for export."""
    roi_inputs: ROIInputs
    roi_outputs: ROIOutputs
    gong_signals: Optional[ExtractedSignals] = None
    crm_context: Optional[CRMContext] = None
    metadata: dict = Field(default_factory=dict, description="Metadata about generation")
