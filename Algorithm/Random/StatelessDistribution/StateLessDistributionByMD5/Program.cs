using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Security.Cryptography;

namespace MD5Distribution
{
    class Program
    {
        static readonly int Size = 16;
        static public byte[] CalculateMD5Value(byte[] bytesContent)
        {
            byte[] bytesKey;

            using (MD5 md5Hash = MD5.Create())
            {
                bytesKey = md5Hash.ComputeHash(bytesContent);
            }

            return bytesKey;
        }

        static public void display(int[] countResult, int sum, string start, string end)
        {
            Console.WriteLine("\nDistribution Result from {0} to {1}", start, end);
            for (int i = 0; i < Size; i++)
            {
                int percent = (countResult[i] * 100) / sum;
                Console.WriteLine("mode {0,2}: percent:  {1,8}/{2,8} = {3,2}%", i, countResult[i], sum, percent);
            }
            Console.WriteLine("");
        }

        static void Main(string[] args)
        {
            string strPrefix = "bffddad.3cb1.";
            string strSuffix = ".Coremail.emailsender@126.com";

            int start = 0;
            int end = 2000;// 1000 * 1000;

            if (args.Length >= 2)
            {
                start = int.Parse(args[0]);
                end = int.Parse(args[1]);
            }
            else
            {
                Console.WriteLine("No specified start & end, use default value {0}/{1}, to specified use this.exe start end > result.txt", start, end);
            }

            Console.WriteLine("start to calculate prefix:{0}, subfix:{1},start:{2},end:{3}", strPrefix, strSuffix, start, end);

            string startEmailId = "", endEmailId = "", EmailId = "";
            StringBuilder sb = new StringBuilder();
            int[] countResult = new int[Size];

            for (int i = start; i < end; i++)
            {
                sb.Clear();
                sb.Append(strPrefix);
                sb.AppendFormat("{0}", i);
                sb.Append(strSuffix);

                EmailId = sb.ToString();

                if (i == start) { startEmailId = EmailId; }
                if (i == end - 1) { endEmailId = EmailId; }

                byte[] MD5Value = CalculateMD5Value(Encoding.UTF8.GetBytes(EmailId));

                int idx = (MD5Value[0]) % Size;
                countResult[idx]++;
                if (i != 0 && (i % 100 == 0))
                {
                    display(countResult, i + 1, startEmailId, EmailId);
                }
            }

            Console.WriteLine("end to calculate prefix:{0}, subfix:{1},start:{2},end:{3}", strPrefix, strSuffix, start, end);
            display(countResult, end - start, startEmailId, endEmailId);
        }
    }
}