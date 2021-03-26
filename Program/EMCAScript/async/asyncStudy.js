async function lazyMerge(content){
    return new Promise((resolve, reject)=>{
        setTimeout(function(){
            resolve('content:' + content);
        }, 1*1000)
    });
}


var gen = function* (){
  var rA = yield lazyMerge('fileA');
  console.log(rA.toString());
  var rB = yield lazyMerge('fileB'+ '&' + rA);
  console.log(rB.toString());
};

var g = gen();
var AYieldResult = g.next(); //{value:lazyMerge('fileA'), done:false}
var APromise = AYieldResult.value; //lazyMerge('fileA')即一个promise对象

//APromise.then => 得到content:fileA
APromise.then(function(contentA){
   var BYieldResult =  g.next(contentA); //{value:lazyMerge('fileB'+'&'+'content:fileA'), done:false},把rA = yield lazyMerge(fileA) 替换成 rA = contentA，然后一直执行到var rB = yield lazyMerge('fileB'+'&'+'content:fileA');
   var resultBP = BYieldResult.value;//lazyMerge('fileB'+'&'+'content:fileA')即一个promise对象
   return resultBP;
}).then(function(contentB){//APromise.then => 得到了fileB_content
    return g.next(contentB); //把var rB = yield lazyMerge('fileB'+'&'+'content:fileA');换成var rB = 'content:fileB&content:fileA';并执行到最后
});