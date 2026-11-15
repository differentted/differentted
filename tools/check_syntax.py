# 检查 index.html 里主脚本的语法（改完代码必须跑一次）。用法：python3 tools/check_syntax.py
# 原理：取出第一个 <script> 块存成临时 js，用 node --check 检查（第二个 <script> 块是嵌入的模板，不用管）
import re, subprocess, sys, tempfile, os
s=open(os.path.join(os.path.dirname(__file__),'..','index.html'),encoding='utf-8').read()
blk=re.findall(r'<script>(.*?)</script>',s,re.S)[0]
f=tempfile.NamedTemporaryFile('w',suffix='.js',delete=False,encoding='utf-8'); f.write(blk); f.close()
r=subprocess.run(['node','--check',f.name]); os.unlink(f.name)
print('语法检查通过' if r.returncode==0 else '语法有错，见上面'); sys.exit(r.returncode)
