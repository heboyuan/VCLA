#!/usr/bin/env python

import rospy
import time
from eight_queen.msg import queens

def publisher():
    pub =  rospy.Publisher('solution', queens, queue_size=98)
    rospy.init_node('publisher', anonymous=True)
    def queen(A, cur=0):
        if cur == len(A):
            msg = queens()
            msg.result = A
            pub.publish(msg)
            time.sleep(3)
            print(A)
            return 0
        for col in range(len(A)):
            A[cur], flag = col, True
            for row in range(cur):
                if A[row] == col or abs(col - A[row]) == cur - row:
                    flag = False
                    break
            if flag:
                queen(A, cur+1)
    queen([None]*8)

if __name__ == '__main__':
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass
