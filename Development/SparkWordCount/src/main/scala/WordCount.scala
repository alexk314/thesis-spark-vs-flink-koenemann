import org.apache.spark.rdd.RDD
import org.apache.spark.{SparkConf, SparkContext}

import java.text.SimpleDateFormat
import java.util.Calendar

object WordCount {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setAppName("Spark WordCount App")
    println("----------------Word Count Program started------------------")
    val sc = new SparkContext(conf)

    // Read CLI input:
    val minPartitions: Int = Integer.valueOf(args(0)) // 1nd input parameter
    // val inputFileName = args(1)

    // Create Uris for input/output: Fixed input
    val inputFileName = "100MiB"
    val inputFileUri = "/input_data/" + inputFileName
    println("Will read input File from path: " + inputFileUri)


    println(s"Read text file and split file into $minPartitions")
    val rdd = sc.textFile(inputFileUri, minPartitions) //Todo: why not moved to executor?


    println("--------Create RDD and parallelize-----------")
    val splitData = rdd.flatMap(line => line.split(" "))
    println("Starting Word Count")
    val wordCounts = splitData.map(word => (word, 1)).reduceByKey(_ + _)
    println("-----------------Fetching Results----------------")
    val result: Array[(String, Int)] = wordCounts.collect() //Precaution, the driver has to handle the output file
    println("---------------------Print parts of the result----------------------")
    val top10 = result.filter(_._1.startsWith("great"))
    top10.foreach(row => println(row))
  }

}