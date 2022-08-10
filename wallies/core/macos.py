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


OPTIONS = {
    NSWorkspaceDesktopImageScalingKey: NSImageScaleProportionallyUpOrDown,
    NSWorkspaceDesktopImageAllowClippingKey: True
}

# optDict = NSDictionary.dictionaryWithObjects_forKeys_([NSImageScaleProportionallyUpOrDown, fillColor], [NSWorkspaceDesktopImageScalingKey,NSWorkspaceDesktopImageFillColorKey]);

# get shared workspace
ws = NSWorkspace.sharedWorkspace()


def get_screen():
    for screen in NSScreen.screens():
        yield screen


def set_wallpapper(screen, image_path: Path):
    url = NSURL.fileURLWithPath_(image_path.as_posix())
    (result, error) = ws.setDesktopImageURL_forScreen_options_error_(
        url, screen, OPTIONS, None)
    return result, error
