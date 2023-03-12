package com.gavin.batisdemo.demo.dao;

import com.gavin.batisdemo.demo.pojo.Student;
import org.apache.ibatis.io.Resources;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;
import org.springframework.stereotype.Repository;

import java.io.IOException;
import java.io.Reader;


@Repository
public class StudentDaoImp implements StudentDao{

    private static SqlSessionFactory sqlSessionFactory;

    static {
        try {
            Reader reader = Resources.getResourceAsReader("com/gavin/batisdemo/demo/dao/mybatis-config.xml");
            sqlSessionFactory = new SqlSessionFactoryBuilder().build(reader);
        } catch (IOException e){
            e.printStackTrace();
        }
    }

    @Override
    public Student selectByPrimaryKey(Integer id)
    {
        Student student = null;
        try (SqlSession session = sqlSessionFactory.openSession()) {
            StudentMapper mapper = session.getMapper(StudentMapper.class);
            student = mapper.selectStudent(id);
        } catch (Exception e){
            e.printStackTrace();
        }
        return student;
    }
}
