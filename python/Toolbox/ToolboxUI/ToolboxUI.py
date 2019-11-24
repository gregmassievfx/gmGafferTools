import IECore

import Gaffer
import GafferUI

import Toolbox

class ToolboxUI(GafferUI.Editor):

    def __init__( self, scriptNode, **kw):
        # create main two part container (top for actions, bottom for feedback)
        self.__splittable = GafferUI.SplitContainer( borderWidth = 2)
        GafferUI.Editor.__init__( self, self.__splittable, scriptNode, **kw)

        with self.__splittable:
            # create splittable container so we can have actions tabs and a feedback window.

            with GafferUI.TabbedContainer( ) as self.__tab1Container:
                # create tabbed container for action buttons

                with GafferUI.ListContainer(spacing=5, borderWidth=5) as self.__toolboxContainer1:
                    self.__tab1Container.setLabel(self.__toolboxContainer1, "test")

                    GafferUI.Label( "Some test buttons")
                    # create action buttons
                    self.__buttonTest1 = GafferUI.Button(text="my button1")
                    self.__buttonTest1.clickedSignal().connect( self.__button1Action, scoped=False)

                    self.__divider1 = GafferUI.Divider(GafferUI.Divider.Orientation.Horizontal)

                    self.__buttonTest2 = GafferUI.Button(text="my button2")
                    self.__buttonTest2.clickedSignal().connect( self.__button2Action, scoped=False )

                with GafferUI.ListContainer(spacing=5, borderWidth=5) as self.__toolboxContainer2:
                    self.__tab1Container.setLabel(self.__toolboxContainer2, "test2")

                    GafferUI.Label("Some test buttons 2")
                    # create action buttons
                    self.__buttonTest3 = GafferUI.Button(text="my button1")
                    self.__buttonTest3.clickedSignal().connect(self.__button1Action, scoped=False)

                    self.__divider1 = GafferUI.Divider(GafferUI.Divider.Orientation.Horizontal)

                    self.__buttonTest4 = GafferUI.Button(text="my button2")
                    self.__buttonTest4.clickedSignal().connect(self.__button2Action, scoped=False)


        # create feedback text window#################################
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


GafferUI.Editor.registerType("Toolbox", ToolboxUI)
