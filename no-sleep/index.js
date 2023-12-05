const robot = require("robotjs");

// 设置一个时间间隔（毫秒）
const interval = 60000; // 例如，每60秒模拟一次键盘输入

// 循环调用函数
function preventScreenSleep() {
  // 模拟按下和释放一个无害的键，参考 https://robotjs.io/docs/syntax
  robot.keyTap("pageup");
  console.log("preventScreenSleep")
}   

// 每隔一段时间调用preventScreenSleep函数
setInterval(preventScreenSleep, interval);