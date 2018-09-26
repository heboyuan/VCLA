#include <stdlib.h>
#include <math.h>
#include <iostream>
#include <map>
#include <vector>
#include <sstream>
#include <ros/ros.h>
#include <visualization_msgs/Marker.h>
#include <tf/transform_broadcaster.h>
#include "tinyxml2.h"

std::vector<tinyxml2::XMLElement*> links;
std::map<std::string,std::string> parent;

void test_print(){
  std::string name;
  std::cout << "links================================================\n"
            << links.size()
            << std::endl;
  for (int i = 0; i<links.size();++i){
    name = links[i]->Attribute("name");
    std::cout << name << std::endl;
  }

  std::map<std::string,std::string>::iterator it;
  std::cout << "parents================================================\n"
            << parent.size()
            << std::endl;
  for ( it = parent.begin(); it != parent.end(); it++ ){
    std::cout << it->first << " -> " << it->second << std::endl;
  }
}

tf::Quaternion toQuaternion(std::string p, std::string r, std::string y)
{
  double pitch = atof(p.c_str());
  double roll = atof(r.c_str());
  double yaw = atof(y.c_str());
	double cy = cos(yaw * 0.5);
	double sy = sin(yaw * 0.5);
	double cr = cos(roll * 0.5);
	double sr = sin(roll * 0.5);
	double cp = cos(pitch * 0.5);
	double sp = sin(pitch * 0.5);

	return tf::Quaternion(sy * cr * cp - cy * sr * sp, cy * cr * cp + sy * sr * sp, cy * sr * cp - sy * cr * sp,cy * cr * sp + sy * sr * cp);
}


void publish(tinyxml2::XMLElement* ele, tf::TransformBroadcaster br){
  tf::Transform transform;

  std::string name = ele->Attribute("name");
  std::cout<<"transform: "<<name << "================================\n";

  std::string dir = ele->FirstChildElement("inertial")->FirstChildElement("origin")->Attribute("rpy");
  std::istringstream s_dir(dir);
  std::string roll, pitch, yaw;
  s_dir >> roll;
  s_dir >> pitch;
  s_dir >> yaw;
  transform.setRotation(toQuaternion(pitch, roll, yaw));

  std::string pos = ele->FirstChildElement("inertial")->FirstChildElement("origin")->Attribute("xyz");
  std::istringstream s_pos(pos);
  std::string s_x, s_y, s_z;
  s_pos >> s_x;
  s_pos >> s_y;
  s_pos >> s_z;
  double x = atof(s_x.c_str());
  double y = atof(s_y.c_str());
  double z = atof(s_z.c_str());
  transform.setOrigin(tf::Vector3(x, y, z));

  std::string ele_parent;
  if(parent.find(name) == parent.end()){
    ele_parent = "base";
  }else{
    ele_parent = parent[name];
  }
  std::cout <<" x: "<<x<<" y: "<<y<<" z: "<<z<<std::endl
            <<" roll: "<<roll<<" pitch: "<<pitch<<" yaw: "<<yaw<<std::endl;
  br.sendTransform(tf::StampedTransform(transform, ros::Time::now(), ele_parent, name));

}


void find(tinyxml2::XMLElement* root){
  if(root == NULL){
    return;
  }

  std::string tag_name = root->Name();
  if(tag_name == "link"){
    links.push_back(root);
  }
  if(tag_name == "parent"){
    std::string link_parent = root->Attribute("link");
    std::string link_child = root->NextSiblingElement()->Attribute("link");
    parent[link_child]=link_parent;
  }
  find(root->FirstChildElement());
  find(root->NextSiblingElement());
}


int main(int argc, char **argv){


  tinyxml2::XMLDocument xml_doc("/home/boyuan/VCLA/practice_ws/src/baxter_robot/urdf/baxter.urdf");
  tinyxml2::XMLError err = xml_doc.LoadFile("/home/boyuan/VCLA/practice_ws/src/baxter_robot/urdf/baxter.urdf");
  if (err != tinyxml2::XML_SUCCESS){
    std::cout << xml_doc.ErrorStr() << std::endl;
    return false;
  }
  tinyxml2::XMLElement* root = xml_doc.FirstChildElement();

  find(root);

  ros::init(argc, argv, "broadcaster");
  ros::NodeHandle node;
  tf::TransformBroadcaster br;

  int i = 1;
  while(node.ok()){
    if (i == links.size()){
      i = 1;
    }

    tf::Transform transform;
    transform.setOrigin( tf::Vector3(0.0, 0.0, 0.0) );
    transform.setRotation( tf::Quaternion(0, 0, 0, 1) );
    br.sendTransform(tf::StampedTransform(transform, ros::Time::now(), "world", "base"));

    publish(links[i],br);

    i++;
  }
}
