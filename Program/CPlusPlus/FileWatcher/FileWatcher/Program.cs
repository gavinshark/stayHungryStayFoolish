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
        static void callbackFunc() {
            Console.WriteLine("File modification event detected!");
        }

        static void Main(string[] args)
        {
            const string filePath = "D:\\tmp\\1.txt";

            FileStatusLoopWatcher flw = new FileStatusLoopWatcher(filePath, callbackFunc);

            if (flw.start()) {
                Console.WriteLine("start is triggered!");
            }
            else {
                Console.WriteLine("Error, flw is not triggered!");
            }

            Thread.Sleep(10*1000);
            if (flw.stop())
            {
                Console.WriteLine("stop is triggered!");
            }
            else
            {
                Console.WriteLine("Error, flw is not triggered!");
            }
            Thread.Sleep(10 * 1000);

            if (flw.start())
            {
                Console.WriteLine("start is triggered!");
            }
            else
            {
                Console.WriteLine("Error, flw is not triggered!");
            }
            Thread.Sleep(10 * 1000);
            if (flw.stop())
            {
                Console.WriteLine("stop is triggered!");
            }
            else
            {
                Console.WriteLine("Error, flw is not triggered!");
            }
        }
    }
}
