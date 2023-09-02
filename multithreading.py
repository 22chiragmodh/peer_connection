import threading

# thread is a sequence of such instructions within a program that can be executed independently of other code

# Each thread contains its own register set and local variables (stored in the stack).

# All threads of a process share global variables (stored in heap) and the program code.

def print_cube(num):
    # function to print cube of given num
    print("Cube: {}" .format(num * num * num))
 
 
def print_square(num):
    # function to print square of given num
    print("Square: {}" .format(num * num))



if __name__ == "__main__":
    t1=threading.Thread(target=print_square,args=(10,))
    t2=threading.Thread(target=print_cube,args=(10,))

    t1.start()
    t2.start()


    t1.join()
    t2.join()

    print("Done")


