// 页面加载时初始化
document.addEventListener('DOMContentLoaded', () => {
    loadHistory();
    loadStats();
});

const inputEl = document.getElementById('input');
const sendBtn = document.getElementById('sendBtn');
const messagesEl = document.getElementById('messages');
const loadingEl = document.getElementById('loading');
const clearBtn = document.getElementById('clearBtn');
const tabBtns = document.querySelectorAll('.tab-btn');

// 事件监听
sendBtn.addEventListener('click', sendMessage);
inputEl.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});
clearBtn.addEventListener('click', clearHistory);
tabBtns.forEach(btn => {
    btn.addEventListener('click', switchTab);
});

// 发送消息
async function sendMessage() {
    const message = inputEl.value.trim();
    if (!message) return;

    inputEl.value = '';

    // 显示用户消息
    addMessage(message, 'user');

    // 显示加载动画
    loadingEl.style.display = 'flex';
    document.getElementById('processContent').innerHTML = '<p class="placeholder">Agent 处理中...</p>';

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        const data = await response.json();

        if (data.success) {
            const result = data.data;

            // 显示 Agent 回复
            addMessage(result.final_answer, 'assistant');

            // 显示执行过程
            displayProcess(result);

            // 刷新历史
            loadHistory();
            loadStats();
        } else {
            addMessage(`错误: ${data.error}`, 'assistant');
        }
    } catch (error) {
        console.error(error);
        addMessage(`发生错误: ${error.message}`, 'assistant');
    } finally {
        loadingEl.style.display = 'none';
    }
}

// 添加消息
function addMessage(text, type) {
    const msgEl = document.createElement('div');
    msgEl.className = `message ${type}`;
    msgEl.textContent = text;
    messagesEl.appendChild(msgEl);
    messagesEl.scrollTop = messagesEl.scrollHeight;
}

// 显示执行过程
function displayProcess(result) {
    let html = '';

    if (result.scratchpad) {
        const lines = result.scratchpad.split('\n');
        lines.forEach(line => {
            if (!line.trim()) return;

            let stepClass = '';
            if (line.includes('Thought:')) stepClass = 'thought';
            else if (line.includes('Action:')) stepClass = 'action';
            else if (line.includes('Observation:')) stepClass = 'observation';
            else if (line.includes('Final Answer:')) stepClass = 'answer';

            if (stepClass) {
                html += `<div class="step ${stepClass}">${escapeHtml(line)}</div>`;
            }
        });
    }

    if (result.tools_used && result.tools_used.length > 0) {
        html += '<div class="step action">使用的工具：</div>';
        result.tools_used.forEach(tool => {
            html += `<div class="step" style="margin-left: 15px; border-left-color: #999;">
                    <strong>${tool.tool}</strong><br/>
                    输入: ${escapeHtml(JSON.stringify(tool.input))}<br/>
                    输出: ${escapeHtml(tool.output)}
                    </div>`;
        });
    }

    document.getElementById('processContent').innerHTML = html || '<p class="placeholder">无执行信息</p>';
}

// 加载历史
async function loadHistory() {
    try {
        const response = await fetch('/api/history');
        const data = await response.json();

        if (data.success) {
            let html = '';
            data.conversations.forEach(conv => {
                const time = new Date(conv.timestamp).toLocaleString('zh-CN');
                html += `
                    <div class="history-item">
                        <div class="history-item-user">👤 用户: ${escapeHtml(conv.user.substring(0, 50))}</div>
                        <div style="color: #666; font-size: 12px; margin-bottom: 4px;">🤖 ${escapeHtml(conv.assistant.substring(0, 100))}</div>
                        <div class="history-item-time">${time}</div>
                    </div>
                `;
            });
            document.getElementById('historyContent').innerHTML = html || '<p class="placeholder">暂无历史</p>';
        }
    } catch (error) {
        console.error(error);
    }
}

// 加载统计
async function loadStats() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();

        if (data.success) {
            const stats = data.stats;
            let html = `
                <div class="stat-item">
                    <span class="stat-label">总对话数</span>
                    <span class="stat-value">${stats.total_conversations}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">对话摘要</span>
                    <span class="stat-value">${stats.total_summaries}</span>
                </div>
            `;

            if (stats.latest_conversation) {
                const time = new Date(stats.latest_conversation.timestamp).toLocaleString('zh-CN');
                html += `
                    <div style="margin-top: 10px; padding: 10px; background: #f9f9f9; border-radius: 6px; font-size: 12px;">
                        <div style="font-weight: 600; margin-bottom: 5px;">最近对话</div>
                        <div style="color: #666; margin-bottom: 3px;">👤 ${escapeHtml(stats.latest_conversation.user.substring(0, 50))}</div>
                        <div style="color: #999; font-size: 11px;">${time}</div>
                    </div>
                `;
            }

            document.getElementById('statsContent').innerHTML = html;
        }
    } catch (error) {
        console.error(error);
    }
}

// 清空历史
async function clearHistory() {
    if (!confirm('确定要清空所有历史记录吗？')) return;

    try {
        const response = await fetch('/api/clear', { method: 'POST' });
        const data = await response.json();

        if (data.success) {
            messagesEl.innerHTML = '<div class="message system">✨ 历史已清空，开始新对话</div>';
            loadHistory();
            loadStats();
        }
    } catch (error) {
        console.error(error);
    }
}

// 切换选项卡
function switchTab(e) {
    tabBtns.forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));

    e.target.classList.add('active');
    const tabName = e.target.getAttribute('data-tab');
    document.getElementById(tabName).classList.add('active');
}

// 快速提问
function ask(question) {
    inputEl.value = question;
    inputEl.focus();
}

// HTML 转义
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}
