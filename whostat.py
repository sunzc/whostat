#!/bin/env python

class WorkDay:
	def __init__(self, dt):
		self.date = dt
		self.periods = []
		self.total_time = 0
	def get_length(self):
		ttime = 0.0
		for pd in self.periods:
			ttime += pd.get_length()
		self.total_time = ttime
		return ttime

class Period:
	def __init__(self, st, et):
		self.st = st	# start time
		self.et = et	# end time
	def get_length(self):
		return (self.et - self.st + 1)/2.0

class OsHacker:
	def __init__(self, name):
		self.netID = name
		self.total_time = 0
		self.avg_wt = 0
		self.workdays = []

	def commit_a_period(self, pd, date):
		lw = len(self.workdays)
		if (lw != 0 and self.workdays[lw - 1].date == date) :
			self.workdays[lw - 1].periods.append(pd)
		else:
			wd = WorkDay(date)
			wd.periods.append(pd)
			self.workdays.append(wd)

	def do_statistic(self):
		ttime = 0.0
		for wd in self.workdays:
			ttime += wd.get_length()
		self.total_time = ttime

	def show_job(self):
		self.do_statistic()
		print "OS hacker: " + self.netID
		print "Total time : " + str(self.total_time)
		for wd in self.workdays:
			if wd.date > 25:
				print "Nov " + str(wd.date)
			else:
				print "Dec " + str(wd.date)
			print "  time in a day: " + str(wd.get_length())
			for pd in wd.periods:
				print "     " + str(pd.st/2.0) + "--" + str(pd.et/2.0)

		print ""

class Record:
	def __init__(self):
		self.namelist = []
		self.time = 0
		self.date = 0
	def show(self):
		print "record " + str(self.date) + " " + str(self.time) + " " + str(self.namelist)

class RecordHandler:
	def __init__(self, logfile):
		self.fd = open(logfile, 'r')	# log file, record who is on the server every half hour
		self.init_date = 28	# record which day it is
		self.init_time = 3	# record which hour it is
		self.cur_date = self.init_date	# record which day it is
		self.cur_time = self.init_time	# record which hour it is
		self.os_hackers = {}

	def handle_log(self):
		rc = self.get_a_record()
		n2p = {}	# name to period
		while(rc != None):
			# rc.show()
			if rc.time == 0:	# a new day, it's time to commit a period
				# print "rc.time == 0"
				for name in n2p:
					if n2p[name] != None:
						if name not in self.os_hackers:
							os_hacker = OsHacker(name)
							self.os_hackers[name] = os_hacker
						new_date = self.get_date() - 1
						if (new_date == 0):
							new_date = 30
						self.os_hackers[name].commit_a_period(n2p[name], new_date)
						n2p[name] = None
			for name in n2p:
				if n2p[name] != None:	# on-line students half an hour ago
					if name in rc.namelist:	# still on-line, period continues
						n2p[name].et += 1
					else:	# offline, the end of a period
						if name not in self.os_hackers:
							os_hacker = OsHacker(name)
							self.os_hackers[name] = os_hacker
						self.os_hackers[name].commit_a_period(n2p[name], self.get_date())
						n2p[name] = None

			for name in rc.namelist:
				if (name not in n2p) or (n2p[name] == None):	# already handled
					pd = Period(rc.time, rc.time)
					n2p[name] = pd

			rc = self.get_a_record()

	def get_a_record(self):
		rc = Record()
		namelist = []
		line = self.fd.readline()
		while(line != "" and line != "\n"):
			name = line.split()[0]
			if name not in namelist:
				namelist.append(name)
			line = self.fd.readline()

		rc.namelist = namelist
		rc.time = self.get_time()
		rc.date = self.get_date()
		self.inc_time()

		if line == "" and namelist == []:
			return None
		else:
			return rc
		
	def get_date(self):
		return self.cur_date

	def get_time(self):
		return self.cur_time

	def inc_time(self):
		new_time = self.cur_time + 1
		if (new_time % 48 == 0):	# every half an hour
			new_date = self.cur_date + 1
			if new_date == 31:
				new_date = 1
			self.cur_date = new_date
			new_time = 0

		self.cur_time = new_time 

if __name__ == "__main__":
	rh = RecordHandler("who.txt")
	rh.handle_log()

	for os_hacker in rh.os_hackers:
		rh.os_hackers[os_hacker].do_statistic()
		if rh.os_hackers[os_hacker].total_time > 30.0:
			rh.os_hackers[os_hacker].show_job()
