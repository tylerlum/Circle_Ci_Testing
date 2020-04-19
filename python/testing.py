#!/usr/bin/env python
import rospy
import time
from Sailbot import *
from utilities import *
from local_pathfinding.msg import latlon, AISShip, AISMsg

if __name__ == "__main__":
    # Create sailbot ROS object that subscribes to relevant topics
    sailbot = Sailbot(nodeName='testing')
    referenceLatlon = PORT_RENFREW_LATLON
    obstacleTypesByIndex = ['ellipse', 'wedge', 'circles']
    obstacleTypeIndex = 0

    while not rospy.is_shutdown():
        state = sailbot.getCurrentState()
        if len(state.AISData.ships) == 0:
            continue

        obstacleType = obstacleTypesByIndex[obstacleTypeIndex]
        obstacles = getObstacles(state.AISData.ships, state.position, state.speedKmph, referenceLatlon, obstacleType)

        startTime = time.time()
        xy = [0, 0]
        isValidPosition = isValid(xy, obstacles)
        endTime = time.time()

        rospy.logwarn("{} took {} seconds to run isValid on {} ships".format(obstacleType, endTime - startTime, len(state.AISData.ships)))
        rospy.logwarn("This means on average {} seconds per ship.".format((endTime - startTime) / len(state.AISData.ships)))
        if obstacleType == 'circles':
            numObstacles = 0
            for c in obstacles:
                numObstacles += c.numObstacles()
            rospy.logwarn("Actually made of {} circles".format(numObstacles))
            rospy.logwarn("This means on average {} seconds per circle.".format((endTime - startTime) / numObstacles))

        time.sleep(1)
        # Increment obstacleTypeIndex
        obstacleTypeIndex = (obstacleTypeIndex + 1) % len(obstacleTypesByIndex)

        if obstacleTypeIndex == 0:
            rospy.logwarn("***************************")
