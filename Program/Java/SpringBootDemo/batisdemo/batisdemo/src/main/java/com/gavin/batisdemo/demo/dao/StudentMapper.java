package com.gavin.batisdemo.demo.dao;

import com.gavin.batisdemo.demo.pojo.Student;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface StudentMapper {
    Student selectStudent(Integer id);

    int updateStudent(Student student);
}
