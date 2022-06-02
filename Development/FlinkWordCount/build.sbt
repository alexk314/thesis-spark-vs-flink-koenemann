name := "flink-word-count"
version := "1.0"
scalaVersion := "2.12.15"
val flinkVersion = "1.14.0"
// https://mvnrepository.com/artifact/org.apache.flink/flink-scala
libraryDependencies += "org.apache.flink" %% "flink-scala" %  flinkVersion  % "provided"
libraryDependencies += "org.apache.flink" %% "flink-streaming-scala" %  flinkVersion  % "provided"
