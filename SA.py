from Tkinter import *
import random
import time
import math

#config options for the screen frame
canvasH = 600
canvasW = 600
psychedelic_mode = True

# a subclass of Canvas for dealing with resizing of windows
class ResizingCanvas(Canvas):
    def __init__(self,parent,**kwargs):
        Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,wscale,hscale)

root = Tk()
root.title("Simulated Annealing")
frame = Frame(root)
frame.pack(expand=YES, fill=BOTH)
w = ResizingCanvas(frame, width=canvasW, height=canvasH*0.75, highlightthickness=0)
w.pack(expand=YES ,fill=BOTH)


#simulation parameters
T = start_temp = 1
coolingFactor = 0.99998
numPts= length = 300
maxIter = 1000000

#cooling function
def cooling(start_temp, alpha):
    T = start_temp * alpha
    return T

#create initial state
def getPath(numPts):
    path = []

    for i in range(numPts):
        x = random.random()
        y = random.random()

        path.append([x,y])
    return path

def scaleList(point):
    scaleX = point[0]*w.winfo_width()
    scaleY = point[1]*w.winfo_height()
    scaledPoint = [scaleX, scaleY]
    return scaledPoint

#determine the probability of accepting a move to a neighbor
def P(current_cost, next_cost, T):
    if next_cost < current_cost:
        return 1
    else:
        return math.exp( -abs(current_cost-next_cost)/T )

#generate a neighbor state and its cost
def getNeighbor(path):
    copy = path[:]
    # index1 = random.randrange(0,length)
    # index2 = (index1 + 1)%length
    # point1 = copy[index1]
    # point2 = copy[index2]
    #
    # copy[index1] = point2
    # copy[index2] = point1
    n = random.randrange(0,length+1)
    m = random.randrange(0,length+1)
    if n < m:
        copy[n:m] = reversed(copy[n:m])
    else:
        copy[m:n] = reversed(copy[m:n])

    i=0
    cost=0
    while i < length:
        a = copy[i]
        b = copy[(i+1)%length]
        cost += math.hypot(b[0]-a[0], b[1]-a[1])
        i+= 1

    # dist = np.diff(copy, axis=0)
    # segdists = np.hypot(dist[:,0], dist[:,1])
    # cost = np.sum(segdists)

    return copy, cost

def getColor():
    colors = ["red", "yellow", "blue", "green", "orange", "violet"]
    if psychedelic_mode:
        color = random.choice(colors)
    else:
        return "black"
    return color

#function to draw current path and graph cost history to the screen
def draw(my_path, costs):
    i=5
    w.delete("all")
    scaledPath = [map(scaleList, my_path[:])]
    height = w.winfo_height()
    ratio = height/start_cost
    color = getColor()
    for cost in costs:
        w.create_line(i,height , i,height - cost*ratio , fill="gray", width = 3)
        i+=3
    #
    # i=0
    # while i < length-1:
    #     w.create_line(path[i],path[i+1])
    #     i+= 1
    # w.create_line(path[length-1], path[0])
    item = w.create_line(scaledPath, fill=color)
    w.create_line(scaledPath[0],scaledPath[len(scaledPath)-1])



##### MAIN BODY #####


current_path, current_cost = getNeighbor(getPath(numPts))
best_cost = start_cost = current_cost
costs = []
iterations = 0
accepted_count = 0

#begin iterations
while iterations < maxIter:
    next_path, next_cost = getNeighbor(current_path)  #get a neighbor for the current path
    iterations+= 1
    p=P(current_cost, next_cost, T)  # accept new path with probability
    T = cooling(T, coolingFactor)
    if random.random() < p:
        current_path = next_path
        current_cost = next_cost
        accepted_count+=1
    if current_cost < best_cost:
        best_cost = current_cost

    if iterations % 1000 == 0:       #every 100 iterations
        if len(costs)*3 >= w.winfo_width():
            costs = costs[1:]
        costs.append(current_cost)
        draw(current_path, costs)
        w.create_text(20,w.winfo_height()-80 , anchor = SW, text = "Accepted: "+str(accepted_count), fill="blue")
        w.create_text(20,w.winfo_height()-60 , anchor = SW, text = "Iteration: "+str(round(iterations/1000 ,1))+'k', fill="blue")
        w.create_text(20,w.winfo_height()-40 , anchor = SW, text = "Temp: "+str(T), fill="blue")
        w.create_text(20,w.winfo_height()-20 , anchor = SW, text = "Starting Cost: "+str(start_cost), fill="blue")
        w.create_text(20,w.winfo_height() , anchor = SW, text = "Best Cost: "+str(best_cost), fill="blue")
        w.addtag_all("all")
        w.pack()
        frame.update_idletasks()
        frame.update()

frame.mainloop()
