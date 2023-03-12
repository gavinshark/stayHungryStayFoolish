package com.gavin.batisdemo.demo.service;


import com.gavin.batisdemo.demo.pojo.Student;
import com.gavin.batisdemo.demo.dao.StudentDao;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;


@Service
public class StudentServiceImp implements StudentService{
    @Autowired
    private StudentDao studentDao;

    @Override
    public Student GetStudentByid(Integer id){
        Student student = studentDao.selectByPrimaryKey(id);
        return student;
    }

    @Override
    public Boolean UpdateStudent(Integer id, String name){
        Boolean bRet = studentDao.UpdateStudent(id, name);
        return bRet;
    }

    @Transactional(rollbackFor = {Exception.class, RuntimeException.class})
    @Override
    public Boolean UpdateStudentRollback(Integer id, String name){
        Boolean bRet = studentDao.UpdateStudent(id, name);
        int a = 10/0;
        return bRet;
    }
}
