def echo_sticker(update, context):
    """Echo the user Sticker message."""
    #print(update.message)
    #print(update.message.sticker.set_name)
    #print(context.bot)
    #sticker_set = context.bot.get_sticker_set(update.message.sticker.set_name)
    #for sticker in sticker_set.stickers:
    #   try:
    #       s_file = sticker.get_file()
    #       s_file.download()
    #    except:
    #        print("failed to download sticker"+s_file.file_path)
    update.message.reply_sticker(update.message.sticker)

def echo_text(update, context):
    """Echo the user message."""
    #update.effective_user
    #print(update.message)
    update.message.reply_text(update.message.text)


from telegram.ext import MessageHandler, Filters

handlers = { Filters.text : echo_text,
			 Filters.sticker: echo_sticker }

def init(dispatcher):
	for x,y in handlers.items():
		dispatcher.add_handler(MessageHandler(x,y))
