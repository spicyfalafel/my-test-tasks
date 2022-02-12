(ns health-samurai.server
  (:require
   [immutant.web :as web]
   ))

(defn app [req]
  {:status  200
   :headers {"Content-Type" "text/html"}
   :body    "hello HTTP!"})


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
