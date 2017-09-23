import random
import direct.directbase.DirectStart
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import *
from direct.showbase.ShowBaseGlobal import *
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
import os, sys
from direct.task import Task

#The x position for all objects interacting with the plane is bounded between 
#-1500 and 1500 for all the classes as the plane doesnt go beyond this.The y
#positioin is from 0 to the positioin of the base ship which is 20000. The z 
#axis is 10 for all classes so the objects lie in one plane.


#This class creates the health pickups in the scene and renders them into the 
#screen. It also creates the collision spheres for each of the pickups and puts 
#them in a list which can be used later if needed. 
class Firstaid:
    def __init__(self):
        self.x = random.randint(-1500,1500)
        self.y = random.randint(0, 20000)  
        self.z = 10
        self.aid = loader.loadModel("hp")
        self.aid.reparentTo(render)
        self.aid.setPos(self.x, self.y, self.z) 
        self.aid.setScale(7, 7, 7)

        #collisions spheres made here
        self.aidSphere = CollisionSphere(0, 0, 0, 1)
        self.aidplayer = CollisionNode("aidplayer")
        self.aidplayer.addSolid(self.aidSphere)
        self.aidShape = self.aid.attachNewNode(self.aidplayer)

#This function creates instances of the Firstaid class and puts them in a list.
def DrawAidPickups():
        aidsList = []
        num = 0
        while num < 200:  
            aidsList.append(Firstaid())
            num += 1

#This class creates the ammo pickups in the scene and renders them into the 
#screen. It also creates the collision spheres for each of the pickups and puts 
#them in a list which can be used later if needed.
class Ammo:
    def __init__(self):
        self.x = random.randint(-1500,1500)
        self.y = random.randint(0, 20000)  
        self.z = 0
        self.ammo = loader.loadModel("mp")
        self.ammo.reparentTo(render)
        self.ammo.setPos(self.x, self.y, self.z)  
        self.ammo.setScale(4, 4, 4)

        #collisions spheres made here
        self.ammoSphere = CollisionSphere(0, 0, 0, 5)
        self.ammoplayer = CollisionNode("ammoplayer")
        self.ammoplayer.addSolid(self.ammoSphere)
        self.ammoShape = self.ammo.attachNewNode(self.ammoplayer)

#This function creates instances of the Ammo class and puts them in a list.
def DrawAmmoPickups():
        ammoList = []
        num = 0
        while num < 150:  
            ammoList.append(Ammo())
            num += 1

#This class makes the base ship at the end of the game and a collision sphere 
#for it.
class Base(ShowBase):
    def __init__(self):
        self.base = loader.loadModel("base")
        self.base.reparentTo(render)
        self.base.setPos(0, 20000, -350)
        self.base.setHpr(0,0,0)
        self.base.setScale(100,100,100)

        #collision sphere made here
        self.baseSphere = CollisionSphere(0, 0, 2.5, 8)
        self.baseplayer = CollisionNode("baseplayer")
        self.baseplayer.addSolid(self.baseSphere)
        self.baseShape = self.base.attachNewNode(self.baseplayer)
        self.baseShape.show()

#This class makes the skysphere which is parented to the instance of the plane
#i.e. 'p' which is created at the end of the code.
class SkySphere:
    def __init__(self):
        self.texture = loader.loadCubeMap("LinearPinkNebula_#.png")
        self.sphere = loader.loadModel("InvertedSphere.egg")

        self.sphere.setTexGen(TextureStage.getDefault(),TexGenAttrib.MWorldPosition)
        self.sphere.setTexProjector(TextureStage.getDefault(),render, self.sphere)
        self.sphere.setTexture(self.texture)

        self.sphere.setLightOff()
        self.sphere.setScale(20000)

        self.sphere.writeBamFile("PurpleSkySphere.bam")
        self.sphere.reparentTo(p.plane)

        self.rotateSky = self.sphere.hprInterval(200,Point3(360, 0, 0),startHpr=Point3(0, 0, 0))
        self.rotateSky.loop()

        self.sphere.setFogOff()

#Makes the asteroid corridor on the left of the maincorridor. Does not have 
#collision spheres because the plane does not interact with these.
class Asteroids_Left:
    def __init__(self):
        self.x = random.randint(-2000, -1500)
        self.y = random.randint(0, 20000)   
        self.z = random.randint(-1100,100)
        self.models = ["big brown", "brown", "grey", "large", "med", "metal"]
        self.model = random.choice(self.models)
        self.scale = random.randint(10,40)

        self.ast = loader.loadModel(self.model)
        self.ast.reparentTo(render)
        self.ast.setPos(self.x, self.y, self.z)      
        self.ast.setScale(self.scale,self.scale,self.scale)

#Creates instances of the above class and puts them in the list.
def DrawAst_Left():
    asteroids=[]
    num=0
    while num <600:       # number of asteroids being rendered
        asteroids.append(Asteroids_Left())
        num+=1

#Makes the asteroid corridor on the right of the main corridor. Does not have 
#collision spheres because the plane does not interact with these.
class Asteroids_Right:
        def __init__(self):
            self.x = random.randint(1500, 2000)
            self.y = random.randint(0, 20000)  # in 1 sec it goes aprox 71 forward so this will make around 1.5 mins
            self.z = random.randint(-1100, 100)
            self.models = ["big brown", "brown", "grey", "large", "med", "metal"]
            self.model = random.choice(self.models)
            self.scale = random.randint(10, 40)

            self.ast = loader.loadModel(self.model)
            self.ast.reparentTo(render)
            self.ast.setPos(self.x, self.y, self.z)  # change to self.x, self.y, self.z later
            self.ast.setScale(self.scale, self.scale, self.scale)
        # make asteroids appear

#Creates instances of the above class and puts them in the list.
def DrawAst_Right():
        asteroids2 = []
        num = 0
        while num < 600:  # number of asteroids being rendered
            asteroids2.append(Asteroids_Right())
            num += 1

#Makes the asteroid corridor below the main corridor. Does not have 
#collision spheres because the plane does not interact with these.
class Asteroids_Floor:
    def __init__(self):
        self.x = random.randint(-1500, 1500)
        self.y = random.randint(0, 20000)  # in 1 sec it goes aprox 71 forward so this will make around 1.5 mins
        self.z = random.randint(-1500, -1100)
        self.models = ["big brown", "brown", "grey", "large", "med", "metal"]
        self.model = random.choice(self.models)
        self.scale = random.randint(20, 60)

        self.ast = loader.loadModel(self.model)
        self.ast.reparentTo(render)
        self.ast.setPos(self.x, self.y, self.z)  # change to self.x, self.y, self.z later
        self.ast.setScale(self.scale, self.scale, self.scale)

        # make asteroids appear

#Creates instances of the above class and puts them in the list.
def DrawAst_Floor():
    asteroids3 = []
    num = 0
    while num < 300:  # number of asteroids being rendered
        asteroids3.append(Asteroids_Floor())
        num += 1

#This class chooses a random position for the asteroid. It then chooses whether
#to make the asteroid big or small and chooses the radius for the collision
#sphere respectively. 
class Asteroids_Corridor(ShowBase):
    def __init__(self):
        self.x = random.randint(-1500,1500)
        self.y = random.randint(0, 20000) 
        self.z = -15
        self.models = ["big brown"]
        self.model = random.choice(self.models)
        self.scale = random.choice([10,25])
        if self.scale==10:
            self.radius=0.5
        elif self.scale==25:
            self.radius=2

        self.ast = loader.loadModel(self.model)
        self.ast.reparentTo(render)
        self.ast.setPos(self.x, self.y, self.z)  
        self.ast.setScale(self.scale, self.scale, self.scale)

        #collision spheres made here
        self.astSphere = CollisionSphere(0, 0, 1, self.radius)
        self.astplayer = CollisionNode("astplayer")
        self.astplayer.addSolid(self.astSphere)
        self.astShape = self.ast.attachNewNode(self.astplayer)

#Creates instances of the above class and puts them in the list.
def DrawAst_Corridor():
    asteroids4 = []
    num = 0
    while num < 400:  # number of asteroids being rendered
        asteroids4.append(Asteroids_Corridor())
        num += 1

#The init method makes the missile and renders it into the scene. The rest of 
#the functions control movement. missInAst and missOutAst execute when missile 
#interacts with asteroids.
class Missiles(ShowBase):
    def __init__(self):
        self.miss = loader.loadModel("m")
        self.miss.reparentTo(render)
        self.miss.setPos(p.plane.getX()-5, p.plane.getY(), p.plane.getZ()-15)
        self.miss.setScale(3,3,3)
        self.miss.setHpr(0,0,90)

        taskMgr.add(self.shoot, "shoot")
        taskMgr.add(self.setCollision, "setCollision")

    def shoot(self, task):
        dt = globalClock.getDt()
        self.miss.setFluidY(self.miss, 501*dt)
        return task.cont

    def setCollision(self, task):
        self.missSphere = CollisionSphere(0, 0, 0, 0.1)
        self.missplayer = CollisionNode("missplayer")
        self.missplayer.addSolid(self.missSphere)
        self.missShape = self.miss.attachNewNode(self.missplayer)
        base.cTrav = CollisionTraverser()
        base.cHan = CollisionHandlerEvent()

        base.cTrav.addCollider(self.missShape, base.cHan)
        base.cHan.addInPattern("%fn-in-%in")
        base.cHan.addOutPattern("%fn-out-%in")
        self.accept("missplayer-in-astplayer", self.missInAst)
        self.accept("missplayer-out-astplayer", self.missOutAst)
        base.cTrav.traverse(render)
        return task.again

    def missInAst(self, task):
        self.boom = loader.loadModel("EBoom") 
        self.boom.reparentTo(self.miss)
        self.boom.setScale(70,70,70)
        self.boomFx=loader.loadMusic("explosion.mp3")
        self.boomFx.play()
        taskMgr.doMethodLater(1, self.missOutAst, "missOutAst")
        p.extraTime+=1
        gui.timer['value']=p.totalTime

    def missOutAst(self, task):
        self.boom.removeNode()
        loader.unloadModel(self.miss)

#Main class where the gameplay is done.
class Plane(ShowBase):

    #Makes the plpane and renders it. Adds task to task manager. These get 
    #executed repeatedly.
    def __init__(self):
        self.health = 5
        self.extraTime=0
        base.disableMouse()
        base.setBackgroundColor(0, 0, 0, 1)
        self.plane = loader.loadModel("a2")
        self.plane.reparentTo(render)
        self.plane.setPos(0, 0, 10)
        self.plane.setHpr(0,0,0)
        self.plane.setScale(0.5,0.5,0.5)

        base.camera.reparentTo(self.plane)
        base.camera.setY(self.plane, -40)
        base.camera.setZ(self.plane, 10)
        base.camera.setHpr(0,-10,0)
        #base.camLens.setFov(70, 90)
        #base.camLens.setNearFar(4, 40000)

        taskMgr.add(self.allCollisions, "allCollisions")
        taskMgr.add(self.moveForward, "moveForward")
        taskMgr.add(self.keyEvent, "keyEvent")
        taskMgr.add(self.extraArgs, "extraArgs")
        taskMgr.add(self.keymap, "keymap")
        taskMgr.add(self.planeSound, "planeSound")
        taskMgr.add(self.timerTask, "timerTask")

    #Main music in the game
    def planeSound(self, task):
        self.gameSound = loader.loadMusic("gameMusic.mp3")
        self.gameSound.play()
        self.planeEngine = loader.loadMusic("Engine.wav")

    #Keymaps for the different keys. Uses the next function and sets key state 
    #according to whether the key is pressed or not. The keys which need three
    #different states have None as the initial value.
    def keymap(self, task):
        self.keyMap = {"d":None, "a":None, "w":False, "s":False}
        self.accept("d", self.setKey, ["d", True])
        self.accept("d-up", self.setKey, ["d", False])
        self.accept("a", self.setKey, ["a", True])
        self.accept("a-up", self.setKey, ["a", False])
        self.accept("w", self.setKey, ["w", True])
        self.accept("w-up", self.setKey, ["w", False])
        self.accept("s", self.setKey, ["s", True])
        self.accept("s-up", self.setKey, ["s", False])

    def setKey(self, key, value):
        self.keyMap[key]=value

    #Extra variables needed throughout the class.
    def extraArgs(self, task):
        self.missileNum = 2
        self.distTravForward=0

        self.distTrav = 0
        self.distravUpDown = p.plane.getZ()-10
        self.maxDist = 20

        self.speed = 0
        self.addSpeed = 10
        self.maxSpeed = 50

        self.angle = 0
        self.addAngle = 15
        self.maxAngle = 30

    #Makes collisioin sphere for plane and makes the collision handler which
    #handles all the collisions in the game.
    def allCollisions(self, task):
        self.planeSphere = CollisionSphere(0, -1, 3, 6)
        self.planeplayer = CollisionNode("planeplayer")
        self.planeplayer.addSolid(self.planeSphere)
        self.planeShape = self.plane.attachNewNode(self.planeplayer)

        base.cTrav = CollisionTraverser()
        base.cHan = CollisionHandlerEvent()
        base.cTrav.addCollider(self.planeShape, base.cHan)
        base.cHan.addInPattern("%fn-in-%in")
        base.cHan.addOutPattern("%fn-out-%in")

        self.accept("planeplayer-in-aidplayer", self.planeInAidPickup)
        self.accept("planeplayer-in-ammoplayer", self.planeInAmmoPickup)
        self.accept("planeplayer-in-astplayer", self.planeInAst)
        self.accept("planeplayer-in-baseplayer", self.planeInBase)
        base.cTrav.traverse(render)
        return task.again

    #The next four functions execute when one of the collisions takes place.
    def planeInBase(self, task):
        taskMgr.remove("moveForward")
        self.w = Win()

    def planeInAidPickup(self, task):
        if self.health<15:
            self.health+=5
        gui.health['value']=self.health
        self.pickupSound = loader.loadMusic("PowerupSound.mp3")
        self.pickupSound.play()

    def planeInAmmoPickup(self, task):
        self.missileNum+=1
        gui.ammo['text'] = ("Ammo:" + str(self.missileNum))
        self.pickupSound = loader.loadMusic("PowerupSound.mp3")
        self.pickupSound.play()

    def planeInAst(self, task):
        #self.boom = loader.loadModel("EBoom") 
        #self.boom.reparentTo(p.plane)
        #self.boom.setScale(100,100,100)
        self.boomFx=loader.loadMusic("explosion.mp3")
        self.boomFx.play()
        if self.health>0:
            self.health-=1
        gui.health['value']=self.health
        if self.health==0:
            taskMgr.remove("moveForward")
            w=Win()
        taskMgr.doMethodLater(1, self.planeOutAst, "planeOutAst")

    def planeOutAst(self, task):
        pass
        #self.boom.removeNode()


    #Next few functions control the movement of plane and bound it.
    def moveForward(self, task):
        dt = globalClock.getDt()
        self.plane.setFluidY(self.plane, 500*dt)
        self.distTravForward+=500*dt
        gui.score['text']=( "Score = "+ str(int(self.distTravForward)))
        return task.cont

    def move(self):
        self.plane.setFluidX(self.plane, self.speed)
        #X is set in regard to the last position of plane hence it moves forward.

    def turn(self):
        self.plane.setR(self.angle)

    def reset(self, task):
        self.angle=0
        self.speed=0
        self.plane.setHpr(0,0,0)
        self.move()

    def turnRight(self, task):
        dt = globalClock.getDt()
        if self.speed>self.maxSpeed:
            self.speed = self.maxSpeed
            #add to the distance here
            self.distTrav+=self.speed
        else:
            self.speed+=(self.addSpeed*dt)
            #add to the distance here
            self.distTrav+=self.speed

        #check if out of bounds
        #print(self.distTrav)
        self.checkBounds()
        self.move()

    def turnLeft(self, task):
        dt = globalClock.getDt()
        if (self.speed)<(-self.maxSpeed):
            self.speed = -self.maxSpeed
            #subtract from total d travelled
            self.distTrav+=self.speed
        else:
            self.speed-=(self.addSpeed*dt)
            #subtract from total d travelled
            self.distTrav+=self.speed

        #check if out of bounds
        #print(self.distTrav)
        self.checkBounds()
        self.move()

    def jumpity(self, task):
        self.plane.setFluidZ(self.plane, 10)
        self.checkBoundsUp()

    def checkBoundsUp(self):
        if self.plane.getZ()>30:
            self.plane.setFluidZ(30)

    def checkBounds(self):
        if abs(self.distTrav)>2000:
            self.plane.setX(0)
            self.distTrav=0

    #Tell what function to execute depending on the state of the key.
    def keyEvent(self, task):
        if(self.keyMap["a"] == True):
            self.turnLeft(task)
        elif(self.keyMap["d"] == True):
            self.turnRight(task)
        elif(self.keyMap["a"] == False):
            self.reset(task)
        elif(self.keyMap["d"] == False):
            self.reset(task)
        if (self.keyMap["s"] == True and self.missileNum>0):
            self.missileNum-=1
            gui.ammo['text'] = ("Ammo:" + str(self.missileNum))
            self.missile = Missiles() #Add the missilie here
            self.launchFx = loader.loadMusic("launchMissile.mp3")
            self.launchFx.play()
        if(self.keyMap["w"] == False):
            self.plane.setFluidZ(10)
        elif(self.keyMap["w"] == True):
            self.jumpity(task)
        return task.cont

    #Keep a track of time.
    def timerTask(self,task):
        self.time = int(task.time)
        self.totalTime = self.time-self.extraTime
        if self.totalTime<0:
            self.totalTime=0
        gui.timer['value']=self.totalTime
        if self.totalTime >45:
            w = Win()
            taskMgr.remove("moveForward")
        return task.cont

#This screen is displayed when the user either runs out of time or reaches the 
#end and wins the game.
class Win:
    def __init__(self):
        self.win=DirectFrame(frameColor=(0, 0, 0, 1),frameSize=(-2, 2, -2, 2),
            pos=(0, 0, 0)) 

        self.background = OnscreenImage(image = 'Background.jpg', 
            pos = (0, 0, 0), scale = (1, 1, 1), parent=self.win) 

        self.scoreText = DirectLabel(text = ("Score = "+str(p.distTravForward)), 
            scale=.2, parent=self.win, text_fg=(0,0,1,1), text_bg=(0,1,0.6,1), 
            pos=(0,0,0.2))

        self.exit = DirectButton(text='Exit', text_fg= (1,1,0,1), 
            text_bg=(0,0,1,1), scale=.1, parent=self.win, pressEffect=1, 
            pos=(0,0,0.8), relief=DGG.RAISED, command=self.exits)
        gui.health.hide()
        gui.timer.hide()

    def exits(self):
        sys.exit()

#Can be accesed from a button on the main screen. Gives the instructions on how
#to play the game.
class Instructions:
    def __init__(self):
        self.struct=DirectFrame(frameColor=(0, 0, 0, 1),frameSize=(-2, 2, -2, 2),
            pos=(0, 0, 0)) 

        self.background = OnscreenImage(image = 'Background.jpg', 
            pos = (0, 0, 0), scale = (1, 1, 1), parent=self.struct) 

        self.instruct = """
        W to jump over small asteroids
        S to shoot missiles
        A to go left
        D to go right

        Reach the base ship at end 
        without letting the health 
        meter go to zero or running out of time.
        Asteroids wont be destroyed with the ammo because
        they are fragments of a dwarf star alloy planet.
        It exploded in your face and now you need to 
        navigate the debri field. Shooting at them
        creates a temporal disruption which gives you
        more time to reach the base ship.
        So shoot and run.
        Collect health packs (red)
        and Ammo packs (green) along the way to help you.
        MAY THE FORCE BE WITH YOU.
        """

        self.text = DirectLabel(text = self.instruct, scale=.05, 
            parent=self.struct, text_fg=(1,0,0,1), text_bg=(0,0,1,1), 
            pos=(0,0,0.5))

        self.game = DirectButton(text="Return To Game", scale=.08, 
            parent=self.struct,text_fg=(1,1,0,1),  text_bg=(0,0,1,1), 
            pressEffect=1, pos=(0,0,0.8), relief=DGG.RAISED, 
            command=self.backToGame)

    def backToGame(self):
        self.struct.destroy()
        gui.health.show()
        gui.timer.show()

#MAkes the widgets on the screens and has the functions which need to be
#executed on clicking either of the button. Instruction instance is made in this
#class.
class GUI:
    def __init__(self):
        self.exit = DirectButton(text = ("Exit"), scale=.08,
            parent=base.aspect2d, pressEffect=1, text_fg=(1,1,0,1), 
            text_bg=(0,0,1,1), pos=(1.1,0,0.6), command=self.exits) 

        self.instruct = DirectButton(text = ("Instructions"), scale=.08, 
            parent=base.aspect2d,pressEffect=1, text_fg=(1,1,0,1), 
            text_bg=(1,0,0,1), pos=(1.1,0,0.4), command=self.instructions)

        self.healthText = DirectLabel(text = ("HEALTH"), scale=.08, 
            parent=base.aspect2d, text_fg=(0,0,1,1), text_bg=(0,1,0.6,1), 
            pos=(-1.1,0,0.9))
        self.health = DirectWaitBar(value=5, range=15, scale=.2,
            parent=base.aspect2d, barColor=(0,1,0,1), pos=(-1.1,0,0.8))
        
        self.ammo = DirectLabel(text = ("Ammo:2"), scale=.08, 
            parent=base.aspect2d, text_fg=(1,1,0,1), text_bg=(1,0,0,1), 
            pos=(-1.1,0,0.2))
        
        self.timerText = DirectLabel(text = ("TIMER"), scale=.08, 
            parent=base.aspect2d, text_fg=(0,0,1,1), text_bg=(0,1,0.6,1), 
            pos=(-1.1,0,0.6))
        self.timer = DirectWaitBar(value=0, range=45, scale=.2, 
            parent=base.aspect2d, barColor=(0,0,1,1), pos=(-1.1,0,0.5))

        self.score = DirectLabel(text = ("Score = 0"), scale=.07, 
            parent=base.aspect2d, text_fg=(0,0,1,1), text_bg=(0,1,0.6,1), 
            pos=(1.1,0,0.8))

    def instructions(self):
        self.i = Instructions()
        self.timer.hide()
        self.health.hide()

    def exits(self):
        sys.exit()

class start:
    def __init__(self):
        self.exit = DirectButton(text = ("Start"), scale=0.06,
            parent=base.aspect2d, pressEffect=1, text_fg=(1,1,0,1),
            text_bg=(0,0,1,1), pos=(0,0,0), command=self.starts)

        self.title = OnscreenText(text="PSYCHEDELIC",
                                  parent=base.aspect2d, scale=.2,
                                  align=TextNode.ARight, pos=(0.6, -0.9),
                                  fg=(0, 0.7, 0.6, 1), shadow=(0, 0, 0, 0.5))

    def starts(self):
        DrawAidPickups()
        DrawAmmoPickups()
        DrawAst_Left()
        DrawAst_Right()
        DrawAst_Floor()
        DrawAst_Corridor()
        gui.healthText.show()
        gui.health['value']=3
        gui.health.show()
        gui.ammo.show()
        gui.timerText.show()
        gui.timer['value']=0
        gui.timer.show()
        gui.score.show()
        self.exit.hide()
        self.title.hide()


p = Plane()
b = Base()
ss = SkySphere()
gui = GUI()
gui.healthText.hide()
gui.health.hide()
gui.ammo.hide()
gui.timerText.hide()
gui.timer.hide()
gui.score.hide()

s=start()
run()