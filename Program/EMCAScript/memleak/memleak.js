var globalMap = {};
var i = 0;

function wait(ms) {
    return new Promise(resolve =>setTimeout(() =>resolve(), ms));
};

async function memleak(ms){
    while(true){
        await wait(ms);
        let str = '任何函数都可以让暂停的协程继续执行。任何函数都可以让暂停的协程继续执行。任何函数都可以让暂停的协程继续执行。任何函数都可以让暂停的协程继续执行。' + i;
        globalMap[i] = str;
        i++
    }
}

memleak(1);