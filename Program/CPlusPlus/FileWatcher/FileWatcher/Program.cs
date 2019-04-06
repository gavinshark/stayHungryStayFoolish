using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace FileWatcher
{
    class Program
    {
        const int timeInterval = 5 * 1000;
        static void callbackFunc() {
            DateTime now = DateTime.Now;
            Console.WriteLine("{0} File event detected!", now);
        }

        static void Main(string[] args)
        {
            const string filePath = "D:\\tmp\\1.txt";
            //const string filePath = "57756";
            DateTime now = DateTime.Now;

            FileLoopWatcher flw = new FileLoopWatcher(filePath, FileLoopWatcher.FILE_LOOP_WATCHER_EVENT_CREATE | FileLoopWatcher.FILE_LOOP_WATCHER_EVENT_MODIFY,callbackFunc);
            //Thread.Sleep(timeInterval * 2);
            Console.WriteLine("{0} start 1 start!", now);
            if (flw.Start())
            {
                now = DateTime.Now;
                Console.WriteLine("{0} start 1 is triggered!", now);
            }
            else {
                Console.WriteLine("Error, flw is not triggered!");
            }

             Thread.Sleep(timeInterval * 2);
            now = DateTime.Now;
            Console.WriteLine("{0} start 2 start!", now);
            if (flw.Start())
            {
                now = DateTime.Now;
                Console.WriteLine("{0} start 2 is triggered!", now);
            }
            else
            {
                Console.WriteLine("Error, start 2 is not triggered!");
            }
            Thread.Sleep(timeInterval*3);

            now = DateTime.Now;
            Console.WriteLine("{0} End start!", now);
            if (flw.End())
            {
                now = DateTime.Now;
                Console.WriteLine("{0} End end!", now);
            }
            else
            {
                Console.WriteLine("Error, End is not triggered!");
            }
            Thread.Sleep(timeInterval*2);
            now = DateTime.Now;
            Console.WriteLine("{0} start 3 start!", now);
            if (flw.Start())
            {
                now = DateTime.Now;
                Console.WriteLine("{0} start 3 end!", now);
            }
            else
            {
                Console.WriteLine("Error, Start 3 is not triggered!");
            }
            Thread.Sleep(timeInterval * 10);
            Console.WriteLine("Test over!");
            Console.ReadKey();
        }
    }
}
