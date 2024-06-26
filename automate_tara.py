from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import boto3

# Initialize the WebDriver (Chrome in this example)
driver = webdriver.Chrome()

def login_and_set_options(memberID, memberDob, service_value=" "):
    # URL of the login page
    login_url = ' '
    
    # Load the login page
    driver.get(login_url)
    
    # Fill in the login form
    member_id_field = driver.find_element(By.NAME, 'memberId')  # Update with actual field name
    dob_field = driver.find_element(By.NAME, 'memberDob')  # Update with actual field name
    member_id_field.send_keys(memberID)
    dob_field.send_keys(memberDob)
    
    # Submit the login form
    dob_field.send_keys(Keys.RETURN)
    
    # Wait for the dashboard to load
    time.sleep(5)
    
    # Check if login was successful
    if "dashboard" in driver.current_url:
        print("Login success.")
    else:
        send_email_notification(memberID, "Login failed")
        print("Login failed. Email notification sent.")
        return

    search_service_and_notify(driver, memberID, service_value)

def search_service_and_notify(driver, memberID, service_value):
    try:
        # Wait for the dashboard elements to load
        wait = WebDriverWait(driver, 10)
        
        # Find and set the "Select your service" dropdown
        service_select = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-labelledby="select2-select_procedure_code1-container"]')))
        service_select.click()
        
        # Type the search query into the dropdown
        search_input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'select2-search__field')))
        search_input.send_keys(service_value)
        
        # Wait for the search results to appear and select the appropriate option
        desired_option = wait.until(EC.presence_of_element_located((By.XPATH, f'//li[contains(text(), "{service_value}")]')))
        desired_option.click()
        
        # Click the "The least expensive option" button
        least_expensive_button = wait.until(EC.element_to_be_clickable((By.NAME, 'theleastexpensiveoption')))  # Update with actual field name or ID
        least_expensive_button.click()

        # Wait for the results to load
        time.sleep(5)

        # Check if there are service providers listed in the table
        provider_list = driver.find_elements(By.CLASS_NAME, 'trRows')
        
        if provider_list:
            send_email_notification(memberID, "Login and query search success")
            print("Service providers found. Email notification sent.")
        else:
            send_email_notification(memberID, "Login success but query search failed")
            print("No service providers found. Email notification sent.")
    except Exception as e:
        send_email_notification(memberID, f"Error during service search: {str(e)}")
        print(f"Error during service search: {str(e)}")

def send_email_notification(memberID, message):
    # Create a Boto3 session with AWS credentials
    session = boto3.Session(
        aws_access_key_id=' ',
        aws_secret_access_key=' ',
        aws_session_token=' ',
        region_name=' '  # Optional: specify the AWS region 
    )
    
    # Initialize the SNS client
    client = session.client('sns')
    
    # Define the email message
    full_message = f"{message} for member ID: {memberID}"
    
    # Send the email
    response = client.publish(
        TopicArn=' ',  # Update with your SNS topic ARN
        Message=full_message,
        Subject=message
    )
    
    # Print the response
    print("Email notification sent:", response)

if __name__ == '__main__':
    memberID = ' '
    memberDob = ' '
    service_value = ' '
    login_and_set_options(memberID, memberDob, service_value)
