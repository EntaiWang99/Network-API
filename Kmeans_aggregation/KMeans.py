from numpy import *  
import time  
import matplotlib.pyplot as plt  
  
  
# calculate Euclidean distance  
def euclDistance(vector1, vector2):  
	return sqrt(sum(power(vector2 - vector1, 2)))  

# init centroids with random samples  
def initCentroids(dataSet, k):  
	numSamples, dim = dataSet.shape   
	centroids = zeros((k, dim))  	
	for i in range(k):  
		index = int(random.uniform(0, numSamples)) 
		centroids[i, :] = dataSet[index, :]  
	return centroids  
  
# k-means cluster 
def kmeans(dataSet, k):  
	numSamples = dataSet.shape[0]  
    # first column stores which cluster this sample belongs to,  
    # second column stores the error between this sample and its centroid  
	clusterAssment = mat(zeros((numSamples, 2)))  
	clusterChanged = True  
  
    ## step 1: init centroids  
	centroids = initCentroids(dataSet, k) 
  
	while clusterChanged:  
		clusterChanged = False  
        ## for each sample  
		for i in range(numSamples):  #range
			minDist  = 100000.0  
			minIndex = 0  
            ## for each centroid  
            ## step 2: find the centroid who is closest  
			for j in range(k):  
				distance = euclDistance(centroids[j, :], dataSet[i, :])  
				if distance < minDist:  
					minDist  = distance  
					minIndex = j  
              
            ## step 3: update its cluster 

			if clusterAssment[i, 0] != minIndex:  
				clusterChanged = True  
				clusterAssment[i, :] = minIndex, minDist**2  
  
        ## step 4: update centroids  
		for j in range(k): 
			pointsInCluster = dataSet[nonzero(clusterAssment[:, 0].A == j)[0]]
			centroids[j, :] = mean(pointsInCluster, axis = 0) 
  
	print ('Congratulations, cluster complete!')  
	return centroids, clusterAssment  
  
# show your cluster only available with 2-D data 

def showCluster(dataSet, k, centroids, clusterAssment):  
	numSamples, dim = dataSet.shape  
	if dim != 2:  
		print ("Sorry! I can not draw because the dimension of your data is not 2!")  
		return 1  
  
	mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']  
	# mark = ['aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'black', \
		# 'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse','chocolate']
	if k > len(mark):  
		print ("Sorry! Your k is too large!")  
		return 1 
     
  
    # draw all samples  
	for i in range(numSamples):  
		markIndex = int(clusterAssment[i, 0])
		plt.plot(dataSet[i, 0], dataSet[i, 1], mark[markIndex])  
  
	mark = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']  
	# mark = ['aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'black', \
	# 	'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse','chocolate']

    # draw the centroids  
	for i in range(k):  
		plt.plot(centroids[i, 0], centroids[i, 1], mark[i], markersize = 12)  
  
	plt.show() 


# 'coral':                '#FF7F50',
# 'cornflowerblue':       '#6495ED',
# 'cornsilk':             '#FFF8DC',
# 'crimson':              '#DC143C',
# 'cyan':                 '#00FFFF',
# 'darkblue':             '#00008B',
# 'darkcyan':             '#008B8B',
# 'darkgoldenrod':        '#B8860B',
# 'darkgray':             '#A9A9A9',
# 'darkgreen':            '#006400',
# 'darkkhaki':            '#BDB76B',
# 'darkmagenta':          '#8B008B',
# 'darkolivegreen':       '#556B2F',
# 'darkorange':           '#FF8C00',
# 'darkorchid':           '#9932CC',
# 'darkred':              '#8B0000',
# 'darksalmon':           '#E9967A',
# 'darkseagreen':         '#8FBC8F',
# 'darkslateblue':        '#483D8B',
# 'darkslategray':        '#2F4F4F',
# 'darkturquoise':        '#00CED1',
# 'darkviolet':           '#9400D3',
# 'deeppink':             '#FF1493',
# 'deepskyblue':          '#00BFFF',
# 'dimgray':              '#696969',
# 'dodgerblue':           '#1E90FF',
# 'firebrick':            '#B22222',
# 'floralwhite':          '#FFFAF0',
# 'forestgreen':          '#228B22',
# 'fuchsia':              '#FF00FF',
# 'gainsboro':            '#DCDCDC',
# 'ghostwhite':           '#F8F8FF',
# 'gold':                 '#FFD700',
# 'goldenrod':            '#DAA520',
# 'gray':                 '#808080',
# 'green':                '#008000',
# 'greenyellow':          '#ADFF2F',
# 'honeydew':             '#F0FFF0',
# 'hotpink':              '#FF69B4',
# 'indianred':            '#CD5C5C',
# 'indigo':               '#4B0082',
# 'ivory':                '#FFFFF0',
# 'khaki':                '#F0E68C',
# 'lavender':             '#E6E6FA',
# 'lavenderblush':        '#FFF0F5',
# 'lawngreen':            '#7CFC00',
# 'lemonchiffon':         '#FFFACD',
# 'lightblue':            '#ADD8E6',
# 'lightcoral':           '#F08080',
# 'lightcyan':            '#E0FFFF',
# 'lightgoldenrodyellow': '#FAFAD2',
# 'lightgreen':           '#90EE90',
# 'lightgray':            '#D3D3D3',
# 'lightpink':            '#FFB6C1',
# 'lightsalmon':          '#FFA07A',
# 'lightseagreen':        '#20B2AA',
# 'lightskyblue':         '#87CEFA',
# 'lightslategray':       '#778899',
# 'lightsteelblue':       '#B0C4DE',
# 'lightyellow':          '#FFFFE0',
# 'lime':                 '#00FF00',
# 'limegreen':            '#32CD32',
# 'linen':                '#FAF0E6',
# 'magenta':              '#FF00FF',
# 'maroon':               '#800000',
# 'mediumaquamarine':     '#66CDAA',
# 'mediumblue':           '#0000CD',
# 'mediumorchid':         '#BA55D3',
# 'mediumpurple':         '#9370DB',
# 'mediumseagreen':       '#3CB371',
# 'mediumslateblue':      '#7B68EE',
# 'mediumspringgreen':    '#00FA9A',
# 'mediumturquoise':      '#48D1CC',
# 'mediumvioletred':      '#C71585',
# 'midnightblue':         '#191970',
# 'mintcream':            '#F5FFFA',
# 'mistyrose':            '#FFE4E1',
# 'moccasin':             '#FFE4B5',
# 'navajowhite':          '#FFDEAD',
# 'navy':                 '#000080',
# 'oldlace':              '#FDF5E6',
# 'olive':                '#808000',
# 'olivedrab':            '#6B8E23',
# 'orange':               '#FFA500',
# 'orangered':            '#FF4500',
# 'orchid':               '#DA70D6',
# 'palegoldenrod':        '#EEE8AA',
# 'palegreen':            '#98FB98',
# 'paleturquoise':        '#AFEEEE',
# 'palevioletred':        '#DB7093',
# 'papayawhip':           '#FFEFD5',
# 'peachpuff':            '#FFDAB9',
# 'peru':                 '#CD853F',
# 'pink':                 '#FFC0CB',
# 'plum':                 '#DDA0DD',
# 'powderblue':           '#B0E0E6',
# 'purple':               '#800080',
# 'red':                  '#FF0000',
# 'rosybrown':            '#BC8F8F',
# 'royalblue':            '#4169E1',
# 'saddlebrown':          '#8B4513',
# 'salmon':               '#FA8072',
# 'sandybrown':           '#FAA460',
# 'seagreen':             '#2E8B57',
# 'seashell':             '#FFF5EE',
# 'sienna':               '#A0522D',
# 'silver':               '#C0C0C0',
# 'skyblue':              '#87CEEB',
# 'slateblue':            '#6A5ACD',
# 'slategray':            '#708090',
# 'snow':                 '#FFFAFA',
# 'springgreen':          '#00FF7F',
# 'steelblue':            '#4682B4',
# 'tan':                  '#D2B48C',
# 'teal':                 '#008080',
# 'thistle':              '#D8BFD8',
# 'tomato':               '#FF6347',
# 'turquoise':            '#40E0D0',
# 'violet':               '#EE82EE',
# 'wheat':                '#F5DEB3',
# 'white':                '#FFFFFF',
# 'whitesmoke':           '#F5F5F5',
# 'yellow':               '#FFFF00',
# 'yellowgreen':          '#9ACD32'