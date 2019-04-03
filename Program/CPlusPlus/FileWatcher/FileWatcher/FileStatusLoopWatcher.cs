using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.IO;
using System.Configuration;

namespace FileWatcher {
    public class FileStatusLoopWatcher
    {
        //file info
        private string m_strFilePath;
        private DateTime m_createdTime;
        private DateTime m_lastWriteTime;
        //default invalid date time if file does not exist
        static DateTime DEFAULT_DATETIME = new DateTime(1900, 1, 1);

        //call back function
        private Action m_eventAction;
        
        //monitor thread parameter
        private Thread m_thread;
        private int m_iFileMonitorIntervalinSecs;
        private volatile int m_monitorEnable;
        private volatile int m_monitorThreadKeepAlive;
        private readonly object m_SyncObject;

        public FileStatusLoopWatcher(string strFilePath, Action action) {
            m_strFilePath = strFilePath;
            if (0 != m_strFilePath.Length && File.Exists(m_strFilePath))
            {
                m_lastWriteTime = File.GetLastWriteTime(m_strFilePath);
                m_createdTime = File.GetCreationTime(m_strFilePath);

            } else {
                m_createdTime = DEFAULT_DATETIME;
                m_lastWriteTime = DEFAULT_DATETIME;
            }
            m_eventAction = action;
            try
            {
                m_iFileMonitorIntervalinSecs = int.Parse(ConfigurationManager.AppSettings.Get("fileModifiedMonitorIntervalinSecs"));
            }
            catch (Exception e) {
                m_iFileMonitorIntervalinSecs = 10;
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
                if (0 != m_monitorEnable && 0 != m_strFilePath.Length && File.Exists(m_strFilePath)) {
                    DateTime createdTime = File.GetCreationTime(m_strFilePath);
                    DateTime writeTime = File.GetLastWriteTime(m_strFilePath);
                    if (createdTime != m_createdTime || writeTime != m_lastWriteTime) {
                        m_createdTime = createdTime;
                        m_lastWriteTime = writeTime;
                        m_eventAction?.Invoke();
                    }
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
            if (null == m_thread) {
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

        ~FileStatusLoopWatcher() {
            //recycle the monitor thread
            Interlocked.Exchange(ref m_monitorThreadKeepAlive, 0);
            if (null != m_thread && 0 != m_iFileMonitorIntervalinSecs) {
                m_thread.Join(m_iFileMonitorIntervalinSecs * 1000 * 3);
            }
        }
    }
}