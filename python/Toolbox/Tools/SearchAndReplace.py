import GafferUI


def searchAndReplace( editor, search, replace, searchType, searchScope ):

    print  search, replace, searchType, searchScope

    scriptNode = GafferUI.Editor.scriptNode( editor )


    searchNodes = []
    if searchScope == "In Selected Nodes":

        searchNodes = scriptNode.selection()

    elif searchScope == "In Gaffer Scene":

        # need to get all nodes in node viewer
        #children = parent.children(Gaffer.Node)
        searchNodes = []
    else:

        return

    if len(searchNodes) == 0:
         print "No nodes to search in"
         return

  #  for child in children: