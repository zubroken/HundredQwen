from __future__ import annotations

HOME_PAGE_HTML = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>百问即查 v1.0.4 - AI 智能学习助手</title>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/highlight.js@11/lib/core.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/highlight.js@11/lib/languages/python.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/highlight.js@11/lib/languages/javascript.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/highlight.js@11/lib/languages/bash.min.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/highlight.js@11/styles/github-dark.min.css">
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1"></script>
<style>

:root {
  --c-primary: #2563eb;
  --c-primary-dark: #1d4ed8;
  --c-primary-light: #93c5fd;
  --c-accent: #0891b2;
  --c-bg: #eff6ff;
  --c-surface: #ffffff;
  --c-text: #0f172a;
  --c-text-secondary: #64748b;
  --c-border: #e2e8f0;
  --c-border-light: #f1f5f9;
  --c-sidebar-bg: #1e3a5f;
  --c-sidebar-end: #1e3a5f;
  --c-success: #059669;
  --c-danger: #dc2626;
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 24px;
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.04);
  --shadow-md: 0 4px 16px rgba(0,0,0,0.06);
  --shadow-lg: 0 8px 32px rgba(0,0,0,0.08);
  --shadow-xl: 0 12px 48px rgba(0,0,0,0.10);
  --transition-fast: 0.15s ease;
  --transition: 0.25s ease;
  --transition-slow: 0.35s ease;
}
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:-apple-system,'Microsoft YaHei','PingFang SC',sans-serif; background:var(--c-bg); color:var(--c-text); min-height:100vh; display:flex; }
::-webkit-scrollbar { width:5px; } ::-webkit-scrollbar-thumb { background:#c0c8dc; border-radius:3px; }

/* ===== 侧边栏 ===== */
.sidebar { width:260px; min-width:260px; background:var(--c-sidebar-bg); color:#fff; display:flex; flex-direction:column; height:100vh; position:fixed; left:0; top:0; z-index:100; }
.sb-logo { font-size:22px; font-weight:800; background:linear-gradient(135deg,var(--c-primary-light),#60a5fa); -webkit-background-clip:text; -webkit-text-fill-color:transparent; padding:24px 24px 4px; letter-spacing:-0.3px; }
.sb-sub { font-size:11px; color:#7b9bc0; padding:0 24px 20px; letter-spacing:0.5px; }
.sb-menu { flex:1; overflow-y:auto; padding:0 14px; }
.sb-item { display:flex; align-items:center; gap:10px; padding:11px 14px; border-radius:var(--radius-md); cursor:pointer; font-size:14px; color:#93bfec; transition:all var(--transition); margin-bottom:2px; position:relative; }
.sb-item:hover { background:rgba(255,255,255,0.08); color:#bfdbfe; }
.sb-item .nav-icon { width:20px; height:20px; flex-shrink:0; }
.sb-section { margin:12px 0; }
.sb-section-title { display:flex; align-items:center; gap:8px; padding:10px 14px; border-radius:var(--radius-md); cursor:pointer; font-size:14px; color:#93bfec; font-weight:600; transition:all var(--transition); user-select:none; }
.sb-section-title:hover { background:rgba(255,255,255,0.08); color:#bfdbfe; }
.sb-section-title .nav-icon { width:16px; height:16px; flex-shrink:0; }
.sb-section-title.collapsed .arrow { transform:rotate(-90deg); }
.arrow { display:inline-block; transition:transform var(--transition); font-size:10px; }
.sb-sub-items { padding-left:4px; overflow:hidden; }
.sb-sub-items.collapsed { display:none; }
.sb-sub-item { display:flex; align-items:center; gap:8px; padding:10px 14px; border-radius:var(--radius-sm); cursor:pointer; font-size:13px; color:#7b9bc0; transition:all var(--transition); margin-bottom:1px; position:relative; }
.sb-sub-item:hover { background:rgba(255,255,255,0.06); color:#93bfec; }
.sb-sub-item .nav-icon { width:16px; height:16px; flex-shrink:0; }
.sb-sub-item.active { background:rgba(37,99,235,0.25); color:#bfdbfe; font-weight:600; box-shadow:inset 3px 0 0 var(--c-primary); }
.sb-sub-item.disabled { color:#5c7a99; cursor:not-allowed; opacity:0.5; }
.sb-sub-item.disabled:hover { background:transparent; color:#5c7a99; }
.sb-sub-item small { font-size:10px; background:rgba(255,255,255,0.1); padding:2px 6px; border-radius:10px; }
.sb-bottom { padding:14px; border-top:1px solid rgba(255,255,255,0.08); }
.sb-bottom .sb-item { color:#7b9bc0; }

/* ===== 侧边栏用户卡片 ===== */
.sb-user-card { display:flex; align-items:center; gap:12px; padding:12px 16px; margin:0 10px 12px; border-radius:var(--radius-md); cursor:pointer; transition:all var(--transition); }
.sb-user-card:hover { background:rgba(255,255,255,0.08); }
.sb-user-card-avatar { width:40px; height:40px; border-radius:50%; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
.sb-user-card-info { flex:1; min-width:0; }
.sb-user-card-name { font-size:14px; font-weight:600; color:#bfdbfe; }
.sb-user-card-major { font-size:11px; color:#7b9bc0; margin-top:1px; }

/* ===== 主内容区 ===== */
.main { margin-left:260px; flex:1; min-height:100vh; display:flex; flex-direction:column; position:relative; }

/* ===== 面板容器 ===== */
.panel { display:none; flex:1; padding:80px 40px 40px; overflow-y:auto; animation:fadeIn var(--transition-slow); }
.panel.active { display:flex; flex-direction:column; }
.panel h2 { font-size:24px; font-weight:700; color:var(--c-text); margin-bottom:24px; letter-spacing:-0.3px; }
@keyframes fadeIn { from{opacity:0;transform:translateY(8px);} to{opacity:1;transform:translateY(0);} }

/* ===== 仪表盘 ===== */
.dash-grid { display:grid; grid-template-columns:repeat(auto-fill, minmax(280px, 1fr)); gap:20px; }
.dash-card { background:var(--c-surface); border-radius:var(--radius-lg); padding:28px; display:flex; gap:18px; align-items:center; box-shadow:var(--shadow-sm); border:1px solid var(--c-border-light); transition:all var(--transition); cursor:default; }
.dash-card:hover { box-shadow:var(--shadow-lg); transform:translateY(-3px); border-color:transparent; }
.dash-icon { width:56px; height:56px; border-radius:14px; display:flex; align-items:center; justify-content:center; font-size:26px; flex-shrink:0; box-shadow:0 4px 12px rgba(0,0,0,0.06); }
.dash-info { flex:1; }
.dash-value { font-size:24px; font-weight:700; color:var(--c-text); letter-spacing:-0.3px; }
.dash-label { font-size:13px; color:var(--c-text-secondary); margin-top:2px; font-weight:500; }
.dash-bar { height:6px; background:var(--c-border-light); border-radius:3px; margin-top:12px; overflow:hidden; }
.dash-bar-fill { height:100%; background:linear-gradient(90deg,var(--c-primary),var(--c-accent)); border-radius:3px; transition:width 0.8s ease; }

/* ===== 智能问答面板 ===== */
.chat-panel-body { display:flex; flex-direction:column; width:100%; max-width:760px; margin:auto; max-height:100%; }
.chat-msgs { flex:1; overflow-y:auto; padding:8px 0; display:flex; flex-direction:column; gap:10px; }
.c-msg { max-width:85%; padding:14px 18px; border-radius:14px; font-size:14px; line-height:1.7; animation:msgIn var(--transition); }
@keyframes msgIn { from{opacity:0;transform:translateY(8px) scale(0.98);} to{opacity:1;transform:translateY(0) scale(1);} }
.c-msg.user { align-self:flex-end; background:linear-gradient(135deg,var(--c-primary),var(--c-primary-dark)); color:#fff; border-bottom-right-radius:4px; box-shadow:0 4px 12px rgba(37,99,235,0.25); }
.c-msg.bot { align-self:flex-start; background:var(--c-surface); color:#333; border:1px solid var(--c-border-light); border-bottom-left-radius:4px; box-shadow:var(--shadow-sm); }
.c-msg.bot pre { background:#1e293b; color:#e2e8f0; padding:14px 16px; border-radius:8px; overflow-x:auto; margin:10px 0; font-size:13px; line-height:1.6; }
.c-msg.bot pre code { background:none; padding:0; font-family:'Consolas','Courier New',monospace; }
.c-msg.bot code { background:rgba(37,99,235,0.08); color:#2563eb; padding:2px 6px; border-radius:4px; font-size:13px; }
.c-msg.bot pre code { color:#e2e8f0; }
.c-msg.bot h3 { font-size:16px; margin:12px 0 6px; }
.c-msg.bot h4 { font-size:14px; margin:10px 0 4px; }
.c-msg.bot ul, .c-msg.bot ol { padding-left:20px; margin:8px 0; }
.c-msg.bot li { margin:4px 0; }
.c-msg.bot table { border-collapse:collapse; margin:10px 0; width:100%; }
.c-msg.bot th, .c-msg.bot td { border:1px solid var(--c-border); padding:8px 12px; text-align:left; font-size:13px; }
.c-msg.bot th { background:var(--c-bg); font-weight:600; }
.c-msg.bot blockquote { border-left:3px solid var(--c-primary); margin:10px 0; padding:8px 16px; background:rgba(37,99,235,0.04); border-radius:0 8px 8px 0; }
#panel-chat { padding:40px; }
.chat-input-area { display:flex; flex-direction:column; padding:16px 0; border-radius:var(--radius-lg); }
.chat-input-area textarea { width:100%; border:2px solid var(--c-border); border-radius:var(--radius-md); padding:12px 14px; font-size:15px; font-family:inherit; outline:none; transition:all var(--transition); background:var(--c-surface); resize:none; line-height:1.5; min-height:48px; max-height:160px; box-sizing:border-box; }
.chat-input-area textarea:focus { border-color:var(--c-primary); box-shadow:0 0 0 3px rgba(37,99,235,0.08); }
.chat-input-bar { display:flex; justify-content:space-between; align-items:center; padding:8px 4px 0; }
.chat-input-hint { font-size:12px; color:var(--c-text-secondary); }
.chat-input-area button { padding:9px 24px; background:linear-gradient(135deg,var(--c-primary),var(--c-primary-dark)); border:none; border-radius:var(--radius-md); color:#fff; font-weight:600; font-size:14px; cursor:pointer; transition:all var(--transition); box-shadow:0 4px 12px rgba(37,99,235,0.2); white-space:nowrap; }
.chat-input-area button:hover { transform:translateY(-1px); box-shadow:0 6px 20px rgba(37,99,235,0.35); }
.chat-input-area button:disabled { opacity:0.5; cursor:not-allowed; transform:none; box-shadow:none; }

/* 麦克风按钮 */
.mic-btn { width:36px; height:36px; border-radius:50%; border:none; background:#94a3b8; cursor:pointer; display:flex; align-items:center; justify-content:center; transition:all var(--transition); flex-shrink:0; box-shadow:none; padding:0 !important; }
.mic-btn:hover { background:#64748b; transform:scale(1.05) !important; box-shadow:none !important; }
.mic-btn.recording { background:#ef4444; animation:micPulse 1.2s infinite; }
.mic-btn.processing { background:#2563eb; }
@keyframes micPulse { 0%,100% { box-shadow:0 0 0 0 rgba(239,68,68,0.5); } 50% { box-shadow:0 0 0 8px rgba(239,68,68,0); } }

/* ===== 技能树 ===== */
.st-chapter-card { background:var(--c-surface); border-radius:16px; padding:22px 28px; cursor:pointer; transition:all var(--transition); position:relative; }
.st-chapter-card:hover { transform:translateY(-2px); box-shadow:0 8px 24px rgba(0,0,0,0.08); }
.st-chapter-card.done { border:2px solid #16a34a; }
.st-chapter-card.active { border:2px solid #2563eb; }
.st-chapter-card.unlocked { border:2px solid var(--c-border); }
.st-chapter-card.locked { opacity:0.5; border:2px dashed var(--c-border); background:#f8fafc; cursor:not-allowed; }
.st-chapter-card.locked:hover { transform:none; box-shadow:none; }
.st-chapter-header { display:flex; justify-content:space-between; align-items:flex-start; }
.st-chapter-name { font-size:22px; font-weight:800; color:var(--c-text); letter-spacing:-0.5px; }
.st-chapter-en { font-size:15px; font-weight:400; color:var(--c-text-secondary); margin-left:6px; }
.st-chapter-status { font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:1px; }
.st-chapter-nodes { font-size:13px; color:var(--c-text-secondary); margin-top:8px; }
.st-chapter-progress { width:100%; height:6px; background:#e5e7eb; border-radius:3px; margin-top:14px; }
.st-progress-fill { height:100%; border-radius:3px; transition:width 0.5s ease; }

.st-detail-back { font-size:13px; color:var(--c-primary); cursor:pointer; margin-bottom:24px; display:inline-block; }
.st-node-card { width:490px; background:var(--c-surface); border-radius:14px; padding:16px 22px; cursor:pointer; transition:all var(--transition); }
.st-node-card:hover { transform:translateY(-2px); box-shadow:0 6px 20px rgba(0,0,0,0.08); }
.st-node-card.done { border:2px solid #16a34a; }
.st-node-card.in-progress { border:2px solid #f59e0b; }
.st-node-card.locked { opacity:0.45; border:2px dashed var(--c-border); background:#f8fafc; cursor:not-allowed; }
.st-node-card.locked:hover { transform:none; box-shadow:none; }
.st-node-left { margin-left:0; margin-right:auto; }
.st-node-right { margin-left:auto; margin-right:0; }
.st-node-icon { width:44px;height:44px;border-radius:10px;display:flex;align-items:center;justify-content:center;flex-shrink:0; }
.st-node-info { flex:1; }
.st-node-title { font-weight:700;font-size:15px;color:var(--c-text); }
.st-node-levels { font-size:12px;color:var(--c-text-secondary);margin-top:3px; }
.st-node-score { text-align:right;flex-shrink:0; }

.st-level-tabs { display:flex;gap:8px;margin-top:14px;padding-top:14px;border-top:1px solid var(--c-border-light); }
.st-level-tab { flex:1;text-align:center;padding:10px 6px;border-radius:8px;font-size:12px;font-weight:600;cursor:pointer;transition:all var(--transition);border:1px solid transparent; }
.st-level-tab.done { background:#f0fdf4;color:#16a34a; }
.st-level-tab.active { background:#eff6ff;color:#2563eb;border-color:#2563eb; }
.st-level-tab.locked { background:#f8fafc;color:#94a3b8;cursor:not-allowed; }

.st-lines-layer { position:absolute;left:0;top:0;width:100%;height:100%;pointer-events:none;z-index:0; }

/* ===== 做练习题面板 ===== */
.ex-step { max-width:600px; }
.ex-step h3 { font-size:18px; font-weight:600; color:var(--c-text); margin-bottom:20px; }
.ex-type-grid, .ex-course-grid { display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px; margin-bottom:24px; }
.ex-type-btn, .ex-course-btn { padding:18px 16px; border:2px solid var(--c-border); border-radius:var(--radius-md); background:var(--c-surface); font-size:15px; cursor:pointer; transition:all var(--transition); text-align:center; box-shadow:var(--shadow-sm); }
.ex-type-btn:hover, .ex-course-btn:hover { border-color:#93c5fd; background:#f8f9ff; transform:translateY(-1px); box-shadow:var(--shadow-md); }
.ex-type-btn.sel, .ex-course-btn.sel { border-color:var(--c-primary); background:rgba(37,99,235,0.05); color:var(--c-primary); font-weight:600; box-shadow:0 0 0 3px rgba(37,99,235,0.08); }
.ex-count-input { padding:14px 18px; border:2px solid var(--c-border); border-radius:var(--radius-md); font-size:18px; width:120px; text-align:center; outline:none; transition:all var(--transition); }
.ex-count-input:focus { border-color:var(--c-primary); box-shadow:0 0 0 3px rgba(37,99,235,0.08); }
.ex-step-btns { display:flex; gap:10px; margin-top:20px; }
.ex-next-btn, .ex-back-btn, .ex-start-btn { padding:11px 28px; border-radius:var(--radius-md); font-size:14px; font-weight:600; cursor:pointer; transition:all var(--transition); }
.ex-next-btn, .ex-start-btn { background:linear-gradient(135deg,var(--c-primary),var(--c-primary-dark)); border:none; color:#fff; box-shadow:0 4px 12px rgba(37,99,235,0.2); }
.ex-next-btn:hover, .ex-start-btn:hover { transform:translateY(-1px); box-shadow:0 6px 20px rgba(37,99,235,0.35); }
.ex-next-btn:disabled, .ex-start-btn:disabled { opacity:0.5; cursor:not-allowed; transform:none; box-shadow:none; }
.ex-back-btn { background:var(--c-surface); border:2px solid var(--c-border); color:var(--c-text-secondary); }
.ex-back-btn:hover { border-color:#ccc; background:#fafafa; }

/* 逐题作答 */
.ex-question { background:var(--c-surface); border:1px solid var(--c-border-light); border-radius:var(--radius-lg); padding:28px; box-shadow:var(--shadow-md); max-width:680px; }
.ex-q-progress { font-size:13px; color:var(--c-primary); font-weight:600; margin-bottom:18px; }
.ex-q-stem { font-size:16px; line-height:1.7; margin-bottom:20px;color:var(--c-text); }
.ex-q-options { display:flex; flex-direction:column; gap:10px; margin-bottom:20px; }
.ex-q-opt { padding:14px 18px; border:2px solid var(--c-border); border-radius:var(--radius-md); cursor:pointer; transition:all var(--transition); font-size:14px; }
.ex-q-opt:hover { border-color:#93c5fd; background:#f8f9ff; }
.ex-q-opt.sel { border-color:var(--c-primary); background:rgba(37,99,235,0.05); box-shadow:0 0 0 3px rgba(37,99,235,0.06); }
.ex-q-input { width:100%; padding:14px; border:2px solid var(--c-border); border-radius:var(--radius-md); font-size:15px; font-family:inherit; min-height:100px; resize:vertical; outline:none; margin-bottom:20px; transition:all var(--transition); }
.ex-q-input:focus { border-color:var(--c-primary); box-shadow:0 0 0 3px rgba(37,99,235,0.08); }
.ex-submit-btn { padding:11px 32px; background:linear-gradient(135deg,var(--c-primary),var(--c-primary-dark)); border:none; border-radius:var(--radius-md); color:#fff; font-weight:600; font-size:14px; cursor:pointer; transition:all var(--transition); box-shadow:0 4px 12px rgba(37,99,235,0.2); }
.ex-submit-btn:hover { transform:translateY(-1px); box-shadow:0 6px 20px rgba(37,99,235,0.35); }

/* 结果页 */
.ex-result { max-width:680px; }
.ex-score { font-size:36px; font-weight:800; color:var(--c-primary); text-align:center; margin:16px 0; }
.ex-score span { font-size:16px; color:var(--c-text-secondary); font-weight:400; }
.ex-review-item { background:var(--c-surface); border:1px solid var(--c-border-light); border-radius:var(--radius-md); padding:16px; margin-bottom:10px; box-shadow:var(--shadow-sm); }
.ex-review-item .r-correct { color:var(--c-success); font-weight:600; }
.ex-review-item .r-wrong { color:var(--c-danger); font-weight:600; }
.ex-review-item .r-exp { background:#f0f2ff; padding:12px; border-radius:var(--radius-sm); margin-top:8px; font-size:13px; color:#555; }

/* ===== 个人信息页面 ===== */
.pf-head { display:flex; align-items:center; justify-content:space-between; margin-bottom:20px; }
.pf-head h3 { font-size:18px; color:var(--c-text); }
.pf-back { padding:6px 14px; border:1px solid var(--c-border); border-radius:var(--radius-sm); background:var(--c-surface); cursor:pointer; font-size:13px; color:var(--c-text-secondary); transition:all var(--transition); }
.pf-back:hover { border-color:var(--c-primary); color:var(--c-primary); }
.pf-body { max-width:640px; }
.pf-foot { padding:16px 0 24px; display:flex; gap:10px; justify-content:space-between; border-top:1px solid #f5f5f8; margin-top:20px; }

/* 头像选择器 */
.pf-avatar-section { text-align:center; margin-bottom:20px; }
.pf-avatar-preview { width:72px; height:72px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; font-size:32px; cursor:pointer; transition:all var(--transition); border:3px solid var(--c-border); }
.pf-avatar-preview:hover { border-color:var(--c-primary); transform:scale(1.05); box-shadow:0 0 0 4px rgba(37,99,235,0.1); }
.avatar-picker-grid { display:grid; grid-template-columns:repeat(4, 1fr); gap:10px; max-width:320px; margin:16px auto 0; }
.avatar-pick { width:64px; height:64px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:26px; cursor:pointer; transition:all var(--transition); border:3px solid transparent; }
.avatar-pick:hover { transform:scale(1.1); }
.avatar-pick.sel { border-color:var(--c-primary); box-shadow:0 0 0 4px rgba(37,99,235,0.18); }

/* 通用表单字段 */
.pf-field { margin-bottom:14px; }
.pf-field label { display:block; font-size:12px; font-weight:600; color:var(--c-text-secondary); margin-bottom:4px; text-transform:uppercase; letter-spacing:0.5px; }
.pf-field input, .pf-field textarea, .pf-field select { width:100%; padding:10px 14px; border:1.5px solid var(--c-border); border-radius:var(--radius-sm); font-size:14px; font-family:inherit; outline:none; transition:all var(--transition); background:var(--c-surface); }
.pf-field input:focus, .pf-field textarea:focus, .pf-field select:focus { border-color:var(--c-primary); box-shadow:0 0 0 3px rgba(37,99,235,0.08); }
.pf-field textarea { resize:vertical; min-height:60px; }
.pf-checkbox-group { display:flex; flex-wrap:wrap; gap:8px; }
.pf-checkbox-group label { display:flex; align-items:center; gap:6px; padding:6px 12px; border:1px solid var(--c-border); border-radius:var(--radius-sm); cursor:pointer; font-size:13px; font-weight:400; color:var(--c-text); transition:all var(--transition); }
.pf-checkbox-group label:hover { border-color:var(--c-primary); background:rgba(37,99,235,0.04); }
.pf-checkbox-group label.checked { border-color:var(--c-primary); background:rgba(37,99,235,0.08); color:var(--c-primary); font-weight:600; }
.pf-checkbox-group input { display:none; }
.pf-field input:disabled { background:#f5f6fa; color:#999; cursor:not-allowed; }

.save-btn { padding:10px 32px; background:linear-gradient(135deg,var(--c-primary),var(--c-primary-dark)); border:none; border-radius:var(--radius-md); color:#fff; font-size:14px; font-weight:600; cursor:pointer; transition:all var(--transition); box-shadow:0 4px 12px rgba(37,99,235,0.2); }
.save-btn:hover { transform:translateY(-1px); box-shadow:0 6px 20px rgba(37,99,235,0.35); }
.delete-btn { padding:10px 20px; background:transparent; border:1px solid #fca5a5; border-radius:var(--radius-md); color:var(--c-danger); font-size:13px; cursor:pointer; transition:all var(--transition); }
.delete-btn:hover { background:#fef2f2; border-color:var(--c-danger); }
.save-msg { text-align:center; font-size:12px; margin-top:8px; }

/* ===== PPT生成面板 ===== */
.ppt-body { max-width:700px; }
.ppt-theme-grid { display:grid; grid-template-columns:repeat(auto-fill, minmax(160px, 1fr)); gap:12px; margin-bottom:24px; }
.ppt-theme-card { padding:10px; border:2px solid var(--c-border); border-radius:var(--radius-lg); cursor:pointer; text-align:center; transition:all var(--transition); background:var(--c-surface); box-shadow:var(--shadow-sm); }
.ppt-theme-card:hover { border-color:#93c5fd; transform:translateY(-2px); box-shadow:var(--shadow-md); }
.ppt-theme-card.sel { border-color:var(--c-primary); box-shadow:0 0 0 4px rgba(37,99,235,0.15); }
.tc-thumb { width:100%; aspect-ratio:4/3; object-fit:cover; border-radius:8px; background:#e2e8f0; display:block; }
.ppt-theme-card .tc-name { font-size:12px; font-weight:600; color:#444; margin-top:8px; display:block; }
.ppt-count-row { display:flex; gap:10px; margin-bottom:24px; }
.ppt-count-btn { padding:12px 24px; border:2px solid var(--c-border); border-radius:var(--radius-md); font-size:15px; font-weight:600; background:var(--c-surface); cursor:pointer; transition:all var(--transition); box-shadow:var(--shadow-sm); }
.ppt-count-btn:hover { border-color:#93c5fd; background:#f8f9ff; transform:translateY(-1px); }
.ppt-count-btn.sel { border-color:var(--c-primary); background:var(--c-primary); color:#fff; box-shadow:0 4px 12px rgba(37,99,235,0.3); }
.ppt-gen-btn { padding:16px 48px; background:linear-gradient(135deg,var(--c-primary),var(--c-primary-dark)); border:none; border-radius:var(--radius-md); color:#fff; font-size:16px; font-weight:600; cursor:pointer; transition:all var(--transition); display:block; width:100%; box-shadow:0 4px 16px rgba(37,99,235,0.25); }
.ppt-gen-btn:hover { transform:translateY(-2px); box-shadow:0 8px 24px rgba(37,99,235,0.4); }
.ppt-gen-btn:disabled { opacity:0.5; cursor:not-allowed; transform:none; box-shadow:none; }
.ppt-progress-wrap { margin-top:24px; padding:24px; background:var(--c-surface); border-radius:var(--radius-lg); border:1px solid var(--c-border-light); box-shadow:var(--shadow-md); }
.ppt-progress-bar { height:8px; background:var(--c-border-light); border-radius:4px; overflow:hidden; margin-bottom:10px; }
.ppt-progress-fill { height:100%; background:linear-gradient(90deg,var(--c-primary),var(--c-accent)); border-radius:4px; transition:width 0.5s ease; }
.ppt-progress-text { font-size:13px; color:var(--c-text-secondary); text-align:center; }
.ppt-result { margin-top:24px; text-align:center; }
.ppt-download-btn { display:inline-block; padding:14px 36px; background:linear-gradient(135deg,var(--c-success),#15803d); border:none; border-radius:var(--radius-md); color:#fff; font-size:15px; font-weight:600; text-decoration:none; cursor:pointer; transition:all var(--transition); box-shadow:0 4px 12px rgba(22,163,74,0.25); }
.ppt-download-btn:hover { transform:translateY(-2px); box-shadow:0 8px 24px rgba(22,163,74,0.4); }
/* 课程文档 */
.doc-gen-btn { padding:16px 48px; background:linear-gradient(135deg,var(--c-primary),var(--c-primary-dark)); border:none; border-radius:var(--radius-md); color:#fff; font-size:16px; font-weight:600; cursor:pointer; transition:all var(--transition); display:block; width:100%; box-shadow:0 4px 16px rgba(37,99,235,0.25); }
.doc-gen-btn:hover { transform:translateY(-2px); box-shadow:0 8px 24px rgba(37,99,235,0.4); }
.doc-gen-btn:disabled { opacity:0.5; cursor:not-allowed; transform:none; box-shadow:none; }
.doc-progress-pulse { animation:docPulse 1.8s ease-in-out infinite; }
@keyframes docPulse { 0%,100% { opacity:1; } 50% { opacity:0.4; } }
.doc-result { margin-top:24px; }
.doc-result-toolbar { display:flex; justify-content:space-between; align-items:center; padding:12px 16px; background:var(--c-surface); border-radius:var(--radius-md) var(--radius-md) 0 0; border:1px solid var(--c-border-light); border-bottom:none; }
.doc-action-btn { padding:6px 14px; border:1px solid var(--c-border); border-radius:var(--radius-sm); font-size:13px; font-weight:600; background:var(--c-bg); color:var(--c-text); cursor:pointer; transition:all var(--transition); display:inline-flex; align-items:center; gap:4px; }
.doc-action-btn:hover { border-color:var(--c-primary); background:var(--c-primary); color:#fff; }
.doc-content { padding:20px 24px; background:var(--c-surface); border:1px solid var(--c-border-light); border-radius:0 0 var(--radius-md) var(--radius-md); max-height:70vh; overflow-y:auto; }
.doc-content h1 { font-size:1.5em; border-bottom:2px solid var(--c-primary); padding-bottom:8px; margin-bottom:16px; }
.doc-content h2 { font-size:1.2em; margin-top:24px; color:var(--c-primary); }
.doc-content h3 { font-size:1.05em; margin-top:16px; }
.doc-content blockquote { border-left:4px solid var(--c-primary); background:#f0f4ff; padding:8px 16px; margin:12px 0; color:#555; }
.doc-content pre { background:var(--c-bg); border-radius:var(--radius-sm); padding:12px 16px; overflow-x:auto; }
.doc-content code { font-family:'Cascadia Code','Fira Code',monospace; font-size:0.9em; }
.ppt-hint { font-size:12px; color:#999; margin-top:8px; }

/* ===== 知识库面板 ===== */
.kb-filter-btn { padding:6px 14px; border:1.5px solid var(--c-border); border-radius:20px; font-size:12px; font-weight:600; background:var(--c-surface); color:var(--c-text-secondary); cursor:pointer; transition:all var(--transition); }
.kb-filter-btn:hover { border-color:var(--c-primary); color:var(--c-primary); }
.kb-filter-btn.sel { background:var(--c-primary); border-color:var(--c-primary); color:#fff; }
.kb-result-card { background:var(--c-surface); border:1px solid var(--c-border-light); border-radius:var(--radius-md); padding:16px; margin-bottom:10px; box-shadow:var(--shadow-sm); transition:all var(--transition); }
.kb-result-card:hover { box-shadow:var(--shadow-md); }
.kb-result-title { font-size:15px; font-weight:700; color:var(--c-text); margin-bottom:4px; }
.kb-result-breadcrumb { font-size:12px; color:var(--c-primary); margin-bottom:6px; font-weight:500; }
.kb-result-meta { font-size:11px; color:var(--c-text-secondary); margin-bottom:8px; display:flex;gap:8px;flex-wrap:wrap;align-items:center; }
.kb-result-badge { display:inline-block; padding:2px 8px; border-radius:10px; font-size:10px; font-weight:600; background:var(--c-border-light); color:var(--c-text-secondary); }
.kb-result-text { font-size:13px; color:#555; line-height:1.6; margin-bottom:10px; max-height:80px; overflow:hidden; }
.kb-result-text.expanded { max-height:none; }
.kb-result-actions { display:flex; gap:8px; }
.kb-action-btn { padding:5px 12px; border:1px solid var(--c-border); border-radius:var(--radius-sm); font-size:12px; cursor:pointer; background:var(--c-surface); color:var(--c-text-secondary); transition:all var(--transition); }
.kb-action-btn:hover { border-color:var(--c-primary); color:var(--c-primary); }
.kb-action-btn.primary { background:var(--c-primary); color:#fff; border-color:var(--c-primary); }
.kb-doc-item { display:flex; align-items:center; justify-content:space-between; padding:8px 12px; background:var(--c-bg); border-radius:var(--radius-sm); margin-bottom:6px; font-size:13px; }

/* ===== 登录/注册面板 ===== */
.login-overlay { position:fixed; inset:0; background:linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #0f172a 100%); display:flex; align-items:center; justify-content:center; z-index:9999; }
.login-card { background:var(--c-surface); border-radius:var(--radius-xl); padding:40px 36px; width:400px; max-width:90vw; box-shadow:0 20px 60px rgba(0,0,0,0.3); }
.login-card h2 { font-size:22px; font-weight:700; color:var(--c-text); margin-bottom:28px; text-align:center; letter-spacing:-0.3px; }
.login-card .form-group { margin-bottom:18px; }
.login-card label { display:block; font-size:13px; font-weight:600; color:var(--c-text-secondary); margin-bottom:6px; }
.login-card input, .login-card select { width:100%; padding:12px 14px; border:2px solid var(--c-border); border-radius:var(--radius-md); font-size:15px; font-family:inherit; outline:none; transition:all var(--transition); background:var(--c-surface); }
.login-card input:focus, .login-card select:focus { border-color:var(--c-primary); box-shadow:0 0 0 3px rgba(37,99,235,0.08); }
.login-card .login-btn { width:100%; padding:13px; background:linear-gradient(135deg,var(--c-primary),var(--c-primary-dark)); border:none; border-radius:var(--radius-md); color:#fff; font-weight:600; font-size:16px; cursor:pointer; transition:all var(--transition); box-shadow:0 4px 12px rgba(37,99,235,0.2); margin-top:8px; }
.login-card .login-btn:hover { transform:translateY(-1px); box-shadow:0 6px 20px rgba(37,99,235,0.35); }
.login-card .switch-link { text-align:center; margin-top:16px; font-size:13px; color:var(--c-text-secondary); }
.login-card .switch-link a { color:var(--c-primary); cursor:pointer; font-weight:600; text-decoration:none; }
.login-card .switch-link a:hover { text-decoration:underline; }

/* ===== Toast 通知 ===== */
.toast { position:fixed; top:24px; right:24px; padding:14px 24px; border-radius:var(--radius-md); color:#fff; font-size:14px; font-weight:600; z-index:99999; animation:fadeIn 0.3s ease; box-shadow:var(--shadow-lg); }
.toast.success { background:var(--c-success); }
.toast.error { background:var(--c-danger); }

</style>
</head>


<div id="loginOverlay" class="login-overlay" style="display:none">
  <div class="login-card" id="loginCard">
    <h2>百问即查</h2>
    <div class="form-group"><label>学号</label><input id="loginSid" placeholder="输入学号" onkeydown="if(event.key==='Enter')doLogin()"></div>
    <div class="form-group"><label>密码</label><input id="loginPwd" type="password" placeholder="输入密码" onkeydown="if(event.key==='Enter')doLogin()"></div>
    <button class="login-btn" onclick="doLogin()">登 录</button>
    <div id="loginMsg" style="text-align:center;margin-top:8px;font-size:13px;color:#ef4444;"></div>
    <p class="switch-link">没有账号？<a onclick="showRegister()">去注册</a></p>
  </div>
  <div class="login-card" id="registerCard" style="display:none">
    <h2>注册新账号</h2>
    <div class="form-group"><label>昵称</label><input id="regNickname" placeholder="输入你的昵称" onkeydown="if(event.key==='Enter')doRegister()"></div>
    <div class="form-group"><label>专业</label><select id="regMajor"><option value="人工智能" selected>人工智能</option></select></div>
    <button class="login-btn" onclick="doRegister()">注 册</button>
    <p class="switch-link">已有账号？<a onclick="showLogin()">去登录</a></p>
  </div>
</div>

<div id="appMain" style="display:''">

<svg xmlns="http://www.w3.org/2000/svg" style="display:none">
  <defs>
    <symbol id="icon-dashboard" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>
    </symbol>
    <symbol id="icon-chat" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
    </symbol>
    <symbol id="icon-exercise" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M17 3a2.85 2.85 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/><path d="m15 5 4 4"/>
    </symbol>
    <symbol id="icon-ppt" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/>
    </symbol>
    <symbol id="icon-course" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/>
    </symbol>
    <symbol id="icon-path" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="5" cy="19" r="2"/><circle cx="19" cy="5" r="2"/><path d="M5 17c2.5-3 7-5 12-10"/>
    </symbol>
    <symbol id="icon-logout" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/>
    </symbol>
    <symbol id="icon-user" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>
    </symbol>
    <symbol id="icon-book" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/>
    </symbol>
    <symbol id="icon-clock" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
    </symbol>
    <symbol id="icon-pin" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M12 2v7l-4 7h8l-4-7V2"/><circle cx="12" cy="22" r="2"/>
    </symbol>
    <symbol id="icon-rocket" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="M12 15l-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4l.5-1.5"/><path d="M12 9v4"/>
    </symbol>
    <symbol id="icon-save" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/>
    </symbol>
    <symbol id="icon-loading" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M21 12a9 9 0 1 1-6.219-8.56"/><animateTransform attributeName="transform" type="rotate" from="0 12 12" to="360 12 12" dur="1s" repeatCount="indefinite"/>
    </symbol>
    <symbol id="icon-check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <polyline points="20 6 9 17 4 12"/>
    </symbol>
    <symbol id="icon-chevron-down" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <polyline points="6 9 12 15 18 9"/>
    </symbol>
    <symbol id="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
    </symbol>
    <symbol id="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
    </symbol>
    <symbol id="icon-monitor" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/>
    </symbol>
    <symbol id="icon-brain" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/><path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/>
    </symbol>
    <symbol id="icon-sparkle" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/>
    </symbol>
    <symbol id="icon-target" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>
    </symbol>
    <symbol id="icon-fire" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/>
    </symbol>
    <symbol id="icon-zap" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
    </symbol>
  </defs>
</svg>

<!-- ===== 侧边栏 ===== -->
<nav class="sidebar">
  <div class="sb-logo">百问即查</div>
  <div class="sb-sub">v1.0.4</div>
  <div class="sb-user-card" id="sbUserCard" onclick="showProfile()">
    <div class="sb-user-card-avatar" id="sbAvatar"></div>
    <div class="sb-user-card-info">
      <div class="sb-user-card-name" id="sbName">张三</div>
      <div class="sb-user-card-major">人工智能</div>
    </div>
  </div>
  <div class="sb-menu">
    <div class="sb-item" data-panel="dashboard" onclick="switchPanel('dashboard')">
      <svg class="nav-icon"><use href="#icon-dashboard"/></svg> 学习仪表盘
    </div>
    <div class="sb-section">
      <div class="sb-section-title" id="assistantToggle" onclick="toggleAssistant()">
        <svg class="nav-icon" width="16" height="16"><use href="#icon-chevron-down"/></svg> 百问助手
      </div>
      <div class="sb-sub-items" id="assistantSubItems">
        <div class="sb-sub-item" data-panel="chat" onclick="switchPanel('chat')">
          <svg class="nav-icon"><use href="#icon-chat"/></svg> 智能问答
        </div>
        <div class="sb-sub-item" data-panel="exercise" onclick="switchPanel('exercise')">
          <svg class="nav-icon"><use href="#icon-exercise"/></svg> 做练习题
        </div>
        <div class="sb-sub-item" data-panel="ppt" onclick="switchPanel('ppt')">
          <svg class="nav-icon"><use href="#icon-ppt"/></svg> PPT 生成
        </div>
        <div class="sb-sub-item" data-panel="kb" onclick="switchPanel('kb')">
          <svg class="nav-icon"><use href="#icon-book"/></svg> 知识库查询
        </div>
        <div class="sb-sub-item" data-panel="document" onclick="switchPanel('document')">
          <svg class="nav-icon"><use href="#icon-course"/></svg> 课程文档
        </div>
        <div class="sb-sub-item disabled">
          <svg class="nav-icon"><use href="#icon-path"/></svg> 学习路径 <small>待开发</small>
        </div>
      </div>
    </div>
  </div>
  <div class="sb-bottom">
    <div class="sb-item" onclick="doLogout()">
      <svg class="nav-icon"><use href="#icon-logout"/></svg> 退出登录
    </div>
  </div>
</nav>

<!-- ===== 主内容区 ===== -->
<div class="main" id="mainApp">

  <!-- 仪表盘面板 -->
  <div class="panel active" id="panel-dashboard">
    <h2><svg width="24" height="24" style="vertical-align:middle;margin-right:4px;color:var(--c-primary)"><use href="#icon-dashboard"/></svg>学习仪表盘</h2>
    <div class="dash-grid">
      <div class="dash-card">
        <div class="dash-icon" style="background:linear-gradient(135deg,#2563eb,#1d4ed8);"><svg width="24" height="24" style="color:#fff"><use href="#icon-book"/></svg></div>
        <div class="dash-info">
          <div class="dash-value">3 / 6</div>
          <div class="dash-label">已学习资源类型</div>
          <div class="dash-bar"><div class="dash-bar-fill" style="width:50%;"></div></div>
        </div>
      </div>
      <div class="dash-card" id="studyTimeCard">
        <div class="dash-icon" style="background:linear-gradient(135deg,#0891b2,#2563eb);"><svg width="24" height="24" style="color:#fff"><use href="#icon-clock"/></svg></div>
        <div class="dash-info">
          <div class="dash-value">加载中...</div>
          <div class="dash-label">本周学习时间</div>
        </div>
      </div>
      <div class="dash-card">
        <div class="dash-icon" style="background:linear-gradient(135deg,#f093fb,#f5576c);"><svg width="24" height="24" style="color:#fff"><use href="#icon-pin"/></svg></div>
        <div class="dash-info">
          <div class="dash-value">人工智能基础</div>
          <div class="dash-label">最近学习</div>
        </div>
      </div>
      <div class="dash-card" id="stEntryCard" onclick="stToggle()" style="cursor:pointer;border:2px dashed var(--c-primary);background:linear-gradient(135deg,#eff6ff,#dbeafe);">
        <div class="dash-icon" style="background:linear-gradient(135deg,#f59e0b,#f97316);"><svg width="24" height="24" style="color:#fff"><use href="#icon-path"/></svg></div>
        <div class="dash-info">
          <div class="dash-value" style="font-size:18px;">Python 技能树</div>
        </div>
      </div>
    </div>

    <section id="resourceWorkbench" style="margin-top:24px;background:#fff;border:1px solid #e2e8f0;border-radius:16px;padding:22px;box-shadow:var(--shadow-sm);">
      <div style="display:flex;justify-content:space-between;gap:16px;align-items:flex-start;flex-wrap:wrap;margin-bottom:16px;">
        <div>
          <h3 style="margin:0;font-size:18px;color:#0f172a;">个性化学习资源包</h3>
          <p style="margin:4px 0 0;color:#64748b;font-size:13px;">基于学生画像、知识库引用和五类 Agent 生成可刷新保留的学习闭环。</p>
        </div>
        <div style="display:flex;gap:8px;flex:1;min-width:280px;max-width:560px;">
          <input id="resourceTopicInput" value="Transformer 注意力机制" placeholder="输入学习主题" style="flex:1;min-width:0;border:2px solid #e2e8f0;border-radius:10px;padding:10px 12px;font-size:14px;outline:none;">
          <button id="resourceGenerateBtn" onclick="generateResourceBundle()" style="border:0;border-radius:10px;background:#2563eb;color:#fff;padding:0 18px;font-weight:700;cursor:pointer;white-space:nowrap;">生成个性化资源包</button>
        </div>
      </div>
      <div id="resourceStageList" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:8px;margin-bottom:16px;">
        <div class="resource-stage" data-stage="profile" style="padding:10px;border-radius:10px;background:#eff6ff;color:#1d4ed8;font-size:13px;font-weight:600;">分析画像</div>
        <div class="resource-stage" data-stage="citation" style="padding:10px;border-radius:10px;background:#f8fafc;color:#64748b;font-size:13px;font-weight:600;">检索教材依据</div>
        <div class="resource-stage" data-stage="agents" style="padding:10px;border-radius:10px;background:#f8fafc;color:#64748b;font-size:13px;font-weight:600;">生成五类资源</div>
        <div class="resource-stage" data-stage="path" style="padding:10px;border-radius:10px;background:#f8fafc;color:#64748b;font-size:13px;font-weight:600;">规划学习路径</div>
      </div>
      <div id="resourceWarning" style="display:none;margin-bottom:14px;padding:10px 12px;border-radius:10px;background:#fffbeb;color:#92400e;font-size:13px;"></div>
      <div style="display:grid;grid-template-columns:minmax(0,1.5fr) minmax(260px,0.9fr);gap:16px;">
        <div>
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
            <h4 style="margin:0;font-size:15px;color:#0f172a;">五类资源</h4>
            <span style="font-size:12px;color:#64748b;">document · mindmap · exercise · reading · code_example</span>
          </div>
          <div id="resourceBundleCards" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:10px;">
            <div style="grid-column:1/-1;padding:18px;border:1px dashed #cbd5e1;border-radius:12px;color:#64748b;text-align:center;">暂无资源包，输入主题后生成。</div>
          </div>
          <div id="resourceCitationList" style="margin-top:12px;font-size:12px;color:#475569;"></div>
        </div>
        <aside style="border-left:1px solid #e2e8f0;padding-left:16px;">
          <h4 style="margin:0 0 10px;font-size:15px;color:#0f172a;">学习路径</h4>
          <div id="learningPathNodes" style="display:flex;flex-direction:column;gap:8px;">
            <div style="padding:14px;border:1px dashed #cbd5e1;border-radius:12px;color:#64748b;font-size:13px;">生成资源包后自动规划路径。</div>
          </div>
        </aside>
      </div>
    </section>

  </div>

  <!-- ===== Python 技能树 · 全屏覆盖层 ===== -->
  <div id="skillTreeOverlay" style="display:none;position:fixed;inset:0;background:#f8fafc;z-index:10000;overflow-y:auto;">
    <div style="max-width:900px;margin:0 auto;padding:32px 24px;">
      <div style="margin-bottom:28px;">
        <button onclick="stClose()" style="display:inline-flex;align-items:center;gap:6px;padding:8px 18px;background:#2563eb;color:#fff;border:none;border-radius:8px;font-size:13px;font-weight:600;cursor:pointer;transition:all 0.2s;box-shadow:0 2px 8px rgba(37,99,235,0.2);">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
          返回仪表盘
        </button>
      </div>
      <div style="margin-bottom:24px;">
        <h2 style="margin:0;font-size:24px;font-weight:800;color:#0f172a;">Python 技能树</h2>
        <p style="margin:4px 0 0;font-size:13px;color:#64748b;">7 章闯关 · 28 个知识点 · 前一章达 70% 解锁下一章</p>
      </div>
      <div id="stDebug" style="background:#fffbeb;padding:10px;margin-bottom:16px;border-radius:8px;font-size:12px;display:none;"></div>
      <!-- 练习题弹窗 -->
      <div id="stExerciseOverlay" style="display:none;position:fixed;inset:0;background:rgba(15,23,42,0.6);z-index:10001;align-items:center;justify-content:center;">
        <div id="stExercisePanel" style="background:#fff;border-radius:16px;width:700px;max-width:90vw;max-height:85vh;overflow-y:auto;box-shadow:0 20px 60px rgba(0,0,0,0.3);"></div>
      </div>
      <div id="skillTreeContent">
        <div id="stChapterList"><p style="text-align:center;padding:60px;color:#94a3b8;">加载中...</p></div>
      </div>
    </div>
  </div>

  <!-- 智能问答面板 -->
  <div class="panel" id="panel-chat">
    <h2><svg width="24" height="24" style="vertical-align:middle;margin-right:4px;color:var(--c-primary)"><use href="#icon-chat"/></svg>智能问答</h2>
    <div class="chat-panel-body">
      <div class="chat-msgs" id="chatMsgs">
        <div class="c-msg bot">你好！我是百问助手，有什么学习问题我可以帮你解答？</div>
      </div>
      <div class="chat-input-area">
        <textarea id="chatInput" placeholder="输入你的问题..." rows="1"></textarea>
        <div class="chat-input-bar">
          <div style="display:flex;align-items:center;gap:6px;flex:1;min-width:0;">
            <span class="chat-input-hint" style="white-space:nowrap;">Enter发送</span>
            <select id="chatModel" style="padding:3px 6px;border:1px solid var(--c-border);border-radius:4px;font-size:11px;background:var(--c-surface);color:var(--c-text-secondary);outline:none;cursor:pointer;">
              <option value="deepseek">DeepSeek</option>
              <option value="spark">Spark</option>
            </select>
            <select id="chatEffort" style="padding:3px 6px;border:1px solid var(--c-border);border-radius:4px;font-size:11px;background:var(--c-surface);color:var(--c-text-secondary);outline:none;cursor:pointer;">
              <option value="low">Low</option>
              <option value="high" selected>High</option>
              <option value="max">Max</option>
            </select>
          </div>
          <div style="display:flex;align-items:center;gap:8px;">
            <button class="mic-btn" id="chatMicBtn" onclick="toggleMic()" title="语音输入">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M12 2a3 3 0 0 0-3 3v6a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v1a7 7 0 0 1-14 0v-1"/><line x1="12" y1="19" x2="12" y2="22"/></svg>
            </button>
            <button id="chatSendBtn" onclick="sendChat()">发 送</button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 做练习题面板 -->
  <div class="panel" id="panel-exercise">
    <h2><svg width="24" height="24" style="vertical-align:middle;margin-right:4px;color:var(--c-primary)"><use href="#icon-exercise"/></svg>做练习题</h2>
    <div id="exContainer"></div>
  </div>

  <!-- PPT生成面板 -->
  <div class="panel" id="panel-ppt">
    <h2><svg width="24" height="24" style="vertical-align:middle;margin-right:4px;color:var(--c-primary)"><use href="#icon-ppt"/></svg>PPT 生成</h2>
    <div class="ppt-body">
      <h4 style="margin-bottom:12px;color:#444;">选择模板</h4>
      <div class="ppt-theme-grid" id="pptThemeGrid"></div>
      <div class="pf-field">
        <label>PPT 主题</label>
        <input id="pptQuery" placeholder="输入你想生成的PPT主题，例如：人工智能入门指南">
      </div>
      <h4 style="margin-bottom:12px;color:#444;">内容详细度</h4>
      <div class="ppt-count-row" id="pptDetailRow">
        <button class="ppt-count-btn" data-level="brief">简洁</button>
        <button class="ppt-count-btn sel" data-level="standard">标准</button>
        <button class="ppt-count-btn" data-level="detailed">详尽</button>
      </div>
      <div class="ppt-hint" style="margin-bottom:20px;">简洁版约3-4章核心要点 · 标准版约5-7章均衡展开 · 详尽版约8-10章全面覆盖</div>
      <button class="ppt-gen-btn" id="pptGenBtn" onclick="startPPT()"><svg width="18" height="18" style="vertical-align:middle;margin-right:6px;color:#fff"><use href="#icon-rocket"/></svg>开始生成 PPT</button>
      <div class="ppt-progress-wrap" id="pptProgressWrap" style="display:none;">
        <div class="ppt-progress-bar"><div class="ppt-progress-fill" id="pptProgressFill" style="width:0%;"></div></div>
        <div class="ppt-progress-text" id="pptProgressText"> 正在生成大纲...</div>
      </div>
      <div class="ppt-result" id="pptResult" style="display:none;">
        <a class="ppt-download-btn" id="pptDownloadBtn" href="#" target="_blank"> 下载 PPT</a>
        <div class="ppt-hint">点击下载生成的PPT文件</div>
      </div>
      <div class="ppt-hint" id="pptHint" style="margin-top:16px;">生成PPT需要约30-60秒，任务创建后可关闭页面稍后查看。</div>
    </div>
  </div>


  <!-- 知识库查询面板 -->
  <div class="panel" id="panel-kb">
    <h2><svg width="24" height="24" style="vertical-align:middle;margin-right:4px;color:var(--c-primary)"><use href="#icon-book"/></svg>知识库查询</h2>
    <div class="kb-body" style="max-width:760px;">
      <div class="chat-input-area" style="margin-bottom:12px;">
        <input id="kbInput" placeholder="搜索教材/概念/论文关键词..." onkeydown="if(event.keyCode===13) searchKB()">
        <button onclick="searchKB()">搜索</button>
      </div>
      <div style="display:flex;gap:8px;margin-bottom:8px;flex-wrap:wrap;align-items:center;" id="kbTypeFilters">
        <button class="kb-filter-btn sel" data-type="all" onclick="setKBFilter('all')">全部</button>
        <button class="kb-filter-btn" data-type="concept" onclick="setKBFilter('concept')">概念</button>
        <button class="kb-filter-btn" data-type="pdf" onclick="setKBFilter('pdf')">教材PDF</button>
        <button class="kb-filter-btn" data-type="textbook" onclick="setKBFilter('textbook')">教材参考</button>
        <button class="kb-filter-btn" data-type="paper" onclick="setKBFilter('paper')">论文</button>
      </div>
      <div style="display:flex;gap:8px;margin-bottom:16px;align-items:center;">
        <span style="font-size:13px;color:var(--c-text-secondary);white-space:nowrap;">教材：</span>
        <select id="kbDocFilter" onchange="onKBDocChange()" style="flex:1;padding:8px 12px;border:1px solid var(--c-border);border-radius:var(--radius-sm);font-size:13px;font-family:inherit;outline:none;background:var(--c-surface);">
          <option value="">全部教材</option>
        </select>
      </div>
      <label style="display:flex;align-items:center;gap:6px;margin-bottom:16px;font-size:13px;color:var(--c-text-secondary);cursor:pointer;">
        <input type="checkbox" id="kbIncludeArxiv" onchange="kbState.includeArxiv=this.checked"> 同时搜索 arXiv 论文
      </label>
      <div id="kbStats" style="font-size:12px;color:var(--c-text-secondary);margin-bottom:12px;"></div>
      <div id="kbResults"></div>
      <div id="kbEmpty" style="display:none;text-align:center;padding:40px;color:var(--c-text-secondary);">
        暂无内容。请工程师将教材 PDF 放入 data/knowledge/ 目录。
      </div>
    </div>
  </div>

  <!-- ===== 课程文档面板 ===== -->
  <div class="panel" id="panel-document">
    <h2><svg width="24" height="24" style="vertical-align:middle;margin-right:4px;color:var(--c-primary)"><use href="#icon-course"/></svg>课程文档生成</h2>
    <div class="doc-body" style="max-width:760px;">
      <div class="pf-field">
        <label>课程 / 主题</label>
        <input id="docTopic" placeholder="例如：反向传播算法推导、CNN卷积网络原理、注意力机制详解...">
      </div>
      <h4 style="margin-bottom:12px;color:#444;">难度等级</h4>
      <div class="ppt-count-row" id="docDiffRow">
        <button class="ppt-count-btn" data-level="beginner">入门</button>
        <button class="ppt-count-btn sel" data-level="intermediate">进阶</button>
        <button class="ppt-count-btn" data-level="advanced">高级</button>
      </div>
      <div class="ppt-hint" style="margin-bottom:16px;">入门适合初学者 · 进阶需要一定基础 · 高级面向有经验的学习者</div>
      <h4 style="margin-bottom:12px;color:#444;">文档篇幅</h4>
      <div class="ppt-count-row" id="docDetailRow">
        <button class="ppt-count-btn" data-level="brief">精简</button>
        <button class="ppt-count-btn sel" data-level="standard">标准</button>
        <button class="ppt-count-btn" data-level="detailed">详尽</button>
      </div>
      <div class="ppt-hint" style="margin-bottom:20px;">精简约2-3节核心要点 · 标准约4-6节均衡展开 · 详尽约7-10节全面覆盖</div>
      <button class="doc-gen-btn" id="docGenBtn" onclick="startDocGen()"><svg width="18" height="18" style="vertical-align:middle;margin-right:6px;color:#fff"><use href="#icon-sparkle"/></svg>生成课程文档</button>
      <div class="ppt-progress-wrap" id="docProgressWrap" style="display:none;">
        <div class="ppt-progress-bar"><div class="ppt-progress-fill doc-progress-pulse" id="docProgressFill" style="width:60%;"></div></div>
        <div class="ppt-progress-text" id="docProgressText"> AI 正在撰写文档...</div>
      </div>
      <div class="doc-result" id="docResult" style="display:none;">
        <div class="doc-result-toolbar">
          <span id="docResultTitle" style="font-weight:700;font-size:15px;"></span>
          <div style="display:flex;gap:8px;">
            <button class="doc-action-btn" onclick="copyDocument()"><svg width="14" height="14"><use href="#icon-save"/></svg> 复制</button>
            <button class="doc-action-btn" onclick="downloadDocument()"><svg width="14" height="14"><use href="#icon-save"/></svg> 下载 .md</button>
            <button class="doc-action-btn" onclick="resetDocument()">✕ 关闭</button>
          </div>
        </div>
        <div class="doc-content markdown-body" id="docContent"></div>
      </div>
    </div>
  </div>

  <!-- ===== 个人信息页面 ===== -->
  <div class="panel" id="panel-profile">
    <div class="pf-head">
      <button class="pf-back" onclick="closeProfile()">← 返回</button>
      <h3>个人信息</h3>
      <span></span>
    </div>
    <div class="pf-body">
      <div class="pf-avatar-section">
        <div class="pf-avatar-preview" id="pfAvatarPreview" onclick="toggleAvatarPicker()">
          <svg id="pfAvatarEmoji" width="28" height="28" style="color:#fff"><use href="#icon-user"/></svg>
        </div>
        <div class="avatar-picker-grid" id="avatarPickerGrid" style="display:none;"></div>
      </div>
      <div class="pf-field"><label>学号</label><input id="pfSid" disabled></div>
      <div class="pf-field"><label>姓名</label><input id="pfName"></div>
      <div class="pf-field"><label>专业</label><input id="pfMajor" value="人工智能" disabled></div>
      <div class="pf-field"><label>年级</label><select id="pfGrade"><option value="">请选择年级</option><option value="大一">大一</option><option value="大二">大二</option><option value="大三">大三</option><option value="大四">大四</option></select></div>
      <div class="pf-field"><label>知识基础</label><textarea id="pfKnowledgeBase" placeholder="描述你已掌握的课程和技能"></textarea></div>
      <div class="pf-field"><label>认知风格</label><select id="pfCognitiveStyle"><option value="">请选择认知风格</option><option value="逻辑型">逻辑型：偏好系统性推理和结构化学习</option><option value="视觉型">视觉型：偏好图表、示意图和可视化方式</option><option value="读写型">读写型：偏好通过阅读和写作来学习</option><option value="动觉型">动觉型：偏好动手实践和体验式学习</option><option value="听觉型">听觉型：偏好听讲解和讨论来学习</option></select></div>
      <div class="pf-field"><label>薄弱知识点（逗号分隔）</label><textarea id="pfWeakPoints" placeholder="例如：反向传播、Transformer注意力机制"></textarea></div>
      <div class="pf-field"><label>学习目标（逗号分隔）</label><textarea id="pfGoals" placeholder="例如：掌握PyTorch框架、完成AI项目"></textarea></div>
      <div class="pf-field"><label>学习节奏</label><select id="pfPace"><option value="">请选择学习节奏</option><option value="快">快：基础扎实，可接受高难度内容</option><option value="中">中：稳步推进，需要适当消化时间</option><option value="慢">慢：需要循序渐进，多练习巩固</option></select></div>
      <div class="pf-field"><label>兴趣方向（逗号分隔）</label><textarea id="pfInterests" placeholder="例如：机器学习、深度学习、NLP"></textarea></div>
      <div class="pf-field"><label>偏好资源类型（可多选）</label><div class="pf-checkbox-group" id="pfResourceTypes"></div></div>
      <div class="pf-field"><label>编程经验</label><select id="pfProgrammingExp"><option value="">请选择编程经验</option><option value="零基础">零基础：未接触过编程</option><option value="了解基础语法">了解基础语法：学过Python/C等基础</option><option value="能独立完成小项目">能独立完成小项目：有一定项目经验</option><option value="熟练使用NumPy/Pandas">熟练使用NumPy/Pandas：数据科学生态</option><option value="熟练使用PyTorch/TensorFlow">熟练使用PyTorch/TensorFlow：深度学习框架</option><option value="有生产环境开发经验">有生产环境开发经验：工程能力扎实</option></select></div>
    </div>
    <div class="pf-foot">
      <button class="save-btn" onclick="saveProfile()"><svg width="16" height="16" style="vertical-align:middle;margin-right:4px;color:#fff"><use href="#icon-save"/></svg>保存修改</button>
      <button class="delete-btn" onclick="deleteAccount()">注销账号</button>
    </div>
    <div class="save-msg" id="pfSaveMsg" style="display:none;"></div>
  </div>

</div>

</div><!-- close appMain -->


<script>

const BASE = '';
let studentId = '';
let profileData = null;
let currentPanel = 'dashboard';
let exState = { step:'type', type:'', count:5, course:'', questions:[], currentIdx:0, userAnswers:[] };
let chosenAvatarId = 'avatar-1';

const AVATARS = [
  { id:'avatar-1', icon:'book', gradient:'linear-gradient(135deg,#2563eb,#60a5fa)' },
  { id:'avatar-2', icon:'monitor', gradient:'linear-gradient(135deg,#3b82f6,#60a5fa)' },
  { id:'avatar-3', icon:'brain', gradient:'linear-gradient(135deg,#10b981,#34d399)' },
  { id:'avatar-4', icon:'rocket', gradient:'linear-gradient(135deg,#f97316,#fb923c)' },
  { id:'avatar-5', icon:'sparkle', gradient:'linear-gradient(135deg,#ec4899,#f472b6)' },
  { id:'avatar-6', icon:'target', gradient:'linear-gradient(135deg,#06b6d4,#22d3ee)' },
  { id:'avatar-7', icon:'fire', gradient:'linear-gradient(135deg,#ef4444,#f87171)' },
  { id:'avatar-8', icon:'zap', gradient:'linear-gradient(135deg,#6366f1,#818cf8)' }
];

const COURSE_OPTIONS = {
  '人工智能': ['Python编程','机器学习基础','深度学习入门','自然语言处理','计算机视觉','强化学习'],
  'default': ['Python编程','机器学习基础','深度学习入门']
};

function getCourseOptions(profile) {
  const major = profile?.major || '';
  for (const [k,v] of Object.entries(COURSE_OPTIONS)) {
    if (major.includes(k)) return v;
  }
  return COURSE_OPTIONS['default'];
}

async function api(path, opts={}) {
  const r = await fetch(BASE+path, {headers:{'Content-Type':'application/json'},...opts});
  if (!r.ok) { const e = await r.json().catch(()=>({})); const error = new Error(e.detail||r.statusText); error.status = r.status; throw error; }
  return await r.json();
}

// === 登录/注册 ===
function showLogin() {
  document.getElementById('loginCard').style.display = '';
  document.getElementById('registerCard').style.display = 'none';
  document.getElementById('loginMsg').textContent = '';
}

function showRegister() {
  document.getElementById('loginCard').style.display = 'none';
  document.getElementById('registerCard').style.display = '';
}

function doLogin() {
  var sidEl = document.getElementById('loginSid');
  var pwdEl = document.getElementById('loginPwd');
  var sid = sidEl.value.trim();
  var pwd = pwdEl.value.trim();
  sidEl.style.borderColor = ''; sidEl.placeholder = '输入学号';
  pwdEl.style.borderColor = ''; pwdEl.placeholder = '输入密码';
  if (!sid) { sidEl.style.borderColor = '#ef4444'; sidEl.placeholder = '未输入账号!'; sidEl.value = ''; sidEl.focus(); return; }
  if (!pwd) { pwdEl.style.borderColor = '#ef4444'; pwdEl.placeholder = '未输入密码!'; pwdEl.value = ''; pwdEl.focus(); return; }
  api('/api/login', {method:'POST', body:JSON.stringify({student_id:sid, password:pwd})})
    .then(d => { if (d.success) { studentId=d.student_id; profileData=d.profile; enterApp(d.profile); } })
    .catch(e => { document.getElementById('loginMsg').textContent = e.message||'登录失败'; });
}

function doRegister() {
  const nickname = document.getElementById('regNickname').value.trim();
  if (!nickname) { showToast('请输入昵称', 'error'); return; }
  api('/api/register', {method:'POST', body:JSON.stringify({nickname:nickname, major:'人工智能'})})
    .then(d => {
      if (d.success) {
        launchConfetti();
        showToast('注册成功', 'success');
        setTimeout(() => showToast('你的学号是: ' + d.student_id, 'success'), 500);
        document.getElementById('loginSid').value = d.student_id;
        setTimeout(() => showLogin(), 2000);
      }
    })
    .catch(e => { showToast(e.message||'注册失败', 'error'); });
}

function launchConfetti() {
  confetti({ particleCount: 100, spread: 70, origin: { y: 0.6 } });
  setTimeout(() => confetti({ particleCount: 50, angle: 60, spread: 55, origin: { x: 0 } }), 200);
  setTimeout(() => confetti({ particleCount: 50, angle: 120, spread: 55, origin: { x: 1 } }), 200);
}

function showToast(msg, type) {
  const t = document.createElement('div');
  t.className = 'toast ' + type;
  t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(() => t.remove(), 3000);
}

function enterApp(profile) {
  document.getElementById('loginOverlay').style.display = 'none';
  document.getElementById('appMain').style.display = '';
  profileData = profile;
  chosenAvatarId = profile.avatar || 'avatar-1';
  updateSidebarUser(profile.name || '张三', chosenAvatarId);
  switchPanel('dashboard');
  loadStudyTime();
  loadResourceWorkbench();
  onHashChange();
}

function formatStudyDuration(seconds) {
  seconds = Math.max(0, Number(seconds) || 0);
  var hours = Math.floor(seconds / 3600);
  var minutes = Math.floor((seconds % 3600) / 60);
  return minutes ? hours + ' 小时 ' + minutes + ' 分钟' : hours + ' 小时';
}

function ensureStudyTimeControls() {
  var card = document.getElementById('studyTimeCard');
  if (!card || document.getElementById('studyTimeStart')) return;
  var info = card.querySelector('.dash-info');
  if (!info) return;
  var status = document.createElement('div');
  status.id = 'studyTimeStatus';
  status.style.cssText = 'font-size:12px;color:var(--c-text-secondary);margin-top:8px;';
  info.appendChild(status);
  var actions = document.createElement('div');
  actions.style.cssText = 'display:flex;gap:6px;margin-top:10px;';
  actions.innerHTML = '<button id="studyTimeStart" onclick="studyTimeStart(event)" style="padding:6px 10px;border:0;border-radius:6px;background:#2563eb;color:#fff;cursor:pointer;font-size:12px;">开始学习</button>'
    + '<button id="studyTimePause" onclick="studyTimePause(event)" style="padding:6px 10px;border:1px solid #cbd5e1;border-radius:6px;background:#fff;color:#334155;cursor:pointer;font-size:12px;display:none;">暂停</button>'
    + '<button id="studyTimeEnd" onclick="studyTimeEnd(event)" style="padding:6px 10px;border:1px solid #fecaca;border-radius:6px;background:#fff;color:#dc2626;cursor:pointer;font-size:12px;display:none;">结束</button>';
  info.appendChild(actions);
}

async function loadStudyTime() {
  ensureStudyTimeControls();
  try {
    var data = await api('/api/study-time/' + studentId);
    var card = document.getElementById('studyTimeCard');
    if (!card) return;
    var value = card.querySelector('.dash-value');
    var status = document.getElementById('studyTimeStatus');
    value.textContent = formatStudyDuration(data.week_seconds);
    status.textContent = data.active ? '学习会话进行中' : '暂无进行中的学习会话';
    document.getElementById('studyTimeStart').style.display = data.active ? 'none' : '';
    document.getElementById('studyTimePause').style.display = data.active ? '' : 'none';
    document.getElementById('studyTimeEnd').style.display = data.active ? '' : 'none';
  } catch (e) {
    var card = document.getElementById('studyTimeCard');
    if (card) card.querySelector('.dash-value').textContent = '加载失败';
  }
}

async function studyTimeAction(event, action) {
  if (event) event.stopPropagation();
  try {
    await api('/api/study-time/' + studentId + '/' + action, {method:'POST'});
    await loadStudyTime();
  } catch (e) {
    showToast(e.message || '学习会话操作失败', 'error');
  }
}
function studyTimeStart(event) { return studyTimeAction(event, 'start'); }
function studyTimePause(event) { return studyTimeAction(event, 'pause'); }
function studyTimeEnd(event) { return studyTimeAction(event, 'end'); }

function setResourceStages(activeIndex) {
  var stages = document.querySelectorAll('.resource-stage');
  stages.forEach(function(stage, index) {
    var done = index < activeIndex;
    var active = index === activeIndex;
    stage.style.background = done ? '#f0fdf4' : active ? '#eff6ff' : '#f8fafc';
    stage.style.color = done ? '#15803d' : active ? '#1d4ed8' : '#64748b';
    stage.textContent = (done ? '✓ ' : active ? '• ' : '') + stage.textContent.replace(/^✓ |^• /, '');
  });
}

function resourceTypeLabel(type) {
  return {
    document: '讲解文档',
    mindmap: '思维导图',
    exercise: '练习题',
    reading: '拓展阅读',
    code_example: '代码案例'
  }[type] || type;
}

async function loadResourceWorkbench() {
  if (!studentId || !document.getElementById('resourceWorkbench')) return;
  try {
    var data = await api('/api/generation/resource-bundles/' + studentId);
    var bundles = data.bundles || [];
    if (bundles.length) renderResourceBundle(bundles[bundles.length - 1]);
    var path = await api('/api/generation/learning-path/' + studentId).catch(function(){ return null; });
    if (path) renderLearningPath(path);
  } catch (e) {
    showResourceWarning('资源包加载失败：' + e.message);
  }
}

async function generateResourceBundle() {
  var input = document.getElementById('resourceTopicInput');
  var btn = document.getElementById('resourceGenerateBtn');
  var topic = input.value.trim();
  if (!topic) { showToast('请输入学习主题', 'error'); return; }
  btn.disabled = true;
  btn.textContent = '生成中...';
  showResourceWarning('');
  setResourceStages(0);
  try {
    setResourceStages(1);
    var result = await api('/api/generation/resource-bundle', {
      method:'POST',
      body:JSON.stringify({
        student_id: studentId,
        course_name: profileData?.major || '人工智能',
        topic: topic,
        difficulty: 'intermediate',
        resource_types: ['document','mindmap','exercise','reading','code_example']
      })
    });
    setResourceStages(4);
    renderResourceBundle(result);
    renderLearningPath(result.path);
    await loadStudyTime();
    showToast('资源包已生成', 'success');
  } catch (e) {
    var message = resourceGenerationErrorMessage(e);
    showResourceWarning(message);
    showToast(message, 'error');
  } finally {
    btn.disabled = false;
    btn.textContent = '生成个性化资源包';
  }
}

function resourceGenerationErrorMessage(error) {
  var messages = {
    400: '输入内容未通过安全检查，请调整主题后重试。',
    404: '未找到对应的学习档案，请重新登录后再试。',
    422: '请求参数有误，请检查学习主题和资源类型。',
    502: '生成服务暂时不可用，已保留当前页面内容，请稍后重试。'
  };
  return messages[error && error.status] || '资源包生成失败，请稍后重试。';
}

function showResourceWarning(message) {
  var el = document.getElementById('resourceWarning');
  if (!el) return;
  el.style.display = message ? '' : 'none';
  el.textContent = message || '';
}

function renderResourceBundle(bundle) {
  var cardWrap = document.getElementById('resourceBundleCards');
  if (!cardWrap || !bundle) return;
  var resources = bundle.resources || [];
  if (!resources.length) {
    cardWrap.innerHTML = '<div style="grid-column:1/-1;padding:18px;border:1px dashed #cbd5e1;border-radius:12px;color:#64748b;text-align:center;">资源包暂无可展示资源。</div>';
  } else {
    cardWrap.innerHTML = resources.map(function(resource) {
      var citations = resource.citations || bundle.citations || [];
      var summary = resource.content?.summary || resource.content?.description || resource.content?.reading_guide || resource.content?.explanation || resource.title || '';
      return '<article style="border:1px solid #e2e8f0;border-radius:12px;padding:14px;background:#fff;">'
        + '<div style="font-size:12px;color:#2563eb;font-weight:700;">' + resourceTypeLabel(resource.resource_type) + '</div>'
        + '<h5 style="margin:6px 0 8px;font-size:15px;color:#0f172a;">' + (resource.title || '学习资源') + '</h5>'
        + '<p style="margin:0;color:#64748b;font-size:12px;line-height:1.5;max-height:56px;overflow:hidden;">' + summary + '</p>'
        + '<div style="margin-top:10px;display:flex;justify-content:space-between;color:#64748b;font-size:12px;">'
        + '<span>' + (resource.difficulty || 'intermediate') + '</span><span>引用 ' + citations.length + '</span></div>'
        + '</article>';
    }).join('');
  }
  renderCitations(bundle.citations || []);
  if (bundle.warnings && bundle.warnings.length) showResourceWarning(bundle.warnings.join('；'));
}

function renderCitations(citations) {
  var el = document.getElementById('resourceCitationList');
  if (!el) return;
  if (!citations.length) {
    el.innerHTML = '<div style="padding:10px;border-radius:10px;background:#fffbeb;color:#92400e;">知识库未找到充分依据，请核验。</div>';
    return;
  }
  el.innerHTML = '<div style="font-weight:700;margin-bottom:6px;color:#0f172a;">引用依据</div>'
    + citations.slice(0, 3).map(function(c) {
      return '<div style="padding:8px 10px;border-radius:8px;background:#f8fafc;margin-bottom:6px;">'
        + (c.title || '知识库') + (c.page ? ' · p.' + c.page : '')
        + '<div style="color:#64748b;margin-top:3px;">' + (c.snippet || '').slice(0, 120) + '</div></div>';
    }).join('');
}

function renderLearningPath(path) {
  var wrap = document.getElementById('learningPathNodes');
  if (!wrap || !path) return;
  var nodes = path.nodes || [];
  if (!nodes.length) {
    wrap.innerHTML = '<div style="padding:14px;border:1px dashed #cbd5e1;border-radius:12px;color:#64748b;font-size:13px;">学习路径暂无节点。</div>';
    return;
  }
  wrap.innerHTML = nodes.map(function(node, index) {
    var done = node.status === 'completed';
    return '<div style="padding:12px;border:1px solid ' + (done ? '#bbf7d0' : '#e2e8f0') + ';border-radius:12px;background:' + (done ? '#f0fdf4' : '#fff') + ';">'
      + '<div style="display:flex;justify-content:space-between;gap:8px;"><strong style="font-size:13px;color:#0f172a;">' + (index + 1) + '. ' + node.title + '</strong>'
      + '<span style="font-size:11px;color:#64748b;">' + (node.estimated_hours || 1) + 'h</span></div>'
      + '<p style="margin:6px 0;color:#64748b;font-size:12px;line-height:1.45;">' + (node.description || '按关联资源完成本阶段学习。') + '</p>'
      + '<button onclick="completeLearningPathNode(\\'' + path.path_id + '\\',\\'' + node.node_id + '\\')" ' + (done ? 'disabled' : '') + ' style="padding:6px 10px;border-radius:8px;border:1px solid #2563eb;background:' + (done ? '#f0fdf4' : '#eff6ff') + ';color:#2563eb;font-size:12px;cursor:' + (done ? 'default' : 'pointer') + ';">' + (done ? '已完成' : '标记完成') + '</button>'
      + '</div>';
  }).join('');
}

async function completeLearningPathNode(pathId, nodeId) {
  try {
    var path = await api('/api/generation/learning-path/' + pathId + '/nodes/' + nodeId, {
      method:'PUT',
      body:JSON.stringify({status:'completed'})
    });
    renderLearningPath(path);
    await loadResourceWorkbench();
  } catch (e) {
    showToast(e.message || '路径更新失败', 'error');
  }
}
function updateSidebarUser(name, avatarId) {
  document.getElementById('sbName').textContent = name;
  const a = AVATARS.find(x => x.id === avatarId) || AVATARS[0];
  const avatarEl = document.getElementById('sbAvatar');
  avatarEl.style.background = a.gradient;
  avatarEl.innerHTML = '<svg width=\"20\" height=\"20\" style=\"color:#fff\"><use href=\"#icon-'+a.icon+'\"/></svg>';
}

function doLogout() { location.reload(); }

// === 侧边栏 ===
function toggleAssistant() {
  document.getElementById('assistantToggle').classList.toggle('collapsed');
  document.getElementById('assistantSubItems').classList.toggle('collapsed');
}

function switchPanel(name) {
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  const panel = document.getElementById('panel-'+name);
  if (panel) panel.classList.add('active');
  document.querySelectorAll('.sb-sub-item:not(.disabled)').forEach(i => i.classList.remove('active'));
  const sideItem = document.querySelector('.sb-sub-item[data-panel=\"'+name+'\"]');
  if (sideItem) sideItem.classList.add('active');
  currentPanel = name;
  if (name === 'exercise') renderExStep();
  if (name === 'chat') setTimeout(() => document.getElementById('chatInput').focus(), 300);
  if (name === 'kb') loadKBDocs();
  if (name === 'ppt') { loadThemes(); resetPPT(); }
  if (name === 'kb') { loadKBStats(); }
}

// === 智能问答 ===
// marked v5+ 不支持 setOptions，改用 parse() 传参
let _markedOpts = null;
function _getMarkedOpts() {
  if (_markedOpts) return _markedOpts;
  _markedOpts = { breaks: true, gfm: true };
  try {
    if (typeof hljs !== 'undefined') {
      hljs.configure({ languages: ['python','javascript','bash'] });
      _markedOpts.highlight = function(code, lang) {
        if (lang && hljs.getLanguage(lang)) return hljs.highlight(code, { language: lang }).value;
        return code;
      };
    }
  } catch(e) { console.log('hljs error:', e); }
  return _markedOpts;
}

function autoResizeChatInput() {
  const input = document.getElementById('chatInput');
  input.style.height = 'auto';
  input.style.height = Math.min(input.scrollHeight, 160) + 'px';
}

document.addEventListener('DOMContentLoaded', function() {
  const input = document.getElementById('chatInput');
  input.addEventListener('input', autoResizeChatInput);
  input.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendChat();
    }
  });
});

// === 语音输入 ===
let micRecorder = null;
let micStream = null;
let micRecording = false;

async function toggleMic() {
  var btn = document.getElementById('chatMicBtn');
  var input = document.getElementById('chatInput');

  if (micRecording) {
    // 停止录音
    micRecorder.stop();
    btn.classList.remove('recording');
    btn.classList.add('processing');
    input.placeholder = '识别中...';
    micRecording = false;
  } else {
    // 开始录音
    try {
      micStream = await navigator.mediaDevices.getUserMedia({ audio: true });
      micRecorder = new MediaRecorder(micStream, { mimeType: 'audio/webm' });
      var chunks = [];
      micRecorder.ondataavailable = function(e) { chunks.push(e.data); };
      micRecorder.onstop = async function() {
        // 停止所有音轨
        micStream.getTracks().forEach(function(t) { t.stop(); });
        var blob = new Blob(chunks, { type: 'audio/webm' });
        try {
          var formData = new FormData();
          formData.append('audio', blob, 'recording.webm');
          var resp = await fetch('/api/speech/recognize', { method: 'POST', body: formData });
          if (!resp.ok) {
            var err = await resp.json().catch(function() { return {}; });
            throw new Error(err.detail || '识别失败');
          }
          var data = await resp.json();
          input.value = (input.value ? input.value + ' ' : '') + (data.text || '');
        } catch(e) {
          alert('语音识别失败: ' + e.message);
        }
        btn.classList.remove('processing');
        input.placeholder = '输入你的问题...';
      };
      micRecorder.start();
      btn.classList.add('recording');
      input.placeholder = '正在聆听...';
      micRecording = true;
    } catch(e) {
      alert('无法访问麦克风: ' + e.message);
    }
  }
}

async function sendChat() {
  const input = document.getElementById('chatInput');
  const btn = document.getElementById('chatSendBtn');
  const text = input.value.trim();
  if (!text) return;
  input.value = '';
  input.style.height = 'auto';
  addChatMsg('user', text);
  const thinkingEl = addChatMsg('bot', '思考中...');
  btn.disabled = true;
  try {
    const data = await api('/api/chat-simple', {method:'POST', body:JSON.stringify({student_id:studentId, message:text, model:document.getElementById('chatModel').value, effort:document.getElementById('chatEffort').value})});
    const html = (typeof marked !== 'undefined') ? marked.parse(data.reply, _getMarkedOpts()) : data.reply.replace(/\\n/g, '<br>');
    thinkingEl.innerHTML = html;
    if (data.profile) { profileData = data.profile; }
  } catch(e) {
    thinkingEl.textContent = '出错了: ' + e.message;
  }
  btn.disabled = false;
}

function addChatMsg(role, text, isHtml) {
  const div = document.createElement('div');
  div.className = 'c-msg ' + role;
  if (isHtml) div.innerHTML = text;
  else div.textContent = text;
  document.getElementById('chatMsgs').appendChild(div);
  document.getElementById('chatMsgs').scrollTop = document.getElementById('chatMsgs').scrollHeight;
  return div;
}

// === 做练习题 ===
function renderExStep() {
  const c = document.getElementById('exContainer');
  const s = exState;
  let html = '';

  if (s.step === 'type') {
    html = '<div class=\"ex-step\"><h3>选择题型</h3><div class=\"ex-type-grid\">'+
      '<button class=\"ex-type-btn'+(s.type==='choice'?' sel':'')+'\" onclick=\"pickExType(\\'choice\\')\"> 选择题</button>'+
      '<button class=\"ex-type-btn'+(s.type==='fill_blank'?' sel':'')+'\" onclick=\"pickExType(\\'fill_blank\\')\">️ 填空题</button>'+
      '<button class=\"ex-type-btn'+(s.type==='short_answer'?' sel':'')+'\" onclick=\"pickExType(\\'short_answer\\')\"> 简答题</button>'+
      '</div><button class=\"ex-next-btn\" onclick=\"exNextStep()\">下一步 →</button></div>';
  } else if (s.step === 'count') {
    html = '<div class=\"ex-step\"><h3>出题个数</h3>'+
      '<input type=\"number\" class=\"ex-count-input\" id=\"exCount\" value=\"'+s.count+'\" min=\"1\" max=\"20\">'+
      '<div class=\"ex-step-btns\"><button class=\"ex-back-btn\" onclick=\"exPrevStep()\">← 上一步</button>'+
      '<button class=\"ex-next-btn\" onclick=\"exPickCount()\">下一步 →</button></div></div>';
  } else if (s.step === 'course') {
    const courses = getCourseOptions(profileData);
    html = '<div class=\"ex-step\"><h3>选择课程</h3><div class=\"ex-course-grid\">'+
      courses.map((c,i) => '<button class=\"ex-course-btn'+(s.course===c?' sel':'')+'\" onclick=\"pickExCourse(\\''+c+'\\')\">'+['','',''][i]+' '+c+'</button>').join('')+
      '</div><div class=\"ex-step-btns\"><button class=\"ex-back-btn\" onclick=\"exPrevStep()\">← 上一步</button>'+
      '<button class=\"ex-start-btn\" onclick=\"startExercise()\"'+(s.course?'':' disabled')+'>开始答题</button></div></div>';
  } else if (s.step === 'answering') {
    const q = s.questions[s.currentIdx];
    html = '<div class=\"ex-question\"><div class=\"ex-q-progress\">第 '+(s.currentIdx+1)+' / '+s.questions.length+' 题</div>'+
      '<div class=\"ex-q-stem\">'+q.stem+'</div>';
    if (q.type === 'choice' && q.options) {
      html += '<div class=\"ex-q-options\">'+q.options.map((o,i) =>
        '<div class=\"ex-q-opt'+(s.userAnswers[s.currentIdx]===String.fromCharCode(65+i)?' sel':'')+'\" onclick=\"pickOption(\\''+String.fromCharCode(65+i)+'\\')\">'+o+'</div>'
      ).join('')+'</div>';
    } else if (q.type === 'fill_blank') {
      html += '<input class=\"ex-q-input\" id=\"exAnswerInput\" placeholder=\"请输入你的答案...\" value=\"'+(s.userAnswers[s.currentIdx]||'')+'\">';
    } else {
      html += '<textarea class=\"ex-q-input\" id=\"exAnswerInput\" placeholder=\"请输入你的答案...\">'+(s.userAnswers[s.currentIdx]||'')+'</textarea>';
    }
    html += '<div class=\"ex-step-btns\">'+
      (s.currentIdx>0?'<button class=\"ex-back-btn\" onclick=\"exPrevQuestion()\">← 上一题</button>':'<div></div>')+
      '<button class=\"ex-submit-btn\" onclick=\"submitAnswer()\">'+(s.currentIdx<s.questions.length-1?'下一题 →':'提交答案')+'</button></div></div>';
  } else if (s.step === 'result') {
    const correct = s.userAnswers.filter((a,i) => a === s.questions[i].answer).length;
    const total = s.questions.length;
    html = '<div class=\"ex-result\"><div class=\"ex-score\">'+correct+' / '+total+' <span>正确</span></div>';
    s.questions.forEach((q,i) => {
      const ok = s.userAnswers[i] === q.answer;
      html += '<div class=\"ex-review-item\"><strong>Q'+(i+1)+'.</strong> '+q.stem+
        '<div>你的答案: <span class=\"'+(ok?'r-correct':'r-wrong')+'\">'+(s.userAnswers[i]||'未作答')+'</span></div>'+
        '<div>正确答案: <span class=\"r-correct\">'+q.answer+'</span></div>'+
        (q.explanation?'<div class=\"r-exp\"> '+q.explanation+'</div>':'')+'</div>';
    });
    html += '<div style=\"text-align:center;margin-top:20px;\"><button class=\"ex-start-btn\" onclick=\"resetExercise()\">再做一组</button></div></div>';
  }
  c.innerHTML = html;
}

function pickExType(t) { exState.type=t; renderExStep(); }
function exNextStep() {
  if (exState.step==='type' && !exState.type) return;
  exState.step = exState.step==='type'?'count':exState.step==='count'?'course':'course';
  renderExStep();
}
function exPrevStep() {
  exState.step = exState.step==='course'?'count':exState.step==='answering'?'course':'type';
  renderExStep();
}
function exPickCount() {
  const v = parseInt(document.getElementById('exCount').value)||5;
  exState.count = Math.min(20, Math.max(1, v));
  renderExStep();
  exNextStep();
}
function pickExCourse(c) { exState.course=c; renderExStep(); }
async function startExercise() {
  exState.step = 'answering';
  exState.currentIdx = 0;
  exState.userAnswers = [];
  const exDiv = document.getElementById('exContainer');
  exDiv.innerHTML = '<div style=\"padding:40px;text-align:center;color:#888;\"> 正在出题...</div>';
  try {
    const data = await api('/api/exercise/generate', {
      method:'POST', body:JSON.stringify({student_id:studentId, question_type:exState.type, count:exState.count, course_name:exState.course})
    });
    exState.questions = data.questions || [];
    if (!exState.questions.length) throw new Error('未获取到题目');
    renderExStep();
  } catch(e) {
    exDiv.innerHTML = '<div style=\"padding:40px;text-align:center;color:#dc2626;\">出题失败: '+e.message+'<br><button class=\"ex-back-btn\" style=\"margin-top:12px;\" onclick=\"resetExercise()\">重试</button></div>';
  }
}
function pickOption(val) {
  exState.userAnswers[exState.currentIdx] = val;
  renderExStep();
}
function submitAnswer() {
  if (exState.type==='fill_blank'||exState.type==='short_answer') {
    const inp = document.getElementById('exAnswerInput');
    if (inp) exState.userAnswers[exState.currentIdx] = inp.value.trim();
  }
  if (exState.currentIdx < exState.questions.length-1) {
    exState.currentIdx++;
    renderExStep();
  } else {
    exState.step = 'result';
    renderExStep();
  }
}
function exPrevQuestion() {
  if (exState.currentIdx > 0) { exState.currentIdx--; renderExStep(); }
}
function resetExercise() {
  exState = { step:'type', type:'', count:5, course:'', questions:[], currentIdx:0, userAnswers:[] };
  renderExStep();
}

// === Hash 路由 ===
function navigateTo(view) {
  console.log('[router] navigateTo:', view);
  if (view === 'profile') {
    location.hash = 'profile';
  } else {
    location.hash = '';
  }
}

function onHashChange() {
  const hash = location.hash.replace('#', '');
  if (hash === 'profile') {
    if (!profileData) { navigateTo('chat'); return; }
    showProfilePage();
  } else {
    switchPanel('dashboard');
  }
}
window.addEventListener('hashchange', onHashChange);

// === 个人信息页面 ===
function showProfile() {
  console.log('[router] showProfile called, profileData:', !!profileData);
  if (!profileData) return;
  navigateTo('profile');
}

const RESOURCE_TYPE_OPTIONS = ['代码案例','项目实战','论文导读','概念图解','视频讲解','练习题'];

function buildResourceTypeCheckboxes(selected) {
  const container = document.getElementById('pfResourceTypes');
  container.innerHTML = RESOURCE_TYPE_OPTIONS.map(t => {
    const isSel = selected.includes(t);
    return '<label class=\"'+(isSel?'checked':'')+'\" onclick=\"toggleResourceType(this)\"><input type=\"checkbox\" value=\"'+t+'\" '+(isSel?'checked':'')+'>'+t+'</label>';
  }).join('');
}

function toggleResourceType(el) {
  el.classList.toggle('checked');
  const cb = el.querySelector('input');
  cb.checked = !cb.checked;
}

function getSelectedResourceTypes() {
  const cbs = document.querySelectorAll('#pfResourceTypes input');
  return Array.from(cbs).filter(c => c.checked).map(c => c.value);
}

function showProfilePage() {
  const p = profileData;
  document.getElementById('pfSid').value = studentId;
  document.getElementById('pfName').value = p.name || '';
  document.getElementById('pfMajor').value = '人工智能';
  document.getElementById('pfGrade').value = p.grade || '';
  document.getElementById('pfKnowledgeBase').value = p.knowledge_base || '';
  document.getElementById('pfCognitiveStyle').value = p.cognitive_style || '';
  document.getElementById('pfWeakPoints').value = (p.weak_points||[]).join('、');
  document.getElementById('pfGoals').value = (p.learning_goals||[]).join('、');
  document.getElementById('pfPace').value = p.learning_pace || '';
  document.getElementById('pfInterests').value = (p.interest_topics||[]).join('、');
  document.getElementById('pfProgrammingExp').value = p.programming_exp || '';
  buildResourceTypeCheckboxes(p.preferred_resource_types || []);
  document.getElementById('pfSaveMsg').style.display = 'none';
  chosenAvatarId = p.avatar || 'avatar-1';
  updateProfileAvatar(chosenAvatarId);
  buildAvatarPicker();
  switchPanel('profile');
}

function closeProfile() { navigateTo('chat'); }

function updateProfileAvatar(avatarId) {
  const a = AVATARS.find(x => x.id === avatarId) || AVATARS[0];
  document.getElementById('pfAvatarPreview').style.background = a.gradient;
  document.getElementById('pfAvatarEmoji').innerHTML = '<svg width=\"28\" height=\"28\" style=\"color:#fff\"><use href=\"#icon-'+a.icon+'\"/></svg>';
}

function buildAvatarPicker() {
  const grid = document.getElementById('avatarPickerGrid');
  grid.innerHTML = AVATARS.map(a =>
    '<div class=\"avatar-pick'+(chosenAvatarId===a.id?' sel':'')+'\" style=\"background:'+a.gradient+'\" onclick=\"selectAvatar(\\''+a.id+'\\')\"><svg width=\"22\" height=\"22\" style=\"color:#fff\"><use href=\"#icon-'+a.icon+'\"/></svg></div>'
  ).join('');
}

function toggleAvatarPicker() {
  const grid = document.getElementById('avatarPickerGrid');
  grid.style.display = grid.style.display === 'none' ? 'grid' : 'none';
  if (grid.style.display !== 'none') buildAvatarPicker();
}

function selectAvatar(id) {
  chosenAvatarId = id;
  updateProfileAvatar(id);
  buildAvatarPicker();
}

async function saveProfile() {
  const updates = {
    name: document.getElementById('pfName').value.trim(),
    major: '人工智能',
    grade: document.getElementById('pfGrade').value.trim(),
    knowledge_base: document.getElementById('pfKnowledgeBase').value.trim(),
    cognitive_style: document.getElementById('pfCognitiveStyle').value.trim(),
    weak_points: document.getElementById('pfWeakPoints').value.split(/[、,，]/).map(s=>s.trim()).filter(Boolean),
    learning_goals: document.getElementById('pfGoals').value.split(/[、,，]/).map(s=>s.trim()).filter(Boolean),
    learning_pace: document.getElementById('pfPace').value.trim(),
    interest_topics: document.getElementById('pfInterests').value.split(/[、,，]/).map(s=>s.trim()).filter(Boolean),
    preferred_resource_types: getSelectedResourceTypes(),
    programming_exp: document.getElementById('pfProgrammingExp').value.trim(),
    avatar: chosenAvatarId
  };
  try {
    await api('/api/profile/update', {method:'PUT', body:JSON.stringify({student_id:studentId, updates})});
    document.getElementById('pfSaveMsg').textContent = '保存成功！';
    document.getElementById('pfSaveMsg').style.color = '#16a34a';
    document.getElementById('pfSaveMsg').style.display = 'block';
    // 重新拉取最新画像（Agent 校验后可能有变化）
    try {
      const loginResp = await api('/api/login', {method:'POST', body:JSON.stringify({student_id:studentId, password:'1'})});
      if (loginResp.success) { profileData = loginResp.profile; }
    } catch(e) {}
    updateSidebarUser(updates.name || '张三', chosenAvatarId);
  } catch(e) {
    document.getElementById('pfSaveMsg').textContent = '保存失败: ' + e.message;
    document.getElementById('pfSaveMsg').style.color = '#dc2626';
    document.getElementById('pfSaveMsg').style.display = 'block';
  }
}

async function deleteAccount() {
  if (!confirm('确定要注销账号吗？此操作不可恢复！')) return;
  try {
    await api('/api/account/'+studentId, {method:'DELETE'});
    alert('账号已注销');
    location.reload();
  } catch(e) { alert('注销失败: ' + (e.message||'请重试')); }
}

// ===== PPT 生成 =====
let pptState = { themes:[], chosenTheme:'auto', detailLevel:'standard', sid:null, polling:false };

async function loadThemes() {
  try {
    const data = await api('/api/zhiwen/themes');
    pptState.themes = data.themes || [];
    renderThemeGrid();
    if (!data.configured) {
      document.getElementById('pptHint').textContent = 'ℹ️ 智文服务未配置，模板为内置列表。需要 ZHIWEN_APP_ID + ZHIWEN_APP_SECRET 才能生成PPT。';
    }
  } catch(e) {
    pptState.themes = [];
    renderThemeGrid();
  }
}

function renderThemeGrid() {
  const grid = document.getElementById('pptThemeGrid');
  grid.innerHTML = pptState.themes.map(t =>
    '<div class="ppt-theme-card'+(pptState.chosenTheme===t.key?' sel':'')+'" onclick="selectTheme(\\''+t.key+'\\')">'+
    '<img class=\"tc-thumb\" src=\"'+t.thumbnail+'\" alt=\"'+t.name+'\" loading=\"lazy\" onerror=\"this.src=\\'data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 width=%22160%22 height=%22120%22><rect fill=%22%23e2e8f0%22 width=%22160%22 height=%22120%22/><text x=%2280%22 y=%2265%22 text-anchor=%22middle%22 fill=%22%2394a3b8%22 font-size=%2214%22>'+t.name+'</text></svg>\\'\">'+
    '<span class="tc-name">'+t.name+'</span></div>'
  ).join('');
}

function selectTheme(key) {
  pptState.chosenTheme = key;
  renderThemeGrid();
}

document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.ppt-count-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var level = this.getAttribute('data-level');
      pptState.detailLevel = level;
      document.querySelectorAll('.ppt-count-btn').forEach(function(b) { b.classList.remove('sel'); });
      this.classList.add('sel');
    });
  });
});

async function startPPT() {
  const query = document.getElementById('pptQuery').value.trim();
  if (!query) { alert('请输入PPT主题'); return; }

  const btn = document.getElementById('pptGenBtn');
  btn.disabled = true;
  btn.textContent = ' 正在创建任务...';
  document.getElementById('pptProgressWrap').style.display = 'block';
  document.getElementById('pptResult').style.display = 'none';
  document.getElementById('pptProgressFill').style.width = '5%';
  document.getElementById('pptProgressText').textContent = ' 正在创建PPT任务...';

  try {
    const data = await api('/api/zhiwen/ppt/create', {
      method:'POST',
      body:JSON.stringify({query:query, theme:pptState.chosenTheme, detail_level:pptState.detailLevel})
    });
    pptState.sid = data.sid;
    document.getElementById('pptProgressText').textContent = ' 任务已创建，正在生成大纲...';
    document.getElementById('pptProgressFill').style.width = '15%';
    pollProgress();
  } catch(e) {
    alert('创建PPT失败: ' + e.message);
    btn.disabled = false;
    btn.textContent = ' 开始生成 PPT';
    document.getElementById('pptProgressWrap').style.display = 'none';
  }
}

function pollProgress() {
  if (!pptState.sid) return;
  pptState.polling = true;

  api('/api/zhiwen/ppt/progress', {
    method:'POST',
    body:JSON.stringify({sid:pptState.sid})
  }).then(function(data) {
    if (!pptState.polling) return;
    var p = data.process || 0;
    var text;
    if (p < 30) text = ' 正在生成大纲... ('+p+'%)';
    else if (p < 70) text = ' 正在生成PPT内容... ('+p+'%)';
    else if (p < 100) text = ' 正在导出PPT文件... ('+p+'%)';
    else text = ' PPT生成完成！';

    document.getElementById('pptProgressFill').style.width = Math.max(p, 5)+'%';
    document.getElementById('pptProgressText').textContent = text;

    if (p >= 100 && data.pptUrl) {
      document.getElementById('pptResult').style.display = 'block';
      document.getElementById('pptDownloadBtn').href = data.pptUrl;
      document.getElementById('pptGenBtn').disabled = false;
      document.getElementById('pptGenBtn').textContent = ' 重新生成 PPT';
      pptState.polling = false;
    } else if (data.errMsg) {
      document.getElementById('pptProgressText').textContent = ' 生成失败: ' + data.errMsg;
      document.getElementById('pptGenBtn').disabled = false;
      document.getElementById('pptGenBtn').textContent = ' 重试';
      pptState.polling = false;
    } else {
      setTimeout(pollProgress, 3000);
    }
  }).catch(function(e) {
    if (pptState.polling) setTimeout(pollProgress, 3000);
  });
}

function resetPPT() {
  pptState.sid = null;
  pptState.polling = false;
  document.getElementById('pptProgressWrap').style.display = 'none';
  document.getElementById('pptResult').style.display = 'none';
  document.getElementById('pptGenBtn').disabled = false;
  document.getElementById('pptGenBtn').textContent = ' 开始生成 PPT';
}

// ===== 课程文档生成 =====
let docState = { difficulty:'intermediate', detailLevel:'standard', currentDoc:null };

document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('#docDiffRow .ppt-count-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
      docState.difficulty = this.getAttribute('data-level');
      document.querySelectorAll('#docDiffRow .ppt-count-btn').forEach(function(b) { b.classList.remove('sel'); });
      this.classList.add('sel');
    });
  });
  document.querySelectorAll('#docDetailRow .ppt-count-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
      docState.detailLevel = this.getAttribute('data-level');
      document.querySelectorAll('#docDetailRow .ppt-count-btn').forEach(function(b) { b.classList.remove('sel'); });
      this.classList.add('sel');
    });
  });
});

async function startDocGen() {
  var topic = document.getElementById('docTopic').value.trim();
  if (!topic) { alert('请输入课程主题'); return; }

  var btn = document.getElementById('docGenBtn');
  btn.disabled = true;
  btn.textContent = ' AI 正在生成文档...';
  document.getElementById('docProgressWrap').style.display = 'block';
  document.getElementById('docResult').style.display = 'none';

  try {
    var data = await api('/api/document/generate', {
      method:'POST',
      body:JSON.stringify({
        student_id:studentId,
        topic:topic,
        difficulty:docState.difficulty,
        detail_level:docState.detailLevel,
        course_name:'人工智能'
      })
    });
    docState.currentDoc = data;
    renderDocument(data);
    document.getElementById('docProgressWrap').style.display = 'none';
    document.getElementById('docResult').style.display = 'block';
    btn.textContent = ' 重新生成文档';
    btn.disabled = false;
  } catch(e) {
    alert('生成文档失败: ' + (e.message||'请重试'));
    document.getElementById('docProgressWrap').style.display = 'none';
    btn.textContent = ' 生成课程文档';
    btn.disabled = false;
  }
}

function renderDocument(doc) {
  document.getElementById('docResultTitle').textContent = doc.title;
  var md = '# ' + doc.title + '\\n\\n';
  md += '> **难度**: ' + (doc.difficulty_label||'进阶') + ' | **课程**: ' + (doc.course_name||'人工智能') + ' | **生成时间**: ' + (doc.created_at||'') + '\\n\\n';
  if (doc.key_concepts && doc.key_concepts.length) {
    md += '## 核心概念\\n\\n';
    doc.key_concepts.forEach(function(c) { md += '- **' + c + '**\\n'; });
    md += '\\n';
  }
  if (doc.prerequisites && doc.prerequisites.length) {
    md += '## 预备知识\\n\\n';
    doc.prerequisites.forEach(function(p) { md += '- ' + p + '\\n'; });
    md += '\\n';
  }
  if (doc.sections && doc.sections.length) {
    doc.sections.forEach(function(sec) {
      var prefix = sec.level === 1 ? '## ' : '### ';
      md += prefix + sec.title + '\\n\\n' + sec.content + '\\n\\n';
    });
  }
  if (doc.summary) { md += '## 总结\\n\\n' + doc.summary + '\\n\\n'; }
  if (doc.references && doc.references.length) {
    md += '## 参考资料\\n\\n';
    doc.references.forEach(function(r, i) { md += (i+1) + '. ' + r + '\\n'; });
  }
  var html = marked.parse(md, _getMarkedOpts());
  document.getElementById('docContent').innerHTML = html;
}

function copyDocument() {
  var text = document.getElementById('docContent').innerText;
  navigator.clipboard.writeText(text).then(function() {
    showToast('已复制到剪贴板');
  }).catch(function() { showToast('复制失败，请手动选择'); });
}

function downloadDocument() {
  var text = document.getElementById('docContent').innerText;
  var blob = new Blob([text], {type:'text/markdown'});
  var url = URL.createObjectURL(blob);
  var a = document.createElement('a');
  a.href = url;
  a.download = (docState.currentDoc ? docState.currentDoc.title : 'document') + '.md';
  a.click();
  URL.revokeObjectURL(url);
}

function resetDocument() {
  docState.currentDoc = null;
  document.getElementById('docResult').style.display = 'none';
}

// ===== 知识库搜索 =====
let kbState = { typeFilter:'all', docId:'', includeArxiv:false, docsLoaded:false };

async function loadKBDocs() {
  if (kbState.docsLoaded) return;
  try {
    const data = await api('/api/knowledge/documents');
    const select = document.getElementById('kbDocFilter');
    select.innerHTML = '<option value="">全部教材</option>';
    (data.documents||[]).forEach(d => {
      select.innerHTML += '<option value="'+d.id+'">'+d.title+'</option>';
    });
    kbState.docsLoaded = true;
  } catch(e) { console.log('加载教材列表失败:', e); }
}

function onKBDocChange() {
  kbState.docId = document.getElementById('kbDocFilter').value;
  if (document.getElementById('kbInput').value.trim()) searchKB();
}

async function searchKB() {
  const q = document.getElementById('kbInput').value.trim();
  if (!q) { loadKBStats(); return; }
  document.getElementById('kbResults').innerHTML = '<div style=\"text-align:center;padding:40px;color:var(--c-text-secondary);\">搜索中...</div>';

  try {
    const data = await api('/api/knowledge/search', {
      method:'POST',
      body:JSON.stringify({query:q, type_filter:kbState.typeFilter, doc_id:kbState.docId, include_arxiv:kbState.includeArxiv})
    });
    renderKBResults(data);
  } catch(e) {
    document.getElementById('kbResults').innerHTML = '<div style=\"text-align:center;padding:40px;color:var(--c-danger);\">搜索失败: '+e.message+'</div>';
  }
}

function setKBFilter(type) {
  kbState.typeFilter = type;
  document.querySelectorAll('.kb-filter-btn').forEach(b => b.classList.remove('sel'));
  document.querySelector('.kb-filter-btn[data-type=\"'+type+'\"]').classList.add('sel');
  if (document.getElementById('kbInput').value.trim()) searchKB();
}

function renderKBResults(data) {
  const local = data.local || {};
  const arxiv = data.arxiv || [];
  const results = local.results || [];
  let html = '';

  if (results.length === 0 && arxiv.length === 0) {
    html = '<div style=\"text-align:center;padding:40px;color:var(--c-text-secondary);\">未找到相关结果，请尝试其他关键词。</div>';
  }

  // 本地结果
  results.forEach(r => {
    const typeLabel = {'concept':'概念','pdf':'教材','textbook':'教材','paper':'论文'}[r.type]||r.type||'其他';
    html += '<div class=\"kb-result-card\">'+
      '<div class=\"kb-result-title\">'+r.title+'</div>'+
      (r.chapter && r.chapter_title ? '<div class=\"kb-result-breadcrumb\">第'+r.chapter+'章 '+r.chapter_title+(r.section?' > '+r.section:'')+'</div>' : '')+
      '<div class=\"kb-result-meta\">'+
        '<span class=\"kb-result-badge\">'+typeLabel+'</span>'+
        (r.difficulty?'<span class=\"kb-result-badge\">'+r.difficulty+'</span>':'')+
        (r.page?'<span style=\"font-size:11px;\">第'+r.page+'页</span>':'')+
        (r.score?'<span style=\"font-size:11px;\">匹配度: '+'&#9679;'.repeat(Math.min(5,r.score))+'</span>':'')+
      '</div>'+
      '<div class=\"kb-result-text\" id=\"kb-text-'+r.id+'\">'+r.text.substring(0,200)+'...</div>'+
      '<div class=\"kb-result-actions\">'+
        '<button class=\"kb-action-btn\" onclick=\"toggleKBText(\\''+r.id+'\\')\">展开</button>'+
        '<button class=\"kb-action-btn primary\" onclick=\"exportKB(\\''+r.id+'\\',\\''+r.title.replace(/'/g,\"\\\\'\")+'\\')\">下载 docx</button>'+
      '</div></div>';
  });

  // arXiv 结果
  arxiv.forEach(p => {
    html += '<div class=\"kb-result-card\">'+
      '<div class=\"kb-result-title\">'+p.title+'</div>'+
      '<div class=\"kb-result-meta\">'+
        '<span class=\"kb-result-badge\">arXiv</span>'+
        '<span style=\"font-size:11px;\">'+(p.authors||[]).slice(0,3).join(', ')+'</span>'+
        (p.published?'<span style=\"font-size:11px;\">'+p.published+'</span>':'')+
      '</div>'+
      '<div class=\"kb-result-text\">'+(p.summary||'').substring(0,300)+'</div>'+
      '<div class=\"kb-result-actions\">'+
        (p.pdf_url?'<a class=\"kb-action-btn\" href=\"'+p.pdf_url+'\" target=\"_blank\">下载 PDF</a>':'')+
        '<button class=\"kb-action-btn primary\" onclick=\"exportArxiv(\\''+p.id+'\\',\\''+(p.title||'').replace(/'/g,\"\\\\'\")+'\\',\\''+(p.summary||'').replace(/'/g,\"\\\\'\")+'\\',\\''+(p.authors||[]).join(', ').replace(/'/g,\"\\\\'\")+'\\',\\''+(p.published||'').replace(/'/g,\"\\\\'\")+'\\')\">下载 docx</button>'+
      '</div></div>';
  });

  document.getElementById('kbResults').innerHTML = html;
}

function toggleKBText(id) {
  const el = document.getElementById('kb-text-'+id);
  if (!el) return;
  el.classList.toggle('expanded');
  const btn = el.nextElementSibling.querySelector('.kb-action-btn');
  if (btn) btn.textContent = el.classList.contains('expanded') ? '收起' : '展开';
}

async function exportKB(id, title) {
  const card = document.getElementById('kb-text-'+id);
  if (!card) return;
  const full = card.closest('.kb-result-card');
  const text = card.textContent || '';
  try {
    const data = await api('/api/knowledge/export', {
      method:'POST',
      body:JSON.stringify({entry_id:id, title:title, text:text, full_text:text, source:'知识库'})
    });
    alert('已导出到: '+data.filepath);
  } catch(e) { alert('导出失败: '+e.message); }
}

async function exportArxiv(id, title, summary, authors, published) {
  try {
    const data = await api('/api/knowledge/export', {
      method:'POST',
      body:JSON.stringify({
        entry_id:'arxiv_'+id, title:title, text:summary, full_text:summary,
        source:'arXiv', authors:authors?authors.split(', '):[], published:published
      })
    });
    alert('已导出到: '+data.filepath);
  } catch(e) { alert('导出失败: '+e.message); }
}

async function loadKBStats() {
  try {
    const data = await api('/api/knowledge/stats');
    const types = data.types || {};
    const typeStr = Object.entries(types).map(([k,v]) => k+':'+v).join(', ');
    document.getElementById('kbStats').textContent = '已索引: '+data.documents+'个文档, '+data.chunks+'个分块 ('+typeStr+')';
    document.getElementById('kbEmpty').style.display = data.documents > 0 ? 'none' : 'block';
  } catch(e) {}
}

// ===== 跳过登录直接进入主界面 =====
studentId = 'stu_001';
(function initApp() {
  api('/api/profile/stu_001').then(function(d) {
    profileData = d;
    enterApp(d);
  }).catch(function(e) {
    console.error('初始化失败:', e);
    document.body.innerHTML = '<div style=\"padding:40px;text-align:center;font-family:sans-serif;\"><h2 style=\"color:#dc2626;\">⚠ 初始化失败</h2><p>'+e.message+'</p><p style=\"color:#64748b;\">请确认后端服务正常运行</p></div>';
  });
})();

// ===== Python 技能树 · 全屏覆盖层 =====
let stData = null, stView = 'chapters';

function stToggle() {
  document.getElementById('skillTreeOverlay').style.display = 'block';
  document.body.style.overflow = 'hidden';
  if (!stData) stLoad();
  else stRenderChapters();
}

function stClose() {
  document.getElementById('skillTreeOverlay').style.display = 'none';
  document.body.style.overflow = '';
}

async function stLoad() {
  var el = document.getElementById('stChapterList');
  var dbg = document.getElementById('stDebug');
  el.innerHTML = '<p style=\"text-align:center;padding:40px;color:#64748b;\">加载中...</p>';
  dbg.style.display = 'block';
  dbg.innerHTML = '加载技能树数据...';
  try {
    stData = await api('/api/skill-tree?student_id=' + studentId);
    stRenderChapters();
    dbg.style.display = 'none';
  } catch(e) {
    dbg.innerHTML = '<span style=\"color:#dc2626;\">加载失败: ' + e.message + '</span>';
    el.innerHTML = '<p style=\"text-align:center;padding:40px;color:#dc2626;\">加载失败，请重试</p>';
  }
}

function stRenderChapters() {
  var container = document.getElementById('skillTreeContent');
  stView = 'chapters';
  if (!stData) return;

  var html = '<div id=\"stChaptersWrap\" style=\"position:relative;max-width:700px;margin:0 auto;padding:20px 0;\">';

  stData.chapters.forEach(function(ch) {
    var cls = 'locked', statusTxt = '锁定', sc = '#94a3b8', pc = '#94a3b8';
    if (ch.unlocked && ch.progress === 0) { cls = 'unlocked'; statusTxt = '已解锁'; sc = '#64748b'; pc = '#94a3b8'; }
    if (ch.unlocked && ch.progress > 0 && ch.progress < 100) { cls = 'active'; statusTxt = '进行中'; sc = '#2563eb'; pc = '#2563eb'; }
    if (ch.progress >= 100) { cls = 'done'; statusTxt = '已完成'; sc = '#16a34a'; pc = '#16a34a'; }

    var gradient = ch.id === 1 ? '#16a34a,#22c55e' : ch.id === 2 ? '#2563eb,#60a5fa' : '#64748b,#94a3b8';
    if (ch.progress >= 100) gradient = '#16a34a,#22c55e';

    html += '<div class=\"st-node-card ' + cls + ' st-node-left\" id=\"stCh' + ch.id + '\" style=\"margin-bottom:100px;position:relative;z-index:1;\"';
    if (ch.unlocked) html += ' onclick=\"stOpenChapter(' + ch.id + ')\"';
    html += '>';
    html += '<div style=\"display:flex;align-items:center;gap:14px;\">';
    html += '<div class=\"st-node-icon\" style=\"background:linear-gradient(135deg,' + gradient + ');\">';
    html += '<svg width=\"20\" height=\"20\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"#fff\" stroke-width=\"2\"><circle cx=\"12\" cy=\"12\" r=\"10\"/><path d=\"M12 6v6l4 2\"/></svg></div>';
    html += '<div class=\"st-node-info\">';
    html += '<div style=\"display:flex;align-items:center;gap:8px;\"><span class=\"st-node-title\">第' + ch.id + '章：' + ch.name_cn + '</span><span style=\"font-size:13px;color:#64748b;\">' + ch.name_en + '</span></div>';
    html += '<div class=\"st-node-levels\">' + ch.nodes.map(function(n){return n.title;}).join(' · ') + '</div></div>';
    html += '<div class=\"st-node-score\"><div style=\"font-size:22px;font-weight:800;color:' + sc + ';\">' + ch.progress + '<span style=\"font-size:13px;\">%</span></div>';
    html += '<div style=\"font-size:11px;color:' + sc + ';\">第' + ch.id + '章 · ' + statusTxt + '</div></div>';
    html += '</div></div>';
  });
  html += '</div>';
  document.getElementById('stChapterList').innerHTML = html;

  // 动态绘制连线
  setTimeout(function() { stDrawChapterLines(); }, 50);
}

function stDrawChapterLines() {
  var svg = document.getElementById('stChapterLines');
  if (!svg) {
    svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('id', 'stChapterLines');
    svg.setAttribute('class', 'st-lines-layer');
    var wrap = document.getElementById('stChaptersWrap');
    if (wrap) wrap.insertBefore(svg, wrap.firstChild);
  }
  svg.setAttribute('width', '100%');
  svg.setAttribute('height', '100%');

  var html = '';
  for (var i = 1; i < stData.chapters.length; i++) {
    var prevCard = document.getElementById('stCh' + i);
    var nextCard = document.getElementById('stCh' + (i + 1));
    if (!prevCard || !nextCard) continue;

    var prevRect = prevCard.getBoundingClientRect();
    var nextRect = nextCard.getBoundingClientRect();
    var wrapRect = document.getElementById('stChaptersWrap').getBoundingClientRect();

    var x1 = prevRect.left + prevRect.width / 2 - wrapRect.left;
    var y1 = prevRect.bottom - wrapRect.top;
    var x2 = nextRect.left + nextRect.width / 2 - wrapRect.left;
    var y2 = nextRect.top - wrapRect.top;
    var color = stData.chapters[i-1].progress >= 70 ? '#16a34a' : '#cbd5e1';

    html += '<line x1=\"' + x1 + '\" y1=\"' + y1 + '\" x2=\"' + x2 + '\" y2=\"' + y2 + '\" stroke=\"' + color + '\" stroke-width=\"2.5\" stroke-linecap=\"round\"/>';
  }
  svg.innerHTML = html;
}

async function stOpenChapter(chapterId) {
  var ch = stData.chapters.find(function(c){return c.id === chapterId;});
  if (!ch || !ch.unlocked) return;
  try {
    var detail = await api('/api/skill-tree/chapter/' + chapterId + '?student_id=' + studentId);
    stRenderDetail(detail);
  } catch(e) { alert('加载章节详情失败: ' + e.message); }
}

function stRenderDetail(detail) {
  var container = document.getElementById('skillTreeContent');
  stView = 'detail';
  var nc = detail.nodes.length;
  var html = '<div style=\"margin-bottom:16px;\"><button onclick=\"stRenderChapters()\" style=\"display:inline-flex;align-items:center;gap:6px;padding:8px 18px;background:#2563eb;color:#fff;border:none;border-radius:8px;font-size:13px;font-weight:600;cursor:pointer;transition:all 0.2s;box-shadow:0 2px 8px rgba(37,99,235,0.2);\"><svg width=\"16\" height=\"16\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.5\"><polyline points=\"15 18 9 12 15 6\"/></svg>返回技能树</button></div>';
  html += '<div id=\"stDetailWrap\" style=\"position:relative;max-width:700px;margin:0 auto;padding:20px 0;\">';
  html += '<h3 style=\"margin-bottom:4px;\">' + detail.name_cn + ' <span style=\"font-weight:400;color:#64748b;font-size:16px;\">' + detail.name_en + '</span></h3>';

  detail.nodes.forEach(function(node, idx) {
    var isR = idx % 2 !== 0;
    var cls = node.done ? 'done' : (node.status === 'in_progress' ? 'in-progress' : (detail.unlocked ? '' : 'locked'));
    var acls = isR ? 'st-node-right' : 'st-node-left';
    var mb = idx < nc - 1 ? 'margin-bottom:180px;' : '';

    html += '<div class=\"st-node-card ' + cls + ' ' + acls + '\" id=\"stNd' + idx + '\" style=\"' + mb + 'position:relative;z-index:1;\">';
    html += '<div style=\"display:flex;align-items:center;gap:14px;\">';
    html += '<div class=\"st-node-icon\" style=\"background:linear-gradient(135deg,' + node.gradient + ');\">';
    html += '<svg width=\"20\" height=\"20\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"#fff\" stroke-width=\"2\"><circle cx=\"12\" cy=\"12\" r=\"10\"/><path d=\"M12 6v6l4 2\"/></svg></div>';
    html += '<div class=\"st-node-info\"><div class=\"st-node-title\">' + node.title + '</div>';
    html += '<div class=\"st-node-levels\">' + node.exercise_count + ' 道练习题 · 已完成 ' + node.done_count + ' 题</div></div>';
    html += '<div class=\"st-node-score\"><div style=\"font-size:20px;font-weight:800;color:' + (node.done?'#16a34a':'#64748b') + ';\">' + node.progress_pct + '%</div></div>';
    html += '</div>';

    if (detail.unlocked && node.exercise_count > 0) {
      html += '<div style=\"margin-top:12px;padding-top:12px;border-top:1px solid #f1f5f9;\">';
      var stars = ['⭐','⭐⭐','⭐⭐⭐','⭐⭐⭐⭐','⭐⭐⭐⭐⭐'];
      node.exercises.forEach(function(ex, ei) {
        var done = ex.status === 'completed';
        var active = ex.status === 'in_progress';
        var btnStyle = done ? 'background:#f0fdf4;color:#16a34a;border:1px solid #16a34a;' :
                       active ? 'background:#eff6ff;color:#2563eb;border:1px solid #2563eb;' :
                       'background:#fff;color:#64748b;border:1px solid #e2e8f0;';
        html += '<button onclick=\"stStartExercise(' + detail.id + ',\\\'' + node.id + '\\\',' + ei + ')\" style=\"display:block;width:100%;padding:8px 12px;margin-bottom:6px;border-radius:8px;font-size:12px;cursor:pointer;text-align:left;transition:all 0.15s;' + btnStyle + '\">';
        html += '<span style=\"margin-right:6px;\">' + (done ? '✅' : active ? '⏳' : stars[Math.min(ei,4)]) + '</span>';
        html += '第' + (ei+1) + '题：' + (node.exercises[ei].title || '编程练习');
        html += done ? ' <span style=\"font-size:10px;\">(' + ex.score + '/5分)</span>' : '';
        html += '</button>';
      });
      html += '</div>';
    }
    html += '</div>';
  });
  html += '</div>';
  document.getElementById('stChapterList').innerHTML = html;

  setTimeout(function() { stDrawDetailLines(); }, 50);
}

function stDrawDetailLines() {
  var svg = document.getElementById('stDetailLines');
  var wrap = document.getElementById('stDetailWrap');
  if (!wrap) return;
  if (!svg) {
    svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('id', 'stDetailLines');
    svg.setAttribute('class', 'st-lines-layer');
    wrap.insertBefore(svg, wrap.firstChild);
  }
  svg.setAttribute('width', '100%');
  svg.setAttribute('height', '100%');

  var wrapRect = wrap.getBoundingClientRect();
  var html = '';
  var nodes = document.querySelectorAll('#stDetailWrap .st-node-card');
  for (var i = 0; i < nodes.length - 1; i++) {
    var cur = nodes[i], nxt = nodes[i+1];
    var cr = cur.getBoundingClientRect(), nr = nxt.getBoundingClientRect();
    var x1 = cr.left + cr.width / 2 - wrapRect.left;
    var y1 = cr.bottom - wrapRect.top;
    var x2 = nr.left + nr.width / 2 - wrapRect.left;
    var y2 = nr.top - wrapRect.top;
    var color = '#cbd5e1';
    html += '<line x1=\"' + x1 + '\" y1=\"' + y1 + '\" x2=\"' + x2 + '\" y2=\"' + y2 + '\" stroke=\"' + color + '\" stroke-width=\"2\" stroke-linecap=\"round\"/>';
  }
  svg.innerHTML = html;
}

var stExState = null; // {chapterId, nodeId, exerciseData}

async function stStartExercise(chapterId, nodeId, exIndex) {
  var overlay = document.getElementById('stExerciseOverlay');
  var panel = document.getElementById('stExercisePanel');
  overlay.style.display = 'flex';
  panel.innerHTML = '<div style=\"padding:40px;text-align:center;color:#64748b;\">加载题目...</div>';

  try {
    var data = await api('/api/skill-tree/exercise/generate', {
      method:'POST',
      body:JSON.stringify({student_id:studentId, chapter_id:chapterId, node_id:nodeId, level:'l3', exercise_index:exIndex || 0})
    });
    stExState = {chapterId:chapterId, nodeId:nodeId, exIndex:exIndex || 0, exercise:data.exercise};
    stRenderExercise();
  } catch(e) {
    panel.innerHTML = '<div style=\"padding:40px;text-align:center;color:#dc2626;\">生成失败: ' + e.message + '</div>';
  }
}

function stCloseExercise() {
  document.getElementById('stExerciseOverlay').style.display = 'none';
  stExState = null;
}

function stRenderExercise() {
  var s = stExState;
  if (!s) return;
  var ex = s.exercise;
  var panel = document.getElementById('stExercisePanel');

  var html = '<div style=\"padding:28px 32px;\">';
  html += '<div style=\"display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;\">';
  html += '<div><span style=\"font-size:12px;color:#64748b;font-weight:600;\">代码实战</span>';
  html += '<h3 style=\"margin:4px 0 0;font-size:20px;\">' + (ex.title || '编程练习') + '</h3></div>';
  html += '<button onclick=\"stCloseExercise()\" style=\"width:34px;height:34px;border-radius:50%;border:2px solid #e2e8f0;background:#fff;font-size:18px;cursor:pointer;color:#94a3b8;\">✕</button></div>';

  html += '<div style=\"margin-bottom:16px;padding:16px;background:#f8fafc;border-radius:10px;\">';
  html += '<div style=\"font-weight:700;font-size:15px;margin-bottom:8px;\">题目描述</div>';
  html += '<div style=\"font-size:14px;color:#334155;line-height:1.6;white-space:pre-wrap;\">' + (ex.description || '') + '</div>';
  if (ex.example_input) html += '<div style=\"margin-top:10px;font-size:13px;color:#64748b;\"><b>示例输入：</b><code>' + ex.example_input + '</code></div>';
  if (ex.example_output) html += '<div style=\"font-size:13px;color:#64748b;\"><b>示例输出：</b><code>' + ex.example_output + '</code></div>';
  html += '</div>';

  html += '<div style=\"margin-bottom:16px;\"><div style=\"font-weight:700;font-size:14px;margin-bottom:6px;\">你的代码</div>';
  html += '<textarea id=\"stCodeInput\" style=\"width:100%;height:220px;border:2px solid #e2e8f0;border-radius:10px;padding:14px;font-family:Consolas,monospace;font-size:14px;outline:none;resize:none;box-sizing:border-box;background:#1e293b;color:#e2e8f0;line-height:1.6;\" placeholder=\"# 在这里编写你的 Python 代码...\"></textarea></div>';
  html += '<button onclick=\"stSubmitExercise()\" style=\"width:100%;padding:14px;background:linear-gradient(135deg,#2563eb,#1d4ed8);color:#fff;border:none;border-radius:10px;font-size:15px;font-weight:600;cursor:pointer;\">提交代码</button>';

  html += '</div>';
  panel.innerHTML = html;
}

function stSubmitExercise() {
  var code = document.getElementById('stCodeInput').value;
  if (!code.trim()) { alert('请先编写代码'); return; }
  stDoSubmit(code);
}

async function stDoSubmit(userAnswer) {
  if (!userAnswer) { alert('请先完成答题'); return; }
  var panel = document.getElementById('stExercisePanel');
  panel.innerHTML = '<div style=\"padding:40px;text-align:center;color:#64748b;\">AI 评判中...</div>';

  try {
    var s = stExState;
    var result = await api('/api/skill-tree/exercise/submit', {
      method:'POST',
      body:JSON.stringify({student_id:studentId, chapter_id:s.chapterId, node_id:s.nodeId, level:'l3', user_answer:userAnswer, exercise_data:s.exercise, exercise_index:s.exIndex || 0})
    });

    var correct = result.correct;
    var html = '<div style=\"padding:28px 32px;text-align:center;\">';
    html += '<div style=\"font-size:64px;\">' + (correct ? '✅' : '❌') + '</div>';
    html += '<div style=\"font-size:22px;font-weight:800;color:' + (correct ? '#16a34a' : '#dc2626') + ';margin:12px 0;\">' + (correct ? '回答正确！' : '还有改进空间') + '</div>';
    html += '<div style=\"font-size:14px;color:#64748b;margin-bottom:8px;\">评分: ' + (result.score || 0) + ' / 5</div>';
    html += '<div style=\"font-size:14px;color:#334155;max-width:500px;margin:0 auto 20px;line-height:1.6;text-align:left;background:#f8fafc;padding:16px;border-radius:10px;white-space:pre-wrap;\">' + (result.feedback || '') + '</div>';
    html += '<button onclick=\"stAfterSubmit()\" style=\"padding:12px 32px;background:linear-gradient(135deg,#2563eb,#1d4ed8);color:#fff;border:none;border-radius:10px;font-size:14px;font-weight:600;cursor:pointer;\">继续学习</button>';
    html += '</div>';
    panel.innerHTML = html;
    stData = await api('/api/skill-tree?student_id=' + studentId);
  } catch(e) {
    panel.innerHTML = '<div style=\"padding:40px;text-align:center;color:#dc2626;\">提交失败: ' + e.message + '<br><button onclick=\"stCloseExercise()\" style=\"margin-top:12px;padding:8px 24px;background:#2563eb;color:#fff;border:none;border-radius:8px;cursor:pointer;\">关闭</button></div>';
  }
}

function stAfterSubmit() {
  stCloseExercise();
  var s = stExState;
  if (s && stView === 'detail') {
    stOpenChapter(s.chapterId);
  } else {
    stRenderChapters();
  }
}

// ===== 页面级错误处理 =====
window.addEventListener('error', function(e) {
  var msg = document.getElementById('loginMsg');
  if (msg && e.target && e.target.tagName === 'SCRIPT') msg.textContent = '页面脚本错误: ' + e.message;
});

</script>
</body>
</html>
'''


def load_home_page_html() -> str:
    return HOME_PAGE_HTML
