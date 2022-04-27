from posixpath import split
import socket
import threading

def exist_compte(ref):
        text=str(ref)
        text=text[2:-1]
        print(text)
        f=open("comptes.txt","r")
        l=f.readlines()
        exist=False
        for line in l:
            L=list(line.split("."))
            if (text==L[0]):
                exist=True
        return(exist)

class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):

        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port, ))

    def run(self): 
   
        print("Connexion de %s %s" % (self.ip, self.port, ))

        r = self.clientsocket.recv(2048)
        print("client de reference", r, "est connecte")
        print(r[:4])
        print(r[4:])
        if (r[:4]==b"auth"):
            res=exist_compte(r[4:])
            print(res)
            if(res):
                self.clientsocket.send(b"exist")
                
            else:
                self.clientsocket.send(b"not exist")

        elif (r[:5]==b"depot"):
            text=str(r)
            print(r)
            text=text[2:-1]
            text=text.split(',')
            print(text)
            string=text[0]+text[1]+text[2]
            print(string)
            self.clientsocket.send(string.encode())

        elif (r[:6]==b"retrait"):
            r=r.split(',')
            self.clientsocket.send(r[0]+r[1]+r[2])
            
        print("Client déconnecté...")


        

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind(("",1111))

while True:
    tcpsock.listen(10)
    print( "En écoute...")
    (clientsocket, (ip, port)) = tcpsock.accept()
    newthread = ClientThread(ip, port, clientsocket)
    newthread.start()