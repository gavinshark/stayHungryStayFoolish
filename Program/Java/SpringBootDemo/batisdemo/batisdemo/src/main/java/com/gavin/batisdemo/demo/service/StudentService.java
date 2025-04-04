package com.gavin.batisdemo.demo.service;

import com.gavin.batisdemo.demo.pojo.Student;

public interface StudentService {
    Student GetStudentByid(Integer id);

    Boolean UpdateStudent(Integer id, String name);

    Boolean UpdateStudentRollback(Integer id, String name);
}
