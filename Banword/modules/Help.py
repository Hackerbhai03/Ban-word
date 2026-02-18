from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from Banword import Banword as app

# Show Help Menu
@app.on_callback_query(filters.regex("^show_help$"))
async def show_help(_, query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Admin Commands", callback_data="help_admin")],
            [InlineKeyboardButton("Other Commands", callback_data="help_misc")],
            [InlineKeyboardButton("« Back", callback_data="back_to_start")]
        ]
    )
    await query.message.edit_text(
        "**Help Menu**\nSelect a category below:",
        reply_markup=keyboard
    )

# Admin Commands
@app.on_callback_query(filters.regex("^help_admin$"))
async def help_admin(_, query: CallbackQuery):
    await query.message.edit_text(
        """**Admin Commands:**
•owner = @Oyekanhaa""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("« Back", callback_data="show_help")]]
        )
    )


# Misc Commands
@app.on_callback_query(filters.regex("^help_misc$"))
async def help_misc(_, query: CallbackQuery):
    await query.message.edit_text(
        """**Other Commands:**
• /start - Start the bot
• /stats - Bot statistics
• /addsudo - Add sudo user
• /delsudo - Remove sudo""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("« Back", callback_data="show_help")]]
        )
    )
