import IECore

import Gaffer
import GafferUI

from Qt import QtWidgets
from Qt import QtCore

import Toolbox

class ToolboxUI(GafferUI.Editor):

    def __init__( self, scriptNode, **kw):
        # create main two part container (top for actions, bottom for feedback)
        self.__splittable = GafferUI.SplitContainer( borderWidth = 2)
        GafferUI.Editor.__init__( self, self.__splittable, scriptNode, **kw)

        with self.__splittable:
            # create main area for action buttons
            self.__toolboxContainer = GafferUI.ListContainer( spacing=5, borderWidth=5 )

            with self.__toolboxContainer:

                GafferUI.Label( "Some test buttons")
                # create action buttons
                self.__buttonTest1 = GafferUI.Button(text="my button1")
                self.__buttonTest1.clickedSignal().connect( self.__button1Action() )

                self.__divider1 = GafferUI.Divider(GafferUI.Divider.Orientation.Horizontal)

                self.__buttonTest2 = GafferUI.Button(text="my button2")
                self.__buttonTest2.clickedSignal().connect( self.__button2Action() )

        # create feedback text window#################################
        with self.__splittable:

            self.__outputWidget = GafferUI.MultiLineTextWidget(
                text="Toolbox output",
                editable=False,
                wrapMode=GafferUI.MultiLineTextWidget.WrapMode.None,
                role=GafferUI.MultiLineTextWidget.Role.Code,
            )
            self.__outputWidget._qtWidget().setProperty("gafferTextRole", "output")
            self.__outputWidget.appendText(str("banana"))

    def outputWidget(self):
        return self.__outputWidget

    def __button1Action(self):
        print "yep, hit button 1"
        Toolbox.test()
        # self.__outputWidget.appendText( str("banana") )

    def __button2Action(self):
        print "yep, hit button 2"
        Toolbox.test()


GafferUI.Editor.registerType("Toolbox", ToolboxUI)


# class _MessageHandler(IECore.MessageHandler):
#
#     def __init__(self, textWidget):
#         IECore.MessageHandler.__init__(self)
#
#         self.__textWidget = textWidget
#
#     def handle(self, level, context, message):
#         html = formatted = "<h1 class='%s'>%s : %s </h1><pre class='message'>%s</pre><br>" % (
#             IECore.Msg.levelAsString(level),
#             IECore.Msg.levelAsString(level),
#             context,
#             message
#         )
#         self.__textWidget.appendHTML(html)
#         # update the gui so messages are output as they occur, rather than all getting queued
#         # up till the end.
#         QtWidgets.QApplication.instance().processEvents(QtCore.QEventLoop.ExcludeUserInputEvents)
