import time
from datetime import datetime
import random


import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException

timestamp = datetime.now().strftime("%m%d%H%M%S")
email = f"testqa{timestamp}@mailinator.com"
inbox_name = email.split("@")[0]
agency_email = f"agency{timestamp}@mailinator.com"

phone = str(random.randint(9846000015, 9846999919))

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(5)

driver.get("https://authorized-partner.vercel.app/register")
driver.maximize_window()



driver.find_element(By.XPATH, "//button[@id='remember']").click()

driver.find_element(By.XPATH, "//button[normalize-space()='Continue']").click()

#Filling the Details of the Set up your Account Page

#to fill the phone no first to verify it
wait = WebDriverWait(driver, 20)

phone_input = wait.until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "input[name='phoneNumber']")
    )
)
phone_input.clear()
phone_input.send_keys(phone)


# #to fill the first name
wait = WebDriverWait(driver, 10)

first_name_input = wait.until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "input[name='firstName']")
    )
)
first_name_input.clear()
first_name_input.send_keys("Max")


#to fill the last name
wait = WebDriverWait(driver, 10)

last_name_input = wait.until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "input[name='lastName']")
    )
)
last_name_input.clear()
last_name_input.send_keys("Parker")

#to fill the email address
wait = WebDriverWait(driver, 10)

email_input = wait.until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "input[name='email']")
    )
)
email_input.clear()
email_input.send_keys(email)


#to fill the password
wait = WebDriverWait(driver, 10)

password_input = wait.until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "input[name='password']")
    )
)
password_input.clear()
password_input.send_keys("Max9898@")

#to fill the confirm password
wait = WebDriverWait(driver, 10)

confirm_password_input = wait.until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "input[name='confirmPassword']")
    )
)
confirm_password_input.clear()
confirm_password_input.send_keys("Max9898@")

#To click the next button on first page
driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

#wait until the otp verification page is loaded
wait.until(
    EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "input[data-input-otp='true']")
    )
)
print("  OTP input visible")

#function to retrieve the otp code

def get_otp_from_mailinator(driver, inbox_name, main_window):
    print("  Opening Mailinator to fetch OTP...")

    wait = WebDriverWait(driver, 15)
    # Open Mailinator in new tab
    driver.execute_script("window.open('https://www.mailinator.com', '_blank')")
    driver.switch_to.window(driver.window_handles[-1])

    wait = WebDriverWait(driver, 15)
    # Open the public inbox
    driver.get(f"https://www.mailinator.com/v4/public/inboxes.jsp?to={inbox_name}")


    otp_code = None

    # Try for up to 60 seconds
    for attempt in range(12):
        time.sleep(5)

        emails = driver.find_elements(By.CSS_SELECTOR, "tr.ng-scope")

        if emails:
            emails[0].click()  # Open latest email
            time.sleep(2)

            # Mailinator email body is inside iframe
            iframes = driver.find_elements(By.TAG_NAME, "iframe")

            for iframe in iframes:
                driver.switch_to.frame(iframe)
                body_text = driver.find_element(By.TAG_NAME, "body").text
                driver.switch_to.default_content()

                # Extract 6-digit OTP
                match = re.search(r"\b\d{6}\b", body_text)
                if match:
                    otp_code = match.group()
                    print(f"  OTP found: {otp_code}")
                    break

        if otp_code:
            break

        print(f"  Waiting for OTP... ({(attempt + 1) * 5}s)")
        driver.refresh()

    # Close Mailinator tab
    driver.close()
    driver.switch_to.window(main_window)

    if not otp_code:
        raise Exception("OTP not received within 60 seconds")

    return otp_code

#save the handle of the current window
main_window = driver.current_window_handle

otp_code = get_otp_from_mailinator(driver, inbox_name, main_window)

print("OTP received:", otp_code)

wait = WebDriverWait(driver, 15)

# Wait for OTP input field
otp_input = wait.until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "input[data-input-otp='true']")
    )
)

# Focus input
otp_input.click()

# Type OTP digit by digit (required by OTP libraries)
for digit in otp_code:
    otp_input.send_keys(digit)


verify_btn = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//button[normalize-space()='Verify Code']")
    )
)

driver.execute_script("arguments[0].click();", verify_btn)

print("OTP verified successfully")

#Filling the Details of the Agency Details Page

#to fill the name of the agency
wait = WebDriverWait(driver, 10)

agency_name_input = wait.until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "input[name='agency_name']")
    )
)
agency_name_input.clear()
agency_name_input.send_keys("ABC Education Services")

#to fill the role in the agency
wait = WebDriverWait(driver, 10)

role_input = wait.until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "input[name='role_in_agency']")
    )
)
role_input.clear()
role_input.send_keys("Director")

#to fill the email address of the agency
wait = WebDriverWait(driver, 10)

agency_email_input = wait.until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "input[name='agency_email']")
    )
)
agency_email_input.clear()
agency_email_input.send_keys(agency_email)

#to fill the website of the agency
wait = WebDriverWait(driver, 10)

agency_website_input = wait.until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "input[name='agency_website']")
    )
)
agency_website_input.clear()
agency_website_input.send_keys("www.abceducation.com")

#to fill the adress of the agency
wait = WebDriverWait(driver, 10)

agency_address_input = wait.until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "input[name='agency_address']")
    )
)
agency_address_input.clear()
agency_address_input.send_keys("Thamel, Kathmandu, Nepal")

#to select the agency region of operation of the custom dropdown using button
wait = WebDriverWait(driver, 15)

# Open region dropdown
region_dropdown = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[role="combobox"]'))
)
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", region_dropdown)
region_dropdown.click()

try:
    # Wait for the dropdown option "Nepal" and click it
    nepal_option = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//*[(@role='option' or self::div or self::span or self::li) "
            "and normalize-space()='Nepal']"
        ))
    )

    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", nepal_option)
    nepal_option.click()

    # Optional: verify Nepal is selected
    wait.until(
        EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, 'button[role="combobox"]'),
            "Nepal"
        )
    )

    print("  Region       : Nepal")

except TimeoutException:
    print("  Region       : Nepal option was not found or not selected")
    raise

#To click the next button on first page
driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()


#Filling the Details of the Professional ExperiencePage

#selecting the years of experience from the dropdown menu 
exp_level = "2 years"

# Wait until the professional experience page is loaded
wait.until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, "input[name='number_of_students_recruited_annually']")
    )
)

experience_dropdown = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "(//button[@role='combobox' and not(@disabled)])[last()]")
    )
)
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", experience_dropdown)
driver.execute_script("arguments[0].click();", experience_dropdown)

experience_option_xpath = (
    "//*[@role='option' and contains("
    "translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), "
    f"'{exp_level}'"
    ")]"
)
experience_option = wait.until(EC.element_to_be_clickable((By.XPATH, experience_option_xpath)))
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", experience_option)
experience_option.click()
print(f"  Experience  : {exp_level}")
time.sleep(0.5)

#filling the no of students recurited anually
wait = WebDriverWait(driver, 10)

num_student_input = wait.until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "input[name='number_of_students_recruited_annually']")
    )
)
num_student_input.clear()
num_student_input.send_keys("100")

#filling the focus area detail
wait = WebDriverWait(driver, 10)

focusarea_input = wait.until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "input[name='focus_area']")
    )
)
focusarea_input.clear()
focusarea_input.send_keys("Undergraduate admissions to Canada and Australia")


#filling the success metrics detail
wait = WebDriverWait(driver, 10)

success_input = wait.until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "input[name='success_metrics']")
    )
)
success_input.clear()
success_input.send_keys("90")

#ticking all the boxes in Services Provided
service_cbs = driver.find_elements(By.CSS_SELECTOR, 'button[role="checkbox"]')
for cb in service_cbs:
    if cb.get_attribute("data-state") == "unchecked":
        cb.click()
        time.sleep(0.2)
print("  Services    : all checked")

#submit the detail fillled by clicking next
driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

#Filling the Details of the  Verification and Preferences

#filling the business registration number
wait = WebDriverWait(driver, 10)

reg_num_input = wait.until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "input[name='business_registration_number']")
    )
)
reg_num_input.clear()
reg_num_input.send_keys("REG-2024-12345")


# Open the Preferred Countries dropdown and select a country
preferred_country = "Australia"

driver.find_element(By.CSS_SELECTOR, 'button[role="combobox"]').click()
time.sleep(1.5)

try:
    country_option = driver.find_element(
        By.XPATH,
        f"//*[@role='option'][contains(normalize-space(.), '{preferred_country}')]"
    )
    country_option.click()
    print(f"  Country     : {preferred_country}")
except NoSuchElementException:
    # If the exact country is not available, pick the first option
    dialog = driver.find_element(By.CSS_SELECTOR, '[role="dialog"]')
    first_option = dialog.find_element(By.XPATH, ".//div[span]")
    first_option.click()
    print("  Country     : first available option selected")

time.sleep(0.5)



#filling the Certification Detail
wait = WebDriverWait(driver, 10)

certf_detail_input = wait.until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "input[name='certification_details']")
    )
)
certf_detail_input.clear()
certf_detail_input.send_keys("ICEF Certified Education Agent")

# Tick all four "Preferred Institution Types" checkboxes
institution_cbs = driver.find_elements(By.CSS_SELECTOR, 'button[role="checkbox"]')
for cb in institution_cbs:
    if cb.get_attribute("data-state") == "unchecked":
        cb.click()
        time.sleep(0.2)
print("  Institutions  : all checked")

#to upload a doc file in the upload business documents
file_path = "/home/kaushalendra/Vrit/sample.doc"
file_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="file"]')
if file_inputs:
    driver.execute_script(
        "arguments[0].style.display = 'block'; arguments[0].style.opacity = '1';",
        file_inputs[0]
    )
file_inputs[0].send_keys(file_path)
print(" Document    :  uploaded")
time.sleep(1)

#to click the submit button and submit the whole form 
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()



time.sleep(15)
driver.close()
