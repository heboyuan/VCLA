;; Auto-generated. Do not edit!


(when (boundp 'geo2tf::geometry)
  (if (not (find-package "GEO2TF"))
    (make-package "GEO2TF"))
  (shadow 'geometry (find-package "GEO2TF")))
(unless (find-package "GEO2TF::GEOMETRY")
  (make-package "GEO2TF::GEOMETRY"))

(in-package "ROS")
;;//! \htmlinclude geometry.msg.html


(defclass geo2tf::geometry
  :super ros::object
  :slots (_x _y _z _quaternion_x _quaternion_y _quaternion_z _quaternion_w ))

(defmethod geo2tf::geometry
  (:init
   (&key
    ((:x __x) 0.0)
    ((:y __y) 0.0)
    ((:z __z) 0.0)
    ((:quaternion_x __quaternion_x) 0.0)
    ((:quaternion_y __quaternion_y) 0.0)
    ((:quaternion_z __quaternion_z) 0.0)
    ((:quaternion_w __quaternion_w) 0.0)
    )
   (send-super :init)
   (setq _x (float __x))
   (setq _y (float __y))
   (setq _z (float __z))
   (setq _quaternion_x (float __quaternion_x))
   (setq _quaternion_y (float __quaternion_y))
   (setq _quaternion_z (float __quaternion_z))
   (setq _quaternion_w (float __quaternion_w))
   self)
  (:x
   (&optional __x)
   (if __x (setq _x __x)) _x)
  (:y
   (&optional __y)
   (if __y (setq _y __y)) _y)
  (:z
   (&optional __z)
   (if __z (setq _z __z)) _z)
  (:quaternion_x
   (&optional __quaternion_x)
   (if __quaternion_x (setq _quaternion_x __quaternion_x)) _quaternion_x)
  (:quaternion_y
   (&optional __quaternion_y)
   (if __quaternion_y (setq _quaternion_y __quaternion_y)) _quaternion_y)
  (:quaternion_z
   (&optional __quaternion_z)
   (if __quaternion_z (setq _quaternion_z __quaternion_z)) _quaternion_z)
  (:quaternion_w
   (&optional __quaternion_w)
   (if __quaternion_w (setq _quaternion_w __quaternion_w)) _quaternion_w)
  (:serialization-length
   ()
   (+
    ;; float64 _x
    8
    ;; float64 _y
    8
    ;; float64 _z
    8
    ;; float64 _quaternion_x
    8
    ;; float64 _quaternion_y
    8
    ;; float64 _quaternion_z
    8
    ;; float64 _quaternion_w
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _x
       (sys::poke _x (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _y
       (sys::poke _y (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _z
       (sys::poke _z (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _quaternion_x
       (sys::poke _quaternion_x (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _quaternion_y
       (sys::poke _quaternion_y (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _quaternion_z
       (sys::poke _quaternion_z (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _quaternion_w
       (sys::poke _quaternion_w (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _x
     (setq _x (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _y
     (setq _y (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _z
     (setq _z (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _quaternion_x
     (setq _quaternion_x (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _quaternion_y
     (setq _quaternion_y (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _quaternion_z
     (setq _quaternion_z (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _quaternion_w
     (setq _quaternion_w (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get geo2tf::geometry :md5sum-) "dce9e430f28a40b69510d1179e073686")
(setf (get geo2tf::geometry :datatype-) "geo2tf/geometry")
(setf (get geo2tf::geometry :definition-)
      "float64 x
float64 y
float64 z
float64 quaternion_x
float64 quaternion_y
float64 quaternion_z
float64 quaternion_w

")



(provide :geo2tf/geometry "dce9e430f28a40b69510d1179e073686")


