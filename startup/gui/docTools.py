##########################################################################
#
#  Copyright (c) 2019, Cinesite VFX Ltd. All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#      * Redistributions of source code must retain the above
#        copyright notice, this list of conditions and the following
#        disclaimer.
#
#      * Redistributions in binary form must reproduce the above
#        copyright notice, this list of conditions and the following
#        disclaimer in the documentation and/or other materials provided with
#        the distribution.
#
#      * Neither the name Cinesite VFX nor the names of any other contributors
#      to this software may be used to endorse or promote products derived from
#      this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
##########################################################################

# Some helpers for those making Gaffer example scenes to be included with the
# distribution. Based on:
#
#   https://github.com/GafferHQ/gaffer/wiki/Examples-Style-Guide
#
#  - Right-click Node menu tools to conform Backdrop color/title/size/etc...
#  - Right-click Node menu tool to enclose the selection in a Backdrop.
#  - Node create menu conveniences for title/tip/note/general backdrops.

import Gaffer
import GafferUI

import functools
import imath


# Used by creation/conform tools

backdropDefaults = {

	"title" : {
		"color": None,
		"title" : "Example: ",
		"width" : 40
	},

	"tip" : {
		"color" : imath.Color3f( 0.3, 0.5, 0.4605 ),
		"title" : "Tip: ",
		"width" : 30
	},

	"note" : {
		"color" : imath.Color3f( 0.3479, 0.4386, 0.5 ),
		"title" : "Note: ",
		"width" : 30
	},

	"general" : {
		"color": None,
		"width" : 40
	}
}

# Just using a default node size for those without __uiBound. This should
# really go ask its NodeGadget.
defaultNodeSize = imath.Box2f( imath.V2f( 0.0 ), imath.V2f( 10, 5 ) )


def conform( node, type_ = "default" ) :
	"""
	Conform a Backdrop's color, title prefix and width based on the style guide.
	"""

	with Gaffer.UndoScope( node.ancestor( Gaffer.ScriptNode ) ) :

		defaults = backdropDefaults.get( type_, {} )

		setColor( node, defaults.get( "color", None ) )

		w =  defaults.get( "width", None )
		if w :
			conformWidth( node, w )

		t = defaults.get( "title", "" )
		if t :
			existingT = node["title"].getValue().split( ":" )[-1].strip()
			if existingT == "Title" :
				existingT = ""

			if not existingT.startswith( t ) :
				t += existingT
				node["title"].setValue( t )


def conformWidth( node, width = 40 ) :
	"""
	Conform the width of any node with a __uiBound to the supplied dimension.
	"""

	with Gaffer.UndoScope( node.ancestor( Gaffer.ScriptNode ) ) :

		existingBound = node["__uiBound"].getValue()
		min_ = existingBound.min()
		max_ = existingBound.max()
		node["__uiBound"].setValue( imath.Box2f( min_, imath.V2f( min_.x + width, max_.y ) ) )


def encloseSelectionWithBackdrop( parent, padding = 2 ) :
	"""
	Roughly encloses the selection in a backdrop node. If there are other
	backdrops in the selection, they will be re-layered on top of the new one.
	"""

	scriptNode = parent.ancestor( Gaffer.ScriptNode ) or parent

	sel = scriptNode.selection()
	if len(sel) == 0 :
		return

	with Gaffer.UndoScope( scriptNode ) :

		extents = imath.Box2f()
		extents.makeEmpty()

		color = None
		existingBackdrops = []

		for s in sel :
			p = s["__uiPosition"].getValue()
			b = s["__uiBound"].getValue() if "__uiBound" in s else defaultNodeSize
			extents.extendBy( p + b.min() )
			extents.extendBy( p + b.max() )
			if isinstance( s, Gaffer.Backdrop ) :
				color = Gaffer.Metadata.value( s, "nodeGadget:color" )
				existingBackdrops.append( s )

		extents.extendBy( extents.min() - imath.V2f( padding ) )
		extents.extendBy( extents.max() + imath.V2f( padding ) )

		# We need to remove the existing backdrops, add the underlying one
		# then add the old ones back, otherwise the new one will be on top
		for b in existingBackdrops :
			parent.removeChild( b )

		backdrop = Gaffer.Backdrop()
		backdrop["title"].setValue( "" )
		setColor( backdrop, color )

		backdrop.addChild( Gaffer.V2fPlug( "__uiPosition", defaultValue = imath.V2f( 0, 0 ), flags = Gaffer.Plug.Flags.Default | Gaffer.Plug.Flags.Dynamic, ) )
		backdrop.addChild( Gaffer.Box2fPlug( "__uiBound", defaultValue = imath.Box2f( imath.V2f( -10, -10 ), imath.V2f( 10, 10 ) ), flags = Gaffer.Plug.Flags.Default | Gaffer.Plug.Flags.Dynamic, ) )
		backdrop["__uiPosition"].setValue( extents.min() )
		backdrop["__uiBound" ].setValue( imath.Box2f( imath.V2f( 0.0 ), extents.max() - extents.min() ) )

		parent.addChild( backdrop )

		for b in existingBackdrops :
			parent.addChild( b )

	return backdrop


def setColor( node, color = None ) :

	with Gaffer.UndoScope( node.ancestor( Gaffer.ScriptNode ) ) :

		if color :
			Gaffer.Metadata.registerValue( node, "nodeGadget:color", color )
		else :
			Gaffer.Metadata.deregisterValue( node, "nodeGadget:color" )


def newBackdrop( parent, type_ = "default" ) :
	"""
	Creates a new backdrop, initializing it with default tile, width and color
	based on the supplied type_ - @see backdropDefaults.
	"""

	with Gaffer.UndoScope( parent.ancestor( Gaffer.ScriptNode ) ) :

		b = Gaffer.Backdrop()
		b.addChild( Gaffer.Box2fPlug( "__uiBound", defaultValue = imath.Box2f( imath.V2f( -10, -10 ), imath.V2f( 10, 10 ) ), flags = Gaffer.Plug.Flags.Default | Gaffer.Plug.Flags.Dynamic, ) )
		conform( b, type_ )
		parent.addChild( b )

		GafferUI.NodeEditor.acquire( b, floating = True )

		return b


# Right-click menu tools

def appendGraphEditorContextMenu( graphEditor, node, menuDefinition ) :

	menuDefinition.append( "/Backdrop Divider", { "divider" : True } )

	if isinstance( node, Gaffer.Backdrop ) :

		menuDefinition.append( "/Backdrop/Set Color/Title", { "command" : functools.partial( setColor, node, backdropDefaults["title"]["color"] ) } )
		menuDefinition.append( "/Backdrop/Set Color/Note", { "command" : functools.partial( setColor, node, backdropDefaults["note"]["color"] ) } )
		menuDefinition.append( "/Backdrop/Set Color/Tip", { "command" : functools.partial( setColor, node, backdropDefaults["tip"]["color"] ) } )
		menuDefinition.append( "/Backdrop/Set Color/General", { "command" : functools.partial( setColor, node,  backdropDefaults["general"]["color"] ) } )

		menuDefinition.append( "/Backdrop/Set Width/20", { "command" : functools.partial( conformWidth, node, 20 ) } )
		menuDefinition.append( "/Backdrop/Set Width/30", { "command" : functools.partial( conformWidth, node, 30 ) } )
		menuDefinition.append( "/Backdrop/Set Width/40", { "command" : functools.partial( conformWidth, node, 40 ) } )

		menuDefinition.append( "/Backdrop/Conform Divider", { "divider" : True } )

		menuDefinition.append( "/Backdrop/Conform/Title", { "command" : functools.partial( conform, node, "title") } )
		menuDefinition.append( "/Backdrop/Conform/Note", { "command" : functools.partial( conform, node, "note" ) } )
		menuDefinition.append( "/Backdrop/Conform/Tip", { "command" : functools.partial( conform, node, "tip" ) } )
		menuDefinition.append( "/Backdrop/Conform/General", { "command" : functools.partial( conform, node, "general" ) } )

		menuDefinition.append( "/Backdrop/Tools Divider", { "divider" : True } )

	menuDefinition.append( "/Backdrop/Enclose Selection", { "command" : functools.partial( encloseSelectionWithBackdrop, node.parent() ) } )

GafferUI.GraphEditor.nodeContextMenuSignal().connect( appendGraphEditorContextMenu, scoped = False )


# Creation conveniences for making new, pre-configured backdrops

def makeDocBackdrop( category, menu ) :
	graphEditor = menu.ancestor( GafferUI.GraphEditor )
	newBackdrop( graphEditor.graphGadget().getRoot(), category )

nodeMenu = GafferUI.NodeMenu.acquire( application )
nodeMenu.definition().append( "/Docs/Backdrop (title)", { "command": functools.partial( makeDocBackdrop, "title" ) } )
nodeMenu.definition().append( "/Docs/Backdrop (general)", { "command": functools.partial( makeDocBackdrop, "general" ) } )
nodeMenu.definition().append( "/Docs/Backdrop (note)", { "command": functools.partial( makeDocBackdrop, "note" ) } )
nodeMenu.definition().append( "/Docs/Backdrop (tip)", { "command": functools.partial( makeDocBackdrop, "tip" ) } )
