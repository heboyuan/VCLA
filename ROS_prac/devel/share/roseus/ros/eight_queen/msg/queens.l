;; Auto-generated. Do not edit!


(when (boundp 'eight_queen::queens)
  (if (not (find-package "EIGHT_QUEEN"))
    (make-package "EIGHT_QUEEN"))
  (shadow 'queens (find-package "EIGHT_QUEEN")))
(unless (find-package "EIGHT_QUEEN::QUEENS")
  (make-package "EIGHT_QUEEN::QUEENS"))

(in-package "ROS")
;;//! \htmlinclude queens.msg.html


(defclass eight_queen::queens
  :super ros::object
  :slots (_result ))

(defmethod eight_queen::queens
  (:init
   (&key
    ((:result __result) (make-array 8 :initial-element 0 :element-type :integer))
    )
   (send-super :init)
   (setq _result __result)
   self)
  (:result
   (&optional __result)
   (if __result (setq _result __result)) _result)
  (:serialization-length
   ()
   (+
    ;; int32[8] _result
    (* 4    8)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32[8] _result
     (dotimes (i 8)
       (write-long (elt _result i) s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32[8] _result
   (dotimes (i (length _result))
     (setf (elt _result i) (sys::peek buf ptr- :integer)) (incf ptr- 4)
     )
   ;;
   self)
  )

(setf (get eight_queen::queens :md5sum-) "12c75e77d788a697d2f52c983b334323")
(setf (get eight_queen::queens :datatype-) "eight_queen/queens")
(setf (get eight_queen::queens :definition-)
      "int32[8] result

")



(provide :eight_queen/queens "12c75e77d788a697d2f52c983b334323")


