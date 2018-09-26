
(cl:in-package :asdf)

(defsystem "eight_queen-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "queens" :depends-on ("_package_queens"))
    (:file "_package_queens" :depends-on ("_package"))
  ))