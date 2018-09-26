
(cl:in-package :asdf)

(defsystem "geo2tf-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "geometry" :depends-on ("_package_geometry"))
    (:file "_package_geometry" :depends-on ("_package"))
  ))