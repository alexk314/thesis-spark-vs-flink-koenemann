import org.apache.spark.SparkConf
import org.apache.spark._
import org.apache.spark.streaming._
import org.apache.spark.streaming.StreamingContext._
import org.apache.spark.streaming.scheduler.{StreamingListener, StreamingListenerReceiverError, StreamingListenerReceiverStopped}

import scala.util.control.NonFatal

object WordCountStream {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setAppName("Spark WordCount App")
    println("----------------Word Count Program started------------------")
    val batchDuration = Milliseconds(1000)
    val sc = new StreamingContext(conf, batchDuration) // TODO: Verify batch duration

    // Read CLI input:
    val minPartitions: Int = Integer.valueOf(args(0)) // 1nd input parameter
    // val inputFileName = args(1)



    val dStream = sc.socketTextStream("192.168.178.56", 9000)


    val splitData = dStream.flatMap(line => line.split(" "))
    val wordCounts = splitData.map(word => (word, 1)).reduceByKey(_ + _)

    println("---------------------Print parts of the result----------------------")
    //wordCounts.filter(_._1.startsWith("great")).print()
    wordCounts.filter(_._1.startsWith("great")).print() // Prints first ten elements

      sc.start()
    // Start the computation
      sc.awaitTermination()
  }

}