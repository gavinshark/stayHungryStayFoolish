package com.gavin.batisdemo.demo.web;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;


import com.gavin.batisdemo.demo.pojo.Student;
import com.gavin.batisdemo.demo.service.StudentService;

@Controller
public class StudentController {
    @Autowired
    private StudentService studentService;

    @RequestMapping(value="/student")
    public @ResponseBody Object GetStudent(Integer id){
        Student student = studentService.GetStudentByid(id);
        return student;
    }
}