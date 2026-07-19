# 百问即查 3.0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 百问即查 3.0 仪表盘改版——免登录、侧边栏导航、智能问答、交互式练习题

**Architecture:** 前端全面重写为侧边栏+主内容区布局，后端新增 `/api/chat-simple` 和 `/api/exercise/generate` 两个端点。旧版多智能体全资源生成逻辑注释保留。数据库新增 `avatar` 字段支持头像选择。

**Tech Stack:** FastAPI + Python f-string 内联 HTML/CSS/JS + SQLite + DeepSeek (OpenAI SDK)

---

## File Structure

| 文件 | 职责 |
|------|------|
| `services/database.py` | 新增 avatar 列 + 更新 `_update_internal` allowed 字段 |
| `main.py` | 版本号 3.0、启动日志、.env 加载 |
| `agents/orchestrator.py` | 注释 `_analyze_request()` 和 `process_request()` |
| `api/routes.py` | 全面重写：新版前端 + `/api/chat-simple` + `/api/exercise/generate` + 注释注册和旧 generate |

---

### Task 1: Database — 添加 avatar 字段

**Files:**
- Modify: `services/database.py`

- [ ] **Step 1: 在 `init_db()` 的 CREATE TABLE 中加入 avatar 列**

在 `students` 表定义中 `updated_at TEXT DEFAULT ''` 后面添加：

```sql
CREATE TABLE IF NOT EXISTS students (
    ...
    programming_exp TEXT DEFAULT '',
    avatar TEXT DEFAULT 'avatar-1',
    created_at TEXT DEFAULT '',
    updated_at TEXT DEFAULT ''
)
```

- [ ] **Step 2: 在 `_seed_defaults()` 的 INSERT 中加入 avatar**

在 `_seed_defaults` 函数的列列表和 VALUES 中加入 `avatar`：

```python
conn.execute("""
    INSERT INTO students (student_id, password, name, school, major, grade,
        knowledge_base, cognitive_style, weak_points, learning_goals,
        learning_pace, interest_topics, preferred_resource_types,
        programming_exp, avatar, created_at, updated_at)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
""", (
    d["student_id"], d["password"], d["name"], d["school"],
    d["major"], d["grade"], d["knowledge_base"], d["cognitive_style"],
    d["weak_points"], d["learning_goals"], d["learning_pace"],
    d["interest_topics"], d["preferred_resource_types"],
    d["programming_exp"], d.get("avatar", "avatar-1"), d["created_at"], d["updated_at"],
))
```

- [ ] **Step 3: 在 `_update_internal()` 的 allowed 集合中加入 `"avatar"`**

```python
allowed = {
    "name", "school", "major", "grade", "knowledge_base",
    "cognitive_style", "weak_points", "learning_goals", "learning_pace",
    "interest_topics", "preferred_resource_types", "programming_exp", "avatar",
}
```

- [ ] **Step 4: 在 `_row_to_profile()` 中读取 avatar**

```python
@staticmethod
def _row_to_profile(row: sqlite3.Row) -> StudentProfile:
    return StudentProfile(
        ...
        programming_exp=row["programming_exp"] or "",
        avatar=row["avatar"] or "avatar-1",
        created_at=row["created_at"] or "",
        updated_at=row["updated_at"] or "",
    )
```

- [ ] **Step 5: 在 `save_profile()` 的 INSERT 中加入 avatar**

```python
conn.execute("""
    INSERT INTO students (student_id, password, name, school, major, grade,
        knowledge_base, cognitive_style, weak_points, learning_goals,
        learning_pace, interest_topics, preferred_resource_types,
        programming_exp, avatar, created_at, updated_at)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
""", (
    profile.student_id, profile.password or "123456",
    profile.name, profile.school, profile.major, profile.grade,
    profile.knowledge_base, profile.cognitive_style,
    json.dumps(profile.weak_points, ensure_ascii=False),
    json.dumps(profile.learning_goals, ensure_ascii=False),
    profile.learning_pace,
    json.dumps(profile.interest_topics, ensure_ascii=False),
    json.dumps(profile.preferred_resource_types, ensure_ascii=False),
    profile.programming_exp, profile.avatar or "avatar-1", now, now,
))
```

- [ ] **Step 6: 更新 StudentProfile 模型，添加 avatar 字段**

读 `models/profile.py`，在 `StudentProfile` dataclass 中添加：

```python
avatar: str = "avatar-1"
```

- [ ] **Step 7: Commit**

```bash
git add services/database.py models/profile.py
git commit -m "feat: add avatar field to students table and profile model"
```

---

### Task 2: Orchestrator — 注释旧分发逻辑

**Files:**
- Modify: `agents/orchestrator.py`

- [ ] **Step 1: 在文件顶部添加 v3.0 注释说明**

```python
"""
[v3.0] 多智能体编排器 —— 全资源生成功能已注释
本文件保留 KEYWORD_TASK_MAP 和 agent_map 以备后续复用。
"""
```

- [ ] **Step 2: 注释 `_analyze_request()` 方法体**

在 `_analyze_request` 函数体开头加 `"""` 返回默认值：

```python
def _analyze_request(self, request: str) -> List[str]:
    """[v3.0 已注释] 旧版 LLM 意图分析，不再使用"""
    # [v3.0 已注释] 全资源生成功能已移除，此方法保留仅作参考
    return ["document"]
```

- [ ] **Step 3: 注释 `process_request()` 方法体**

```python
def process_request(self, profile, request: str) -> dict:
    """[v3.0 已注释] 旧版多智能体协同资源生成，不再使用"""
    # [v3.0 已注释] 原多智能体分发逻辑。前端入口已移除，API 端点已注释。
    logger.warning("[v3.0] process_request 已被禁用，返回空结果")
    return {}
```

- [ ] **Step 4: Commit**

```bash
git add agents/orchestrator.py
git commit -m "chore: comment out old orchestrator dispatch logic for v3.0"
```

---

### Task 3: main.py — 版本号和启动日志更新

**Files:**
- Modify: `main.py`

- [ ] **Step 1: 更新版本描述**

```python
"""
多智能体个性化学习系统 3.0 —— 主程序入口（免登录·仪表盘版）

启动方式：
  python main.py                    # 启动 Web 服务（Mock 模式）
  python main.py --provider openai  # 使用 OpenAI
  python main.py --provider anthropic  # 使用 Anthropic
"""
```

- [ ] **Step 2: 添加 dotenv 加载**

在 import 区域：

```python
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
```

- [ ] **Step 3: 更新启动日志**

```python
logger.info(f"启动 Web 服务: http://localhost:{port}")
logger.info(f"版本: 3.0 (免登录·仪表盘版)")
logger.info(f"LLM 提供商: {args.provider}, 模型: {args.model}")
logger.info(f"可用接口:")
logger.info(f"  POST /api/chat-simple  - 智能问答（纯文本对话）")
logger.info(f"  POST /api/exercise/generate - 练习题生成")
logger.info(f"  POST /api/chat         - 对话式画像构建")
logger.info(f"  GET  /api/profile/     - 获取画像")
logger.info(f"  PUT  /api/profile/update - 更新画像")
logger.info(f"  PUT  /api/config/llm   - 更新LLM配置")
```

- [ ] **Step 4: Commit**

```bash
git add main.py
git commit -m "chore: bump version to 3.0, add dotenv loading, update startup log"
```

---

### Task 4: routes.py — 前端全面重写 + 新 API 端点

**Files:**
- Modify: `api/routes.py`

This is the largest task. The file (~1047 lines) gets a full frontend rewrite and new endpoints.

- [ ] **Step 1: 更新文件头部 docstring 和导入**

在文件顶部添加 v3.0 说明：

```python
"""
FastAPI 路由 v3.0 —— 仪表盘版
新增: /api/chat-simple (智能问答), /api/exercise/generate (练习题生成)
已注释: /api/register, /api/generate (旧多智能体全资源生成)
"""
```

导入保持不变。

- [ ] **Step 2: 注释 RegisterRequest 模型**

```python
# [v3.0 已注释] 注册功能已禁用
# class RegisterRequest(BaseModel):
#     school: str = ""
#     major: str = ""
#     grade: str = ""
#     password: str = ""
#     description: str = ""
```

- [ ] **Step 3: 新增 Pydantic 模型**

```python
class ChatSimpleRequest(BaseModel):
    student_id: str
    message: str

class ExerciseGenerateRequest(BaseModel):
    student_id: str
    question_type: str = "choice"  # choice / fill_blank / short_answer
    count: int = 5
    course_name: str = "人工智能"
```

- [ ] **Step 4: 重写 create_app() 初始化部分**

保留 llm_service, db, orchestrator, agents, resource_db 的初始化，更新版本号：

```python
app = FastAPI(
    title="百问即查 3.0 - AI 智能学习助手",
    version="3.0.0",
)
```

- [ ] **Step 5: 重写 GET / 前端 HTML/CSS/JS**

这是主体的前端重写。完整的新版 HTML/CSS/JS 包含：

**CSS 部分（内联在 `<style>` 中）：**
- 侧边栏样式（220px 固定，深色背景渐变）
- 主内容区样式（flex 自适应）
- 右上角用户区样式（头像圆 + 姓名）
- 仪表盘卡片网格（2列 grid + 渐变图标）
- 智能问答聊天面板样式
- 做练习题多步面板样式
- 个人信息覆盖弹窗样式
- 头像选择器网格（4x2）样式

**HTML 结构：**

```html
<body>
<!-- 侧边栏 -->
<nav class="sidebar" id="sidebar">
  <div class="sb-logo">百问即查</div>
  <div class="sb-sub">3.0</div>
  <div class="sb-menu">
    <div class="sb-item active" data-panel="dashboard">
      <span>📊</span> 学习仪表盘
    </div>
    <div class="sb-section">
      <div class="sb-section-title" id="assistantToggle">
        <span>▼</span> 百问助手
      </div>
      <div class="sb-sub-items" id="assistantSubItems">
        <div class="sb-sub-item" data-panel="chat">
          <span>💬</span> 智能问答
        </div>
        <div class="sb-sub-item" data-panel="exercise">
          <span>📝</span> 做练习题
        </div>
        <div class="sb-sub-item disabled" data-panel="docs">
          <span>📄</span> 课程文档 <small>待开发</small>
        </div>
        <div class="sb-sub-item disabled" data-panel="path">
          <span>🗺️</span> 学习路径 <small>待开发</small>
        </div>
      </div>
    </div>
  </div>
  <div class="sb-bottom">
    <div class="sb-item" onclick="doLogout()">
      <span>🚪</span> 退出登录
    </div>
  </div>
</nav>

<!-- 主内容区 -->
<div class="main" id="mainApp">
  <!-- 右上角用户区 -->
  <div class="user-corner">
    <div class="user-btn" onclick="showProfile()">
      <div class="user-avatar" id="cornerAvatar">
        <span id="cornerEmoji">📚</span>
      </div>
      <span id="cornerName">张三</span>
    </div>
  </div>

  <!-- 仪表盘面板 (默认) -->
  <div class="panel active" id="dashboardPanel">
    <h2>学习仪表盘</h2>
    <div class="dash-grid">
      <div class="dash-card">
        <div class="dash-icon" style="background:linear-gradient(135deg,#6c63ff,#5b52e0)">📖</div>
        <div class="dash-info">
          <div class="dash-value">3/6</div>
          <div class="dash-label">已学习资源类型</div>
          <div class="dash-bar"><div class="dash-bar-fill" style="width:50%"></div></div>
        </div>
      </div>
      <div class="dash-card">
        <div class="dash-icon" style="background:linear-gradient(135deg,#48c6ef,#6c63ff)">⏱</div>
        <div class="dash-info">
          <div class="dash-value">5.5 小时</div>
          <div class="dash-label">本周学习时间</div>
        </div>
      </div>
      <div class="dash-card">
        <div class="dash-icon" style="background:linear-gradient(135deg,#f093fb,#f5576c)">📌</div>
        <div class="dash-info">
          <div class="dash-value">人工智能基础</div>
          <div class="dash-label">最近学习课程</div>
        </div>
      </div>
    </div>
  </div>

  <!-- 智能问答面板 -->
  <div class="panel" id="chatPanel">
    <h2>智能问答</h2>
    <div class="chat-msgs" id="chatMsgs">
      <div class="c-msg bot">你好！我是百问助手。有什么问题我可以帮你解答？</div>
    </div>
    <div class="chat-input-area">
      <input id="chatInput" placeholder="输入你的问题..." onkeydown="if(event.key==='Enter') sendChat()">
      <button onclick="sendChat()">发送</button>
    </div>
  </div>

  <!-- 做练习题面板 -->
  <div class="panel" id="exercisePanel">
    <h2>做练习题</h2>
    <div class="ex-container" id="exContainer">
      <!-- 动态切换步骤内容 -->
    </div>
  </div>
</div>

<!-- 个人信息弹窗 -->
<div class="profile-overlay" id="profileOverlay">
  <div class="profile-modal">
    <div class="profile-head">
      <h3>个人信息</h3>
      <button class="close-btn" onclick="closeProfile()">✕</button>
    </div>
    <div class="profile-body">
      <!-- 头像选择器 -->
      <div class="pf-avatar-section">
        <div class="pf-avatar-preview" id="pfAvatarPreview" onclick="toggleAvatarPicker()">
          <span id="pfAvatarEmoji">📚</span>
        </div>
        <div class="avatar-picker-grid" id="avatarPickerGrid" style="display:none;">
          <!-- 8个头像通过JS生成 -->
        </div>
      </div>
      <!-- 其他字段 -->
      <div class="pf-field"><label>学号</label><input id="pfSid" disabled></div>
      <div class="pf-field"><label>姓名</label><input id="pfName"></div>
      <div class="pf-field"><label>学校</label><input id="pfSchool" list="schoolList"></div>
      <div class="pf-field"><label>专业</label><input id="pfMajor" list="majorList"></div>
      <div class="pf-field"><label>年级</label><select id="pfGrade">...</select></div>
      <div class="pf-field"><label>知识基础</label><textarea id="pfKnowledgeBase"></textarea></div>
      <div class="pf-field"><label>认知风格</label><input id="pfCognitiveStyle"></div>
      <div class="pf-field"><label>薄弱知识点</label><textarea id="pfWeakPoints"></textarea></div>
      <div class="pf-field"><label>学习目标</label><textarea id="pfGoals"></textarea></div>
      <div class="pf-field"><label>学习节奏</label><input id="pfPace"></div>
      <div class="pf-field"><label>兴趣方向</label><textarea id="pfInterests"></textarea></div>
    </div>
    <div class="profile-foot">
      <button class="save-btn" onclick="saveProfile()">保存修改</button>
      <button class="delete-btn" onclick="deleteAccount()">注销账号</button>
    </div>
  </div>
</div>
```

**JavaScript 核心逻辑（内联在 `<script>` 中）：**

```javascript
const BASE = '';
let studentId = '';
let profileData = null;
let currentPanel = 'dashboard';
let exerciseState = { step: 'type', type: '', count: 5, course: '', questions: [], currentIndex: 0, answers: [] };

const AVATARS = [
  { id: 'avatar-1', emoji: '📚', gradient: 'linear-gradient(135deg,#6c63ff,#a78bfa)' },
  { id: 'avatar-2', emoji: '💻', gradient: 'linear-gradient(135deg,#3b82f6,#60a5fa)' },
  { id: 'avatar-3', emoji: '🧠', gradient: 'linear-gradient(135deg,#10b981,#34d399)' },
  { id: 'avatar-4', emoji: '🚀', gradient: 'linear-gradient(135deg,#f97316,#fb923c)' },
  { id: 'avatar-5', emoji: '✨', gradient: 'linear-gradient(135deg,#ec4899,#f472b6)' },
  { id: 'avatar-6', emoji: '🎯', gradient: 'linear-gradient(135deg,#06b6d4,#22d3ee)' },
  { id: 'avatar-7', emoji: '🔥', gradient: 'linear-gradient(135deg,#ef4444,#f87171)' },
  { id: 'avatar-8', emoji: '⚡', gradient: 'linear-gradient(135deg,#6366f1,#818cf8)' },
];

// 课程列表（根据学生画像匹配）
const COURSE_OPTIONS = {
  '人工智能': ['Python编程', '机器学习', '深度学习'],
  '电子信息': ['电路原理', '信号处理', '嵌入式系统'],
  '计算机科学与技术': ['Python编程', '数据结构', '人工智能'],
  '数学与应用数学': ['数学分析', '线性代数', '概率统计'],
  'default': ['Python编程', '人工智能', '数据结构'],
};

function getCourseOptions(profile) {
  const major = profile?.major || '';
  for (const [k, v] of Object.entries(COURSE_OPTIONS)) {
    if (major.includes(k)) return v;
  }
  return COURSE_OPTIONS['default'];
}

// === 自动登录 ===
(function() {
  api('/api/login', {method:'POST', body:JSON.stringify({student_id:'stu_001', password:'123456'})})
    .then(d => { if (d.success) { studentId=d.student_id; profileData=d.profile; enterApp(d.profile); } })
    .catch(() => {});
})();

function enterApp(profile) {
  profileData = profile;
  document.getElementById('cornerName').textContent = profile.name || '张三';
  const avatarId = profile.avatar || 'avatar-1';
  const avatar = AVATARS.find(a => a.id === avatarId) || AVATARS[0];
  updateCornerAvatar(avatar);
  switchPanel('dashboard');
}

function updateCornerAvatar(avatar) {
  const el = document.getElementById('cornerAvatar');
  el.style.background = avatar.gradient;
  document.getElementById('cornerEmoji').textContent = avatar.emoji;
}

// === 侧边栏导航 ===
document.getElementById('assistantToggle').addEventListener('click', function() {
  this.classList.toggle('collapsed');
  document.getElementById('assistantSubItems').classList.toggle('collapsed');
  const arrow = this.querySelector('span');
  arrow.textContent = this.classList.contains('collapsed') ? '▶' : '▼';
});

document.querySelectorAll('.sb-sub-item:not(.disabled)').forEach(item => {
  item.addEventListener('click', function() {
    switchPanel(this.dataset.panel);
  });
});

document.querySelector('.sb-item[data-panel="dashboard"]').addEventListener('click', function() {
  switchPanel('dashboard');
});

function switchPanel(name) {
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.getElementById(name + 'Panel').classList.add('active');
  document.querySelectorAll('.sb-sub-item').forEach(i => i.classList.remove('active'));
  const item = document.querySelector(`.sb-sub-item[data-panel="${name}"]`);
  if (item) item.classList.add('active');
  currentPanel = name;
  if (name === 'exercise') renderExerciseStep();
}

// === 智能问答 ===
async function sendChat() {
  const input = document.getElementById('chatInput');
  const text = input.value.trim();
  if (!text) return;
  input.value = '';
  addChatMsg('user', text);
  addChatMsg('bot', '⏳ ...');
  try {
    const data = await api('/api/chat-simple', {
      method:'POST', body:JSON.stringify({student_id: studentId, message: text})
    });
    document.querySelector('#chatMsgs .c-msg:last-child').textContent = data.reply;
  } catch(e) {
    document.querySelector('#chatMsgs .c-msg:last-child').textContent = '出错了: ' + e.message;
  }
}

function addChatMsg(role, text) {
  const div = document.createElement('div');
  div.className = 'c-msg ' + role;
  div.textContent = text;
  document.getElementById('chatMsgs').appendChild(div);
  document.getElementById('chatMsgs').scrollTop = document.getElementById('chatMsgs').scrollHeight;
}

// === 做练习题 ===
function renderExerciseStep() {
  const container = document.getElementById('exContainer');
  const s = exerciseState;
  let html = '';

  if (s.step === 'type') {
    html = `<div class="ex-step">
      <h3>选择题型</h3>
      <div class="ex-type-grid">
        <button class="ex-type-btn ${s.type==='choice'?'sel':''}" onclick="pickType('choice')">📋 选择题</button>
        <button class="ex-type-btn ${s.type==='fill_blank'?'sel':''}" onclick="pickType('fill_blank')">✏️ 填空题</button>
        <button class="ex-type-btn ${s.type==='short_answer'?'sel':''}" onclick="pickType('short_answer')">📝 简答题</button>
      </div>
      <button class="ex-next-btn" onclick="nextExStep()">下一步 →</button>
    </div>`;
  } else if (s.step === 'count') {
    html = `<div class="ex-step">
      <h3>出题个数</h3>
      <input type="number" class="ex-count-input" id="exCount" value="${s.count}" min="1" max="20">
      <div class="ex-step-btns">
        <button class="ex-back-btn" onclick="prevExStep()">← 上一步</button>
        <button class="ex-next-btn" onclick="pickCount()">下一步 →</button>
      </div>
    </div>`;
  } else if (s.step === 'course') {
    const courses = getCourseOptions(profileData);
    html = `<div class="ex-step">
      <h3>选择课程</h3>
      <div class="ex-course-grid">
        ${courses.map((c, i) => `<button class="ex-course-btn ${s.course===c?'sel':''}" onclick="pickCourse('${c}')">${['📘','📗','📙'][i]} ${c}</button>`).join('')}
      </div>
      <div class="ex-step-btns">
        <button class="ex-back-btn" onclick="prevExStep()">← 上一步</button>
        <button class="ex-next-btn" onclick="startEx()" ${!s.course?'disabled':''}>开始答题</button>
      </div>
    </div>`;
  } else if (s.step === 'answering') {
    const q = s.questions[s.currentIndex];
    html = renderQuestionHTML(q, s.currentIndex);
  } else if (s.step === 'result') {
    html = renderExResult();
  }
  container.innerHTML = html;
}

// ... 其他辅助函数: pickType, nextExStep, prevExStep, pickCount, pickCourse, startEx, submitAnswer, renderQuestionHTML, renderExResult
```

- [ ] **Step 6: 新增 `/api/chat-simple` 端点**

```python
@app.post("/api/chat-simple")
async def chat_simple(req: ChatSimpleRequest):
    """v3.0 智能问答 —— 纯文本 LLM 对话，不生成资源"""
    profile = db.get_student(req.student_id)
    if not profile:
        raise HTTPException(status_code=404, detail="学生画像未找到")

    system_prompt = f"""你是百问助手，一位专业的AI学习辅导老师。
当前学生信息：
- 姓名：{profile.name}
- 学校：{profile.school}
- 专业：{profile.major}
- 年级：{profile.grade}
- 知识基础：{profile.knowledge_base}
- 学习目标：{', '.join(profile.learning_goals) if profile.learning_goals else '未设定'}

请遵守以下规则：
1. 只进行文本对话，不生成文档、图片、思维导图等资源
2. 可以回答问题、分析代码、解释概念、总结文本、写简单程序
3. 回答应简洁有针对性，结合学生的知识水平
4. 使用中文回复"""

    reply = llm_service.chat(system_prompt, req.message)
    return {"reply": reply}
```

- [ ] **Step 7: 新增 `/api/exercise/generate` 端点**

```python
@app.post("/api/exercise/generate")
async def generate_exercise(req: ExerciseGenerateRequest):
    """v3.0 练习题生成 —— 调用 ExerciseAgent 按指定类型和数量出题"""
    profile = db.get_student(req.student_id)
    if not profile:
        raise HTTPException(status_code=404, detail="学生画像未找到")

    request_text = f"课程：{req.course_name}。请生成{req.count}道{_ex_type_name(req.question_type)}，难度递进。"

    exercise_agent = agents[3]  # ExerciseAgent is 4th in the list
    ex_resource = exercise_agent.generate_exercises(profile, request_text)
    questions = ex_resource.content.get("questions", [])

    return {
        "questions": questions,  # 含答案，前端控制不展示
        "total_score": ex_resource.content.get("total_score", 100),
        "estimated_time_minutes": ex_resource.content.get("estimated_time_minutes", 10),
    }

def _ex_type_name(t: str) -> str:
    return {"choice": "选择题", "fill_blank": "填空题", "short_answer": "简答题"}.get(t, "练习题")
```

- [ ] **Step 8: 注释 `/api/register` 端点**

```python
# [v3.0 已注释] 注册功能已禁用，使用默认账户 stu_001
# @app.post("/api/register")
# async def register(req: RegisterRequest):
#     ...
```

- [ ] **Step 9: 注释 `/api/generate` 端点**

```python
# [v3.0 已注释] 旧版多智能体全资源生成已禁用
# 前端入口已移除，Orchestrator.process_request() 已返回空结果
# 如需恢复，取消注释以下代码并恢复 orchestrator.py
# @app.post("/api/generate")
# async def generate_resources(req: GenerateRequest):
#     ...
```

- [ ] **Step 10: 保留的端点（不做改动）**

```
POST /api/login
POST /api/chat
PUT  /api/profile/update
DELETE /api/account/{student_id}
GET  /api/profile/{student_id}
GET  /api/resources/{student_id}
GET  /api/paths/{student_id}
PUT  /api/config/llm
```

- [ ] **Step 11: Commit**

```bash
git add api/routes.py
git commit -m "feat: v3.0 frontend rewrite - sidebar nav, dashboard, chat-simple, interactive exercises"
```

---

### Task 5: 验证和收尾

- [ ] **Step 1: 启动服务测试**

```bash
taskkill /f /im python.exe 2>/dev/null
cd D:\my-claude-project\HundredQwen-xpy_5-7
python main.py
```

- [ ] **Step 2: 验证自动登录**

```bash
curl -s http://localhost:8000/ | grep "stu_001"
# Expected: match
```

- [ ] **Step 3: 验证注册返回 404**

```bash
curl -s -X POST http://localhost:8000/api/register -H "Content-Type: application/json" -d '{}'
# Expected: {"detail":"Not Found"}
```

- [ ] **Step 4: 验证智能问答端点**

```bash
curl -s -X POST http://localhost:8000/api/chat-simple \
  -H "Content-Type: application/json" \
  -d '{"student_id":"stu_001","message":"什么是Python？"}'
# Expected: {"reply": "..."}
```

- [ ] **Step 5: 验证练习题端点**

```bash
curl -s -X POST http://localhost:8000/api/exercise/generate \
  -H "Content-Type: application/json" \
  -d '{"student_id":"stu_001","question_type":"choice","count":3,"course_name":"Python编程"}'
# Expected: {"questions": [...], ...}
```

- [ ] **Step 6: 浏览器测试**

打开 http://localhost:8000 验证：
1. 仪表盘默认显示
2. 侧边栏百问助手展开/收起
3. 智能问答对话功能
4. 做练习题逐题流程
5. 个人信息弹窗编辑+头像选择
6. 课程文档/学习路径显示"待开发"

- [ ] **Step 7: Commit**

```bash
git add .
git commit -m "test: verify v3.0 all endpoints and UI flows"
```
