var gor = require("goreplay_middleware");
var loggerUtil = require("./logger.js");
var config = require("./config.json");

gor.init();

var result = {};
result.matchSuccessCnt = 0;
result.matchFailCnt = 0;
result.batchMatchSuccessCnt = 0;
result.batchMatchFailCnt = 0;

var APITYPE = {
    "MATCH":1,
    "BATCHMATCH":2,
    "INVALID":-1
}

var startDate = new Date();

var logger = loggerUtil(config);
function INFO(str){
    logger.log("info", str);
}
function DEBUG(str){
    logger.log("debug", str);
}
function ERROR(str){
    logger.log("error", str);
}

gor.on("request", function(req) {
    DEBUG("request is :"+ req.http);
    var apiType = getReqAPIType(req);
    if(apiType == APITYPE.INVALID){
        return;
    }
    gor.on("response", req.ID, function(resp) {
        DEBUG("response is :"+ resp.http);
        gor.on("replay", req.ID, function(repl) {
            DEBUG("replay is :"+ repl.http);
            try{
                compareResponse(apiType, resp, repl);
            } catch (e) {
                ERROR("exception in compareResponse, apiType is :"+ apiType +", resp:" + resp.http + ", repl:" + repl.http + ", " + JSON.stringify(e.stack));
            }
            return repl;
        })
        return resp;
    })
    return req
})

function getReqAPIType(req){
    var apiType = APITYPE.INVALID;
    try{
        DEBUG("req path is:" + gor.httpPath(req.http));
        if(0 == gor.httpPath(req.http).indexOf("/match")){//volunerbility here, may match /match[\w]*
            apiType = APITYPE.MATCH;
        }
        else if(0 == gor.httpPath(req.http).indexOf("/batchMatch")){//volunerbility here, may match /batchMatch[\w]*
            apiType = APITYPE.BATCHMATCH;
        }
    } catch(e){
        ERROR("exception caught in getReqAPIType for req:"+req.http +","+ JSON.stringify(e.stack));
    }
    DEBUG("req apiType is:" + apiType);
    return apiType;
}

function compareResponse(apiType, resp, repl){
    if(APITYPE.MATCH == apiType){
        compareMatchResponse(resp, repl);
    } else if(APITYPE.BATCHMATCH == apiType)
    {
        compareBatchMatchResponse(resp, repl);        
    } else {
        ERROR("unsupported resp to compare:" + resp.http + ", repl:" + repl.http);
        return;
    }
}


function compareMatchResponse(resp, repl){
    DEBUG("compareMatchResponse start");
    var bTheSame = false;
    try{
        DEBUG("match resp body," + gor.httpBody(resp.http));
        DEBUG("match repl body," + gor.httpBody(repl.http));
        var respItem = JSON.parse(gor.httpBody(resp.http));
        var replItem = JSON.parse(gor.httpBody(repl.http));
        bTheSame = compareMatchItem(respItem, replItem);        
    } catch (e) {
        bTheSame = false;
        ERROR('exception in compareMatchResponse:'+ JSON.stringify(e.stack));
    }
    
    if(bTheSame){
        DEBUG("compareMatchResponse matchSuccess");
        result.matchSuccessCnt += 1;
        if(result.matchSuccessCnt % config.logMatchSuccessPeriod == 0){
            INFO("compareMatchResponse success for " + result.matchSuccessCnt +" events since " + startDate);
        }
    } else {
        result.matchFailCnt += 1;
        ERROR("compareMatchResponse failed the " + result.matchFailCnt + " time, resp is :" + gor.httpBody(resp.http) + ", repl is :" + gor.httpBody(repl.http));
    }
    return bTheSame;
}


function compareBatchMatchResponse(resp, repl){
    DEBUG("compareBatchMatchResponse start");
    var bTheSame = false;
    try{
        var respBodyStr = gor.httpBody(resp.http);
        var replBodyStr = gor.httpBody(repl.http);
        DEBUG("batch resp body," + respBodyStr);
        DEBUG("batch repl body," + replBodyStr);
        var respBody = JSON.parse(respBodyStr);
        var replBody = JSON.parse(replBodyStr);
        if(respBody.matchResultInfoList && replBody.matchResultInfoList){
            if(respBody.matchResultInfoList.length == replBody.matchResultInfoList.length){
                bTheSame = true;
                for (var idx = 0; idx < respBody.matchResultInfoList.length; idx++){
                    if(!compareMatchItem(respBody.matchResultInfoList[idx], replBody.matchResultInfoList[idx])){
                        bTheSame = false;
                        break;
                    }
                }
            }
        }    
    } catch (e) {
        bTheSame = false;
        ERROR('exception in compareMatchResponse:'+ JSON.stringify(e.stack));
    }
    
    if(bTheSame){
        DEBUG("compareBatchMatchResponse matchSuccess");
        result.batchMatchSuccessCnt += 1;
        if(result.batchMatchSuccessCnt % config.logBatchMathSuccessPeriod == 0){
            INFO("compareBatchMatchResponse success for " + result.batchMatchSuccessCnt + " events since " + startDate);
        }
    } else {
        result.batchMatchFailCnt += 1;
        ERROR("compareBatchMatchResponse failed the " + result.batchMatchFailCnt + " time, resp is :" + gor.httpBody(resp.http) + ", repl is :" + gor.httpBody(repl.http));
    }
    return bTheSame;
}

function compareMatchItem(respItem, replItem){
    if(respItem.companyId != replItem.companyId){
        return false;
    }
    if(respItem.userId != replItem.userId){
        return false;
    }
    if(respItem.companyId != replItem.companyId){
        return false;
    }
    if(!compareStringCantbeNull(respItem.paramA, replItem.paramA)){
        return false;
    }
    if(!compareStringCantbeNull(respItem.paramB, replItem.paramB)){
        return false;
    }
    return true;
}

function compareStringCantbeNull(strA, strB){
    var nullOrEmptyA = (!strA) || (0 == strA.length);
    var nullOrEmptyB = (!strB) || (0 == strB.length);
    if((nullOrEmptyA && nullOrEmptyB) || (strA == strB)){
        return true;
    } else {
        return false;
    }
}

INFO("duplicator middleware start within gor at:"+ startDate);

function unitest(){
    var resp = {};
    var repl = {};
    resp.http = 'HTTP/1.1 200 OK\r\n\
    Date: Fri, 21 Feb 2020 13:44:20 GMT\r\n\
    Content-Type: application/json;charset=utf-8\r\n\
    Content-Length: 301\r\n\r\n\
    {"policyType":1,"matchResultInfoList":[{"companyId":"12345678","userId":"batchtest1@test.com"},{"companyId":"12345678","userId":"user_testId@test.com","paramA":"","paramB":""}]}';
    
    repl.http = 'HTTP/1.1 200 OK\r\n\
    Date: Fri, 21 Feb 2020 13:44:20 GMT\r\n\
    Content-Type: application/json;charset=utf-8\r\n\
    Content-Length: 301\r\n\r\n\
    {"policyType":1,"matchResultInfoList":[{"companyId":"12345678","userId":"batchtest1@test.com"},{"companyId":"12345678","userId":"user_testId@test.com"}]}';

    var bTheSame = compareBatchMatchResponse(resp, repl);
    if(!bTheSame){
        console.log('ERROR! unitest failed');        
    } else {
        console.log('SUCCESS! unitest passed');
    }
}

module.exports = {
    unitest: unitest
};