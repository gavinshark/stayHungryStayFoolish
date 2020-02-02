package com.gavinshark.mybatisDemo;

import java.io.IOException;
import java.io.InputStream;
import java.lang.*;
import org.apache.log4j.Logger;

import org.apache.ibatis.io.Resources;
import org.apache.ibatis.session.*;

public class MybatisWorker {
    public static void displaySalarybyId(Integer id) throws IOException {
        //1. get factory
        InputStream inputStream = Resources.getResourceAsStream("mybatis-config.xml");
        SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);
        //2.get session
        try (SqlSession session = sqlSessionFactory.openSession()) {
            SalaryDao mapper = session.getMapper(SalaryDao.class);
            Salary salary = mapper.getSalaryById(id);
            System.out.println("get salary of id=" + id + ", the result is:" + salary);
            Logger mylogger = Logger.getLogger(MybatisWorker.class.getName());
            mylogger.info("get salary of id=" + id + ", the result is:" + salary);
        }
    }
}
