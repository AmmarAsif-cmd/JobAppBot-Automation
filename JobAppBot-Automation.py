import spacy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class IntelligentJobApplicationBot:
    def __init__(self):
        self.driver = self.initialize_driver()
        self.nlp = spacy.load("en_core_web_sm")

    def initialize_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-logging")
        return webdriver.Chrome(options=chrome_options)

    def random_delay(self):
        time.sleep(2)  

    def find_element_with_retry(self, selector, by=By.NAME):
        attempts = 0
        while attempts < 3:
            try:
                return self.driver.find_element(by, selector)
            except:
                attempts += 1
        return None

    def extract_information_from_text(self, detailed_text):
        doc = self.nlp(detailed_text)

        extracted_info = {}
        for ent in doc.ents:
            extracted_info[ent.label_] = ent.text

        return extracted_info

    def fill_out_fields_from_text(self, detailed_text):
        extracted_info = self.extract_information_from_text(detailed_text)

        for entity_type, value in extracted_info.items():
            field_element = self.find_element_with_retry(entity_type.lower())
            if field_element:
                print(f"Filling out {entity_type} with value: {value}")
                field_element.send_keys(value)
                self.random_delay()

    def attach_cv(self, cv_path):
        cv_keywords = ["cv", "resume"]
        for keyword in cv_keywords:
            cv_input = self.find_element_with_retry(keyword, by=By.XPATH)
            if cv_input:
                print(f"Attaching CV: {cv_path}")
                cv_input.send_keys(cv_path)
                self.random_delay()
                break

    def click_submit_button(self):
        submit_button = self.find_element_with_retry("submit", by=By.XPATH)
        if not submit_button:
            submit_button = self.find_element_with_retry("next", by=By.XPATH)
        if not submit_button:
            submit_button = self.find_element_with_retry("register", by=By.XPATH)
        if not submit_button:
            submit_button = self.find_element_with_retry("continue", by=By.XPATH)

        if submit_button:
            submit_button.click()
            self.random_delay()
            print("Clicked the submit/next/register button.")

    def simulate_human_behavior(self):
        pass

    def run_with_detailed_text_and_cv(self, detailed_text, cv_path):
        try:
            self.driver.get("https://testing-url.com")
            self.fill_out_fields_from_text(detailed_text)
            self.attach_cv(cv_path)
            self.click_submit_button()
            self.simulate_human_behavior()
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.driver.quit()
            print("Script execution completed.")


detailed_text_input = """
Name: Joe Biden
Email: testing@gmail.com
Phone: +4474432324
LinkedIn: https://www.linkedin.com/in/amal-asvsd/
Gender: Male
DOB: October 11, 1991
Nationality: Pakistan
Ethnicity: Asian
Motivation: Seeking new challenges and opportunities.
"""

cv_path_input = "/path/to/cv.pdf"  


bot = IntelligentJobApplicationBot()
bot.run_with_detailed_text_and_cv(detailed_text_input, cv_path_input)
