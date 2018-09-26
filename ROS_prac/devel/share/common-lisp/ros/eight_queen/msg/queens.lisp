; Auto-generated. Do not edit!


(cl:in-package eight_queen-msg)


;//! \htmlinclude queens.msg.html

(cl:defclass <queens> (roslisp-msg-protocol:ros-message)
  ((result
    :reader result
    :initarg :result
    :type (cl:vector cl:integer)
   :initform (cl:make-array 8 :element-type 'cl:integer :initial-element 0)))
)

(cl:defclass queens (<queens>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <queens>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'queens)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name eight_queen-msg:<queens> is deprecated: use eight_queen-msg:queens instead.")))

(cl:ensure-generic-function 'result-val :lambda-list '(m))
(cl:defmethod result-val ((m <queens>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader eight_queen-msg:result-val is deprecated.  Use eight_queen-msg:result instead.")
  (result m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <queens>) ostream)
  "Serializes a message object of type '<queens>"
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let* ((signed ele) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    ))
   (cl:slot-value msg 'result))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <queens>) istream)
  "Deserializes a message object of type '<queens>"
  (cl:setf (cl:slot-value msg 'result) (cl:make-array 8))
  (cl:let ((vals (cl:slot-value msg 'result)))
    (cl:dotimes (i 8)
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:aref vals i) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<queens>)))
  "Returns string type for a message object of type '<queens>"
  "eight_queen/queens")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'queens)))
  "Returns string type for a message object of type 'queens"
  "eight_queen/queens")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<queens>)))
  "Returns md5sum for a message object of type '<queens>"
  "12c75e77d788a697d2f52c983b334323")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'queens)))
  "Returns md5sum for a message object of type 'queens"
  "12c75e77d788a697d2f52c983b334323")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<queens>)))
  "Returns full string definition for message of type '<queens>"
  (cl:format cl:nil "int32[8] result~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'queens)))
  "Returns full string definition for message of type 'queens"
  (cl:format cl:nil "int32[8] result~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <queens>))
  (cl:+ 0
     0 (cl:reduce #'cl:+ (cl:slot-value msg 'result) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <queens>))
  "Converts a ROS message object to a list"
  (cl:list 'queens
    (cl:cons ':result (result msg))
))
