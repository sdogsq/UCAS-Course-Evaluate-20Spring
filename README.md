# UCAS-Course-Evaluate-20Spring

课程自动评估，2020春季学期使用，学期更换会导致评估页面`EvaPage`地址改变。

#### 使用方法

- 保存本项目至本地

    使用git

    ```text
    git clone https://github.com/sdogsq/UCAS-Course-Evaluate-20Spring.git
    ```

    或直接下载。

- 切换至项目保存目录，安装所需依赖

    ```text
    pip install -r requirements.txt
    ```

- 在参数`onestop_data`与中填入SEP用户名及密码。

- 在参数`cdata`与`tdata`中修改课程与老师评语（若需要）。

- 运行程序，等待完成。

#### 更新

July 15, 2020 : 更新2020夏季学期课程及教师评估。

June 23, 2020 : 完善使用说明，修复评教API。

May 6,  2020 : 更新20Spring课程评估及老师评估；

Dec 14, 2019 : 更新登录API为onestop，该接口登陆均不用输入验证码；优化输出格式，具体显示当前评估的课程和老师； 感谢@fubuki8087 加入教师评估。
