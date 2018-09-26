#include <ros/ros.h>
#include <visualization_msgs/Marker.h>
#include <tf/transform_broadcaster.h>
#include "geo2tf/geometry.h"

ros::Subscriber sub;
ros::Publisher pub;

void callback(const geo2tf::geometry::ConstPtr& msg){

  static tf::TransformBroadcaster br;

  tf::Transform transform;
  ros::Rate rate(10.0);
  while (ros::ok()) {
    transform.setOrigin(tf::Vector3(msg->x, msg->y, msg->z));
    transform.setRotation( tf::Quaternion(msg->quaternion_x, msg->quaternion_y, msg->quaternion_z, msg->quaternion_w) );
    br.sendTransform(tf::StampedTransform(transform, ros::Time::now(), "my_frame", "my_tf"));
    rate.sleep();
  }
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "listener");
  ros::NodeHandle n;
  sub = n.subscribe("coordinate", 1000, callback);
  pub = n.advertise<visualization_msgs::Marker>( "visualization_marker", 0 );
  ros::spin();
  return 0;
}
