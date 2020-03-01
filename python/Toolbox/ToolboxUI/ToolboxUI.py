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

                    directions = (
                        # direction, ascii, position
                        ( "NW", "\xf0\x9f\xa1\xbc", (1, 1)),
                        ( "N",  "\xf0\x9f\xa1\xb9", (2, 1)),
                        ( "NE", "\xf0\x9f\xa1\xbd", (3, 1)),
                        ( "W",  "\xf0\x9f\xa1\xb8", (1, 2)),
                        ( None, None, (2, 2)),
                        ( "E",  "\xf0\x9f\xa1\xba", (3, 2)),
                        ( "SW", "\xf0\x9f\xa1\xbf", (1, 3)),
                        ( "S",  "\xf0\x9f\xa1\xbb", (2, 3)),
                        ( "SE", "\xf0\x9f\xa1\xbe", (3, 3))
                    )


                    with GafferUI.GridContainer() as self.__moverGrid:
                        GafferUI.Label( "Select",  parenting={"index": (1,1)} )
                        GafferUI.Label( "      ",  parenting={"index": (2,1)} )
                        GafferUI.Label( "Move",  parenting={"index": (3,1)} )
                        GafferUI.Label("      ", parenting={"index": (4, 1)})


                        ############# SELECTOR ARROW GRID ##############
                        with GafferUI.GridContainer( parenting={"index": (1,2)} ) as self.__selectorGrid:

                            for direction in directions:

                                if direction[0] != None:

                                    GafferUI.Button( text=direction[1], parenting={ "index": (direction[2]) } )
                                    self.__selectorGrid[ direction[2] ]._qtWidget().setMinimumWidth(25)
                                    self.__selectorGrid[ direction[2] ]._qtWidget().setMaximumWidth(25)
                                    self.__selectorGrid[ direction[2] ]._qtWidget().setProperty( "myDirection", direction[0])
                                    self.__selectorGrid[ direction[2] ].clickedSignal().connect(self.__selectorAction, scoped=False)

                        ############# MOVER ARROW GRID ##############
                        with GafferUI.GridContainer( parenting={"index": (3,2)} ) as self.__moverGrid:

                            for direction in directions:

                                if direction[0] != None:

                                    GafferUI.Button( text=direction[1], parenting={ "index": (direction[2]) } )
                                    self.__moverGrid[ direction[2] ]._qtWidget().setMinimumWidth(25)
                                    self.__moverGrid[ direction[2] ]._qtWidget().setMaximumWidth(25)
                                    self.__moverGrid[ direction[2] ]._qtWidget().setProperty( "myDirection", direction[0])
                                    self.__moverGrid[ direction[2] ].clickedSignal().connect(self.__moverAction, scoped=False)

                        ############# SELECT/MOVE OPTIONS ##############
                        with GafferUI.ListContainer( orientation= GafferUI.ListContainer.Orientation.Vertical, parenting={"index": (5, 2)}) as self.__LayoutOptions:

                            self.__limitToBackdropsCheckbox = GafferUI.BoolWidget( text="Limit Selection to Backdrops", checked=True )
                            self.__extendBackdropsCheckbox = GafferUI.BoolWidget(text="Extend Backdrops", checked=True )


                ############# COLOUR TAB ##############
                with GafferUI.ListContainer(spacing=5, borderWidth=5) as self.__toolboxContainer2:
                    self.__tab1Container.setLabel(self.__toolboxContainer2, "Colour")


                    ############# COLOUR GRID ##############
                    with GafferUI.GridContainer() as self.__colorGrid:
                        gridSize = (10,5)
                        for i in range(0, gridSize[0]):
                            for j in range(0, gridSize[1]):
                                HSV = imath.Color4f( (1.0 / gridSize[0]) * float(i), 0.5, 1.0 - ((1.0 / gridSize[1]) * float(j)), 1.0)
                                RGB = HSV.hsv2rgb()
                                GafferUI.ColorSwatch (RGB , useDisplayTransform=False, parenting = {"index": (i,j)})
                                self.__colorGrid[i,j]._qtWidget().setMaximumHeight( 20 )
                                self.__colorGrid[i,j].buttonPressSignal().connect(self.__setColourAction, scoped=False)




                ############# SEARCH AND REPLACE TAB ##############
                with GafferUI.ListContainer(spacing=5, borderWidth=5) as self.__toolboxContainer3:
                    self.__tab1Container.setLabel(self.__toolboxContainer3, "Search and Replace")

                    spacing = 100
                    with GafferUI.ListContainer(spacing=5, borderWidth=5,orientation= GafferUI.ListContainer.Orientation.Horizontal)  as self.__searchList:

                        self.__searchLabel = GafferUI.Label("Search For", horizontalAlignment=GafferUI.Label.HorizontalAlignment.Right)
                        self.__searchLabel._qtWidget().setMinimumWidth(spacing)
                        self.__searchLabel._qtWidget().setMaximumWidth(spacing)
                        self.__searchWidget = GafferUI.TextWidget(text="myTest")

                    with GafferUI.ListContainer(spacing=5, borderWidth=5,orientation= GafferUI.ListContainer.Orientation.Horizontal)  as self.__replaceList:

                        self.__replaceLabel = GafferUI.Label("Replace With", horizontalAlignment=GafferUI.Label.HorizontalAlignment.Right)
                        self.__replaceLabel._qtWidget().setMinimumWidth(spacing)
                        self.__replaceLabel._qtWidget().setMaximumWidth(spacing)
                        self.__replaceWidget = GafferUI.TextWidget( text="banana")

                    with GafferUI.ListContainer(spacing=5, borderWidth=5, orientation=GafferUI.ListContainer.Orientation.Horizontal)  as self.__searchReplaceList:

                        self.__searchReplaceNodePlugsMenu = GafferUI.SelectionMenu()
                        self.__searchReplaceNodePlugsMenu.addItem("Node Names")
                        self.__searchReplaceNodePlugsMenu.addItem("Plug Values")
                        self.__searchReplaceNodePlugsMenu._qtWidget().setMinimumWidth(spacing)
                        self.__searchReplaceNodePlugsMenu._qtWidget().setMaximumWidth(spacing)

                        self.__searchReplaceScopeMenu = GafferUI.SelectionMenu()
                        self.__searchReplaceScopeMenu.addItem("In Selected Nodes")
                        self.__searchReplaceScopeMenu.addItem("In Gaffer Scene")
                        self.__searchReplaceScopeMenu._qtWidget().setMinimumWidth(spacing + 30)
                        self.__searchReplaceScopeMenu._qtWidget().setMaximumWidth(spacing + 30)

                        self.__searchReplaceButton = GafferUI.Button(text="Search and Replace")
                        self.__searchReplaceButton.clickedSignal().connect(self.__findReplaceAction, scoped=False)
                        self.__searchReplaceButton._qtWidget().setMaximumWidth(150)


    def __selectorAction(self , button ):

        Toolbox.selectNodes(self, button._qtWidget().property( "myDirection") )

    def __moverAction(self, button):

        Toolbox.moveNodes(self, button._qtWidget().property ("myDirection") )

    def __setColourAction( self, button, buttonEvent):

        Toolbox.setNodeColourFromSwatch( self, button )

    def __findReplaceAction(self, button):

        search = self.__searchWidget.getText()
        replace = self.__replaceWidget.getText()

        searchType = self.__searchReplaceNodePlugsMenu.getItem( self.__searchReplaceNodePlugsMenu.getCurrentIndex() )
        searchScope = self.__searchReplaceScopeMenu.getItem( self.__searchReplaceScopeMenu.getCurrentIndex() )

        Toolbox.searchAndReplace(self, search, replace, searchType, searchScope )





GafferUI.Editor.registerType("Toolbox", ToolboxUI)
