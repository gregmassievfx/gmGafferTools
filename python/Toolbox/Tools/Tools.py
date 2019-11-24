import Gaffer
import GafferUI
import GafferScene
import imath


def testButton( output ):
    print output

def testFeedback( feedbackWidget, output):
    feedbackWidget.appendText(str(output))


def buildABox( source ):

    # from Tom's blog post, just using as an example

    # The box
    root = GafferUI.Editor.scriptNode( source )

    box = Gaffer.Box( "GroundPlane" )
    Gaffer.Metadata.registerValue( box, 'icon', None )
    root.addChild( box )

    # Internal network

    plane = GafferScene.Plane( "Plane" )
    plane["transform"]["rotate"].setValue( imath.V3f( -90, 0, 0 ) )
    plane["dimensions"].setValue( imath.V2f( 100, 100 ) )
    plane["name"].setValue( "ground" )

    freeze = GafferScene.FreezeTransform( "FreezeTransform" )

    parent = GafferScene.Parent( "Parent" )
    parent["parent"].setValue("/")

    freeze["in"].setInput( plane["out"] )
    parent["child"].setInput( freeze["out"] )

    box.addChild( plane )
    box.addChild( freeze )
    box.addChild( parent )

    # Promote i/o
    boxInPlug = Gaffer.BoxIO.promote( parent["in"] )
    boxOutPlug = Gaffer.BoxIO.promote( parent["out"] )

    # Promote useful Node Editor plugs
    Gaffer.BoxIO.promote( plane["name"] )
    Gaffer.BoxIO.promote( parent["parent"] )
    Gaffer.BoxIO.promote( plane["divisions"] )
    Gaffer.BoxIO.promote( plane["dimensions"] )

    # Add a passthrough
    boxOutNode = boxOutPlug.getInput().node()
    boxInNode = boxInPlug.outputs()[0].node()
    boxOutNode["passThrough"].setInput( boxInNode["out"] )

def actionOnSelection( source, feedbackWidget ):

    scriptNode = GafferUI.Editor.scriptNode(source)

    sel = scriptNode.selection()
    if len(sel) == 0:
        return
    for s in sel:
        feedbackWidget.appendText(str( s ) )
