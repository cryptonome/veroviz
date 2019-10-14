from veroviz._common import *

from veroviz._getSnapLoc import privGetSnapLocBatch

from veroviz._internal import locs2Dict
from veroviz._internal import loc2Dict

from veroviz.utilities import initDataframe

def privCreateNodesFromLocs(locs=None, initNodes=None, nodeType=None, nodeName=None, startNode=1, incrementName=False, incrementStart=1, snapToRoad=False, dataProvider=None, dataProviderArgs=None, leafletIconPrefix=VRV_DEFAULT_LEAFLETICONPREFIX, leafletIconType=VRV_DEFAULT_LEAFLETICONTYPE, leafletColor=VRV_DEFAULT_LEAFLETICONCOLOR, leafletIconText=None, cesiumIconType=VRV_DEFAULT_CESIUMICONTYPE, cesiumColor=VRV_DEFAULT_CESIUMICONCOLOR, cesiumIconText=None):

	"""
	Given a set of nodes lats and lons, return a node dataframe

	Parameters
	----------
	locs: list of lists, Required, default as None
		A list of locations, in the form of [[lat, lon, alt], [lat, lon, alt], ...] or [[lat, lon], [lat, lon], ...]
	initNodes: :ref:`Nodes`, Optional, default as None
		A dataframe containing an existing set of nodes. If `initNodes` is provided, this function will extend to that dataframe.
	nodeType: string, Optional, default as None
		A user-defined text field that can be used to classify nodes. This field is to categorize a batch of nodes (e.g., "restaurants"). If provided, all nodes generated by the `generateNodes()` function call will be given this value. The nodeType is not used by VeRoViz explicitly. 
	nodeName: string, Optional, default as None
		The name of all nodes that are to be generated by this function call. This field is a more detailed description (e.g., "pizza" or "steakhouse"). The nodeName is not used by VeRoViz explicitly. 
	startNode: int, Optional, default as 1
		The starting node number will be the maximum of startNode and any id values contained in the initNodes dataframe (if provided).  
	incrementName: boolean, Optional, default as False
		Toggle to choose if we add increment after nodeName, e.g. 'customer1', 'customer2',...
	incrementStart: int, Optional, default as 1
		The starting number of the increment.
	leafletIconPrefix: string, Optional, default as "glyphicon"
		The collection of Leaflet icons.  Options are "glyphicon" or "fa". See :ref:`Leaflet style`
	leafletIconType: string, Optional, default as "info-sign"
		The specific icon to be used for all generated nodes.  The list of available options depends on the choice of the leafletIconType. See :ref:`Leaflet style`
	leafletColor: string, Optional, default as "blue"
		The icon color of the generated nodes when displayed in Leaflet. One of a collection of pre-specified colors. See :ref:`Leaflet style`
	leafletIconText: string, Optional, default as None
		Text that will be displayed within the node on a Leaflet map. See :ref:`Leaflet style`
	cesiumIconType: string, Optional, default as "pin"
		'pin' is the only option right now. See :ref:`Cesium style`
	cesiumColor: string, Optional, default as "Cesium.Color.BLUE"
		The color of the generated nodes when displayed in Cesium.  One of a collection of pre-specified colors. See :ref:`Cesium style`
	cesiumIconText: string, Optional, default as None
		Text that will be displayed within the node on a Cesium map. See :ref:`Cesium style`

	Return
	------
	:ref:`Nodes`
		A Nodes dataframe with given list of coordinates
	"""

	# Number of nodes
	numNodes = len(locs)

	# Define ids and nodeNames
	if (type(initNodes) is pd.core.frame.DataFrame):
		if (len(initNodes) > 0):
			maxID = max(initNodes['id'])
			startNode = max([maxID + 1, startNode])

	ids = [n for n in range(startNode, startNode + numNodes)]
	if (incrementName):
		nodeNames = [(nodeName + "%s" % (n)) for n in range(incrementStart, incrementStart + numNodes)]
	else:
		nodeNames = [nodeName] * numNodes

	# Snap to road
	# FIXME! - Issue #28 - Multiple nodes might be snapped to the same location 
	if (snapToRoad):
		locs = privGetSnapLocBatch(locs=locs, dataProvider=dataProvider, dataProviderArgs=dataProviderArgs)

	# node dataframe
	nodes = initDataframe('Nodes')

	# generate nodes
	dicLocs = locs2Dict(locs)
	for i in range(len(locs)):
		nodes = nodes.append({
			'id': ids[i],
			'lat': dicLocs[i]['lat'],
			'lon': dicLocs[i]['lon'],
			'altMeters': dicLocs[i]['alt'],
			'nodeName': nodeNames[i],
			'nodeType': nodeType,
			'leafletIconPrefix': leafletIconPrefix,
			'leafletIconType': leafletIconType,
			'leafletColor': leafletColor,
			'leafletIconText': leafletIconText if (leafletIconText != None) else ids[i],
			'cesiumIconType': cesiumIconType,
			'cesiumColor': cesiumColor,
			'cesiumIconText': cesiumIconText if (cesiumIconText != None) else ids[i]
			}, ignore_index=True)

	# if the user provided an initNode dataframe, add the new points after it
	if (type(initNodes) is pd.core.frame.DataFrame):
		nodes = pd.concat([initNodes, nodes], ignore_index=True)

	return nodes

def privCreateArcsFromLocSeq(locSeq=None, initArcs=None, startArc=1, leafletColor=VRV_DEFAULT_LEAFLETARCCOLOR, leafletWeight=VRV_DEFAULT_LEAFLETARCWEIGHT, leafletStyle=VRV_DEFAULT_LEAFLETARCSTYLE, leafletOpacity=VRV_DEFAULT_LEAFLETARCOPACITY, useArrows=True, cesiumColor=VRV_DEFAULT_CESIUMPATHCOLOR, cesiumWeight=VRV_DEFAULT_CESIUMPATHWEIGHT, cesiumStyle=VRV_DEFAULT_CESIUMPATHSTYLE, cesiumOpacity=VRV_DEFAULT_CESIUMPATHOPACITY):

	"""
	Create an Arc dataframe from a list of arcs with coordinates

	Parameters
	----------
	locSeq: list, Required, default as None
		A list of locs that is going to be created, the format is [[lat1, lon1], [lat2, lon2], ...]
	initArcs: :ref:`Arcs`, Optional, default as None
		An Arcs dataframe, if provided, the arcs to be created will append to this dataframe.
	startArc: int, Optional, default as 1
		The start index for the arcs
	leafletColor: string, Optional, default as "orange"
		The color of generated route when displayed in Leaflet.  One of a collection of pre-specified colors. See :ref:`Leaflet style`
	leafletWeight: int, Optional, default as 3
		The weight of generated route when displayed in Leaflet. See :ref:`Leaflet style`
	leafletStyle: string, Optional, default as 'solid'
		The line style of generated route, options are 'solid', 'dotted', 'dashed'. See :ref:`Leaflet style`
	leafletOpacity: float in [0, 1], Optional, default as 0.8
		The opacity of generated route when displayed in Leaflet, range from 0 (invisible) to 1. See :ref:`Leaflet style`
	useArrows: bool, Optional, default as True
		To add arrows to arcs that generated, set `useArrows` to be True.
	cesiumColor: string, Optional, default as "Cesium.Color.ORANGE"
		The color of the generated route when displayed in Cesium.  One of a collection of pre-specified colors. See :ref:`Cesium Style`
	cesiumWeight: int, Optional, default as 3
		The weight of the generated route when displayed in Cesium. See :ref:`Cesium Style`
	cesiumStyle: string, Optional, default as 'solid'
		The line style of the generated route when displayed in Cesium., options are 'solid', 'dotted', 'dashed'. See :ref:`Cesium Style`
	cesiumOpacity: float in [0, 1], Optional, default as 0.8
		The opacity of generated route when displayed in Cesium, range from 0 (invisible) to 1. See :ref:`Cesium Style`

	Return
	------
	:ref:`Arcs`
		An Arcs dataframe

	Examples
	--------
	>>> import veroviz as vrv
	>>> arcs = vrv.createArcsFromList(
	...     locSeq=[
	...         [42.1325, -78.2134], 
	...         [42.5341, -78.3252],
	...         [42.3424, -78.6424]
	...     ])
	"""


	# Number of arcs
	numArcs = len(locSeq)

	# Define odIDs
	if (type(initArcs) is pd.core.frame.DataFrame):
		if (len(initArcs) > 0):
			maxOdID = max(initArcs['odID'])
			startArc = max(maxOdID + 1, startArc)
	odIDs = [n for n in range(startArc, startArc + numArcs)]

	# arc dataframe
	arcs = initDataframe('Arcs')

	# generate arcs
	for i in range(len(locSeq) - 1):
		arcs = arcs.append({
			'odID': odIDs[i],
			'startLat': locSeq[i][0],
			'startLon': locSeq[i][1],
			'endLat': locSeq[i + 1][0],
			'endLon': locSeq[i + 1][1],
			'leafletColor' : leafletColor,
			'leafletWeight' : leafletWeight,
			'leafletStyle' : leafletStyle,
			'leafletOpacity' : leafletOpacity,
			'cesiumColor' : cesiumColor,
			'cesiumWeight' : cesiumWeight,
			'cesiumStyle' : cesiumStyle,
			'cesiumOpacity' : cesiumOpacity,
			'useArrows': useArrows
			}, ignore_index=True)

	# if the user provided an initNode dataframe, add the new points after it
	if (type(initArcs) is pd.core.frame.DataFrame):
		arcs = pd.concat([initArcs, arcs], ignore_index=True)

	return arcs