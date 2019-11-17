import GafferUI
from Toolbox import ToolboxUI

layouts = GafferUI.Layouts.acquire( application )

# register the editors we want to be available to the user

layouts.registerEditor( "Toolbox" )
