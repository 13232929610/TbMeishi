# TbMeishi
应用selenium抓取淘宝美食的信息

本项目主要运用selenium实现主要功能，用谷歌浏览器作为测试，动态抓取淘宝上的美食信息，然后用无界面浏览器提升效率

本项目的主要流程如下：

1.创建webdriver的Chrome对象，打开淘宝首页，然后补抓搜索框和搜索按钮的位置

2.向搜索框中输入关键字信息，然后自动点击搜索按钮

3.跳到商品信息页面，补抓到页面的最大页数

4.补抓页码输入框与确定按钮的位置

5.模拟向输入框中输入数字，点击确定跳转到下一页，如此遍历至页码最大值为止

6.每次翻页都补抓当前页的主要内容，运用pyquery提取出有价值的信息

7.将信息以键值对的格式返回，然后存储到MongoDB中

8.谷歌浏览器用于测试，测试成功后，为了提升效率，改用无界面浏览器