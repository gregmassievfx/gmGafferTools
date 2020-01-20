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


                    ############# ARROW GRID ##############
                    with GafferUI.GridContainer() as self.__colorGrid:
                        gridSize = (7,3)

                        self.__selectorNWButton = GafferUI.Button(text="\xf0\x9f\xa1\xbc", parenting={"index": (1, 1)})
                        self.__selectorNWButton.clickedSignal().connect(self.__selectorAction, scoped=False)
                        self.__selectorNButton =  GafferUI.Button(text="\xf0\x9f\xa1\xb9", parenting={"index": (2, 1)})
                        self.__selectorNButton.clickedSignal().connect(self.__selectorAction, scoped=False)
                        self.__selectorNEButton = GafferUI.Button(text="\xf0\x9f\xa1\xbd", parenting={"index": (3, 1)})
                        self.__selectorNEButton.clickedSignal().connect(self.__selectorAction, scoped=False)

                        self.__selectorWButton =  GafferUI.Button(text="\xf0\x9f\xa1\xb8", parenting={"index": (1, 2)})
                        self.__selectorWButton.clickedSignal().connect(self.__selectorAction, scoped=False)
                        self.__selectorEButton =  GafferUI.Button(text="\xf0\x9f\xa1\xba", parenting={"index": (3, 2)})
                        self.__selectorEButton.clickedSignal().connect(self.__selectorAction, scoped=False)

                        self.__selectorSWButton = GafferUI.Button(text="\xf0\x9f\xa1\xbf", parenting={"index": (1, 3)})
                        self.__selectorSWButton.clickedSignal().connect(self.__selectorAction, scoped=False)
                        self.__selectorSButton =  GafferUI.Button(text="\xf0\x9f\xa1\xbb", parenting={"index": (2, 3)})
                        self.__selectorSButton.clickedSignal().connect(self.__selectorAction, scoped=False)
                        self.__selectorSEButton = GafferUI.Button(text="\xf0\x9f\xa1\xbe", parenting={"index": (3, 3)})
                        self.__selectorSEButton.clickedSignal().connect(self.__selectorAction, scoped=False)

                        GafferUI.Label(" select ", parenting={"index": (2, 2)})
                        GafferUI.Label("  move  ", parenting={"index": (6, 2)})

                        #spacer between selector and mover buttons
                        GafferUI.Label("              ", parenting={"index": (4, 1)} )

                        self.__moverNWButton = GafferUI.Button(text="\xf0\x9f\xa1\xbc", parenting={"index": (5, 1)})
                        self.__moverNButton =  GafferUI.Button(text="\xf0\x9f\xa1\xb9", parenting={"index": (6, 1)})
                        self.__moverNEButton = GafferUI.Button(text="\xf0\x9f\xa1\xbd", parenting={"index": (7, 1)})

                        self.__moverWButton =  GafferUI.Button(text="\xf0\x9f\xa1\xb8", parenting={"index": (5, 2)})
                        self.__moverEButton =  GafferUI.Button(text="\xf0\x9f\xa1\xba", parenting={"index": (7, 2)})

                        self.__moverSWButton = GafferUI.Button(text="\xf0\x9f\xa1\xbf", parenting={"index": (5, 3)})
                        self.__moverSButton =  GafferUI.Button(text="\xf0\x9f\xa1\xbb", parenting={"index": (6, 3)})
                        self.__moverSEButton = GafferUI.Button(text="\xf0\x9f\xa1\xbe", parenting={"index": (7, 3)})



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
                        gridSize = (7,7)
                        for i in range(0, gridSize[0]):
                            for j in range(0, gridSize[1]):
                                HSV = imath.Color4f( (1.0 / gridSize[0]) * float(i), 0.6, 1.0 - ((1.0 / gridSize[1]) * float(j)), 1.0)
                                RGB = HSV.hsv2rgb()
                                GafferUI.ColorSwatch(RGB, useDisplayTransform=False, parenting = {"index": (i,j)})

                                # later I will need to get these colours from the button to set the node colours


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

    def __selectorAction(self , button ):

        #Toolbox.selectNodes(self, "N")
        if button == self.__selectorNWButton:

            Toolbox.selectNodes( self, "NW")

        elif button == self.__selectorNButton:

            Toolbox.selectNodes(self, "N")

        elif button == self.__selectorNEButton:

            Toolbox.selectNodes(self, "NE")

        elif button == self.__selectorWButton:

            Toolbox.selectNodes(self, "W")

        elif button == self.__selectorEButton:

            Toolbox.selectNodes(self, "E")

        elif button == self.__selectorSWButton:

            Toolbox.selectNodes(self, "SW")

        elif button == self.__selectorSButton:

            Toolbox.selectNodes(self, "S")

        elif button == self.__selectorSEButton:

            Toolbox.selectNodes(self, "SE")



GafferUI.Editor.registerType("Toolbox", ToolboxUI)
