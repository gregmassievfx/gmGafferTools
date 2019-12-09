import Gaffer
import GafferUI
import GafferScene
import imath
import Toolbox


def moveNodes(button, quadrant, offset, includeSourceNode=False):
    """Moves nodes in a consistent way for clean layout"""

    scriptNode = GafferUI.Editor.scriptNode(button)
    sel = scriptNode.selection()
    if len(sel) == 0:
        return

    sourceNode = sel[0]



    print "XXXXXXXXXXXXX", sourceNode, type(sourceNode)

    sourceNodePosition = sourceNode["__uiPosition"].getValue()
    parent = sourceNode.parent()


    with Gaffer.UndoScope(parent):

        children = parent.children()

        for child in children:
            if type(child) == Gaffer.Box:

                if includeSourceNode == False and child == sourceNode:

                    pass

                else:

                    childPosition = child["__uiPosition"].getValue()

                    if quadrant == "N" and childPosition[1] >= sourceNodePosition[1]:

                        child["__uiPosition"].setValue( imath.V2f((childPosition[0]), (childPosition[1] + offset[1])))

                    elif quadrant == "NE" and childPosition[0] >= sourceNodePosition[0] and childPosition[1] >= sourceNodePosition[1]:

                        child["__uiPosition"].setValue( imath.V2f((childPosition[0] + offset[0]), (childPosition[1] + offset[1])))

                    elif quadrant == "E" and childPosition[0] >= sourceNodePosition[0]:

                        child["__uiPosition"].setValue( imath.V2f((childPosition[0] + offset[0]), (childPosition[1])))

                    elif quadrant == "SE" and childPosition[0] >= sourceNodePosition[0] and childPosition[1] <= sourceNodePosition[1]:

                        child["__uiPosition"].setValue( imath.V2f((childPosition[0] + offset[0]), (childPosition[1] - offset[1])))

                    elif quadrant == "S" and childPosition[1] <= sourceNodePosition[1]:

                        child["__uiPosition"].setValue( imath.V2f((childPosition[0]), (childPosition[1] - offset[1])))

                    elif quadrant == "SW" and childPosition[0] <= sourceNodePosition[0] and childPosition[1] <= sourceNodePosition[1]:

                        child["__uiPosition"].setValue( imath.V2f((childPosition[0] - offset[0]), (childPosition[1] - offset[1])))

                    elif quadrant == "W" and childPosition[0] <= sourceNodePosition[0]:

                        child["__uiPosition"].setValue( imath.V2f((childPosition[0] - offset[0]), (childPosition[1])))

                    elif quadrant == "NW" and childPosition[0] <= sourceNodePosition[0] and childPosition[1] >= sourceNodePosition[1]:

                        child["__uiPosition"].setValue( imath.V2f((childPosition[0] - offset[0]), (childPosition[1] + offset[1])))


# moveNodes( root['Box1'], ["N",], (10,10), includeSourceNode=True)
# moveNodes( root['Box1'], ["NE",], (10,10), includeSourceNode=True)
# moveNodes( root['Box1'], ["E",], (10,10), includeSourceNode=True)
# moveNodes( root['Box1'], ["SE",], (10,10), includeSourceNode=True)
# moveNodes( root['Box1'], ["S",], (10,10), includeSourceNode=True)
# moveNodes( root['Box1'], ["SW",], (10,10), includeSourceNode=True)
# moveNodes( root['Box1'], ["W",], (10,10), includeSourceNode=True)
# moveNodes( root['Box1'], ["NW",], (10,10), includeSourceNode=True)
