def error(update, context):
    """Log Errors caused by Updates."""
    print('Update "%s" caused error "%s"'%(update, context.error))

def init(dispatcher):
	dispatcher.add_error_handler(error)