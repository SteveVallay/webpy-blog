
class Log:
    def logd(self,tag,msg):
        f=open('log','w')
        f.write(tag+'---'+msg)
        f.close()

