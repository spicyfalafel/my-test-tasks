(ns health-samurai.server
  (:require
   [immutant.web :as web]
   [compojure.route :as cjr]
   [compojure.core :as compojure]
   ))

;; GET /patient
;; POST /patient
;; PUT /patient/{id}
;; DELETE /patient/{id}

(compojure/defroutes routes
  (compojure/GET "/patient" [] {:body "patients get"})
  (compojure/POST "/patient" [] {:body "patients post"})
  (compojure/PUT "/patient/:id" [id] {:body (str "PUT patient with id " id) })
  (compojure/DELETE "/patient/:id" [id] {:body (str "DELETE patient with id " id )}))


(def app routes)

(defn -main [& args]
  (let [args-map (apply array-map args)
        port-str (or (get args-map "-p")
                     (get args-map "--port")
                     "8080")]
    (println "Starting web server on port" port-str)
    (web/run #'app { :port (Integer/parseInt port-str) })))


(comment
  (def server (-main "--port" "8080"))
  (web/stop server))
