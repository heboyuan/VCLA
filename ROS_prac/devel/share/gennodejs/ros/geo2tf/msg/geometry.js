// Auto-generated. Do not edit!

// (in-package geo2tf.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class geometry {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.x = null;
      this.y = null;
      this.z = null;
      this.quaternion_x = null;
      this.quaternion_y = null;
      this.quaternion_z = null;
      this.quaternion_w = null;
    }
    else {
      if (initObj.hasOwnProperty('x')) {
        this.x = initObj.x
      }
      else {
        this.x = 0.0;
      }
      if (initObj.hasOwnProperty('y')) {
        this.y = initObj.y
      }
      else {
        this.y = 0.0;
      }
      if (initObj.hasOwnProperty('z')) {
        this.z = initObj.z
      }
      else {
        this.z = 0.0;
      }
      if (initObj.hasOwnProperty('quaternion_x')) {
        this.quaternion_x = initObj.quaternion_x
      }
      else {
        this.quaternion_x = 0.0;
      }
      if (initObj.hasOwnProperty('quaternion_y')) {
        this.quaternion_y = initObj.quaternion_y
      }
      else {
        this.quaternion_y = 0.0;
      }
      if (initObj.hasOwnProperty('quaternion_z')) {
        this.quaternion_z = initObj.quaternion_z
      }
      else {
        this.quaternion_z = 0.0;
      }
      if (initObj.hasOwnProperty('quaternion_w')) {
        this.quaternion_w = initObj.quaternion_w
      }
      else {
        this.quaternion_w = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type geometry
    // Serialize message field [x]
    bufferOffset = _serializer.float64(obj.x, buffer, bufferOffset);
    // Serialize message field [y]
    bufferOffset = _serializer.float64(obj.y, buffer, bufferOffset);
    // Serialize message field [z]
    bufferOffset = _serializer.float64(obj.z, buffer, bufferOffset);
    // Serialize message field [quaternion_x]
    bufferOffset = _serializer.float64(obj.quaternion_x, buffer, bufferOffset);
    // Serialize message field [quaternion_y]
    bufferOffset = _serializer.float64(obj.quaternion_y, buffer, bufferOffset);
    // Serialize message field [quaternion_z]
    bufferOffset = _serializer.float64(obj.quaternion_z, buffer, bufferOffset);
    // Serialize message field [quaternion_w]
    bufferOffset = _serializer.float64(obj.quaternion_w, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type geometry
    let len;
    let data = new geometry(null);
    // Deserialize message field [x]
    data.x = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [y]
    data.y = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [z]
    data.z = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [quaternion_x]
    data.quaternion_x = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [quaternion_y]
    data.quaternion_y = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [quaternion_z]
    data.quaternion_z = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [quaternion_w]
    data.quaternion_w = _deserializer.float64(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 56;
  }

  static datatype() {
    // Returns string type for a message object
    return 'geo2tf/geometry';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'dce9e430f28a40b69510d1179e073686';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float64 x
    float64 y
    float64 z
    float64 quaternion_x
    float64 quaternion_y
    float64 quaternion_z
    float64 quaternion_w
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new geometry(null);
    if (msg.x !== undefined) {
      resolved.x = msg.x;
    }
    else {
      resolved.x = 0.0
    }

    if (msg.y !== undefined) {
      resolved.y = msg.y;
    }
    else {
      resolved.y = 0.0
    }

    if (msg.z !== undefined) {
      resolved.z = msg.z;
    }
    else {
      resolved.z = 0.0
    }

    if (msg.quaternion_x !== undefined) {
      resolved.quaternion_x = msg.quaternion_x;
    }
    else {
      resolved.quaternion_x = 0.0
    }

    if (msg.quaternion_y !== undefined) {
      resolved.quaternion_y = msg.quaternion_y;
    }
    else {
      resolved.quaternion_y = 0.0
    }

    if (msg.quaternion_z !== undefined) {
      resolved.quaternion_z = msg.quaternion_z;
    }
    else {
      resolved.quaternion_z = 0.0
    }

    if (msg.quaternion_w !== undefined) {
      resolved.quaternion_w = msg.quaternion_w;
    }
    else {
      resolved.quaternion_w = 0.0
    }

    return resolved;
    }
};

module.exports = geometry;
