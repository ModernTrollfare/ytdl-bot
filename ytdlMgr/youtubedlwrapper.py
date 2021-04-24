import youtube_dl
import weakref
from pathlib import Path
import uuid

class YoutubeDownloadWrapper:

	__runningJobs = {}

	@classmethod
	def alreadyExistingJob(cls, query, uid):
		for x in cls.__runningJobs:
			if x.uid == uid and x.query == query:
				return True
		return False

	def setDownloadParam(self, query, uid):
		self.jobName = query;
		self.uid = uid;
		YoutubeDownloadWrapper.__runningJobs[query] = self
		basename = str(uuid.uuid4())
		self.ydl_opts['outtmpl'] = basename+".%(ext)s";
		self.outfilename = basename+".mp3"

	def startDownload(self):
		try:
			try:
				with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
					ydl.download([self.jobName])
			except youtube_dl.utils.DownloadError:
				self.ydl_opts['default_search'] = 'auto'
				with youtube_dl.YoutubeDL(self.ydl_opts) as ydlSearch:
					ydlSearch.download([self.jobName])
		except :
			print("error")
			return False

	def progressHook(self,status):
		self.status = status['status']
		if self.status == 'finished':
			self.progress = """Name : %s
			Converting to MP3
			"""
			self.preconvfilename = status['filename']
		elif self.status == 'downloading':
			if status['total_bytes'] != None:
				if status['total_bytes'] > 20*1024*1024:
					self.errorStr = "Filesize is greater than 20MB - Size %d" % (status['total_bytes'])
					YoutubeDownloadWrapper.__runningJobs['query'] = self
					raise ValueError("Filesize too large")
			elif status['total_bytes_estimate'] != None:
				if status['total_bytes_estimate'] > 20*1024*1024:
					self.errorStr = "Filesize is greater than 20MB - Estimated size %d" % (status['total_bytes'])
					YoutubeDownloadWrapper.__runningJobs['query'] = self
					raise ValueError("Filesize too large")
			#No problem
			self.progress = """Downloading:
			Name : %s
			Time : %d elapsed - %d left (estimated)
			"""
			self.dlpartfilename = status['tmpfilename']
			self.preconvfilename = status['filename']
		elif self.status == 'error':
			self.errorStr = "Error occurred during download."
		YoutubeDownloadWrapper.__runningJobs['query'] = self

	def getStatus(self):
		if self.status == 'error':
			return { "status": self.status,
					 "msg"   : self.errorStr }
		elif self.status == 'finished':
			return { "status": self.status,
					 "progress" : self.progress,
			 		 "filename": self.outfilename }
		else:
			return { "status": self.status,
					 "progress" : self.progress }

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self._finalizer()

	def remove(self):
		self._finalizer()

	@property
	def removed(self):
		return not self._finalizer.alive

	def cleanup(self):
		try:
			p = Path(self.preconvfilename);
			p.unlink();
		except:
			pass
		try:
			p = Path(self.dlpartfilename);
			p.unlink();
		except:
			pass
		try:
			p = Path(self.outfilename);
			p.unlink();
		except:
			pass
		try:
			del YoutubeDownloadWrapper.__runningJobs[self.jobName]
		except:
			pass


	def __init__(self):
		self.status = "pending"
		self.progress = ""
		self.errorStr = "No error...."
		self.jobName = ""
		self.uid = ""
		self.preconvfilename = ""
		self.dlpartfilename = ""
		self.outfilename = ""

		self.ydl_opts = {
		#'download_archive' : 'assets.log',
		'format': 'bestaudio/best',
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192',
		}],
		'progress_hooks': [self.progressHook],
		}
