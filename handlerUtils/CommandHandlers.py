from __future__ import unicode_literals
from ytdlMgr.youtubedlwrapper import YoutubeDownloadWrapper
from pathlib import Path

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def invokeDownloader(cbContext):
    context = cbContext.job.context
    query = context['query']
    update = context['update']
    botContext = context['botContext']

    if YoutubeDownloadWrapper.alreadyExistingJob(query, update.message.from_user) :
        botContext.bot.send_message(chat_id=update.effective_chat.id, text=("You have already queued %s!" % context['query']))
        return

    ydlWrapper = YoutubeDownloadWrapper();
    ydlWrapper.setDownloadParam(query, update.message.from_user )
    botContext.bot.send_message(chat_id=update.effective_chat.id, text=("Start Downloading %s!" % context['query']))
    ydlWrapper.startDownload();
    resultDict = ydlWrapper.getStatus();
    if resultDict['status'] == 'finished':
        botContext.bot.send_message(chat_id=update.effective_chat.id, text=("Done downloading %s! Now uploading...." % context['query']))
        with open(resultDict['filename'], 'rb') as fb:
            try:
                botContext.bot.send_document(chat_id=update.effective_chat.id, document=fb, filename='music.mp3', timeout=600)
            except telegram.error.TelegramError:
                botContext.bot.send_message(chat_id=update.effective_chat.id, text=("Error sending %s! :(" % context['query']))
    elif resultDict['status'] == 'error':
        botContext.bot.send_message(chat_id=update.effective_chat.id, text=("Failed downloading %s!" % context['query']))
    ydlWrapper.cleanup()
    #Todo:
    # 1: call wrapper
    # 2: set outtmpl to some 1-time hash
    # 3: actually download
    # 4: if no error, send result to user
    # else send error to user
    # also need some mutexes

def download(update, context):
    """parse and create a download instance"""

    dlContext = {};
    msgBody = context.args
    print("Message body received:")
    print(msgBody)
    if len(context.args) == 0:
        update.message.reply_text("""You must either provide URL to the video, or item to be queried!
        For example:
        /download https://www.youtube.com/watch?v=0Uhh62MUEic
        /download 宇多田ヒカル『One Last Kiss』""")
        return
    query = " ".join(context.args);

    dlContext['update'] = update;
    dlContext['query'] = query
    dlContext['botContext'] = context
    context.job_queue.run_custom(invokeDownloader, {}, context=dlContext);

    update.message.reply_text("Queued job for '%s'."%query)

def seejobs(update,context):
    print(context.job_queue)
    update.message.reply_text("""on99""")


handlers = { "start" : start,
             "help" : help,
             "download" : download,
             "jobs" : seejobs
             }

from telegram.ext import CommandHandler, MessageHandler, Filters

def init(dispatcher):
    for x,y in handlers.items():
        dispatcher.add_handler(CommandHandler(x,y))
    #dispatcher.add_handler(MessageHandler(Filters.command, defaultCommand))
