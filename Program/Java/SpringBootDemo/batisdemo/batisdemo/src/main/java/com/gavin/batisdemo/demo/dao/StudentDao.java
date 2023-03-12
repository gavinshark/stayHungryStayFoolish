package com.gavin.batisdemo.demo.dao;

import org.apache.ibatis.annotations.Mapper;
import com.gavin.batisdemo.demo.pojo.Student;

@Mapper
public interface StudentDao {
    Student selectByPrimaryKey(Integer id);

    Boolean UpdateStudent(Integer id, String name);
}

