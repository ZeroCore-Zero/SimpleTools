async function main() {
    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
      }
    console.log("Start");
    
    list=document.querySelectorAll("li[class='number']");
    list=list[list.length-1];
    num=Number(list.innerHTML);
    console.log("Get list number");
    
    var i=1;
    while(i<=num) {
        btn=document.querySelector(".el-checkbox__original");
        btn.click();
        btn=document.querySelector('span[style="margin-left: 8px; cursor: pointer; color: rgb(146, 146, 157);"]');
        btn.click();
        console.log(`Finish ${i}th`);
        await sleep(1000);
        i++;
    }
    console.log("Completly finish");
}
main();