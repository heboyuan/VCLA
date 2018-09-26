// Auto-generated. Do not edit!

// (in-package eight_queen.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class queens {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.result = null;
    }
    else {
      if (initObj.hasOwnProperty('result')) {
        this.result = initObj.result
      }
      else {
        this.result = new Array(8).fill(0);
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type queens
    // Check that the constant length array field [result] has the right length
    if (obj.result.length !== 8) {
      throw new Error('Unable to serialize array field result - length must be 8')
    }
    // Serialize message field [result]
    bufferOffset = _arraySerializer.int32(obj.result, buffer, bufferOffset, 8);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type queens
    let len;
    let data = new queens(null);
    // Deserialize message field [result]
    data.result = _arrayDeserializer.int32(buffer, bufferOffset, 8)
    return data;
  }

  static getMessageSize(object) {
    return 32;
  }

  static datatype() {
    // Returns string type for a message object
    return 'eight_queen/queens';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '12c75e77d788a697d2f52c983b334323';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    int32[8] result
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new queens(null);
    if (msg.result !== undefined) {
      resolved.result = msg.result;
    }
    else {
      resolved.result = new Array(8).fill(0)
    }

    return resolved;
    }
};

module.exports = queens;
