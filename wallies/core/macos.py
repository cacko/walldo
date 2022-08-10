#!/usr/bin/python

from AppKit import (
    NSWorkspace, 
    NSScreen, 
    NSWorkspaceDesktopImageScalingKey, 
    NSWorkspaceDesktopImageAllowClippingKey, 
    NSImageScaleProportionallyUpOrDown,
    NSImageScaleProportionallyDown
)
from Foundation import NSURL
from pathlib import Path

paths = [
    Path(__file__).parent / "3.png",
    Path(__file__).parent / "4.png",
]

print(paths)

# make image options dictionary
# we just make an empty one because the defaults are fine
options = {
    # NSWorkspaceDesktopImageScalingKey: NSImageScaleProportionallyUpOrDown,
    # NSWorkspaceDesktopImageAllowClippingKey: True
}

# optDict = NSDictionary.dictionaryWithObjects_forKeys_([NSImageScaleProportionallyUpOrDown, fillColor], [NSWorkspaceDesktopImageScalingKey,NSWorkspaceDesktopImageFillColorKey]);

# get shared workspace
ws = NSWorkspace.sharedWorkspace()

# iterate over all screens
for screen in NSScreen.screens():
    # tell the workspace to set the desktop picture
    url = NSURL.fileURLWithPath_(paths.pop(0).as_posix())
    print(screen, url)
    (result, error) = ws.setDesktopImageURL_forScreen_options_error_(
        url, screen, options, None)
    print(result, error)
