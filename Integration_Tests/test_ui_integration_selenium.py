import pytest
from app import app
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_chatbot_ui():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Navigate to the chatbot
        driver.get("http://127.0.0.1:5000")  # Adjust if your app runs on a different port

        # Wait for the input field to be present
        input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Type your message...']"))
        )
        
        # Send a message to the chatbot
        input_field.send_keys("What services do you offer?")
        
        # Wait for the send button to be clickable and click it
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Send']"))
        )
        submit_button.click()

        # Wait for a response (adjust based on your response handling)
        time.sleep(2)  # You might want to use a more dynamic wait here

        # Validate that the response is displayed in the chat messages area (adjust selector as needed)
        chat_messages = driver.find_element(By.ID, "chat-messages")
        assert "What services do you offer?" in chat_messages.text  # Check if the user's message is displayed
        
    finally:
        driver.quit()  # Ensure the browser closes after the test

if __name__ == "__main__":
    test_chatbot_ui()