package com.gavin.batisdemo.demo.dao;

import com.gavin.batisdemo.demo.pojo.Student;

public interface StudentMapper {
    Student selectStudent(Integer id);

    int updateStudent(Student student);
}
