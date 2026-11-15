# 本地测试用的小服务器（支持音频/视频的断点请求）。用法：在仓库根目录运行 python3 tools/devserver.py，然后打开 http://localhost:8765/index.html
import http.server, os, re, sys
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
    def send_head(self):
        rng=self.headers.get('Range'); path=self.translate_path(self.path)
        if not rng or not os.path.isfile(path): return super().send_head()
        size=os.path.getsize(path); m=re.match(r'bytes=(\d*)-(\d*)',rng)
        a=int(m.group(1) or 0); b=int(m.group(2)) if m.group(2) else size-1; b=min(b,size-1)
        f=open(path,'rb'); f.seek(a)
        self.send_response(206); self.send_header('Content-Type',self.guess_type(path)); self.send_header('Accept-Ranges','bytes')
        self.send_header('Content-Range','bytes %d-%d/%d'%(a,b,size)); self.send_header('Content-Length',str(b-a+1)); self.end_headers()
        self._remain=b-a+1; return f
    def copyfile(self,src,dst):
        n=getattr(self,'_remain',None)
        if n is None: return super().copyfile(src,dst)
        dst.write(src.read(n))
http.server.ThreadingHTTPServer(('',8765),H).serve_forever()
