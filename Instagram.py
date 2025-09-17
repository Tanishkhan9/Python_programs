from instabot import Bot

# Create a bot instance
bot = Bot()

# Login to Instagram (requires username & password)
bot.login(username="your_username", password="your_password")

# Send a message
bot.send_message("Hello from Python 🚀", ["friend_username"])

print("Message sent successfully!")
