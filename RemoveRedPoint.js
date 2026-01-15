/**
 * 北邮云邮平台红点移除
 * 登入云邮切换到通知界面，打开浏览器控制台执行。
 */

async function main() {
    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
      }
    console.log("Start");
    
    let list=document.querySelectorAll("li[class='number']");
    list=list[list.length-1];
    let num=Number(list.innerHTML);
    console.log("Get list number");
    
    for(let i=1; i<=num; i++) {
        document.querySelector(".el-checkbox__original").click();
        document.querySelector('span[style="margin-left: 8px; cursor: pointer; color: rgb(146, 146, 157);"]').click();
        console.log(`Finish ${i}th`);
        await sleep(500);
        i++;
    }
    console.log("Completly finish");
}
main();