(defproject health_samurai "0.1.0-SNAPSHOT"
  :main health-samurai.server
  :dependencies [
                 [ring/ring-core            "1.9.5"]
                 [compojure                 "1.6.2"]
                 [org.clojure/clojure       "1.10.3"]
                 [org.immutant/web          "2.1.10"]
                 [rum                       "0.12.8"]
                 [org.clojure/clojurescript "1.11.4" :scope "provided"]
                 ])
