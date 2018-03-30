#@Author Shelton Cai
#Written with Python 3.6.2
#to run quickhull, call convexHull2D with an array of tuples of floats representing your points
#running the code will generate a random set of points (domain and range{0,100}), and run the code on this set of points

#the code will display the points added to the convex hull array on a plot in intervals of .2 seconds to show the order of the plotting
#note that the order in which they are found is not the order in which they are displayed, I have specifically appended it in an order where
#the points are appended clockwise, for convenience of checking if new points are inside or outside of our hull post calculation
import math
import matplotlib.pyplot as plt
import numpy
#implementation of convex hull via divide and conquer (quickhull)
def convexHull2D(points):
	for p in points:
		plt.plot([p[0]], [p[1]],'b.')
	plt.show(block=False)
	if(len(points) <2):
		return [-1]
	result = []
	sortedArr = sorted(points, key = lambda x: x[0])
	result+=(sortedArr[0])
	l = 2
	j = sortedArr[0]
	k = sortedArr[len(sortedArr)-1]
	m = float((k[1]-j[1]))/float((k[0]-j[0]))
	plt.scatter(j[0], j[1], s=80)
	plt.pause(.2)
	topArr = list(filter(lambda x: (x[1]-j[1])>((x[0]-j[0])*m), sortedArr))
	bottomArr = list(filter(lambda x: (x[1]-j[1])<((x[0]-j[0])*m), sortedArr))
	if(len(topArr)>0):
		result+=recurse2D(topArr, j,k, 1)
	result+=(sortedArr[len(sortedArr)-1])
	plt.scatter(k[0], k[1], s=80)
	plt.pause(.2)
	if(len(bottomArr)>0):
		result+=recurse2D(bottomArr, j,k, 0)
	#the max is added at the end of the array to keep ordering
	return result

# the recursion for d&c, takes params points, the min and max from previous call, and a boolean determining of we are looking up or down(used for sideOf)
def recurse2D(points, j, k, isTop):
	#case with only one point left return point
	if(len(points)==1):
		plt.scatter(points[0][0], points[0][1], s=80)

		plt.pause(.2)
		return points[0]
	#if mroe than one point
	#NOTE: we can assume we will never reach 0 b/c in the caller method, we have a catch for len<2, and at the bottom of this case
	#we do not recurse if there are no points left
	else:
		#sort the points by the area of the triangle they for with j,k
		sortedArr = sorted(points, key = lambda x: linePointDist2D(j,k,x))
		maxP = sortedArr[len(sortedArr)-1]
		topArr = []
		bottomArr = []
		result = []

		#filter out points within the polygon, and create 2 arrays of the points split by the polygon
		if(isTop):
			leftArr = list(filter(lambda x: sideOf(j,maxP,x)<0, points))
			rightArr = list(filter(lambda x: sideOf(maxP, k,x)<0, points))
		else:
			leftArr = list(filter(lambda x: sideOf(j,maxP,x)>0, points))
			rightArr = list(filter(lambda x: sideOf(maxP, k,x)>0, points))

		#plot the result

		#recurse
		#we append the maxP found in between the left and right side in order to have an ordered array as the result
		if(isTop):
			if(len(leftArr)>0):
				result+=recurse2D(leftArr,j,maxP, isTop)
			plt.scatter(maxP[0], maxP[1], s=80)
			plt.pause(.2)
			result+=maxP
			if(len(rightArr)>0):
				result+=recurse2D(rightArr, maxP, k, isTop)
			return result
		else:
			if(len(rightArr)>0):
				result+=recurse2D(rightArr, maxP, k, isTop)
			plt.scatter(maxP[0], maxP[1], s=80)
	
			plt.pause(.2)
			result+=maxP
			if(len(leftArr)>0):
				result+=recurse2D(leftArr,j,maxP, isTop)
			return result


	return
#this returns the size of the triangle formed by j,k,p since triangles will always be bigger for further pts
def linePointDist2D(j,k,p):
	return abs((j[0]-p[0])*(k[1]-j[1])-(j[0]-k[0])*(p[1]-j[1]))/2

#calculates which side of line JK point p is on using cross products
def sideOf(j,k,p):
	return numpy.cross(numpy.asarray(p)-numpy.asarray(j), numpy.asarray(k)-numpy.asarray(j))

#Because our expected input hull is ordered clockwise, we can simply run a cross product with every line segment to check if p is within
#hull is an array of tuples, and p is our new point
def isInside(hull, p):
	for i in range(0, len(hull)-2):
		if(sideOf(hull[i],hull[i+1], p)<0):
			return False
	if(sideOf(hull[len(hull)-1], hull[0], p)<0):
		return False
	return True
#Starts a request for user input to run isInside, plots the new points on the plot, red diamonds being outside, green being inside
def isInsideRunner(hull):
	#Information for user
	print("The points in the convex hull are:" + str(hull) + "\n")
	print("Now receiving user input for new points.This part will test whether the point is inside or outside the convex hull.")
	print("The test will return true for points within and on the hull, and false for points outside the hull")
	print("Invalid inputs will crash the program.")
	cont = True
	#prompt for user input in a loop, and plot the results
	while(cont):
		message = input("Enter input in format float,float, to exit, please enter quit:")
		plt.pause(.5)
		if(message == 'quit'):
			print("ending...")
			cont = False
		else:
			arr = message.split(',')
			isIn = isInside(hull, (float(arr[0]),float(arr[1])))
			if(isIn):
				plt.scatter(arr[0], arr[1], s=80, marker = 'D', c='green')
				print("The point is either on or inside the hull.")
				plt.pause(.5)
			else:
				plt.scatter(arr[0], arr[1], s=80, marker = 'D', c='red')
				print("The point is outside the hull.")
				plt.pause(.5)
#test implementation of convexhull with 40 random points between 0 to 100
def main():
	x = 100* numpy.random.random(40)
	y = 100* numpy.random.random(40)
	samp = list(zip(x,y))
	result = convexHull2D(samp)
	i = 0
	finalResult = []
	while(i<len(result)-2):
		finalResult.append((result[i],result[i+1]))
		i+=2
	while(True):
		isInsideRunner(finalResult)
		break

#run quickhull, the plot will plot points in the convex hull
if __name__== "__main__":
	main()
