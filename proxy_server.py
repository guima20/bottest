#!/usr/bin/env python3
"""
Servidor proxy simples para redirecionar tráfego HTTPS para nossa aplicação Flask
"""
import socket
import threading
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.proxy_request()
    
    def do_POST(self):
        self.proxy_request()
    
    def do_PUT(self):
        self.proxy_request()
    
    def do_DELETE(self):
        self.proxy_request()
    
    def do_HEAD(self):
        self.proxy_request()
    
    def do_OPTIONS(self):
        self.proxy_request()
    
    def proxy_request(self):
        try:
            # URL da aplicação Flask local
            target_url = f"http://localhost:8000{self.path}"
            
            # Headers da requisição original
            headers = {}
            for header, value in self.headers.items():
                if header.lower() not in ['host', 'connection']:
                    headers[header] = value
            
            # Dados do corpo da requisição (para POST/PUT)
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else None
            
            # Fazer a requisição para o Flask
            response = requests.request(
                method=self.command,
                url=target_url,
                headers=headers,
                data=body,
                allow_redirects=False
            )
            
            # Enviar resposta de volta
            self.send_response(response.status_code)
            
            # Copiar headers da resposta
            for header, value in response.headers.items():
                if header.lower() not in ['connection', 'transfer-encoding']:
                    self.send_header(header, value)
            
            # Headers adicionais para HTTPS e CORS
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
            
            self.end_headers()
            
            # Enviar conteúdo da resposta
            self.wfile.write(response.content)
            
        except Exception as e:
            print(f"Erro no proxy: {e}")
            self.send_error(500, f"Proxy Error: {str(e)}")

def start_proxy(port):
    server = HTTPServer(('0.0.0.0', port), ProxyHandler)
    print(f"🚀 Proxy server rodando na porta {port}")
    print(f"📡 Redirecionando para Flask na porta 8000")
    server.serve_forever()

if __name__ == '__main__':
    # Tentar diferentes portas
    for port in [12000, 12001, 9000, 9001, 8080, 8081]:
        try:
            start_proxy(port)
            break
        except OSError as e:
            if "Address already in use" in str(e):
                print(f"❌ Porta {port} em uso, tentando próxima...")
                continue
            else:
                raise e