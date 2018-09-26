# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "geo2tf: 1 messages, 0 services")

set(MSG_I_FLAGS "-Igeo2tf:/home/boyuan/VCLA/practice_ws/src/geo2tf/msg;-Istd_msgs:/opt/ros/kinetic/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(geo2tf_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/boyuan/VCLA/practice_ws/src/geo2tf/msg/geometry.msg" NAME_WE)
add_custom_target(_geo2tf_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "geo2tf" "/home/boyuan/VCLA/practice_ws/src/geo2tf/msg/geometry.msg" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(geo2tf
  "/home/boyuan/VCLA/practice_ws/src/geo2tf/msg/geometry.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/geo2tf
)

### Generating Services

### Generating Module File
_generate_module_cpp(geo2tf
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/geo2tf
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(geo2tf_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(geo2tf_generate_messages geo2tf_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/boyuan/VCLA/practice_ws/src/geo2tf/msg/geometry.msg" NAME_WE)
add_dependencies(geo2tf_generate_messages_cpp _geo2tf_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(geo2tf_gencpp)
add_dependencies(geo2tf_gencpp geo2tf_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS geo2tf_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(geo2tf
  "/home/boyuan/VCLA/practice_ws/src/geo2tf/msg/geometry.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/geo2tf
)

### Generating Services

### Generating Module File
_generate_module_eus(geo2tf
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/geo2tf
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(geo2tf_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(geo2tf_generate_messages geo2tf_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/boyuan/VCLA/practice_ws/src/geo2tf/msg/geometry.msg" NAME_WE)
add_dependencies(geo2tf_generate_messages_eus _geo2tf_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(geo2tf_geneus)
add_dependencies(geo2tf_geneus geo2tf_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS geo2tf_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(geo2tf
  "/home/boyuan/VCLA/practice_ws/src/geo2tf/msg/geometry.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/geo2tf
)

### Generating Services

### Generating Module File
_generate_module_lisp(geo2tf
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/geo2tf
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(geo2tf_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(geo2tf_generate_messages geo2tf_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/boyuan/VCLA/practice_ws/src/geo2tf/msg/geometry.msg" NAME_WE)
add_dependencies(geo2tf_generate_messages_lisp _geo2tf_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(geo2tf_genlisp)
add_dependencies(geo2tf_genlisp geo2tf_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS geo2tf_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(geo2tf
  "/home/boyuan/VCLA/practice_ws/src/geo2tf/msg/geometry.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/geo2tf
)

### Generating Services

### Generating Module File
_generate_module_nodejs(geo2tf
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/geo2tf
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(geo2tf_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(geo2tf_generate_messages geo2tf_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/boyuan/VCLA/practice_ws/src/geo2tf/msg/geometry.msg" NAME_WE)
add_dependencies(geo2tf_generate_messages_nodejs _geo2tf_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(geo2tf_gennodejs)
add_dependencies(geo2tf_gennodejs geo2tf_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS geo2tf_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(geo2tf
  "/home/boyuan/VCLA/practice_ws/src/geo2tf/msg/geometry.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/geo2tf
)

### Generating Services

### Generating Module File
_generate_module_py(geo2tf
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/geo2tf
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(geo2tf_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(geo2tf_generate_messages geo2tf_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/boyuan/VCLA/practice_ws/src/geo2tf/msg/geometry.msg" NAME_WE)
add_dependencies(geo2tf_generate_messages_py _geo2tf_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(geo2tf_genpy)
add_dependencies(geo2tf_genpy geo2tf_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS geo2tf_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/geo2tf)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/geo2tf
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(geo2tf_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/geo2tf)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/geo2tf
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(geo2tf_generate_messages_eus std_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/geo2tf)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/geo2tf
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(geo2tf_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/geo2tf)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/geo2tf
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(geo2tf_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/geo2tf)
  install(CODE "execute_process(COMMAND \"/usr/bin/python\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/geo2tf\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/geo2tf
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(geo2tf_generate_messages_py std_msgs_generate_messages_py)
endif()
