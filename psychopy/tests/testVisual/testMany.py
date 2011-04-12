#!/usr/bin/env python
import nose, sys, os, copy
from psychopy import visual, misc
from psychopy.tests import utils
import numpy

"""Each test class creates a context subclasses _baseVisualTest to run a series
of tests on a single graphics context (e.g. pyglet with shaders)

To add a new stimulus test use _base so that it gets tested in all contexts

"""

class _baseVisualTest:
    #this class allows others to be created that inherit all the tests for
    #a different window config
    @classmethod
    def setupClass(self):
        #Implement this to create self.win on each use
        self.win=None
        self.contextName
        raise NotImplementedError
    @classmethod
    def tearDownClass(self):
        self.win.close()#shutil.rmtree(self.temp_dir)
        
    def testGabor(self):
        win = self.win
        win.flip()
        contextName=self.contextName
        #using init
        gabor = visual.PatchStim(win, mask='gauss', pos=[0.6, -0.6], sf=2, size=2)
        gabor.draw()
        utils.compareScreenshot('data/gabor1_%s.png' %(contextName), win)
        win.flip()#AFTER compare screenshot
        #using .set()
        gabor.setOri(45)
        gabor.setSize(0.2, '-')
        gabor.setColor([45,30,0.3], colorSpace='dkl')
        gabor.setSF(0.2, '+')
        gabor.setPos([-0.5,0.5],'+')
        gabor.draw()
        utils.compareScreenshot('data/gabor2_%s.png' %(contextName), win)
        win.flip()#AFTER compare screenshot
    def testText(self):
        win = self.win
        win.flip()
        contextName=self.contextName
        #set font
        if win.winType=='pygame':
            if sys.platform=='win32': font = 'times'
            else:font = '/Library/Fonts/Times New Roman.ttf'
        else: font = 'Times New Roman'
        #using init
        stim = visual.TextStim(win,text=u'\u03A8a', color=[0.5,1.0,1.0], ori=15,
            height=0.8, pos=[0,0], font=font) 
        stim.draw()
        #compare with a LIBERAL criterion (fonts do differ) 
        utils.compareScreenshot('data/text1_%s.png' %(contextName), win, crit=35)
        win.flip()#AFTER compare screenshot
        #using set
        stim.setText('y')
        stim.setFont(font)
        stim.setOri(-30.5)
        stim.setHeight(1.0)
        stim.setColor([0.1,-1,0.8], colorSpace='rgb')
        stim.setPos([-0.5,0.5],'+')
        stim.draw()
        #compare with a LIBERAL criterion (fonts do differ)
        utils.compareScreenshot('data/text2_%s.png' %(contextName), win, crit=30)
        win.flip()#AFTER compare screenshot
    def testMov(self):
        win = self.win
        if self.win.winType=='pygame':
            raise nose.plugins.skip.SkipTest("movies only available for pyglet backend")
        win.flip()
        contextName=self.contextName
        #try to find test movie file
        fileName = 'testMovie.mp4'
        for prepend in ['','..','data','../data']:
            f = os.path.join(prepend, fileName)
            if os.path.isfile(f): fileName=f
        #check if any file was found
        if not os.path.isfile(fileName):
            raise IOError, 'Could not find movie file: %s' %os.path.abspath(fileName)
        #then do actual drawing
        mov = visual.MovieStim(win, fileName)
        for frameN in range(10):
            mov.draw()
            win.flip()
    def testShape(self):
        win = self.win
        win.flip()
        contextName=self.contextName
        
        shape = visual.ShapeStim(win, lineColor=[1, 1, 1], lineWidth=1.0, 
            fillColor=[0.80000000000000004, 0.80000000000000004, 0.80000000000000004], 
            vertices=[[-0.5, 0],[0, 0.5],[0.5, 0]], 
            closeShape=True, pos=[0, 0], ori=0.0, opacity=1.0, depth=0, interpolate=True)
        shape.draw()
        #NB shape rendering can differ a litte, depending on aliasing
        utils.compareScreenshot('data/shape1_%s.png' %(contextName), win, crit=10.0)
        win.flip()#AFTER compare screenshot
    def testRadial(self):
        win = self.win
        win.flip()
        contextName=self.contextName
        #using init
        wedge = visual.RadialStim(win, tex='sqrXsqr', color=1,size=2,
            visibleWedge=[0, 45], radialCycles=2, angularCycles=2, interpolate=False)
        wedge.draw()
        utils.compareScreenshot('data/wedge1_%s.png' %(contextName), win, crit=10.0)
        win.flip()#AFTER compare screenshot
        #using .set()
        wedge.setOri(180)
        wedge.setContrast(0.8)
        wedge.setRadialPhase(0.1,operation='+')
        wedge.setAngularPhase(0.1)
        wedge.draw()
        utils.compareScreenshot('data/wedge2_%s.png' %(contextName), win, crit=10.0)
        win.flip()#AFTER compare screenshot
    def testDots(self):
        #NB we can't use screenshots here - just check that no errors are raised
        win = self.win
        win.flip()
        contextName=self.contextName
        #using init        
        dots =visual.DotStim(win, color=(1.0,1.0,1.0), dir=270,
            nDots=500, fieldShape='circle', fieldPos=(0.0,0.0),fieldSize=1,
            dotLife=5, #number of frames for each dot to be drawn
            signalDots='same', #are the signal and noise dots 'different' or 'same' popns (see Scase et al)
            noiseDots='direction', #do the noise dots follow random- 'walk', 'direction', or 'position'
            speed=0.01, coherence=0.9)
        dots.draw()
        win.flip()
        #using .set() and check the underlying variable changed
        prevDirs = copy.copy(dots._dotsDir)
        prevSignals = copy.copy(dots._signalDots)
        prevPosRend = copy.copy(dots._fieldPosRendered)
        dots.setDir(20)
        dots.setFieldCoherence(0.5)
        dots.setFieldPos([-0.5,0.5])
        dots.setSpeed(0.1)
        dots.draw()
        win.flip()
        #check that things changed
        nose.tools.assert_false((prevDirs-dots._dotsDir).sum()==0, 
            msg="dots._dotsDir failed to change after dots.setDir():")
        nose.tools.assert_false(prevSignals.sum()==dots._signalDots.sum(), 
            msg="dots._signalDots failed to change after dots.setCoherence()")
        nose.tools.assert_false(numpy.alltrue(prevPosRend==dots._fieldPosRendered), 
            msg="dots._fieldPosRendered failed to change after dots.setPos()")
    def testElementArray(self):
        win = self.win
        contextName=self.contextName
        if not win._haveShaders:
            raise nose.plugins.skip.SkipTest("ElementArray requires shaders, which aren't available")
        win.flip()
        #using init
        thetas = numpy.arange(0,360,10)
        N=len(thetas)
        radii = numpy.linspace(0,1.0,N)
        x, y = misc.pol2cart(theta=thetas, radius=radii)
        xys = numpy.array([x,y]).transpose()
        spiral = visual.ElementArrayStim(win, nElements=N,sizes=0.5,
            sfs=3, xys=xys, oris=thetas)
        spiral.draw()
        utils.compareScreenshot('data/elarray1_%s.png' %(contextName), win)
    def testAperture(self):
        win = self.win
        win.flip()
#        if win.winType=='pygame':
#            raise nose.plugins.skip.SkipTest
        contextName=self.contextName
        gabor1 = visual.PatchStim(win, mask='circle', pos=[0.3, 0.3], 
            sf=4, size=1,
            color=[0.5,-0.5,1])
        gabor2 = visual.PatchStim(win, mask='circle', pos=[-0.3, -0.3], 
            sf=4, size=1,
            color=[-0.5,-0.5,-1])
        aperture = visual.Aperture(win, size=10,pos=[2.5,0])
        aperture.enable()
        gabor1.draw()
        aperture.disable()
        gabor2.draw()
        utils.compareScreenshot('data/aperture1_%s.png' %(contextName), win)
    def testRatingScale(self):
        # try to avoid text; avoid default / 'triangle' because it does not display on win XP
        win = self.win
        win.flip()
        rs = visual.RatingScale(win, low=0,high=1,precision=100, displaySizeFactor=3, pos=(0,-.4),
                        lowAnchorText=' ', highAnchorText=' ', scale=' ', 
                        markerStyle='glow', markerStart=0.7, markerColor='darkBlue')
        rs.draw()
        utils.compareScreenshot('data/ratingscale1_%s.png' %(self.contextName), win, crit=30.0)
        win.flip()#AFTER compare screenshot
    def testRefreshRate(self):
        #make sure that we're successfully syncing to the frame rate
        msPFavg, msPFstd, msPFmed = visual.getMsPerFrame(self.win,nFrames=60, showVisual=True)
        nose.tools.ok_(1000/150.0 < msPFavg < 1000/40.0, "Your frame period is %.1fms which suggests you aren't syncing to the frame" %msPFavg)
        
#create different subclasses for each context/backend
class TestPygletNorm(_baseVisualTest):
    @classmethod
    def setupClass(self):
        self.win = visual.Window([128,128], winType='pyglet', pos=[50,50], allowStencil=False)
        self.contextName='norm'
class TestPygletHeight(_baseVisualTest):
    @classmethod
    def setupClass(self):
        self.win = visual.Window([128,64], winType='pyglet', pos=[50,50], allowStencil=False)
        self.contextName='height'
class TestPygletNormNoShaders(_baseVisualTest):
    @classmethod
    def setupClass(self):
        self.win = visual.Window([128,128], monitor='testMonitor', winType='pyglet', pos=[50,50], allowStencil=False)
        self.win._haveShaders=False
        self.contextName='norm'
class TestPygletNormStencil(_baseVisualTest):
    @classmethod
    def setupClass(self):
        self.win = visual.Window([128,128], monitor='testMonitor', winType='pyglet', pos=[50,50], allowStencil=True)
        self.contextName='stencil'
class TestPygameNorm(_baseVisualTest):
    @classmethod
    def setupClass(self):
        self.win = visual.Window([128,128], monitor='testMonitor', winType='pygame', allowStencil=False)
        self.contextName='norm'
#    @classmethod
#    def teardownClass(self):
#        self.win.close()#shutil.rmtree(self.temp_dir)
#        import pygame
#        pygame.quit()#to be sure
    
if __name__ == "__main__":
    argv = sys.argv
    argv.append('--verbosity=3')
    if 'cover' in argv: 
        argv.remove('cover')
        argv.append('--with-coverage')
        argv.append('--cover-package=psychopy')
    nose.run(argv=argv)
