package com.gavin.batisdemo.demo.web;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;


import com.gavin.batisdemo.demo.pojo.Student;
import com.gavin.batisdemo.demo.service.StudentService;

@Controller
public class StudentController {
    @Autowired
    private StudentService studentService;

    @RequestMapping(value="/student/{id}")
    public @ResponseBody Object GetStudent(@PathVariable Integer id){
        Student student = studentService.GetStudentByid(id);
        return student;
    }

    @RequestMapping(value = "/student/{id}", method = RequestMethod.PUT)
    public @ResponseBody Boolean UpdateStudent(@PathVariable Integer id, String name){
        Boolean bRet = studentService.UpdateStudent(id, name);
        return bRet;
    }

    @RequestMapping(value = "/studentrollback/{id}", method = RequestMethod.PUT)
    public @ResponseBody Boolean UpdateStudentRollback(@PathVariable Integer id, String name){
        Boolean bRet = studentService.UpdateStudentRollback(id, name);
        return bRet;
    }
}