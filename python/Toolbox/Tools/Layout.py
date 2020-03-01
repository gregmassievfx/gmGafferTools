import Gaffer
import GafferUI
import GafferScene
import imath
import Toolbox

def selectNodes( editor, quadrant):

    scriptNode = GafferUI.Editor.scriptNode( editor)

    selection = scriptNode.selection()

    if len(selection) == 0:
         print "nothing selected"
         return

    sourceNode = selection[0]
    sX = sourceNode["__uiPosition"].getValue()[0]
    sY = sourceNode["__uiPosition"].getValue()[1]

    parent = sourceNode.parent()
    children = parent.children( Gaffer.Node )

    for child in children:

        cX = child["__uiPosition"].getValue()[0]
        cY = child["__uiPosition"].getValue()[1]

        if quadrant == "NW" and cX < sX and cY > sY:

            selection.add( child )

        elif quadrant == "N" and cY > sY:

            selection.add( child )

        elif quadrant == "NE" and cX > sX and cY > sY:

            selection.add( child )

        elif quadrant == "W" and cX < sX:

            selection.add( child )

        elif quadrant == "E" and cX > sX:

            selection.add( child )

        elif quadrant == "SW" and cX < sX and cY < sY:

            selection.add( child )

        elif quadrant == "S" and cY < sY:

            selection.add( child )

        elif quadrant == "SE" and cX > sX and cY < sY:

            selection.add( child )



def moveNodes(editor, quadrant ):
    """Moves nodes in a consistent way for clean layout"""

    scriptNode = GafferUI.Editor.scriptNode( editor )

    selection = scriptNode.selection()

    offset = 10

    if len(selection) == 0:
        return

    with Gaffer.UndoScope( scriptNode ):
        
        for node in selection:

            nodePosition = node["__uiPosition"].getValue()

            if quadrant == "NW":

                node["__uiPosition"].setValue(imath.V2f((nodePosition[0] - offset), (nodePosition[1] + offset)))

            elif quadrant == "N":

                node["__uiPosition"].setValue(imath.V2f((nodePosition[0]), (nodePosition[1] + offset)))

            elif quadrant == "NE":

                node["__uiPosition"].setValue(imath.V2f((nodePosition[0] + offset), (nodePosition[1] + offset)))

            elif quadrant == "W":

                node["__uiPosition"].setValue(imath.V2f((nodePosition[0] - offset), (nodePosition[1])))

            elif quadrant == "E":

                node["__uiPosition"].setValue(imath.V2f((nodePosition[0] + offset), (nodePosition[1])))

            elif quadrant == "SW":

                node["__uiPosition"].setValue(imath.V2f((nodePosition[0] - offset), (nodePosition[1] - offset)))

            elif quadrant == "S":

                node["__uiPosition"].setValue(imath.V2f((nodePosition[0]), (nodePosition[1] - offset)))

            elif quadrant == "SE":

                node["__uiPosition"].setValue(imath.V2f((nodePosition[0] + offset), (nodePosition[1] - offset)))



def setNodeColourFromSwatch( editor, button ):

    scriptNode = GafferUI.Editor.scriptNode( editor )

    selection = scriptNode.selection()

    if len(selection) == 0:
        return

    with Gaffer.UndoScope(scriptNode):

        for node in selection:

            swatchColour = button.getColor()
            colour = imath.Color3f( swatchColour[0], swatchColour[1], swatchColour[2] )

            Gaffer.Metadata.registerValue(node, "nodeGadget:color",  colour )
