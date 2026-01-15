/**
 * Bilibili空间动态删除脚本
 * 打开自己的空间，切换到动态界面，打开浏览器控制台粘贴执行。
 */

async function main() {
    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
      }
    window.scrollTo(0, document.getElementById("app").clientHeight)
    document.querySelectorAll('div[data-type="THREE_POINT_DELETE"]').forEach( (element)=>{ element.click() });
    await sleep(1000);
    document.querySelectorAll(".bili-modal__button.confirm").forEach( (element)=>{ element.click() }); 
    location.reload();
}
main();
console.log("Completly finish");

//另一种实现
setInterval(function () {
    $(".bili-dyn-more__menu__item")[1].click();
}, 1000);
setInterval(function (){
    $(".bili-modal__button")[0].click();
}, 1000);
// 作者：被迫重置
// 链接：https://www.zhihu.com/question/306653102/answer/2898189914
// 来源：知乎
// 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。