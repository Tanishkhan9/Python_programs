from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Open Instagram
driver = webdriver.Chrome()  # make sure chromedriver is installed
driver.get("https://www.instagram.com/")

# Login
time.sleep(3)
driver.find_element(By.NAME, "username").send_keys("your_username")
driver.find_element(By.NAME, "password").send_keys("your_password", Keys.RETURN)

# Wait for login
time.sleep(5)

# Go to DM page
driver.get("https://www.instagram.com/direct/inbox/")

time.sleep(5)
# Click "Send Message"
driver.find_element(By.XPATH, "//div[text()='Send message']").click()

time.sleep(2)
# Enter username
search_box = driver.find_element(By.NAME, "queryBox")
search_box.send_keys("friend_username")
time.sleep(2)

# Select user
driver.find_element(By.XPATH, f"//div[text()='friend_username']").click()

# Next button
driver.find_element(By.XPATH, "//div[text()='Chat']").click()
time.sleep(2)

# Type and send message
msg_box = driver.find_element(By.TAG_NAME, "textarea")
msg_box.send_keys("Hello! This is an automated Instagram message 🐍")
msg_box.send_keys(Keys.RETURN)

print("Message sent successfully!")
