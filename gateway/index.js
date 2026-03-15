const express = require('express');
const { spawn } = require('child_process');
const path = require('path');

const app = express();
// 解析 JSON 格式的请求体
app.use(express.json()); 

app.post('/api/task', (req, res) => {
    const userPrompt = req.body.prompt;
    
    if (!userPrompt) {
        return res.status(400).json({ error: '请在请求体中提供 prompt 参数' });
    }

    console.log(`\n[Gateway] 接收到新任务: ${userPrompt}`);
    console.log(`[Gateway] 正在唤起 Python Agent 进行处理...\n`);

    // 构建 Python 脚本的绝对路径
    const scriptPath = path.join(__dirname, '../backend/main.py');
    
    // 唤起 Python 进程 (注意：如果你的环境是 python3，这里可能需要改成 'python3')
    const pythonProcess = spawn('python', [scriptPath, userPrompt], {
        // 强制 Python 进程使用 UTF-8 编码进行标准输入输出
        env: { ...process.env, PYTHONIOENCODING: 'utf-8' }
    });

    let outputData = '';
    let errorData = '';

    // 持续捕获 Python 脚本的 标准输出 (stdout)
    pythonProcess.stdout.on('data', (data) => {
        const text = data.toString();
        // 我们可以在控制台实时打印 Agent 的思考过程
        process.stdout.write(text); 
        outputData += text;
    });

    // 持续捕获 Python 脚本的 错误输出 (stderr)
    pythonProcess.stderr.on('data', (data) => {
        errorData += data.toString();
    });

    // 监听 Python 进程结束事件
    pythonProcess.on('close', (code) => {
        if (code !== 0) {
            console.error(`\n[Gateway] 执行报错:\n${errorData}`);
            return res.status(500).json({ 
                status: 'error', 
                message: 'Agent 执行失败', 
                details: errorData 
            });
        }
        
        // 成功时，将 Python 收集到的最终输出返回给客户端
        res.json({
            status: 'success',
            // 取最后一部分作为纯净的报告内容返回（可根据实际打印格式用正则提取，这里简单返回全部）
            data: outputData.trim()
        });
    });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`=========================================`);
    console.log(`🚀 API Gateway 启动成功！`);
    console.log(`监听端口: http://localhost:${PORT}`);
    console.log(`测试端点: POST http://localhost:${PORT}/api/task`);
    console.log(`=========================================`);
});