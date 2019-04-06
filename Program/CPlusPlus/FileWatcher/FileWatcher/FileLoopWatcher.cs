using System;
using System.Threading;
using System.IO;
using System.Configuration;

namespace FileWatcher {
    //To watch file status changing of adding/ modification/ deleting based on looping querying file's info
    public class FileLoopWatcher
    {
        //event category
        public const int FILE_LOOP_WATCHER_EVENT_NOEVENT= 0;
        public const int FILE_LOOP_WATCHER_EVENT_CREATE = 1;
        public const int FILE_LOOP_WATCHER_EVENT_MODIFY = 2;
        public const int FILE_LOOP_WATCHER_EVENT_DELETE = 4;
        public const int FILE_LOOP_WATCHER_EVENT_ALL = 0xff;
        //file info
        private string m_strFilePath;
        private DateTime m_createdTime;
        private DateTime m_lastWriteTime;
        private bool m_bFileExist;
        //default invalid date time if file does not exist
        private static readonly DateTime DEFAULT_DATETIME = new DateTime(1900, 1, 1);

        //call back function
        private Action m_eventAction;
        private int m_iInterestedEvents;
        
        //monitor thread parameter
        private Thread m_thread;
        private int m_iFileMonitorIntervalinSecs;
        private const string KEY_MONITOR_INTERVAL_IN_SECS = "fileMonitorIntervalinSecs";
        private const int DEFAULT_MONITOR_INTERVAL_IN_SECS = 10;
        private readonly ManualResetEvent m_exitEvent = new ManualResetEvent(false);
        private object m_syncObject;

        public FileLoopWatcher(string strFilePath, int iInterestedEvents, Action action) {
            m_strFilePath = strFilePath;
            m_iInterestedEvents = iInterestedEvents;
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
            
            m_syncObject = new object();
            m_thread = null;
        }

        private void monitorFunc()
        {
            while (m_exitEvent.WaitOne(m_iFileMonitorIntervalinSecs * 1000) == false)
            {
                if (0 != m_strFilePath.Length)
                {
                    try
                    {
                        int iChangeEvents = FILE_LOOP_WATCHER_EVENT_NOEVENT;
                        bool bFileExist = File.Exists(m_strFilePath);
                        //create ?
                        if (bFileExist & !m_bFileExist)
                        {
                            iChangeEvents |= FILE_LOOP_WATCHER_EVENT_CREATE;
                        }
                        //delete ?
                        if (!bFileExist & m_bFileExist)
                        {
                            iChangeEvents |= FILE_LOOP_WATCHER_EVENT_DELETE;
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
                                iChangeEvents |= FILE_LOOP_WATCHER_EVENT_MODIFY;
                            }
                        }
                        //call back
                        if (0 != (m_iInterestedEvents & iChangeEvents))
                        {
                            m_eventAction?.Invoke();
                        }

                    }
                    catch (Exception e)
                    {
                        //print Exception log;
                        Console.WriteLine("Exception : {0} happended during monitoring file:{1}", e.ToString(), m_strFilePath);
                    }
                }
            }
        }

        public bool Start()
        {
            //1. check status
            if (0 == m_strFilePath.Length || null == m_eventAction || 0 == m_iFileMonitorIntervalinSecs) {
                return false;
            }
            //2. create a singleton thread
            if (null == m_thread && null != m_syncObject) {
                lock (m_syncObject) {
                    if (null == m_thread)
                    {
                        m_exitEvent.Reset();
                        m_thread = new Thread(monitorFunc);
                        if (null == m_thread)
                        {
                            return false;
                        }
                        m_thread.Start();
                    }
                    else
                    {
                        return false;
                    }
                }
            }
            else
            {
                return false;
            }
            return true;
        }

        public bool End() {
            if (null != m_thread && m_thread.IsAlive && null != m_syncObject)
            {
                lock (m_syncObject)
                {
                    if (null != m_thread && m_thread.IsAlive)
                    {
                        m_exitEvent.Set();
                        m_thread.Join();
                        m_thread = null;
                        return true;
                    }
                    else
                    {
                        return false;
                    }
                }
            }
            else
            {
                return false;
            }
            return false;
        }        
    }
}