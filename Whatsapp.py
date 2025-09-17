import pywhatkit as kit
import datetime

# Phone number with country code (example: +91 for India)
phone_number = "+1234567890"  # replace with the actual phone number

# Message to send
message = "Hello! This is an automated test message from Python 🚀"

# Get current time
now = datetime.datetime.now()
hour = now.hour
minute = now.minute + 2   # schedule 1 minute ahead

# Send message
kit.sendwhatmsg(phone_number, message, hour, minute)

print("Message scheduled successfully!")
