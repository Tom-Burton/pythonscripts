#!/usr/bin/python
import collections
import random

### user-configurable values ###
build_minutes = 15
day_hours = 10
builds_per_day = 400
runners_per_build = 6
sample_size = 1000
max_concurrency = 120
spot_price = 0.0068 #per hour
days_in_work_year = 252
idle_time = 4 #minutes
####

### variables only for running calculation ###
day_minutes = day_hours*60
usable_minutes = day_minutes-build_minutes
resultslist = []
cost = 0
total_idle =0
###

for sample in range(sample_size):
    result = collections.defaultdict(int)
    day = collections.defaultdict(int)
    idle = collections.defaultdict(int)
    for i in range(builds_per_day): #assign begin and end time to each build
        build_start = random.randint(0, usable_minutes)
        build_finish = build_start + build_minutes
        build_idle = build_finish + idle_time
        for j in range(build_start, build_finish): #record concurrency for builds
            day[j] += runners_per_build
        for k in range(build_finish, build_idle): #record idle minutes
            idle[k] += runners_per_build

    for minute in range(day_minutes): #summarize how many minutes have multiple jobs
        if day[minute] == 0 and idle[minute] != 0: #add idle time where accurate
            day[minute] += idle[minute]
            total_idle += idle[minute]
        result[day[minute]] += 1

    resultslist.append(result)


totals = collections.defaultdict(int)
average = collections.defaultdict(int)
for r in range(len(resultslist)):
    for x in range(day_minutes):
        totals[x] += resultslist[r][x]

for t in range(len(totals)):
    average[t] = totals[t]/sample_size


print("build time: ", build_minutes, " minutes")
print("day length: ", day_hours, " hours")
print("builds per day: ", builds_per_day)
print("runners per build: ", runners_per_build)
print("max concurrency: ", max_concurrency)
print("sample size: ", sample_size)
print("")

wait = 0
for i in range(len(average)):
    if average[i] != 0:
        avg = average[i]
        if i <= max_concurrency:
            print(avg, " minutes with ", i ," runners")
            cost += avg*i
        else:
            wait = wait + (avg*i)/runners_per_build
print(round(wait, 2), " minutes waiting for runners")
cpd = (cost/60)*spot_price
print("cost per day = ", round(cpd,2))
print("cost per year ", round(cpd*days_in_work_year,2))
print("Average idle minutes: ", (total_idle/sample_size)/runners_per_build)
