package com.gavinshark.mybatisDemo;

import java.io.IOException;
import java.io.InputStream;
import java.lang.*;
import org.apache.log4j.Logger;

import org.apache.ibatis.io.Resources;
import org.apache.ibatis.session.*;

public class MybatisWorker {
    private static final String resource = "mybatis-config.xml";
    private static InputStream inputStream;
    private static SqlSessionFactory sqlSessionFactory;
    private static Logger mylogger;
    static {
        try {
            //1. get factory
            mylogger = Logger.getLogger(MybatisWorker.class);
            inputStream = Resources.getResourceAsStream(resource);
            sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);
        } catch (IOException e){
            mylogger.error("error:" + e.toString());
        }
    }
    public static void displaySalarybyId(Integer id) throws IOException {
        //2.get session
        try (SqlSession session = sqlSessionFactory.openSession()) {
            SalaryDao mapper = session.getMapper(SalaryDao.class);
            Salary salary = mapper.getSalaryById(id);
            System.out.println("get salary of id=" + id + ", the result is:" + salary);
            mylogger.info("get salary of id=" + id + ", the result is:" + salary);
        }
    }
}
