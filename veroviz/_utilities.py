from veroviz._common import *
from veroviz._internal import *

def privConvertDistance(distance, fromUnits, toUnits):
	
	try:
		fromUnits = fromUnits.lower()
	except:
		pass

	fromUnits = distanceUnitsDictionary[fromUnits]
	if (fromUnits == 'm'):
		tmpDist = distance * 1.0
	elif (fromUnits == 'km'):
		tmpDist = distance * VRV_CONST_METERS_PER_KILOMETER
	elif (fromUnits == 'mi'):
		tmpDist = distance * VRV_CONST_METERS_PER_MILE
	elif (fromUnits == 'ft'):
		tmpDist = distance * VRV_CONST_METERS_PER_FEET
	elif (fromUnits == 'yard'):
		tmpDist = distance * VRV_CONST_METERS_PER_YARD
	elif (fromUnits == 'nmi'):
		tmpDist = distance * VRV_CONST_METERS_PER_NAUTICAL_MILE

	try:
		toUnits = toUnits.lower()
	except:
		pass
		
	toUnits = distanceUnitsDictionary[toUnits]
	if (toUnits == 'm'):
		convDist = tmpDist / 1.0
	elif (toUnits == 'km'):
		convDist = tmpDist / VRV_CONST_METERS_PER_KILOMETER
	elif (toUnits == 'mi'):
		convDist = tmpDist / VRV_CONST_METERS_PER_MILE
	elif (toUnits == 'ft'):
		convDist = tmpDist / VRV_CONST_METERS_PER_FEET
	elif (toUnits == 'yard'):
		convDist = tmpDist / VRV_CONST_METERS_PER_YARD
	elif (toUnits == 'nmi'):
		convDist = tmpDist / VRV_CONST_METERS_PER_NAUTICAL_MILE

	return convDist
	

def privConvertSpeed(speed, fromUnitsDist, fromUnitsTime, toUnitsDist, toUnitsTime):
	
	try:
		fromUnitsDist = fromUnitsDist.lower()
	except:
		pass
	
	fromUnitsDist = distanceUnitsDictionary[fromUnitsDist]
	if (fromUnitsDist == 'm'):
		tmpSpeed = speed * 1.0
	elif (fromUnitsDist == 'km'):
		tmpSpeed = speed * VRV_CONST_METERS_PER_KILOMETER
	elif (fromUnitsDist == 'mi'):
		tmpSpeed = speed * VRV_CONST_METERS_PER_MILE
	elif (fromUnitsDist == 'ft'):
		tmpSpeed = speed * VRV_CONST_METERS_PER_FEET
	elif (fromUnitsDist == 'yard'):
		tmpSpeed = speed * VRV_CONST_METERS_PER_YARD
	elif (fromUnitsDist == 'nmi'):
		tmpSpeed = speed * VRV_CONST_METERS_PER_NAUTICAL_MILE

	try:
		fromUnitsTime = fromUnitsTime.lower()
	except:
		pass

	fromUnitsTime = timeUnitsDictionary[fromUnitsTime]
	if (fromUnitsTime == 's'):
		tmpSpeed = tmpSpeed / 1.0
	elif (fromUnitsTime == 'min'):
		tmpSpeed = tmpSpeed / VRV_CONST_SECONDS_PER_MINUTE
	elif (fromUnitsTime == 'h'):
		tmpSpeed = tmpSpeed / VRV_CONST_SECONDS_PER_HOUR

	try:
		toUnitsDist = toUnitsDist.lower()
	except:
		pass

	toUnitsDist = distanceUnitsDictionary[toUnitsDist]
	if (toUnitsDist == 'm'):
		tmpSpeed = tmpSpeed / 1.0
	elif (toUnitsDist == 'km'):
		tmpSpeed = tmpSpeed / VRV_CONST_METERS_PER_KILOMETER
	elif (toUnitsDist == 'mi'):
		tmpSpeed = tmpSpeed / VRV_CONST_METERS_PER_MILE
	elif (toUnitsDist == 'ft'):
		tmpSpeed = tmpSpeed / VRV_CONST_METERS_PER_FEET
	elif (toUnitsDist == 'yard'):
		tmpSpeed = tmpSpeed / VRV_CONST_METERS_PER_YARD
	elif (toUnitsDist == 'nmi'):
		tmpSpeed = tmpSpeed / VRV_CONST_METERS_PER_NAUTICAL_MILE

	try:
		toUnitsTime = toUnitsTime.lower()
	except:
		pass

	toUnitsTime = timeUnitsDictionary[toUnitsTime]
	if (toUnitsTime == 's'):
		convSpeed = tmpSpeed * 1.0
	elif (toUnitsTime == 'min'):
		convSpeed = tmpSpeed * VRV_CONST_SECONDS_PER_MINUTE
	elif (toUnitsTime == 'h'):
		convSpeed = tmpSpeed * VRV_CONST_SECONDS_PER_HOUR

	return convSpeed
		
	
def privConvertTime(time, fromUnits, toUnits):
	try:
		fromUnits = fromUnits.lower()
	except:
		pass
		
	fromUnits = timeUnitsDictionary[fromUnits]
	if (fromUnits == 's'):
		tmpTime = time * 1.0
	elif (fromUnits == 'min'):
		tmpTime = time * VRV_CONST_SECONDS_PER_MINUTE
	elif (fromUnits == 'h'):
		tmpTime = time * VRV_CONST_SECONDS_PER_HOUR

	try:
		toUnits = toUnits.lower()
	except:
		pass
		
	toUnits = timeUnitsDictionary[toUnits]
	if (toUnits == 's'):
		convTime = tmpTime / 1.0
	elif (toUnits == 'min'):
		convTime = tmpTime / VRV_CONST_SECONDS_PER_MINUTE
	elif (toUnits == 'h'):
		convTime = tmpTime / VRV_CONST_SECONDS_PER_HOUR

	return convTime
	

def privGetMapBoundary(nodes, arcs, locs):
	
	# Adjust the scope of the map to proper
	allLats = []
	allLons = []
	if (nodes is not None):
		allLats.extend(nodes['lat'].tolist())
		allLons.extend(nodes['lon'].tolist())

	if (arcs is not None):
		allLats.extend(arcs['startLat'].tolist())
		allLats.extend(arcs['endLat'].tolist())
		allLons.extend(arcs['startLon'].tolist())
		allLons.extend(arcs['endLon'].tolist())

	if (locs is not None):
		for i in range(len(locs)):
			allLats.append(locs[i][0])
			allLons.append(locs[i][1])

	maxLat = max(allLats)
	minLat = min(allLats)
	maxLon = max(allLons)
	minLon = min(allLons)

	if (abs(maxLat - minLat) < 0.0001):
		maxLat = maxLat + 0.05
		minLat = minLat - 0.05
	if (abs(maxLon - minLon) < 0.0001):
		maxLon = maxLon + 0.05
		minLon = minLon - 0.05

	maxLat = maxLat + 0.01
	minLat = minLat - 0.01
	maxLon = maxLon + 0.01
	minLon = minLon - 0.01

	return [[minLat, maxLon], [maxLat, minLon]]
	
	
def privInitDataframe(dataframeType):
	
	try:
		dataframeType = dataframeType.lower()
	except:
		pass
	
	if (dataframeType == 'nodes'):
		dataframe = pd.DataFrame(
			columns=nodesColumnList)
	elif (dataframeType == 'assignments'):
		dataframe = pd.DataFrame(
			columns=assignmentsColumnList)
	elif (dataframeType == 'arcs'):
		dataframe = pd.DataFrame(
			columns=arcsColumnList)
	else:
		return

	return dataframe	
	
	
def privExportDataframe(dataframe, filename):
	
	# Replace backslash
	filename = replaceBackslashToSlash(filename)

	if (type(filename) is not str):
		print("Error: filename should be a string, please check the inputs.")
		return

	# Get directory
	if ("/" in filename):
		path = ""
		pathList = filename.split('/')
		if (len(pathList) > 1):
			for i in range(len(pathList) - 1):
				path = path + pathList[i] + '/'
			if not os.path.exists(path):
				os.makedirs(path, exist_ok=True)

	try:
		dataframe.to_csv(path_or_buf=filename, encoding='utf-8')
		if (VRV_SETTING_SHOWOUTPUTMESSAGE):
			print("Message: Data written to %s." % (filename))
	except:
		print("Error: Cannot export dataframe, please check the inputs.")

	return	