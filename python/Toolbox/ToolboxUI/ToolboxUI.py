import IECore

import Gaffer
import GafferUI

import Toolbox
from Qt import QtGui
from Qt import QtWidgets
from Qt import QtCore
import imath

class ToolboxUI(GafferUI.Editor):

    def __init__( self, scriptNode, **kw):
        # create main two part container (top for actions, bottom for feedback)
        self.__splittable = GafferUI.SplitContainer( borderWidth = 2)
        GafferUI.Editor.__init__( self, self.__splittable, scriptNode, **kw)

        with self.__splittable:
            # create splittable container so we can have actions tabs and a feedback window.
            GafferUI.Label(
                "This toolset is designed to make managing graphs simpler and more consistent",
                horizontalAlignment=GafferUI.Label.HorizontalAlignment.Center,
            )

            ############# TAB CONTAINER ##############
            with GafferUI.TabbedContainer( ) as self.__tab1Container:


                ############# LAYOUT TAB ##############
                with GafferUI.ListContainer(spacing=5, borderWidth=5) as self.__toolboxContainer1:
                    self.__tab1Container.setLabel(self.__toolboxContainer1, "Layout")

                    with GafferUI.ListContainer(spacing=1, borderWidth=1, orientation=GafferUI.ListContainer.Orientation.Horizontal) as self.__moverContainer1:

                        self.__moverButton = GafferUI.Button(text="Move Nodes")
                        self.__moverButton.clickedSignal().connect( self.__moverAction, scoped=False)

                        GafferUI.Label( "quadrant")
                        self.__moverQuadrantText = GafferUI.TextWidget( "S" )
                        GafferUI.Label( "x")
                        self.__moverDirectionX = GafferUI.NumericWidget( 10 )
                        GafferUI.Label( "y")
                        self.__moverDirectionY = GafferUI.NumericWidget( 10  )
                        GafferUI.Label( "include selection")
                        self.__moverIncludeSelection = GafferUI.BoolWidget( checked=True, displayMode=GafferUI.BoolWidget.DisplayMode.CheckBox  )

                    self.__divider1 = GafferUI.Divider(GafferUI.Divider.Orientation.Horizontal)

                ############# COLOUR TAB ##############
                with GafferUI.ListContainer(spacing=5, borderWidth=5) as self.__toolboxContainer2:
                    self.__tab1Container.setLabel(self.__toolboxContainer2, "Colour")


                    ############# COLOUR GRID ##############
                    with GafferUI.GridContainer() as self.__colorGrid:
                        gridSize = (6,6)
                        for i in range(0, gridSize[0]):
                            for j in range(0, gridSize[1]):
                                HSV = imath.Color3f( (1.0 / gridSize[0]) * i, 0.5, (1.0 / gridSize[1]) * j)
                                RGB = HSV.hsv2rgb()
                                self.__colorGrid[i, j] = GafferUI.Button(text=( str(round(RGB[0],2) ) + " " + str(round(RGB[1],2) ) + " " + str(round(RGB[2], 2) ) ) )

                                # somehow set the color of the buttons
                                # later I will need to get these colours from the button to set the node colours




                        for d in dir (self.__colorGrid[0,0]):
                            print d

                        # self.__colorGrid[0, 0].setHasFrame( True )
                        # self.__colorGrid[0,0]._setStyleSheet = QtGui.QColor(100, 10, 50 )
                        # dir (self.__colorGrid[0,0]._qtColor)
                        # QtGui.QPalette( QtWidgets.QApplication.instance().palette(self._qtWidget()))
                        # self.__colorGrid[0,0]._Button__palette.setColor(QtGui.QPalette.Enabled, QtGui.QPalette.Light, QtGui.QColor(100, 10, 50 ))
                        # self.__colorGrid[0, 0]._Button__palette.setColor(QtGui.QPalette.Light, QtGui.QColor(100, 10, 50))
                        # self._qtWidget().setPalette(self.__colorGrid[0,0]._Button__palette)


                    GafferUI.Label("Some test buttons 2")
                    # create action buttons
                    self.__buttonTest3 = GafferUI.Button(text="my button1")
                    self.__buttonTest3.clickedSignal().connect(self.__button1Action, scoped=False)

                    self.__divider1 = GafferUI.Divider(GafferUI.Divider.Orientation.Horizontal)

                    self.__buttonTest4 = GafferUI.Button(text="my button2")
                    self.__buttonTest4.clickedSignal().connect(self.__button2Action, scoped=False)


        ############# FEEDBACK WINDOW ##############
        with self.__splittable:

            self.__feedbackWidget = GafferUI.MultiLineTextWidget(
                text="Toolbox Feedback",
                editable=False,
                wrapMode=GafferUI.MultiLineTextWidget.WrapMode.None,
                role=GafferUI.MultiLineTextWidget.Role.Code,
            )

            self.__feedbackWidget._qtWidget().setProperty("gafferTextRole", "output")
            # how on earth do I change the colour?!


    def outputWidget(self):
        return self.__outputWidget

    def __button1Action(self, button):
        Toolbox.testButton( "yep, hit button 1")
        Toolbox.testFeedback(self.__feedbackWidget, "banana")
        Toolbox.buildABox( self )

    def __button2Action(self, button):
        Toolbox.testButton( "yep, hit button 2")
        Toolbox.testFeedback( self.__feedbackWidget, "apple" )
        Toolbox.actionOnSelection( self, self.__feedbackWidget)

    def __moverAction(self, button):
        Toolbox.testFeedback(self.__feedbackWidget, "yep, hit mover button")
        Toolbox.moveNodes(
            self,
            self.__moverQuadrantText.getText(),
            (self.__moverDirectionX.getValue(), self.__moverDirectionY.getValue()),
            includeSourceNode=self.__moverIncludeSelection.getState()
        )




GafferUI.Editor.registerType("Toolbox", ToolboxUI)
