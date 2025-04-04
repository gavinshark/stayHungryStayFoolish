package com.gavin.mvcdemo.web;

import com.gavin.mvcdemo.config.Storage;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
public class RestResolver{
        @Autowired
        private Storage storage;

        @Value("version")
        private String version;

        @RequestMapping(value="/storagePath")
        public @ResponseBody String getStoragePath(){
                return version + ":" + storage.getPath();
        }
}