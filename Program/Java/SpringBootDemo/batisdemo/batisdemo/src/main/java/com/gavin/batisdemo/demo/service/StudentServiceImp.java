package com.gavin.batisdemo.demo.service;


import com.gavin.batisdemo.demo.pojo.Student;
import com.gavin.batisdemo.demo.dao.StudentMapper;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;


@Service
@Slf4j
public class StudentServiceImp implements StudentService{

    @Autowired
    StudentMapper studentMapper;

    @Override
    public Student GetStudentByid(Integer id){
        log.info(String.format("GetStudentByid %d", id));
        Student student = studentMapper.selectStudent(id);
        return student;
    }

    @Override
    public Boolean UpdateStudent(Integer id, String name){
        Student student = new Student(id, name);
        Boolean bRet = (1 == studentMapper.updateStudent(student));
        return bRet;
    }

    @Transactional(rollbackFor = {Exception.class, RuntimeException.class})
    @Override
    public Boolean UpdateStudentRollback(Integer id, String name){
        //Boolean bRet = studentDao.UpdateStudent(id, name);
        Student student = new Student(id, name);
        Boolean bRet = (1 == studentMapper.updateStudent(student));
        int a = 10/0;
        return bRet;
    }
}
