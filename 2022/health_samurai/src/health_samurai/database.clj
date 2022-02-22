(ns health-samurai.database
  (:require
   [next.jdbc :as sql]))

;; (def database-url "postgresql://localhost:5432/postgres")

;; (def pg-db {:dbtype "postgresql"
;;             :dbname "postgres"
;;             :host "localhost"
;;             :user "postgres"
;;             :password "root"})

;; (defn q
;;   ([select-sql table where-sql]
;;   (sql/query pg-db [(str "select "
;;                                 select-sql
;;                                 " from "
;;                                 table
;;                                 " where "
;;                                 where-sql)]))
;;   ([select-sql table]
;;    (sql/query pg-db [(str "select "
;;                                  select-sql
;;                                  " from "
;;                                  table)])))

;; (defn ins!
;;   ([table map-data]
;;    (sql/insert! pg-db table map-data)))

;; (defn ins-patient! [map-data]
;;   (let [birthdate (LocalDate/parse (:birthdate map-data))
;;              kostil (assoc map-data :birthdate birthdate)]
;;     (ins! :patient kostil)))

(defn commands [& args]
  (sql/db-do-commands pg-db
                      args))



(comment
  (q "data" "testing" "data like 'Hel%'")
  (sql/query database-url
             ["select * from testing"])
  (q "*" "testing")


  (sql/insert! database-url
               :testing {:data "Hello wrold"})
  (ins! :testing {:data "Kek"})

  (commands (sql/create-table-ddl :gender
                                  [[:id :serial]
                                  [:name :text]]))
  (ins! :gender {:name "Male"})
  (ins! :gender {:name "Female"})
  (ins-patient! {
                  :firstname "a"
                  :lastname "b"
                  :gender_id 1
                  :birthdate "2000-01-01"
                  :address "address..."
                  :polys_id 1114111411141117
                  })

  (q "*" "gender")
  (q "*" "patient")
  (sql/db-do-commands pd-db (sql/create-table-ddl  :testing [[:data :text]]))
)
