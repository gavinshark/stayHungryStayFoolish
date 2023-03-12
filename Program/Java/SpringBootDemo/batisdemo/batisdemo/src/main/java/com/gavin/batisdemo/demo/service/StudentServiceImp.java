package com.gavin.batisdemo.demo.service;


import com.gavin.batisdemo.demo.pojo.Student;
import com.gavin.batisdemo.demo.dao.StudentDao;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class StudentServiceImp implements StudentService{
    @Autowired
    private StudentDao studentDao;

    @Override
    public Student GetStudentByid(Integer id){
        Student student = studentDao.selectByPrimaryKey(id);
        return student;
    }
}
