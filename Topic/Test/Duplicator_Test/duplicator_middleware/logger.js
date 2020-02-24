'use strict';

const winston = require('winston');

module.exports = (config) => {

    let winston_transports = [];
    
    winston_transports.push(
        new(winston.transports.File)({
            name: 'ops_log',
            level: 'info',
            filename: config.log.ops_file,
            timestamp: true,
            json: false,
            maxsize: 26214400,
            tailable: true,
            maxFiles: 10
        })
    );
    // Set Log levels to syslog + user level
    // detail see: https://github.com/winstonjs/winston/tree/2.x#logging-levels
    let myCustomLevels = {
        levels: {
            audit: 0,
            emerg: 1,
            alert: 2,
            crit: 3,
            error: 4,
            warning: 5,
            notice: 6,
            info: 7,
            debug: 8,
            user: 9
        },
        colors: {
            debug: 'blue',
            info: 'green',
            notice: 'yellow',
            warning: 'red',
            error: 'red',
            crit: 'red',
            alert: 'yellow',
            emerg: 'red',
            user: 'white',
            audit: 'white'
        }
    };
    
    // Set Logger Configurations
    const logger = new(winston.Logger)({
        transports: winston_transports,
        levels: myCustomLevels.levels,
        colors: myCustomLevels.colors
    });
    
    return logger;
};