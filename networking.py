import socket

try:
    import httplib
except:
    import http.client as httplib

# Checks if there is Internet connection
def have_internet():
    conn = httplib.HTTPConnection("www.google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False

# Gets a list of all IPs on local network
def get_L1():
    global L1
    L1 = []
    for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
        if not ip.startswith("127."):
            L1.append(ip)

# Checks for new and gone IPs and returns them
def check_for_new():
    global L1
    L2 = []
    new = []
    gone = []
    for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
        if not ip.startswith("127."):
            L2.append(ip)

    difference = set(L1).symmetric_difference(set(L2))
    i = 0
    for item in difference:
        if difference[i] in L2:
            new.append((difference[i]))
        else:
            gone.append(difference[i])
            L1.remove(difference[i])
        i = i +i
    # print (L1)
    return new, gone
