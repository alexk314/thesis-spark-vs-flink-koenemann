import org.apache.flink.streaming.api.TimeCharacteristic
import org.apache.flink.streaming.api.scala._
import org.apache.flink.streaming.api.windowing.assigners.{TumblingEventTimeWindows, TumblingProcessingTimeWindows}
import org.apache.flink.streaming.api.windowing.time.Time

object WordCount {
  def main(args: Array[String]): Unit = {
    println("Executing stream processing application")
    // Read specified port from args:
    var port: Int = 9000
    if (args.length == 0) {
      println("No port has been specified, 9000 will be used as default. You can specify port by passing: '--9001'")
    } else {
      port = args.apply(0).toInt
    }
    println(s"App will listen to port $port")

    // Create Execution Environment, main entrypoint for flink apps (similar to spark context):
    val env = StreamExecutionEnvironment.getExecutionEnvironment


    // Create DataStream from socket. Return type DataStream is basic data type for flink streaming
    val socketStream: DataStream[String] = env.socketTextStream("192.168.178.56", port, '\n').name("Input socket stream")

    // WordCount logic:
    // Note: \s+ => one or more whitespaces
    // val wordStream = socketStream.flatMap(value => value.split("\\s+")).map(value => (value, 1)).name("split keys to (key, 1)")
    // val counts: DataStream[(String, Int)] = wordStream.keyBy(_._1).window(TumblingProcessingTimeWindows.of(Time.seconds(1))).sum(1).name("aggregate count")
  val windowCounts = socketStream
      .flatMap(w => w.split("\\s+"))
      .map(w => WordWithCount(w, 1))
      .keyBy(_.word)
      .window(TumblingProcessingTimeWindows.of(Time.seconds(1)))
      .sum("count")

    windowCounts.filter(_.word.startsWith("great")).print().name("Print subset of result")
    //counts.map(_._2).keyBy(1).reduce(_+_).print().name("Sum all words")

    // Trigger (lazy) execution:
    env.execute("StreamWordCount")
  }
    /** Data type for words with count */
  case class WordWithCount(word: String, count: Long)
}