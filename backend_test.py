#!/usr/bin/env python3
"""
NetworkingAI Backend API Test Suite
Tests all implemented backend endpoints thoroughly
"""

import requests
import json
import uuid
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/frontend/.env')

# Get backend URL from frontend .env
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'http://localhost:8001')
API_BASE = f"{BACKEND_URL}/api"

print(f"Testing backend at: {API_BASE}")

class NetworkingAITester:
    def __init__(self):
        self.test_results = {}
        self.created_contacts = []
        self.created_campaigns = []
        self.created_goals = []
        
    def log_result(self, test_name, success, message="", details=None):
        """Log test results"""
        self.test_results[test_name] = {
            'success': success,
            'message': message,
            'details': details
        }
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name} - {message}")
        if details and not success:
            print(f"   Details: {details}")
    
    def test_health_check(self):
        """Test basic API health check"""
        try:
            response = requests.get(f"{API_BASE}/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if "NetworkingAI API is running" in data.get("message", ""):
                    self.log_result("Health Check", True, "API is responding correctly")
                    return True
                else:
                    self.log_result("Health Check", False, "Unexpected response message", data)
            else:
                self.log_result("Health Check", False, f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_result("Health Check", False, "Connection failed", str(e))
        return False
    
    def test_contact_crud(self):
        """Test Contact CRUD operations"""
        # Test Create Contact
        contact_data = {
            "name": "Alice Johnson",
            "email": "alice.johnson@techcorp.com",
            "company": "TechCorp Solutions",
            "position": "Senior Software Engineer",
            "industry": "Technology",
            "linkedin_url": "https://linkedin.com/in/alicejohnson",
            "phone": "+1-555-0123",
            "notes": "Met at tech conference, interested in AI solutions",
            "priority": "high",
            "tags": ["ai", "software", "conference"]
        }
        
        try:
            # Create contact
            response = requests.post(f"{API_BASE}/contacts", json=contact_data, timeout=10)
            if response.status_code == 200:
                contact = response.json()
                contact_id = contact.get('id')
                if contact_id:
                    self.created_contacts.append(contact_id)
                    self.log_result("Create Contact", True, f"Contact created with ID: {contact_id}")
                    
                    # Verify lead score calculation
                    lead_score = contact.get('lead_score', 0)
                    if lead_score > 50:  # Should be higher due to complete profile
                        self.log_result("Lead Score Calculation", True, f"Lead score: {lead_score}")
                    else:
                        self.log_result("Lead Score Calculation", False, f"Low lead score: {lead_score}")
                    
                    # Test Get Contact by ID
                    get_response = requests.get(f"{API_BASE}/contacts/{contact_id}", timeout=10)
                    if get_response.status_code == 200:
                        retrieved_contact = get_response.json()
                        if retrieved_contact['name'] == contact_data['name']:
                            self.log_result("Get Contact by ID", True, "Contact retrieved successfully")
                        else:
                            self.log_result("Get Contact by ID", False, "Retrieved contact data mismatch")
                    else:
                        self.log_result("Get Contact by ID", False, f"HTTP {get_response.status_code}")
                    
                    # Test Update Contact
                    update_data = {
                        "notes": "Updated notes - follow up scheduled",
                        "status": "contacted",
                        "priority": "medium"
                    }
                    update_response = requests.put(f"{API_BASE}/contacts/{contact_id}", json=update_data, timeout=10)
                    if update_response.status_code == 200:
                        updated_contact = update_response.json()
                        if updated_contact['notes'] == update_data['notes']:
                            self.log_result("Update Contact", True, "Contact updated successfully")
                        else:
                            self.log_result("Update Contact", False, "Update data not reflected")
                    else:
                        self.log_result("Update Contact", False, f"HTTP {update_response.status_code}")
                    
                    return True
                else:
                    self.log_result("Create Contact", False, "No contact ID returned", contact)
            else:
                self.log_result("Create Contact", False, f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_result("Create Contact", False, "Request failed", str(e))
        
        return False
    
    def test_get_all_contacts(self):
        """Test getting all contacts with filters"""
        try:
            # Get all contacts
            response = requests.get(f"{API_BASE}/contacts", timeout=10)
            if response.status_code == 200:
                contacts = response.json()
                if isinstance(contacts, list):
                    self.log_result("Get All Contacts", True, f"Retrieved {len(contacts)} contacts")
                    
                    # Test filtering by status
                    status_response = requests.get(f"{API_BASE}/contacts?status=contacted", timeout=10)
                    if status_response.status_code == 200:
                        filtered_contacts = status_response.json()
                        self.log_result("Filter Contacts by Status", True, f"Filtered to {len(filtered_contacts)} contacts")
                    else:
                        self.log_result("Filter Contacts by Status", False, f"HTTP {status_response.status_code}")
                    
                    return True
                else:
                    self.log_result("Get All Contacts", False, "Response is not a list", contacts)
            else:
                self.log_result("Get All Contacts", False, f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_result("Get All Contacts", False, "Request failed", str(e))
        
        return False
    
    def test_ai_email_generation(self):
        """Test AI email generation endpoint"""
        if not self.created_contacts:
            self.log_result("AI Email Generation", False, "No contacts available for testing")
            return False
        
        contact_id = self.created_contacts[0]
        email_request = {
            "contact_id": contact_id,
            "email_type": "introduction",
            "context": "Following up from tech conference discussion about AI solutions",
            "tone": "professional"
        }
        
        try:
            response = requests.post(f"{API_BASE}/generate-email", json=email_request, timeout=30)
            if response.status_code == 200:
                email_data = response.json()
                if 'subject' in email_data and 'body' in email_data:
                    self.log_result("AI Email Generation", True, "Email generated successfully")
                    print(f"   Generated Subject: {email_data['subject'][:50]}...")
                    return True
                else:
                    self.log_result("AI Email Generation", False, "Missing subject or body", email_data)
            elif response.status_code == 400:
                # Expected if OpenAI API key is not configured
                error_data = response.json()
                if "OpenAI API key not configured" in error_data.get('detail', ''):
                    self.log_result("AI Email Generation - Error Handling", True, "Correctly handles missing API key")
                    return True
                else:
                    self.log_result("AI Email Generation", False, "Unexpected 400 error", error_data)
            else:
                self.log_result("AI Email Generation", False, f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_result("AI Email Generation", False, "Request failed", str(e))
        
        return False
    
    def test_campaign_management(self):
        """Test campaign CRUD operations"""
        if not self.created_contacts:
            self.log_result("Campaign Management", False, "No contacts available for campaign testing")
            return False
        
        campaign_data = {
            "name": "Q1 Tech Outreach Campaign",
            "description": "Outreach to technology professionals for Q1 networking",
            "contact_ids": [self.created_contacts[0]],
            "scheduled_at": (datetime.utcnow() + timedelta(days=1)).isoformat()
        }
        
        try:
            # Create campaign
            response = requests.post(f"{API_BASE}/campaigns", json=campaign_data, timeout=10)
            if response.status_code == 200:
                campaign = response.json()
                campaign_id = campaign.get('id')
                if campaign_id:
                    self.created_campaigns.append(campaign_id)
                    self.log_result("Create Campaign", True, f"Campaign created with ID: {campaign_id}")
                    
                    # Test Get All Campaigns
                    get_response = requests.get(f"{API_BASE}/campaigns", timeout=10)
                    if get_response.status_code == 200:
                        campaigns = get_response.json()
                        if isinstance(campaigns, list) and len(campaigns) > 0:
                            self.log_result("Get All Campaigns", True, f"Retrieved {len(campaigns)} campaigns")
                        else:
                            self.log_result("Get All Campaigns", False, "No campaigns returned")
                    else:
                        self.log_result("Get All Campaigns", False, f"HTTP {get_response.status_code}")
                    
                    # Test Update Campaign
                    update_data = {
                        "status": "active",
                        "description": "Updated campaign description"
                    }
                    update_response = requests.put(f"{API_BASE}/campaigns/{campaign_id}", json=update_data, timeout=10)
                    if update_response.status_code == 200:
                        self.log_result("Update Campaign", True, "Campaign updated successfully")
                    else:
                        self.log_result("Update Campaign", False, f"HTTP {update_response.status_code}")
                    
                    return True
                else:
                    self.log_result("Create Campaign", False, "No campaign ID returned", campaign)
            else:
                self.log_result("Create Campaign", False, f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_result("Create Campaign", False, "Request failed", str(e))
        
        return False
    
    def test_analytics_api(self):
        """Test analytics and reporting API"""
        try:
            response = requests.get(f"{API_BASE}/analytics", timeout=15)
            if response.status_code == 200:
                analytics = response.json()
                required_fields = [
                    'total_contacts', 'contacts_by_status', 'contacts_by_priority',
                    'total_campaigns', 'campaigns_by_status', 'email_performance',
                    'relationship_scores', 'monthly_growth'
                ]
                
                missing_fields = [field for field in required_fields if field not in analytics]
                if not missing_fields:
                    self.log_result("Analytics API Structure", True, "All required fields present")
                    
                    # Verify data types and values
                    if isinstance(analytics['total_contacts'], int) and analytics['total_contacts'] >= 0:
                        self.log_result("Analytics Data Validation", True, f"Total contacts: {analytics['total_contacts']}")
                    else:
                        self.log_result("Analytics Data Validation", False, "Invalid total_contacts value")
                    
                    # Check email performance structure
                    email_perf = analytics.get('email_performance', {})
                    if 'response_rate' in email_perf and 'conversion_rate' in email_perf:
                        self.log_result("Email Performance Metrics", True, "Performance metrics calculated")
                    else:
                        self.log_result("Email Performance Metrics", False, "Missing performance metrics")
                    
                    return True
                else:
                    self.log_result("Analytics API Structure", False, f"Missing fields: {missing_fields}", analytics)
            else:
                self.log_result("Analytics API", False, f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_result("Analytics API", False, "Request failed", str(e))
        
        return False
    
    def test_networking_goals(self):
        """Test networking goals management"""
        goals_data = {
            "industry": "Technology",
            "role": "Software Engineer",
            "company_size": "50-200 employees",
            "networking_objectives": ["Find mentors", "Build industry connections", "Learn about new technologies"],
            "target_contacts_per_month": 15,
            "preferred_communication_style": "professional",
            "pain_points": ["Limited time for networking", "Difficulty finding relevant contacts"],
            "success_metrics": ["Number of meaningful connections", "Job opportunities discovered"]
        }
        
        try:
            # Create networking goals
            response = requests.post(f"{API_BASE}/networking-goals", json=goals_data, timeout=10)
            if response.status_code == 200:
                goals = response.json()
                goals_id = goals.get('id')
                if goals_id:
                    self.created_goals.append(goals_id)
                    self.log_result("Create Networking Goals", True, f"Goals created with ID: {goals_id}")
                    
                    # Test Get Networking Goals
                    get_response = requests.get(f"{API_BASE}/networking-goals", timeout=10)
                    if get_response.status_code == 200:
                        all_goals = get_response.json()
                        if isinstance(all_goals, list) and len(all_goals) > 0:
                            self.log_result("Get Networking Goals", True, f"Retrieved {len(all_goals)} goal sets")
                        else:
                            self.log_result("Get Networking Goals", False, "No goals returned")
                    else:
                        self.log_result("Get Networking Goals", False, f"HTTP {get_response.status_code}")
                    
                    return True
                else:
                    self.log_result("Create Networking Goals", False, "No goals ID returned", goals)
            else:
                self.log_result("Create Networking Goals", False, f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_result("Create Networking Goals", False, "Request failed", str(e))
        
        return False
    
    def test_interaction_logging(self):
        """Test interaction logging system"""
        if not self.created_contacts:
            self.log_result("Interaction Logging", False, "No contacts available for interaction testing")
            return False
        
        contact_id = self.created_contacts[0]
        interaction_data = {
            "contact_id": contact_id,
            "type": "email_sent",
            "subject": "Follow-up from tech conference",
            "content": "Thanks for the great conversation about AI solutions...",
            "status": "completed"
        }
        
        try:
            # Create interaction log
            response = requests.post(f"{API_BASE}/interactions", json=interaction_data, timeout=10)
            if response.status_code == 200:
                interaction = response.json()
                if interaction.get('id'):
                    self.log_result("Create Interaction Log", True, "Interaction logged successfully")
                    
                    # Test Get Contact Interactions
                    get_response = requests.get(f"{API_BASE}/interactions/{contact_id}", timeout=10)
                    if get_response.status_code == 200:
                        interactions = get_response.json()
                        if isinstance(interactions, list) and len(interactions) > 0:
                            self.log_result("Get Contact Interactions", True, f"Retrieved {len(interactions)} interactions")
                        else:
                            self.log_result("Get Contact Interactions", False, "No interactions returned")
                    else:
                        self.log_result("Get Contact Interactions", False, f"HTTP {get_response.status_code}")
                    
                    return True
                else:
                    self.log_result("Create Interaction Log", False, "No interaction ID returned", interaction)
            else:
                self.log_result("Create Interaction Log", False, f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_result("Create Interaction Log", False, "Request failed", str(e))
        
        return False
    
    def test_contact_discovery(self):
        """Test contact discovery system"""
        discovery_criteria = {
            "industry": "Technology",
            "location": "San Francisco",
            "company_size": "50-200",
            "role": "Software Engineer"
        }
        
        try:
            response = requests.post(f"{API_BASE}/discover-contacts", json=discovery_criteria, timeout=10)
            if response.status_code == 200:
                discovery_result = response.json()
                if 'discovered_contacts' in discovery_result and 'total_found' in discovery_result:
                    contacts = discovery_result['discovered_contacts']
                    total = discovery_result['total_found']
                    self.log_result("Contact Discovery", True, f"Discovered {total} contacts")
                    
                    # Verify contact structure
                    if contacts and len(contacts) > 0:
                        first_contact = contacts[0]
                        required_fields = ['name', 'email', 'company', 'position']
                        if all(field in first_contact for field in required_fields):
                            self.log_result("Discovery Contact Structure", True, "Contact data structure valid")
                        else:
                            self.log_result("Discovery Contact Structure", False, "Missing required contact fields")
                    
                    return True
                else:
                    self.log_result("Contact Discovery", False, "Missing required response fields", discovery_result)
            else:
                self.log_result("Contact Discovery", False, f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_result("Contact Discovery", False, "Request failed", str(e))
        
        return False
    
    def test_enum_values(self):
        """Test enum values in API responses"""
        # Test with different enum values
        test_cases = [
            {"status": "new", "priority": "low"},
            {"status": "contacted", "priority": "medium"},
            {"status": "responded", "priority": "high"}
        ]
        
        success_count = 0
        for i, case in enumerate(test_cases):
            contact_data = {
                "name": f"Test Contact {i+1}",
                "email": f"test{i+1}@example.com",
                "company": "Test Company",
                **case
            }
            
            try:
                response = requests.post(f"{API_BASE}/contacts", json=contact_data, timeout=10)
                if response.status_code == 200:
                    contact = response.json()
                    if contact.get('status') == case['status'] and contact.get('priority') == case['priority']:
                        success_count += 1
                        self.created_contacts.append(contact['id'])
            except:
                pass
        
        if success_count == len(test_cases):
            self.log_result("Enum Values Validation", True, f"All {success_count} enum combinations work")
            return True
        else:
            self.log_result("Enum Values Validation", False, f"Only {success_count}/{len(test_cases)} enum combinations work")
            return False
    
    def cleanup_test_data(self):
        """Clean up test data"""
        cleanup_count = 0
        
        # Delete test contacts
        for contact_id in self.created_contacts:
            try:
                response = requests.delete(f"{API_BASE}/contacts/{contact_id}", timeout=10)
                if response.status_code == 200:
                    cleanup_count += 1
            except:
                pass
        
        if cleanup_count > 0:
            self.log_result("Cleanup Test Data", True, f"Cleaned up {cleanup_count} test contacts")
        
    def run_all_tests(self):
        """Run all backend tests"""
        print("=" * 60)
        print("NETWORKINGAI BACKEND API TEST SUITE")
        print("=" * 60)
        
        # High Priority Tests
        print("\n🔥 HIGH PRIORITY TESTS:")
        health_ok = self.test_health_check()
        contact_crud_ok = self.test_contact_crud()
        contacts_list_ok = self.test_get_all_contacts()
        ai_email_ok = self.test_ai_email_generation()
        analytics_ok = self.test_analytics_api()
        
        # Medium Priority Tests
        print("\n📊 MEDIUM PRIORITY TESTS:")
        campaign_ok = self.test_campaign_management()
        discovery_ok = self.test_contact_discovery()
        goals_ok = self.test_networking_goals()
        interactions_ok = self.test_interaction_logging()
        enums_ok = self.test_enum_values()
        
        # Cleanup
        print("\n🧹 CLEANUP:")
        self.cleanup_test_data()
        
        # Summary
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for test_name, result in self.test_results.items():
                if not result['success']:
                    print(f"  - {test_name}: {result['message']}")
        
        # Critical functionality assessment
        critical_tests = [health_ok, contact_crud_ok, analytics_ok]
        critical_passed = sum(critical_tests)
        
        print(f"\n🎯 CRITICAL FUNCTIONALITY: {critical_passed}/3 tests passed")
        
        return {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'critical_functionality_working': critical_passed >= 2,
            'detailed_results': self.test_results
        }

if __name__ == "__main__":
    tester = NetworkingAITester()
    results = tester.run_all_tests()