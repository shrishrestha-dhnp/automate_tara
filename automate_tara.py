from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import boto3

# Initialize the WebDriver (Chrome in this example)
driver = webdriver.Chrome()

def login_and_set_options(memberID, memberDob, service_value="99214 - Office O/P Est Mod 30-39 Min"):
    # URL of the login page
    login_url = 'https://taradev.deerhold.com'
    
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
        aws_access_key_id='ASIATJWWKHLHPVTP56FP',
        aws_secret_access_key='K75d9Gci/4R0ki1cA81Vci3eYQtOnU+Yufx6bG4k',
        aws_session_token='IQoJb3JpZ2luX2VjEFUaCXVzLWVhc3QtMiJHMEUCIQCAGX/2Uq9HMzcuLmpwiQfQ8/cIFgdCfMCBxnfFesuE/QIgQLTaiPaH+l3yxBkzM2IlwWht9kabgWgl0TjqGqFPpr4qmgMIzv//////////ARACGgwyMjcwMDg5ODU4MDYiDInbG0jBr+/HZzaaPiruAn/R3v6A/SFCss03gIptvzE/nrIOVkBqmoDVYdD+kpgsie+k2hBDQmVE/QGb1wHulh0Kr7osdkCGWZwQy+U7+ajr/J6d6glB5ZM53rtjf7M1HcABG6ezVTnY9qXqOqiHXpnbSgVTbgdyYD4TNkVIsQLkVXfRHJaUdCduP8zQUINqw1PitrHbyLZMCAXhQahqKGnYGjKOJBTtSDqOXNyUrSWNw22c2I5W58Kum7kpTpSqp97vysx6VqEW9X7KOs2kKeJmIFjVX5AUFunf8+qRIeN8CvufzgqYYa/vsgdkCJVc7+N/RG51jfKi9w9QmLFAA66IBFHQiE94d/+yJwPQaXq6ZwBJHwr4tThWSWcO0Se0FVskVEPlm9ZJAYJXU9sK3MYWH901nsKlF0ChUDyEfQpwxdj5HJCgEzPTKl9tR9WdpcuWWxKporjYHZ3I/06Od80rKWEt3RigS06KSREOFkVah+5Qt4xXTeSZcXta0DCXo9CyBjqmAebhBax3OapJpu+9+sg6M58i9TpUk5zQaN4YUe4qOMAr4YTqld3rpAx5AkOda5KF41WaTnKIcgoZav8Fh0ZSDR66hj0IxAE1/n5ztgtdujVat1MR2SOo/+TrLmhraE+HVKOK5WSZtL1/gITJ8jtnFDSMDE/zWpAnRIrJqrOX62x5bM6Uok8eYXxTMTEAVMSD/HdDtnCSFmzeKHpXiHigbmnkVFclthY=',
        region_name='us-east-1'  # Optional: specify the AWS region 
    )
    
    # Initialize the SNS client
    client = session.client('sns')
    
    # Define the email message
    full_message = f"{message} for member ID: {memberID}"
    
    # Send the email
    response = client.publish(
        TopicArn='arn:aws:sns:us-east-1:227008985806:test',  # Update with your SNS topic ARN
        Message=full_message,
        Subject=message
    )
    
    # Print the response
    print("Email notification sent:", response)

if __name__ == '__main__':
    memberID = '123456'
    memberDob = '01/01/1980'
    service_value = '99214 - Office O/P Est Mod 30-39 Min'
    login_and_set_options(memberID, memberDob, service_value)
