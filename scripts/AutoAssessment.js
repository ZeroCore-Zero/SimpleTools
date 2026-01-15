/**
 * 北邮教务系统教师评分自动化脚本
 * 
 * 使用方法：登录教务系统后打开教师评分界面，进入其中一个评分界面后打开浏览器控制台，粘贴脚本执行。
 * 每个教师的评分界面执行一次即可。
 * 如果分数过高/过低重新执行一次。
 */

function main() {
    const page = document.getElementById("NEW_XSD_JXPJ_JXPJ_XSPJ").contentWindow;
    page.window.alert = () => {};
    // 单选题
    page.document.getElementsByName("zbtd").forEach(element => {
        if(Math.random() < 0.6) element.querySelectorAll("input[type=radio]")[0].click();
        else element.querySelectorAll("input[type=radio]")[1].click();
    });
    // 多选题
    Array.from(
        page.document.querySelectorAll("input[type=checkbox]")
    ).slice(0, 10).forEach(element => element.checked=true);
    // 提交
    page.document.getElementsByName("bc")[0].click()
}

main();