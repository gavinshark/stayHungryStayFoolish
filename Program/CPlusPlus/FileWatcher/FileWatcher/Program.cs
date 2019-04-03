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
        const int timeInterval = 10 * 1000;
        static void callbackFunc(int eventid) {
            DateTime now = DateTime.Now;
            Console.WriteLine("{0} File {1} event detected!", now, eventid);
        }

        static void Main(string[] args)
        {
            const string filePath = "D:\\tmp\\1.txt";
            
            FileLoopWatcher flw = new FileLoopWatcher(filePath, callbackFunc);

            if (flw.start())
            {
                DateTime now = DateTime.Now;
                Console.WriteLine("{0} start is triggered!", now);
            }
            else {
                Console.WriteLine("Error, flw is not triggered!");
            }

//             Thread.Sleep(timeInterval);
//             if (flw.stop())
//             {
//                 DateTime now = DateTime.Now;
//                 Console.WriteLine("{0} stop is triggered!", now);
//             }
//             else
//             {
//                 Console.WriteLine("Error, flw is not triggered!");
//             }
//             Thread.Sleep(timeInterval);
// 
//             if (flw.start())
//             {
//                 DateTime now = DateTime.Now;
//                 Console.WriteLine("{0} start is triggered!", now);
//             }
//             else
//             {
//                 Console.WriteLine("Error, flw is not triggered!");
//             }
            Console.ReadKey();
//             if (flw.stop())
//             {
//                 DateTime now = DateTime.Now;
//                 Console.WriteLine("{0} stop is triggered!", now);
//             }
//             else
//             {
//                 Console.WriteLine("Error, flw is not triggered!");
//             }
        }
    }
}
