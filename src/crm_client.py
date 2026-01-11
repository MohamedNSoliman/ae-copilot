"""
CRM client interface and implementations for HubSpot and Salesforce.
"""

import os
import json
from abc import ABC, abstractmethod
from typing import Optional, List
from pathlib import Path
import requests
from .schemas import CRMContext, CRMContact


class CRMClient(ABC):
    """Abstract base class for CRM clients."""
    
    @abstractmethod
    def fetch_account_context(self, account_identifier: str) -> CRMContext:
        """
        Fetch account context from CRM.
        
        Args:
            account_identifier: Account name, domain, or CRM ID
            
        Returns:
            CRMContext with account and contact information
        """
        pass


class HubSpotClient(CRMClient):
    """HubSpot CRM client."""
    
    def __init__(self, private_app_token: Optional[str] = None, mock_mode: bool = False):
        """
        Initialize HubSpot client.
        
        Args:
            private_app_token: HubSpot private app access token
            mock_mode: If True, use mock data instead of API calls
        """
        self.mock_mode = mock_mode or os.getenv("CRM_MOCK_MODE", "false").lower() == "true"
        self.private_app_token = private_app_token or os.getenv("HUBSPOT_PRIVATE_APP_TOKEN")
        
        if not self.mock_mode and not self.private_app_token:
            raise ValueError("HubSpot private app token required when not in mock mode")
        
        self.base_url = "https://api.hubapi.com"
        self.headers = {
            "Authorization": f"Bearer {self.private_app_token}",
            "Content-Type": "application/json"
        } if not self.mock_mode else {}
    
    def fetch_account_context(self, account_identifier: str) -> CRMContext:
        """
        Fetch account context from HubSpot.
        
        Args:
            account_identifier: Company name, domain, or HubSpot company ID
            
        Returns:
            CRMContext with account information
        """
        if self.mock_mode:
            return self._load_mock_crm()
        
        # Search for company by name or domain
        company = self._search_company(account_identifier)
        if not company:
            return CRMContext()
        
        company_id = company.get("id")
        
        # Fetch company properties
        company_props = self._get_company_properties(company_id)
        
        # Fetch associated contacts
        contacts = self._get_company_contacts(company_id)
        
        # Fetch associated deals/opportunities
        deals = self._get_company_deals(company_id)
        
        # Build context
        context = CRMContext(
            account_name=company_props.get("name"),
            domain=company_props.get("domain"),
            industry=company_props.get("industry"),
            employee_count=company_props.get("numberofemployees"),
            region=company_props.get("hs_analytics_region"),
            key_contacts=contacts,
            opp_stage=deals.get("stage") if deals else None,
            opp_amount=deals.get("amount") if deals else None,
            opp_close_date=deals.get("closedate") if deals else None,
            last_activity_notes=company_props.get("notes_last_contacted")
        )
        
        return context
    
    def _search_company(self, identifier: str) -> Optional[dict]:
        """Search for company by name or domain."""
        # Try by domain first
        if "." in identifier:
            response = requests.get(
                f"{self.base_url}/crm/v3/objects/companies",
                headers=self.headers,
                params={"properties": "name,domain", "filterGroups": [{"filters": [{"propertyName": "domain", "operator": "EQ", "value": identifier}]}]}
            )
            if response.status_code == 200:
                results = response.json().get("results", [])
                if results:
                    return results[0]
        
        # Try by name
        response = requests.get(
            f"{self.base_url}/crm/v3/objects/companies/search",
            headers=self.headers,
            json={
                "query": identifier,
                "properties": ["name", "domain", "industry", "numberofemployees"]
            }
        )
        if response.status_code == 200:
            results = response.json().get("results", [])
            if results:
                return results[0]
        
        return None
    
    def _get_company_properties(self, company_id: str) -> dict:
        """Get company properties."""
        response = requests.get(
            f"{self.base_url}/crm/v3/objects/companies/{company_id}",
            headers=self.headers,
            params={"properties": "name,domain,industry,numberofemployees,hs_analytics_region,notes_last_contacted"}
        )
        if response.status_code == 200:
            return response.json().get("properties", {})
        return {}
    
    def _get_company_contacts(self, company_id: str) -> List[CRMContact]:
        """Get contacts associated with company."""
        response = requests.get(
            f"{self.base_url}/crm/v3/objects/companies/{company_id}/associations/contacts",
            headers=self.headers
        )
        if response.status_code != 200:
            return []
        
        contact_ids = [r["id"] for r in response.json().get("results", [])]
        contacts = []
        
        for contact_id in contact_ids[:5]:  # Limit to 5 contacts
            contact_response = requests.get(
                f"{self.base_url}/crm/v3/objects/contacts/{contact_id}",
                headers=self.headers,
                params={"properties": "firstname,lastname,email,jobtitle"}
            )
            if contact_response.status_code == 200:
                props = contact_response.json().get("properties", {})
                contacts.append(CRMContact(
                    name=f"{props.get('firstname', '')} {props.get('lastname', '')}".strip(),
                    title=props.get("jobtitle"),
                    email=props.get("email")
                ))
        
        return contacts
    
    def _get_company_deals(self, company_id: str) -> Optional[dict]:
        """Get deals/opportunities associated with company."""
        response = requests.get(
            f"{self.base_url}/crm/v3/objects/companies/{company_id}/associations/deals",
            headers=self.headers
        )
        if response.status_code != 200:
            return None
        
        deal_ids = [r["id"] for r in response.json().get("results", [])]
        if not deal_ids:
            return None
        
        # Get most recent deal
        deal_response = requests.get(
            f"{self.base_url}/crm/v3/objects/deals/{deal_ids[0]}",
            headers=self.headers,
            params={"properties": "dealstage,amount,closedate"}
        )
        if deal_response.status_code == 200:
            return deal_response.json().get("properties", {})
        
        return None
    
    def _load_mock_crm(self) -> CRMContext:
        """Load mock CRM data from sample file."""
        mock_path = Path(__file__).parent.parent / "data" / "sample_crm.json"
        if mock_path.exists():
            with open(mock_path, 'r') as f:
                data = json.load(f)
                return CRMContext(**data)
        
        # Return default mock data
        return CRMContext(
            account_name="Acme Corp",
            domain="acme.com",
            industry="Technology",
            employee_count=500,
            region="North America",
            key_contacts=[
                CRMContact(name="John Doe", title="VP Engineering", email="john@acme.com"),
                CRMContact(name="Jane Smith", title="CTO", email="jane@acme.com")
            ],
            opp_stage="Qualified",
            opp_amount=50000.0,
            opp_close_date="2024-06-30"
        )


class SalesforceClient(CRMClient):
    """Salesforce CRM client (placeholder for future implementation)."""
    
    def __init__(self, *args, **kwargs):
        """Initialize Salesforce client."""
        raise NotImplementedError("Salesforce integration not yet implemented. Use HubSpot for MVP.")
    
    def fetch_account_context(self, account_identifier: str) -> CRMContext:
        """Fetch account context from Salesforce."""
        raise NotImplementedError("Salesforce integration not yet implemented.")
