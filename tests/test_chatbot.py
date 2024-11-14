import json
import pytest
import sys
import os
import csv
import time

# Adjusting the path to import the app module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app  # Import your Flask app

# Function to write detailed metrics to a CSV file
def write_metrics_to_csv(tc_id, description, input_msg, expected_output, actual_output, status, comments, response_time, relevance_score, completeness_score, improvement_suggestions):
    with open('detailed_metrics.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([tc_id, description, input_msg, expected_output, actual_output, status,
                         comments, response_time, relevance_score, completeness_score, improvement_suggestions])

# Function to create CSV header
def create_csv_header():
    with open('detailed_metrics.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["TC ID", 
                         "Test Description", 
                         "Input", 
                         "Expected Output", 
                         "Actual Output", 
                         "Status", 
                         "Comments", 
                         "Response Time", 
                         "Relevance Score", 
                         "Completeness Score", 
                         "Improvement Suggestions"])

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def run_test(client, tc_id, description, input_msg, expected_output):
    start_time = time.time()
    response = client.post('/chat', json={'message': input_msg})
    response_time = time.time() - start_time
    
    data = json.loads(response.data)
    actual_output = data['response']
    
    status = "Pass" if expected_output.lower() in actual_output.lower() else "Fail"
    
    relevance_score = "8 out of 10" if status == "Pass" else "3 out of 10"
    completeness_score = "8 out of 10" if status == "Pass" else "2 out of 10"
    
    comments = "The response provides relevant information." if status == "Pass" else "The response doesn't provide expected information."
    improvement_suggestions = "" if status == "Pass" else "Improve accuracy and completeness of the response."
    
    write_metrics_to_csv(tc_id, description, input_msg, expected_output, actual_output,
                         status, comments, f"{response_time:.2f}", relevance_score,
                         completeness_score, improvement_suggestions)

# Existing Test Cases
def test_services_for_seniors(client):
    run_test(
        client,
        "TC001",
        "Validate response for services available for seniors in Ontario",
        "What services are available for seniors in Ontario?",
        "A comprehensive list of services available for seniors in Ontario."
    )
    

def test_seniors_co_payment_program(client):
    run_test(
        client,
        "TC002",
        "Validate response for applying to the Seniors Co-Payment Program",
        "How do I apply for the Seniors Co-Payment Program?",
        "Clear instructions on how to apply."
    )

def test_ontario_drug_benefit(client):
    run_test(
        client,
        "TC003",
        "Validate response regarding Ontario Drug Benefit (ODB)",
        "What is the Ontario Drug Benefit (ODB)?",
        "A description of ODB and how to apply."
    )

def test_senior_nutrition(client):
    run_test(
        client,
        "TC004",
        "Validate response about improving nutrition as a senior",
        "How can I improve my nutrition as a senior?",
        "Tips and resources related to nutrition for seniors."
    )

def test_mental_health_support(client):
    run_test(
        client,
        "TC005",
        "Validate response regarding mental health support resources for seniors",
        "What resources are available for senior mental health support?",
        "List of resources and contact information."
    )

def test_contact_siena(client):
    run_test(
        client,
        "TC006",
        "Validate response for contacting Siena",
        "How do I contact Siena?",
        "Contact details including phone number."
    )

def test_pricing_information(client):
    run_test(
        client,
        "TC007",
        "Validate response regarding pricing information",
        "What is the price per month?",
        "Pricing information for Siena's services."
    )

def test_service_availability_toronto(client):
    run_test(
        client,
        "TC008",
        "Validate response about service availability in Toronto",
        "Where are services available in Toronto?",
        "Information about service locations in Toronto."
    )

def test_waiting_time(client):
    run_test(
        client,
        "TC009",
        "Validate response regarding waiting times",
        "What is the waiting time?",
        "Information about typical waiting times for services."
    )

# Additional Test Cases (10 more)
def test_active_living_resources(client):
     run_test(
         client,
         tc_id="TC010", 
         description="Validate active living resources available for seniors", 
         input_msg="What active living resources are available?", 
         expected_output="Community activities and centers available for seniors."
     )

def test_financial_assistance_programs(client):
     run_test(
         client,
         tc_id="TC011", 
         description="Validate financial assistance programs available", 
         input_msg="What financial assistance programs are available?", 
         expected_output="Programs like Old Age Security and Guaranteed Income Supplement."
     )

def test_health_and_wellness_services(client):
     run_test(
         client,
         tc_id="TC012", 
         description="Validate health and wellness services available", 
         input_msg="What health services are available for seniors?", 
         expected_output="Health services including check-ups and preventive care."
     )

def test_housing_support(client):
     run_test(
         client,
         tc_id="TC013", 
         description="Validate housing support available for seniors", 
         input_msg="What housing support is available for seniors?", 
         expected_output="Housing programs like Home Adaptations for Seniors' Independence."
     )

def test_tax_benefits_for_seniors(client):
     run_test(
         client,
         tc_id="TC014", 
         description="Validate tax benefits available for seniors", 
         input_msg="What tax benefits are available for seniors?", 
         expected_output="Tax credits such as the Ontario Senior Homeowners' Property Tax Grant."
     )

def test_employment_resources_for_seniors(client):
     run_test(
         client,
         tc_id="TC015", 
         description="Validate employment resources available for seniors", 
         input_msg="What employment resources are available?", 
         expected_output="Job training programs and Employment Ontario services."
     )

def test_nutrition_resources_for_seniors(client):
     run_test(
         client,
         tc_id="TC016", 
         description="Validate nutrition resources available for seniors", 
         input_msg="What nutrition resources are available?", 
         expected_output="Resources like meal delivery services and nutrition counseling."
     )

def test_transportation_services_for_seniors(client):
     run_test(
         client,
         tc_id="TC017", 
         description="Validate transportation services available for seniors", 
         input_msg="What transportation services are available?", 
         expected_output="Transportation options including public transit discounts and community shuttles."
     )

def test_caregiver_support_resources(client):
     run_test(
         client,
         tc_id="TC018", 
         description="Validate caregiver support resources available", 
         input_msg="What caregiver support resources are available?", 
         expected_output="Support groups and respite care options."
     )

if __name__ == "__main__":
   # Create the CSV file with headers
   with open('detailed_metrics.csv', mode='w', newline='', encoding='utf-8') as file:
       writer = csv.writer(file)
       writer.writerow(["TC ID", 
                        "Test Description", 
                        "Input", 
                        "Expected Output", 
                        "Actual Output", 
                        "Status", 
                        "Comments", 
                        "Response Time", 
                        "Relevance Score", 
                        "Completeness Score", 
                        "Improvement Suggestions"])
    
   pytest.main([__file__])