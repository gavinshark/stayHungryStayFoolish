using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.IO;
using System.Configuration;

namespace FileWatcher {
    //To watch file status changing of adding/ modification/ deleting based on file info
    public class FileLoopWatcher
    {
        //event category
        public static readonly int FILE_LOOP_WATCHER_EVENT_NOEVENT= 0;
        public static readonly int FILE_LOOP_WATCHER_EVENT_CREATE = 1;
        public static readonly int FILE_LOOP_WATCHER_EVENT_MODIFY = 2;
        public static readonly int FILE_LOOP_WATCHER_EVENT_DELETE = 4;
        //file info
        private string m_strFilePath;
        private DateTime m_createdTime;
        private DateTime m_lastWriteTime;
        private bool m_bFileExist;
        //default invalid date time if file does not exist
        private static readonly DateTime DEFAULT_DATETIME = new DateTime(1900, 1, 1);

        //call back function
        private Action<int> m_eventAction;
        
        //monitor thread parameter
        private Thread m_thread;
        private int m_iFileMonitorIntervalinSecs;
        private static readonly string KEY_MONITOR_INTERVAL_IN_SECS = "fileModifiedMonitorIntervalinSecs";
        private static readonly int DEFAULT_MONITOR_INTERVAL_IN_SECS = 10;
        private volatile int m_monitorEnable;
        private volatile int m_monitorThreadKeepAlive;
        private readonly object m_SyncObject;

        public FileLoopWatcher(string strFilePath, Action<int> action) {
            m_strFilePath = strFilePath;
            m_createdTime = DEFAULT_DATETIME;
            m_lastWriteTime = DEFAULT_DATETIME;
            m_bFileExist = false;
            try
            {
                if (0 != m_strFilePath.Length && File.Exists(m_strFilePath))
                {
                    m_lastWriteTime = File.GetLastWriteTime(m_strFilePath);
                    m_createdTime = File.GetCreationTime(m_strFilePath);
                    m_bFileExist = true;
                }
            }
            catch (Exception e) {
                //print Exception log;
                Console.WriteLine("Exception {0} happened when initializing file {1}", e.ToString(), m_strFilePath);
            }
            m_eventAction = action;
            try
            {
                m_iFileMonitorIntervalinSecs = int.Parse(ConfigurationManager.AppSettings.Get(KEY_MONITOR_INTERVAL_IN_SECS));
            }
            catch (Exception e) {
                //print Exception log;
                Console.WriteLine("Exception {0} happened when trying to get param:{1}, use default value instead", e.ToString(), KEY_MONITOR_INTERVAL_IN_SECS);
                m_iFileMonitorIntervalinSecs = DEFAULT_MONITOR_INTERVAL_IN_SECS;
            }
            
            m_monitorEnable = 0;
            m_monitorThreadKeepAlive = 1;
            m_SyncObject = new object();
            m_thread = null;
        }

        private void monitorFunc()
        {
            while (true) {
                if (0 == m_monitorThreadKeepAlive) {
                    break;
                }
                if (0 != m_monitorEnable && 0 != m_strFilePath.Length) {
                    try
                    {
                        int iChangeEventSet = FILE_LOOP_WATCHER_EVENT_NOEVENT;
                        bool bFileExist = File.Exists(m_strFilePath);
                        //create ?
                        if (bFileExist & !m_bFileExist)
                        {
                            iChangeEventSet |= FILE_LOOP_WATCHER_EVENT_CREATE;
                        }
                        //delete ?
                        if (!bFileExist & m_bFileExist)
                        {
                            iChangeEventSet |= FILE_LOOP_WATCHER_EVENT_DELETE;
                        }
                        m_bFileExist = bFileExist;
                        //modify ?
                        if (bFileExist)
                        {
                            DateTime createdTime = File.GetCreationTime(m_strFilePath);
                            DateTime writeTime = File.GetLastWriteTime(m_strFilePath);
                            if (createdTime != m_createdTime || writeTime != m_lastWriteTime)
                            {
                                m_createdTime = createdTime;
                                m_lastWriteTime = writeTime;
                                iChangeEventSet |= FILE_LOOP_WATCHER_EVENT_MODIFY;
                            }
                        }
                        //call back
                        if (FILE_LOOP_WATCHER_EVENT_NOEVENT != iChangeEventSet)
                        {
                            m_eventAction?.Invoke(iChangeEventSet);
                        }

                    }
                    catch (Exception e) {
                        //print Exception log;
                        Console.WriteLine("Exception : {0} happended during monitoring file:{1}", e.ToString(), m_strFilePath);
                    }
                }
                if (0 == m_monitorThreadKeepAlive)
                {
                    break;
                }
                Thread.Sleep(m_iFileMonitorIntervalinSecs * 1000);
            }
        }

        public bool start()
        {
            //1. check object status
            if (0 == m_strFilePath.Length || null == m_eventAction || 0 == m_iFileMonitorIntervalinSecs) {
                return false;
            }
            //2. create a singleton thread
            if (null == m_thread && null != m_SyncObject) {
                lock (m_SyncObject) {
                    if (null == m_thread)
                    {
                        m_thread = new Thread(monitorFunc);
                        if (null == m_thread)
                        {
                            return false;
                        }
                        m_thread.Start();
                    }
                }
            }
            //3. enable the monitor logic
            Interlocked.Exchange(ref m_monitorEnable, 1);
            return true;
        }

        public bool stop() {
            if (null == m_thread) {
                return false;
            }
            Interlocked.Exchange(ref m_monitorEnable, 0);
            return true;
        }

        ~FileLoopWatcher() {
            //recycle the monitor thread
            Interlocked.Exchange(ref m_monitorThreadKeepAlive, 0);
            if (null != m_thread && m_thread.IsAlive && 0 != m_iFileMonitorIntervalinSecs) {
                m_thread.Join(m_iFileMonitorIntervalinSecs * 1000 * 3);
            }
        }
    }
}