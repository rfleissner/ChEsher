
__author__="Reinhard"
__date__ ="$Sep 14, 2014 11:22:58 AM$"

lineSet = """
:ObjectType CLine{0}DSet
:FullFileName {1}
:ClipContours 1
:IsMonochrome 1
:IsTransparent 0
:ShowNodeLabels 0
:ShowElementLabels 0
:FontName Arial
:FontSize 9
:IsFontBold 0
:IsFontItalics 0
:IsFontUnderline 0
:BaseColour {2}
:DrawingStyle 1
:LineStyle 0
:LineWidth 2.000000
:PointStyle 0
:PointSize 4.000000
:IsVisible 1
:IsAnimated 0
:StartColourScale
:Origin 80.000000 55.000000
:Extent 15.000000 40.000000
:FontName Arial
:FontColour 000000
:IsFontBold 0
:IsFontItalics 0
:IsFontUnderline 0
:BackgroundOn 1
:BackgroundColour 0xffffff
:BorderOn 1
:BorderWidth 2
:BorderColour 000000
:IsAspectRatioLocked 1
:IsVisible 0
:Title {3}
:SubTitle
:AboveString Above
:BelowString Below
:LabelFormat 0
:SignificantDigits 3
:IsRangeLabelsOn 0
:RangeLabelSeparator to
:LevelsAreIndex 0
:ScaleLevelCount 10
:ScaleLevelBasis 0
:ScaleMin 0.000000
:ScaleMax 0.000000
:ScaleInterval 0.000000
:ScaleLevel 0 0.000000
:ScaleLevel 1 0.000000
:ScaleLevel 2 0.000000
:ScaleLevel 3 0.000000
:ScaleLevel 4 0.000000
:ScaleLevel 5 0.000000
:ScaleLevel 6 0.000000
:ScaleLevel 7 0.000000
:ScaleLevel 8 0.000000
:ScaleLevel 9 0.000000
:ScaleColourBasis 1
:ScaleColour 0 0xff0000
:ScaleColour 1 0xff7100
:ScaleColour 2 0xffe200
:ScaleColour 3 0xaaff00
:ScaleColour 4 0x38ff00
:ScaleColour 5 0x00ff38
:ScaleColour 6 0x00ffaa
:ScaleColour 7 0x00e2ff
:ScaleColour 8 0x0071ff
:ScaleColour 9 0x0000ff
:EndObjectType CColourScale
:ScaleZ 1.000000
:ShiftZ 0.000000
:CurrentFrame 1
:EndObjectType CLine{0}DSet
"""

meshScalar = """
:ObjectType CT32DScalar
:FullFileName {0}
:ClipContours 1
:IsMonochrome 1
:IsTransparent 0
:ShowNodeLabels 0
:ShowElementLabels 0
:FontName Arial
:FontSize 9
:IsFontBold 0
:IsFontItalics 0
:IsFontUnderline 0
:BaseColour {1}
:DrawingStyle 0
:LineStyle 0
:LineWidth 1.000000
:PointStyle 0
:PointSize 3.000000
:IsVisible 1
:IsAnimated 0
:StartColourScale
:Origin 80.000000 55.000000
:Extent 15.000000 40.000000
:FontName Arial
:FontColour 000000
:IsFontBold 0
:IsFontItalics 0
:IsFontUnderline 0
:BackgroundOn 1
:BackgroundColour 0xffffff
:BorderOn 1
:BorderWidth 2
:BorderColour 000000
:IsAspectRatioLocked 1
:IsVisible 0
:Title {2}
:SubTitle
:AboveString Above
:BelowString Below
:LabelFormat 0
:SignificantDigits 3
:IsRangeLabelsOn 0
:RangeLabelSeparator to
:LevelsAreIndex 0
:ScaleLevelCount 10
:ScaleLevelBasis 0
:ScaleMin 0
:ScaleMax 10
:ScaleInterval 1.800000
:ScaleLevel 0 0.000000
:ScaleLevel 1 1.000000
:ScaleLevel 2 2.000000
:ScaleLevel 3 3.000000
:ScaleLevel 4 4.000000
:ScaleLevel 5 5.000000
:ScaleLevel 6 6.000000
:ScaleLevel 7 7.000000
:ScaleLevel 8 8.000000
:ScaleLevel 9 9.000000
:ScaleColourBasis 1
:ScaleColour 0 0xff0000
:ScaleColour 1 0xff7100
:ScaleColour 2 0xffe200
:ScaleColour 3 0xaaff00
:ScaleColour 4 0x38ff00
:ScaleColour 5 0x00ff38
:ScaleColour 6 0x00ffaa
:ScaleColour 7 0x00e2ff
:ScaleColour 8 0x0071ff
:ScaleColour 9 0x0000ff
:EndObjectType CColourScale
:ScaleZ 1.000000
:ShiftZ 0.000000
:CurrentFrame 1
:EndObjectType CT32DScalar
"""

view2d = """
:ViewType CEnSim2DView
:Title 2D View
:SubTitle
:ViewLocked 0
:PersistantPopups 0
:ExtendedPopupInfo 0
:ShowProbeLocations 1
:DateTimeFormat 0
:DefaultLabelHeight 8
:AnimateBarActive 0
:AnimateBarLabelStyle 0
:AnimateFrameRate 20
:AnimationStep 1
:ShowGrid 0
:ShowGridLabels 0
:GridDivisionsHint 5
:GridColour 0xc0c0c0
:GridFontName Arial
:GridFontSize 3
:BackgroundColour 0xffffff
:StreamLineMaxPoints 60
:StreamLineTimeStep 180.000000
:EndViewType CEnSim2DView
"""

view3d = """
:ViewType CEnSim3DView
:Title 3D View
:SubTitle
:ViewLocked 0
:PersistantPopups 0
:ExtendedPopupInfo 0
:ShowProbeLocations 1
:DateTimeFormat 0
:DefaultLabelHeight 8
:AnimateBarActive 0
:AnimateBarLabelStyle 0
:AnimateFrameRate 20
:AnimationStep 1
:ShowGrid 1
:ShowGridLabels 1
:GridDivisionsHint 5
:GridColour 0xc0c0c0
:GridFontName Arial
:GridFontSize 1
:BackgroundColour 0xffffff
:ViewMaximized 1
:MotionTarget 1
:ShowCrossHairs 1
:Near 50
:Far 5000
:DefaultView 1
:EndViewType CEnSim3DView
"""
