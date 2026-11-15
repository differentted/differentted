# 库洛米打卡乐园 · 交接说明（给接手的 Claude Code）

> 这份文件会被 Claude Code 自动读取。接手前请从头到尾读一遍，**不要再让家长重复讲**。
> 最后更新：2026-11-15（由之前的云端 Claude 会话整理）

---

## 一、先读这里：和家长合作的规矩（非常重要）

1. **所有回复只用中文。** 家长看不懂英文，多次因为收到英文而生气。代码注释也写中文。
2. **不要一件件问，直接做完。** 家长原话：「你就把这个事情全部做到小孩可以直接使用就行了，不要一个个问我」。能自己判断的就自己决定，做完再汇报。
3. **做完就上线**：改完→测试→提交→推送到 GitHub 的 `main` 分支（见第四节），孩子刷新网页就能用。
4. **说不能做之前先想办法。** 家长原话：「你所有说没有办法做到的，你自己去解决…只要是免费的，你就去给我做到」。确实做不到（比如需要家长本人登录的账号）要说清楚原因，并给出替代方案。
5. 汇报要具体：改了什么、在哪里能看到、怎么用、测试结果如何。不要只说"已完成"。
6. 家长是非程序员，给操作步骤时要一步步写清楚（点哪里、按哪个按钮）。
7. 孩子的真实数据在云端，**测试时绝不能改到真实数据**（见第六节）。

---

## 二、这是什么

给家里小朋友用的**打卡 + 学习 + 养电子宠物**网页（单页应用），主要用户是茜茜（账号名 xixi）。
线上网址：**https://differentted.github.io/differentted/**
孩子用 iPad、手机、**科大讯飞学习机**（安卓，浏览器能力弱：没有语音合成、AudioContext 会抢声道）打开。

家里人：茜茜（主要用户）、其他小朋友账号（嫣嫣 yanyan 等），家长（妈妈）。家长在澳洲悉尼（时区 Australia/Sydney）。

---

## 三、文件在哪里

### 1. 代码仓库
- GitHub：**`differentted/differentted`**（https://github.com/differentted/differentted）
- 家长电脑上装了 **GitHub Desktop**。本地文件夹一般在：
  - Windows：`文档\GitHub\differentted`
  - 苹果电脑：`~/Documents/GitHub/differentted`
  - 如果还没有：打开 GitHub Desktop → File → Clone repository → 选 `differentted/differentted` → Clone。
- **开工前先拉最新代码**（GitHub Desktop 点 "Fetch origin / Pull"，或 `git pull origin main`），因为之前一直是云端 Claude 在改。

### 2. 主要文件
| 文件/文件夹 | 是什么 |
|---|---|
| `index.html` | **整个网页就这一个文件**（约 3MB、5 万行，HTML+CSS+JS 全在里面） |
| `gh_deploy.html` | `index.html` 的完全一样的副本。**每次改完都要 `cp index.html gh_deploy.html`** |
| `pets/` | 2026-11 新增的 11 只宠物的全部图片（`pet_<种类>_<用途>.webp`） |
| 根目录 `*.webp / *.mp4 / *.mp3` | 老宠物（小金麟 xiaojinlin、毛绒小奶龙 naolong、小金龙 xiaojinlong、双鱼宝宝 shuangyu）的图片/蛋动画/跳舞音乐、背景音乐、报数音频 `count_sprite.mp3` |
| `hanzi/` | 汉字笔顺：hanzi-writer 3.7.3（MIT）+ 每个字的笔画数据 `hanzi/data/<字>.json`（Arphic 授权，见 `ARPHICPL.TXT`）|
| `lib/three.min.js` | 3D 小屋用的 Three.js r149（MIT）|
| `tools/` | 开发小工具：`devserver.py`（本地服务器）、`check_syntax.py`（语法检查）、`test_template.js`（浏览器测试模板）|

---

## 四、怎么改代码、怎么上线（之前一直这样做）

### 改代码的习惯
- 新功能一般写成一整段独立代码，**插在 `index.html` 里这行注释的前面**：
  `/* 2026-11新增：英语单词/句子按《新概念英语》第一册课文顺序编排`
  （用 Python 做"精确字符串替换"插入，替换前先确认目标字符串只出现一次。）
- 要改老功能，常用**包装函数**的方式覆盖，不动原来的代码：
  ```js
  var _旧=某函数; 某函数=function(){ var r=_旧.apply(this,arguments); /* 加新逻辑 */ return r; };
  ```
  后定义的会覆盖前面的，所以新代码要放在被包装函数的后面。
- 每段新代码开头写一段中文注释：为什么做、规则是什么（家长看得懂的那种）。

### 每次改完必须做
1. `python3 tools/check_syntax.py`：语法检查，必须通过。
2. 本地打开测试：`python3 tools/devserver.py`，浏览器打开 `http://localhost:8765/index.html`。要自动测试就参照 `tools/test_template.js` 用 Playwright，**记得拦截云端请求**。
3. `cp index.html gh_deploy.html`
4. 提交并推送到 `main`：
   ```bash
   git add -A
   git commit -m "中文写清楚改了什么"
   git push origin main
   ```
   （之前云端会话是先推到分支 `claude/webpage-voice-content-optimization-cy7h0j`，再快进合并到 `main`。本地直接推 `main` 就行，推之前先 `git pull` 避免冲突。）
5. 网站由 **GitHub Pages** 从 `main` 分支自动发布，约 1～2 分钟后生效。打开线上网址强制刷新确认（电脑 Ctrl+F5 / Cmd+Shift+R，平板下拉刷新）。

---

## 五、整体结构（找代码时用）

- 数据：`store`（整个家庭的存档，localStorage 键 `kuroCheckinV3`）→ `store.accounts[孩子id].state`。代码里的 `state` = 当前孩子。`state.day` = 当天数据，跨天自动重置。
- 保存：`saveStore()`（存本机 + 上传云端），`saveStoreLocalOnly()`（只存本机，后台频繁保存用这个）。
- 页面切换：`showPage('home'|'pet'|'shop'|'bag'|'board'|'wheel'|'visit'|'profile'|…)`；底部导航在 `<nav class="tabbar">`。
- 金币：`state.moneyBalance`，加金币 `earnCoins(n,'原因')`，扣/加用 `addCoinChange(±n,'原因')`。
- 弹窗：`showModal(id)` / `hideModal(id)`；3D 全屏时弹窗要把 zIndex 设到 10050 以上。
- 小提示：`ttsToast(文字, 毫秒)`。
- 朗读：`studySpeak(文字, 'en-US'|'zh-CN')`；英音/美音女声设置在 `ttsAccent`。

### 主要功能模块（搜函数名能找到）
| 功能 | 关键函数/变量 |
|---|---|
| 打卡（运动/学习/家务…）、转盘、商店、背包、心愿挑战 | 原有代码 |
| 学习内容：新概念英语第一册单词/句子、人教版汉字（笔顺 `openStrokeModal`）、成语+成语考试 `cyExam`/`cySubmit`、阅读理解 `cnRenderReading`、数学应用题 `cnRenderMathWP`（含🏆精英班英文题 `MATH_ELITE`） | `renderStudyAids`、`dailyTheme` |
| 学完自测（考前复习页→正式考试，防作弊） | `startSelfTest`、`stRenderReview`、`stBeginExam`、`stFinish`、`state.selfTests`、`state.learnLog` |
| 背熟清单 + 妈妈考一考（考两次，每次给一半零花钱） | `rcToggle`、`rcOpenTest`、`rcTestFinish`、`state.recite` |
| 精灵图鉴（收集/孵蛋/进化/材料） | `crState`、`crAddEnergy`、`crSelfTestReward`、`CR_QUESTS`、`CR_STONES` |
| 宠物：选宠物 `openChoose`、宠物资料 `PET_LIBRARY` + 显示顺序 `PET_ORDER`、骨骼动画 `RIGS`/`rgPose`/`rgRender`、受伤效果 `lpDrawInjury`、多宠物互动 `companionSprites` | |
| 3D 小屋（Three.js）：`openHouse3D`、`h3Init`、`h3BuildHouse`、建造中心 `HOUSE_TIERS`/`hbState()`、昼夜 `h3IsNightNow`（7:00 天亮、18:00 天黑）、家里乱/拆家 `h3MessInfo`、草地/嫌脏不回家 `h3IsOutdoor`、嵌入宠物页 `h3SetEmbedded` | |
| 3D 照顾动作（吃饭/喝水/洗澡拟人动画） | `c3Start`、`c3Care`、`c3TickEat/Drink/Bath` |
| 3D 装修 DIY 商店（标配/高配/豪华） | `DIY_ITEMS`、`diyOpen`、`diyBuild` |
| 家庭小管家（宠物吵架闹脾气，孩子当家长处理；哄宠物要花时间或金币） | `FAM_EVENTS`、`famStart`、`famResolve`、`famCoax`、`FAM_ACC` |
| 防刷奖励 | `afEligible`/`AF_MAX_EFF`（自测）、`AF_READ_REWARD_MAX`（阅读）、`AF_QUIZ_COIN_MAX`（小测验）、⚖️宠物乐园大法官 `jdAdd`/`jdPunish` |
| 和「小小存钱银行」数据互通 | `bankRpc`、`bankPut`、`bankOpenLink`、`rcPayout`、`goBank`（底部「🐷存钱银行」按钮）|

---

## 六、云端数据（孩子的真实存档，小心！）

- 服务：Supabase，网址 `https://yngdnajnlilamqsxydnv.supabase.co`，表 `kuluomi_sync`，公开 key（publishable，网页里本来就有）`sb_publishable_IDyd8JeUSRRZ5FVNk9VK8g_5izNiYdC`。
- 每个家庭一行，`id` 例如 xixi 家：`fam_xixi_pqnr4c6b1k0z`；嫣嫣家：`fam_yanyan_9okngkti8flm`；另一个家庭 `6GtaRbPnAT56Qf3e`（里面账号叫「宝宝」，宠物小晖晖）。`data.accounts[...]` 里是每个孩子的 `state`。
- **只读查看可以**（排查问题时常用）：
  `curl "https://yngdnajnlilamqsxydnv.supabase.co/rest/v1/kuluomi_sync?id=eq.fam_xixi_pqnr4c6b1k0z&select=*" -H "apikey: <上面的key>"`
- **不要直接写云端**；测试时用 Playwright 拦截 `**/*supabase.co/**`（要用真实数据测，就先下载一份，在拦截里把 GET 返回这份数据、POST 一律假装成功）。
- 网页打开时会用云端存档覆盖本机，所以新加的存档字段要考虑「同一天本机和云端合并」（相关函数 `captureLocalDaySnapshotForMerge`、`mergeLearnAndCreatures`）。

### 小小存钱银行（另一个网页，另一个 AI 负责）
- 网址 https://mybaby-bank.netlify.app ，数据也在 Supabase：`https://zlhvmtivifzuvpwmlgyl.supabase.co`，key `sb_publishable_5QIGn5queV9tno67RoAowA_h-qoY6ap`，通过 RPC `pb_put / pb_get / pb_since` 读写，按「家庭暗号」区分家庭。
- 打卡乐园往那边写两种数据：
  - `klm/money/<编号>`：零花钱转账单，`{from:'kuromi',id,kid,kidName,date,at,type:'earn',amount,cur:'CNY',note,status:'pending'}`，存钱银行家长确认后改成 `ok` 或 `no`。
  - `klm/recite/<孩子id>`：背熟清单，`items[{type,en,cn,day,status:'checked'|'r1'|'pass',r1Day,testDay,lastFail,money}]`。
- 打卡乐园自己的「零花钱」页已经按家长要求**删掉**了，钱只在存钱银行管。
- 规则：**金币按打卡乐园的规则，星星按存钱银行的规则（看自觉）**，两边互不影响。背熟零花钱：单词共 1 毛，句子共 1～4 毛（按长短），当天考第 1 次、第二天考第 2 次，每次过关给一半。

---

## 七、已经定好的规则（家长确认过，别随便改）

- 3D 小屋：建好以后宠物页默认显示 3D（孩子可切回平面小窝，记在 `state.petView`）；家里「又乱又脏」或「拆家」时宠物不肯回家，在草地上，要先完成当天家务打卡再点「🧹打扫房子」。
- 自测防刷：每个词一天只给一次奖励（累计最多 5 天）；至少 4 道新内容才算有效自测，每天最多 3 次；其余为练习模式，不给奖励。
- 阅读/故事打卡：要先答下面的小题、读够时间（按字数，30 秒～2 分半），每种每天前 2 篇有奖励。小测验金币每天最多 20。随机掉落属性石每天最多 2 颗。
- ⚖️大法官：违规分 3 分警告、6 分最后警告、9 分回收当天学习奖励并冻结（家长密码可解除）。
- 家长密码：`store.parentPin`（4 位数字，家长第一次用时自己设置）。
- 家庭小管家：宠物越多越爱吵架；处理不好宠物生气；哄宠物要「陪伴（花时间）」或「买零食 5 金币 / 礼物 20 金币」。
- 已经刷到的奖励（xixi 在 11/15 一天孵了 27 只精灵）家长说**保留**，不要回收。

---

## 八、还没做完的事（接着做）

1. **11 只新宠物换成豆包画的图**（家长最在意）。
   - 现在这 11 只（`pets/pet_*`）的阶段图、动作图、蛋、跳舞动图，是程序用骨骼姿势加道具画出来的，家长觉得不够好，想用**豆包**重新画。
   - 计划：家长（或本地 Claude 操作电脑上的豆包）为每只宠物生成 2 张合集图：①「动作设定图」3×4 共 12 格（挥手/被摸头/吃饭/喝水/喝奶/出门玩/举哑铃/跳绳/洗澡/难过/跳舞/宠物蛋）；②「成长阶段图」宝宝/少年/成年三格。白底，存到桌面「新宠物图片」文件夹，文件名如「小火龙-动作.png」「小火龙-成长.png」。原图可从线上下载：`https://differentted.github.io/differentted/pets/pet_<种类>_happy.webp`。
   - 拿到图以后：按格子切开 → 去白背景 → 裁边、统一高度约 600px → 存成 `pets/pet_<种类>_<用途>.webp`，覆盖现有文件即可（文件名不变，`PET_LIBRARY` 不用改）。用途名：`baby teen adult touch food water milk out train train2 bath eggImg sad`；跳舞做成动图 `pet_<种类>_dance.webp`（约 280px 高、24 帧左右）。
   - 种类代号：`tu_bai` 蝴蝶结小白兔、`mao_ju` 橘子喵、`mao_fen` 粉裙喵公主、`long_caihong` 彩虹小火龙、`long_huo` 小火龙、`long_pang` 团子胖胖龙、`long_qing` 小青龙、`tu_chuier` 奶芙垂耳兔、`tu_fen` 眨眨兔、`lang_bao` 小狼宝宝、`long_leiting` 雷霆青龙。
   - **重要**：阶段图（baby/teen/adult）在 `RIGS` 里有对应的骨骼关节坐标（按图片宽高的 0～1 比例）。换图后宠物的位置和比例变了，要**重新标关节**（头 head、脖子 neck、骨盆 pelvis、手 arms、脚 legs、尾巴 tail），否则动作会变形。可以参考 `pet_<种类>_happy.webp` 那组的写法。坐着的宠物用 `legs:[], sit:1`。
   - 去背景工具：之前用的是 `pip install "rembg[cpu]"`，模型 `isnet-general-use`（从 GitHub release 下载），效果很好；卡通图偶尔用 `isnet-anime`，两个结果的透明通道取最大值合并。
2. 新宠物目前没有专属跳舞音乐，暂时共用 `naolong_dance.mp3`。

---

## 九、踩过的坑

- 科大讯飞学习机：不能用 AudioContext（会让整页没声音），没有语音合成；报数用普通 `<audio>` 播 `count_sprite.mp3`，跳到第 n-1 秒。
- 会动的 webp（`*_dance.webp`、`xiaojinlong_baby.webp`）不能画进 canvas（会定住），代码里用 `/_dance\.webp|xiaojinlong_baby\.webp/` 识别后直接用 `<img>` 播放。
- 3D 小屋在无显卡环境测试要加 `--use-gl=swiftshader --ignore-gpu-blocklist`，而且很慢，按时间判断的动画在截图里会"跳帧"。
- 动画频率别太高：之前生气/害怕时每秒抖几十下，被家长当成"原地抽搐"的 bug。
- `gh_deploy.html` 忘了同步，线上会出问题。
