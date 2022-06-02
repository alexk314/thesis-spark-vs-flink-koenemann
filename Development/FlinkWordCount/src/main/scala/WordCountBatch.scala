import org.apache.flink.api.common.{ExecutionConfig, RuntimeExecutionMode}
import org.apache.flink.api.java.utils.ParameterTool
import org.apache.flink.streaming.api.scala._
import org.apache.flink.api.common.serialization.SimpleStringEncoder
import org.apache.flink.core.fs.Path
import org.apache.flink.streaming.api.functions.sink.filesystem.StreamingFileSink
import org.apache.flink.streaming.api.functions.sink.filesystem.rollingpolicies.DefaultRollingPolicy

import java.nio.file.Paths
import java.time.LocalDate
import java.util.concurrent.TimeUnit

object WordCountBatch {
  def main(args: Array[String]): Unit = {
    val params: ParameterTool = ParameterTool.fromArgs(args)

    //    val outputPath = "/output/" + LocalDate.now().toString

    // Create Execution Environment, main entrypoint for flink apps (similar to spark context):
    val env = StreamExecutionEnvironment.getExecutionEnvironment



    // Set level of parallelism
    if (params.has("parallelism")) {
      val parallelism = params.get("parallelism").toInt
      println(s"Got parallelism value: $parallelism ")
      env.setParallelism(parallelism)
    }
      // Setting to batch execution node. Note: Overall performance is better in streaming mode even for bounded files
      var executionMode = RuntimeExecutionMode.BATCH
      if (params.has("stream")) {
        executionMode = RuntimeExecutionMode.STREAMING
      }
      println(s"Execution mode: ${executionMode.name()}")
      env.setRuntimeMode(executionMode)

      val text =
        if (params.has("input")) {
          println("Got input path: " + params.get("input"))
          env.readTextFile(params.get("input"))
        } else {
          println("No input specified, using default file")
          println("Use --input to specify file input.")
          env.readTextFile("input_data/10MiB")
        }

      // WordCount logic:
      // Note: \s+ => one or more whitespaces
      val wordStream = text.flatMap(value => value.split("\\s+")).map(value => (value, 1)).name("split keys to (key, 1)")
      val counts: DataStream[(String, Int)] = wordStream.keyBy(_._1).sum(1).name("aggregate count")

      // print results:
      counts.filter(_._1.startsWith("great")).print().name("Print subset of result")


      // Trigger (lazy) execution:
      env.execute("StreamWordCount")
    }
  }