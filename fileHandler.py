#!/usr/bin/python -d
#
# Copyright (C) 2015  Reinhard Fleissner
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

"""Module with functins for reading and writing files."""

__author__="Reinhard Fleissner"
__date__ ="$29.08.2014 18:21:40$"

import ewsEnSim as ws
import xml.etree.cElementTree as ET
from copy import deepcopy as dc
#import dxfwrite
import ezdxf
from dxfwrite import DXFEngine as dxf
import math

def readDAT(filename):
    DAT_file = open(filename, 'r')
    DAT_file_content = DAT_file.readlines()
    DAT_file.close()

    SMS_wspl = {}
    
    start = False
    counter = 1
    for line in range(len(DAT_file_content)):
        keyword = DAT_file_content[line].split()[0]
        values = DAT_file_content[line].split()


        if start is True:
            SMS_wspl[counter] = float(values[0])
            counter += 1
            
        if keyword == 'TS':
            start = True
    
    return SMS_wspl

def read2DM(filename):
    file = open(filename, 'r')
    content = file.readlines()
    file.close()
    
    # SMS_elements = {SMS_element_id: [SMS_node_id, SMS_node_id, SMS_node_id (, SMS_node_id), material]}
    SMS_elements = {}

    # SMS_nodes = {SMS_node_id: [x, y, z]}
    SMS_nodes = {}

    # SMS_strings = {SMS_string_id: [node_id, node_id, node_id, ...]}
    SMS_strings = {}

    # SMS_material = {SMS_material_id: strickler's value}
    SMS_materials = {}

    # SMS_bc_nodes = {SMS_node_id: height}
    SMS_bc_nodes = {}

    # SMS_bc_strings_i = {string_id: value}
    SMS_bc_strings_1 = {}
    SMS_bc_strings_2 = {}
    SMS_bc_strings_3 = {}
    SMS_bc_strings_4 = {}
    SMS_bc_strings_5 = {}
    SMS_bc_strings_6 = {}
    SMS_bc_strings_7 = {}
    
    line = 1
    string_counter = 1
    string_vec = []

    while True:

        keyword = content[line].split()[0]
        values = content[line].split()

        # read elements
        if keyword == 'E3T' or keyword == 'E4Q':

            element_id = int(values[1])
            node_vec = []
            material_id = int(values[-1])

            for i in range(len(values)-2):
                node_vec.append(int(values[i+2]))

            SMS_elements[element_id] = node_vec

        # read nodes
        elif keyword == 'ND':

            node_id = int(values[1])
            coord_vec = []

            for i in range(3):
                coord_vec.append(float(values[i+2]))

            SMS_nodes[node_id] = coord_vec

        # read node strings
        elif keyword == "NS":

            for i in range(len(values)-1):
                node_id = abs(int(values[i+1]))
                string_vec.append(node_id)

            if int(values[-1]) < 0:
                SMS_strings[string_counter] = dc(string_vec)
                del string_vec[:]
                string_counter += 1

        # read material
        elif keyword == 'MAT':

            material_id = int(values[1])
            strickler = float(values[2])

            SMS_materials[material_id] = strickler

        # read boundary conditions for nodes
        elif keyword == 'BCN':

            node_id = int(values[1])
            value = float(values[-1])

            SMS_bc_nodes[node_id] = value

        # read boundary conditions for node strings
        elif keyword == 'BCS':

            type = int(values[2])
            string_id = int(values[1])

            if type == 1:
                val_vec = []
                val_vec.append(float(values[3]))
                val_vec.append(float(values[4]))
                SMS_bc_strings_1[string_id] = val_vec
            elif type == 2:
                val_vec = []
                val_vec.append(float(values[3]))
                SMS_bc_strings_2[string_id] = val_vec
            elif type == 3:
                val_vec = []
                val_vec.append(int(values[3]))
                SMS_bc_strings_3[string_id] = val_vec
            elif type == 4:
                val_vec = []
                val_vec.append(float(values[3]))
                val_vec.append(float(values[4]))
                val_vec.append(float(values[5]))
                val_vec.append(float(values[6]))
                val_vec.append(float(values[7]))
                val_vec.append(float(values[8]))
                SMS_bc_strings_4[string_id] = val_vec
            elif type == 5:
                val_vec = []
                val_vec.append(float(values[3]))
                SMS_bc_strings_5[string_id] = val_vec
            elif type == 6:
                val_vec = []
                val_vec.append(float(values[3]))
                val_vec.append(float(values[4]))
                val_vec.append(float(values[5]))
                val_vec.append(float(values[6]))
                SMS_bc_strings_6[string_id] = val_vec
            elif type == 7:
                SMS_bc_strings_7[string_id] = None
        if keyword == "TIME":
            break
        else:
            line += 1
    
    return SMS_elements, \
            SMS_nodes,\
            SMS_strings,\
            SMS_materials,\
            SMS_bc_nodes,\
            SMS_bc_strings_1,\
            SMS_bc_strings_2,\
            SMS_bc_strings_3,\
            SMS_bc_strings_4,\
            SMS_bc_strings_5,\
            SMS_bc_strings_6,\
            SMS_bc_strings_7\
    
def readI2S(filename):
    return readI3S(filename, 2)

def readI3S(filename, dim=3):
    def num(s):
        try:
            return int(s)
        except ValueError:
            return float(s)
        
    nodestrings = {}
    nodes = {}

    file = open(filename, 'r')
    content = file.readlines()
    file.close()

    endheader = False
    nodecounter = 0
    profilecounter = 0
    from types import IntType
    for line in range(len(content)):
        keyword = ''
        if len(content[line].split()) > 0:
            keyword = content[line].split()[0]
            values = content[line].split()
            if endheader is True:
                line = content[line].split()
                if type(num(line[0])) is IntType:
                    profilecounter += 1
                    nodestrings[profilecounter] = []
                else:
                    nodecounter += 1
                    coords = []
                    for i in range(dim):
                        coords.append(float(values[i]))
                    
                    # duplicates of coordinate nodes are not included
                    if len(nodes) > 0:
                        if coords == nodes[nodecounter-1]:
                            nodecounter = nodecounter - 1
                        else:
                            nodestrings[profilecounter].append(nodecounter)
                            nodes[nodecounter] = coords
                    else:
                        nodestrings[profilecounter].append(nodecounter)
                        nodes[nodecounter] = coords 
                        
            if keyword == ':EndHeader':
                endheader = True

    return nodes, nodestrings

def readCSDefinition(filename):

    file = open(filename, 'r')
    content = file.readlines()
    file.close()

    nCS = int(content[1].split()[0])
    nameCS = {}
    nodesCS = {}
    
    counterCS = 0

    del content[0:2]
        
    for line in range(2*nCS):
        if line % 2 == 0:
            counterCS +=1
            nameCS[counterCS] = content[line].split()[0]
        else:
            nodesCS[counterCS] = [int(content[line].split()[0]), int(content[line].split()[1])]

    return nCS, nameCS, nodesCS

def readCSResults(filename, nCS):

    file = open(filename, 'r')
    content = file.readlines()
    file.close()

    del content[0:2]
    
    resultsCS = {}
    valuesToNextTimestep = nCS + 1
    nValues = 0
    time = []
    counterCS = 1
    
    for i in range(nCS):
        resultsCS[i+1] = []
        
    for line in range(len(content)):
        
        lineContent = content[line].split()
        lineContentFloat = []

        for i in range(len(lineContent)):
            lineContentFloat.append(float(lineContent[i]))
        
        if nValues == 0:
            time.append(lineContentFloat[0])
            del lineContentFloat[0]

            for i in range(len(lineContentFloat)):
                resultsCS[counterCS].append(lineContentFloat[i])
                counterCS += 1
        else:
            for i in range(len(lineContentFloat)):
                resultsCS[counterCS].append(lineContentFloat[i])
                counterCS += 1            
            
        nValues += len(lineContent)
        
        if nValues == valuesToNextTimestep:
            nValues = 0
            counterCS = 1
        
    return time, resultsCS

def writeCSFormatted(filename, nameCS, time, resultsCS, decTime, decFlow):
    
    file = open(filename, 'w')
    file.write('Time\t')
    for key in nameCS:
        file.write("{0}\t".format(nameCS[key]))
    file.write("\n")
    
    for i in range(len(time)):
        file.write("{0}\t".format(round(time[i], decTime)))
        for key in resultsCS:
            file.write("{0}\t".format(round(resultsCS[key][i], decFlow)))
        file.write("\n")

    file.close()

def writeContIsoLineDXF(fname, contour, levels, coloursRGB, layer):
    
    if layer == "":
        layer = "0"
    dwg = ezdxf.new(dxfversion='AC1018')
    
    msp = dwg.modelspace()
    
    for c in range(len(contour)):
    
        if contour[c] is None:
            continue
        
        for segment in contour[c]['segments']:
   
            p1 = contour[c]['vertices'][segment[0]]
            p2 = contour[c]['vertices'][segment[1]]

            poly = msp.add_line(p1, p2, dxfattribs={'layer': layer})
            poly.rgb = coloursRGB[c]

    dwg.saveas(str(fname))

def writeContSolidDXF(fname, contour, levels, coloursRGB, layer):
    
    if layer == "":
        layer = "0"
    dwg = ezdxf.new(dxfversion='AC1018')
    
    msp = dwg.modelspace()
    
    for c in range(len(contour)):
    
        if contour[c] is None:
            continue

        for triangle in contour[c]['triangles']:
   
            p1 = contour[c]['vertices'][triangle[0]]
            p2 = contour[c]['vertices'][triangle[1]]
            p3 = contour[c]['vertices'][triangle[2]]

            solid = msp.add_solid([p1, p2, p3], dxfattribs={'layer': layer})
            solid.rgb = coloursRGB[c]

    dwg.saveas(str(fname))
    
def writeMeshDXF(fname, nodes, mesh, type):

    dwg = dxf.drawing(fname)

    for eID in mesh:
        p1 = (nodes[mesh[eID][0]][0], nodes[mesh[eID][0]][1], nodes[mesh[eID][0]][2])
        p2 = (nodes[mesh[eID][1]][0], nodes[mesh[eID][1]][1], nodes[mesh[eID][1]][2])
        p3 = (nodes[mesh[eID][2]][0], nodes[mesh[eID][2]][1], nodes[mesh[eID][2]][2])
        
        if type == 1:
            dwg.add(dxf.face3d((p1, p2, p3)))
        elif type == 2:
            dwg.add(dxf.polyline((p1, p2, p3, p1)))

    dwg.save()

def writeCSDXF(fname, nameCS, nodeIDsCS, nodesCS, valuesCS, decFlow, scale, prefix, suffix):
    
    from dxfwrite.const import TOP, BOTTOM, LEFT, CENTER, RIGHT
    
    dwg = dxf.drawing(fname)

    # create block for symbol on left side of CS

    arrowLeft = [(0.0,0.25), (1.0, 0.25), (0.5, 1.1160), (0.0,0.25)]

    symbolLeft = dxf.block(name='symbolLeft')
    symbolLeft.add( dxf.solid(arrowLeft, color=0) )

    symbolLeft.add( dxf.attdef(insert=(0, -0.25), tag='CS', height=1.0, color=0, halign=LEFT, valign=TOP ))

    # create block for symbol on right side of CS

    arrowRight = [(0.0,0.25), (-1.0, 0.25), (-0.5, 1.1160), (0.0,0.25)]

    symbolRight = dxf.block(name='symbolRight')
    symbolRight.add( dxf.solid(arrowRight, color=0) )

    symbolRight.add( dxf.attdef(insert=(0, -0.25), tag='CS', height=1.0, color=0, halign=RIGHT, valign=TOP ))
    
    # create block for symbol on center of CS
    
    symbolCenter = dxf.block(name='symbolCenter')
    symbolCenter.add( dxf.attdef(insert=(0.0, 0.03), tag='MAX', height=0.75, color=0, halign=CENTER, valign=BOTTOM) )
    symbolCenter.add( dxf.attdef(insert=(0.0, -0.25), tag='MIN', height=0.75, color=0, halign=CENTER, valign=TOP) )

    # add block definitions to the drawing
    dwg.blocks.add(symbolLeft)
    dwg.blocks.add(symbolCenter)
    dwg.blocks.add(symbolRight)
    
    for csID in nodeIDsCS:
        x1 = nodesCS[nodeIDsCS[csID][0]][0]
        x2 = nodesCS[nodeIDsCS[csID][1]][0]
        y1 = nodesCS[nodeIDsCS[csID][0]][1]
        y2 = nodesCS[nodeIDsCS[csID][1]][1]
    
        p1 = (x1, y1)
        p2 = (x2, y2)
        dx = x2 - x1
        dy = y2 - y1
        phi = math.atan2(dy,dx)*180.0/math.pi
        pm = ((x1+x2)/2.0, (y1+y2)/2.0)

        valMin = valuesCS[csID][0]
        valMax = valuesCS[csID][1]

        dwg.add(dxf.polyline((p1, p2)))
        
        values = {'CS': "{0}".format(nameCS[csID])}
        
        dwg.add(dxf.insert2(blockdef=symbolLeft, insert=p1,
                    attribs=values,
                    xscale=scale,
                    yscale=scale,
                    layer='0',
                    rotation = phi))
                    
        dwg.add(dxf.insert2(blockdef=symbolRight, insert=p2,
                    attribs=values,
                    xscale=scale,
                    yscale=scale,
                    layer='0',
                    rotation = phi))
                    
        valuesCenter = {'MIN': "{0}%.{1}f{2} (min)".format(prefix, decFlow, suffix) % valMin, 'MAX': "{0}%.{1}f{2} (max)".format(prefix, decFlow, suffix) % valMax}
        
        dwg.add(dxf.insert2(blockdef=symbolCenter, insert=pm,
                    attribs=valuesCenter,
                    xscale=scale,
                    yscale=scale,
                    layer='0',
                    rotation = phi))
    dwg.save()
    
def writeLineSetDXF(fname, linesetNodes, lineset, dim):

    dwg = dxf.drawing(fname)

    for lsID in lineset:
        nodes = ()
        for i in range(len(lineset[lsID])):
            x = linesetNodes[lineset[lsID][i]][0]
            y = linesetNodes[lineset[lsID][i]][1]
            if dim == 2:
                nodes += ((x, y),)
            elif dim == 3:
                z = linesetNodes[lineset[lsID][i]][2]
                nodes += ((x, y, z),)

        dwg.add(dxf.polyline(nodes))
        
    dwg.save()

def readT3V(filename):
    nodesT3V = {}
    mesh = {}
    
    file = open(filename, 'r')
    content = file.readlines()
    file.close()

    nodecounter = 0
    elementcounter = 0
    
    nodecount = 0
    elementcount = 0
    
    endheader = False

    for line in range(len(content)):
        keyword = ''
        if len(content[line].split()) > 0:
            keyword = content[line].split()[0]
            values = content[line].split()
            
            if keyword == ':ElementCount':
                elementcount = int(values[1])
                
            if keyword == ':NodeCount':
                nodecount = int(values[1])
                
            if endheader is True:
                
                if nodecounter < nodecount:
                    coords = []
                    for i in range(4):
                        coords.append(float(values[i]))
                    nodecounter += 1
                    nodesT3V[nodecounter] = coords 
                
                elif elementcounter < elementcount:
                    nIDs = []
                    for i in range(3):
                        nIDs.append(int(values[i]))
                    elementcounter += 1
                    mesh[elementcounter] = nIDs                     
                        
            if keyword == ':EndHeader':
                endheader = True

    return nodesT3V, mesh

def readT3VTriangulation(filename):
    
    x = []
    y = []
    u = []
    v = []
    triangles = []
    
    file = open(filename, 'r')
    content = file.readlines()
    file.close()

    nodecounter = 0
    elementcounter = 0
    
    nodecount = 0
    elementcount = 0
    
    endheader = False

    for line in range(len(content)):
        keyword = ''
        if len(content[line].split()) > 0:
            keyword = content[line].split()[0]
            values = content[line].split()
            
            if keyword == ':ElementCount':
                elementcount = int(values[1])
                
            if keyword == ':NodeCount':
                nodecount = int(values[1])
                
            if endheader is True:
                
                if nodecounter < nodecount:
                    x.append(float(values[0]))
                    y.append(float(values[1]))
                    u.append(float(values[2]))
                    v.append(float(values[3]))
                    nodecounter += 1
                    
                elif elementcounter < elementcount:
                    triangles.append([int(values[0])-1, int(values[1])-1, int(values[2])-1])
                    elementcounter += 1
                    
            if keyword == ':EndHeader':
                endheader = True

    return x, y, u, v, triangles

def readT3STriangulation(filename):
    x = []
    y = []
    z = []
    triangles = []

    file = open(filename, 'r')
    content = file.readlines()
    file.close()

    nodecounter = 0
    elementcounter = 0
    
    nodecount = 0
    elementcount = 0
    
    endheader = False

    for line in range(len(content)):
        keyword = ''
        if len(content[line].split()) > 0:
            keyword = content[line].split()[0]
            values = content[line].split()
            
            if keyword == ':ElementCount':
                elementcount = int(values[1])
                
            if keyword == ':NodeCount':
                nodecount = int(values[1])
                
            if endheader is True:
                
                if nodecounter < nodecount:
                    x.append(float(values[0]))
                    y.append(float(values[1]))
                    z.append(float(values[2]))
                    nodecounter += 1
                
                elif elementcounter < elementcount:
                    triangles.append([int(values[0])-1, int(values[1])-1, int(values[2])-1])
                    elementcounter += 1                 
                        
            if keyword == ':EndHeader':
                endheader = True

    return x, y, z, triangles

def readT3S(filename):
    nodesT3S = {}
    mesh = {}

    file = open(filename, 'r')
    content = file.readlines()
    file.close()

    nodecounter = 0
    elementcounter = 0
    
    nodecount = 0
    elementcount = 0
    
    endheader = False

    for line in range(len(content)):
        keyword = ''
        if len(content[line].split()) > 0:
            keyword = content[line].split()[0]
            values = content[line].split()
            
            if keyword == ':ElementCount':
                elementcount = int(values[1])
                
            if keyword == ':NodeCount':
                nodecount = int(values[1])
                
            if endheader is True:
                
                if nodecounter < nodecount:
                    coords = []
                    for i in range(3):
                        coords.append(float(values[i]))
                    nodecounter += 1
                    nodesT3S[nodecounter] = coords 
                
                elif elementcounter < elementcount:
                    nIDs = []
                    for i in range(3):
                        nIDs.append(int(values[i]))
                    elementcounter += 1
                    mesh[elementcounter] = nIDs                     
                        
            if keyword == ':EndHeader':
                endheader = True

    return nodesT3S, mesh

def readCS1(filename):
    levels = []
    colours = []

    file = open(filename, 'r')
    content = file.readlines()
    file.close()

    for line in range(len(content)):
        if content[line].startswith(':ScaleLevel '):
            levels.append(float(content[line].split()[-1]))
        elif content[line].startswith(':ScaleColour '):
            colours.append(content[line].split()[-1][1:].replace('x', '#'))

    return levels, colours

def writeXML(nodes, mesh, surfname, fname):
    root = ET.Element("LandXML")
    units = ET.SubElement(root, "Units")
    metric = ET.SubElement(units, "Metric", areaUnit="squareMeter", linearUnit="meter", volumeUnit="cubicMeter", temperatureUnit="celsius", pressureUnit="milliBars")
    surfaces = ET.SubElement(root, "Surfaces")
    surface = ET.SubElement(surfaces, "Surface", name=str(surfname))
    definition = ET.SubElement(surface, "Definition", surfType="TIN")
    Pnts = ET.SubElement(definition, "Pnts")
    
    for nID in nodes:
        ET.SubElement(Pnts, "P", id=str(nID)).text = str(nodes[nID][1]) + " " + str(nodes[nID][0]) + " " + str(nodes[nID][2])
    
    Faces = ET.SubElement(definition, "Faces")
    for fID in mesh:
        ET.SubElement(Faces, "F").text = str(mesh[fID][0]) + " " + str(mesh[fID][1]) + " " + str(mesh[fID][2])
        
    tree = ET.ElementTree(root)
    tree.write(fname)    

def writeXYZ(nodes, fname):
    file = open(fname, 'w')
    file.write(':FileType\txyz ASCII EnSim 1.0\n')
    file.write(':EndHeader\n')
    for nID in nodes:
        file.write(str(nodes[nID][0]) + ' ' + str(nodes[nID][1]) + ' ' + str(nodes[nID][2]) + '\n')
    file.close()
    
def writeI2S(nodes, profiles, fname):
    writeI3S(nodes, profiles, fname, 2)

def writeI3S(nodes, profiles, fname, dim=3):
    file = open(fname, 'w')
    file.write(':FileType\ti{0}s ASCII EnSim 1.0\n'.format(dim))
    file.write(':AttributeUnits 1 m\n')
    file.write(':EndHeader\n')
    for pID in profiles:
        file.write(str(len(profiles[pID])) + ' 0\n')
        for i in range(len(profiles[pID])):
            nID = profiles[pID][i]
            if dim == 2:
                 file.write(str(nodes[nID][0]) + ' ' + str(nodes[nID][1]) + '\n')
            elif dim ==3:
                file.write(str(nodes[nID][0]) + ' ' + str(nodes[nID][1]) + ' ' + str(nodes[nID][2]) + '\n')
    file.close()

def writeScalarDXF(nodes, SMin, SMax, eps, scale, symbol, useMono, fname):

    colMono = 7
    colPos = 1
    colNeg = 3

    hLine = [(-0.75,0.0), (0.75, 0.0)]
    vLine = [(0.0,-0.75), (0.0,0.75)]
    rad = 0.375

    dwg = dxf.drawing(fname)

    # create block
    scalarsymbol = dxf.block(name='symbol')
    if symbol != 0 and symbol != 3:
        scalarsymbol.add( dxf.polyline(hLine, color=0) )
        scalarsymbol.add( dxf.polyline(vLine, color=0) )
    if symbol != 1 and symbol != 3:
        scalarsymbol.add( dxf.circle(radius=rad, color=0) )

    # define some attributes
    scalarsymbol.add( dxf.attdef(insert=(0.5, 0.5), tag='VAL1', height=1.0, color=0) )
    scalarsymbol.add( dxf.attdef(insert=(0.5, -1.5), tag='VAL2', height=1.0, color=0) )

    # add block definition to the drawing
    dwg.blocks.add(scalarsymbol)
    
    nOfScalars = 0
    
    for nID in nodes:
        x = nodes[nID][0]
        y = nodes[nID][1]
        val1 = nodes[nID][2]
        val2 = nodes[nID][3]

        values = {}
        if val2 is None:
            values = {'VAL1': "%.2f" % val1, 'VAL2': ""}
        else:
            if val2 < eps and val2 > -eps:
                values = {'VAL1': "%.2f" % val1, 'VAL2': ""}
            else:
                values = {'VAL1': "%.2f" % val1, 'VAL2': "%.2f" % val2}
                
        # define color
        col = 0
        if useMono is True:
            col = colMono
        else:
            if val1 >= 0:
                col = colPos
            else:
                col = colNeg

        if val1 >= SMin and val1 <= SMax:
            if val1 < eps and val1 > -eps:
                continue
            else:
                dwg.add(dxf.insert2(blockdef=scalarsymbol, insert=(x, y),
                                    attribs=values,
                                    xscale=scale,
                                    yscale=scale,
                                    layer='0',
                                    color = col))
                nOfScalars += 1
    dwg.save()
    
    return nOfScalars
    
def writeVectorDXF(nodes, VMin, VMax, eps, scale, fname):

    colMono = 7

    arrow = [(1.0,0.0),(0.6,-0.1),(0.6,0.1),(1.0,0.0)]
    arrowline = [(0.0,0.0),(0.6,0.0)]

    dwg = dxf.drawing(fname)

    # create block
    vectorsymbol = dxf.block(name='vector')
    vectorsymbol.add( dxf.polyline(arrow, color=0) )
    vectorsymbol.add( dxf.polyline(arrowline, color=0) )

    # add block definition to the drawing
    dwg.blocks.add(vectorsymbol)

    nOfVectors = 0
    
    for nID in nodes:
        x = nodes[nID][0]
        y = nodes[nID][1]
        u = nodes[nID][2]
        v = nodes[nID][3]
        velocity = (u**2.0 + v**2.0)**(1.0/2.0)
        phi = math.atan2(v,u)*180.0/math.pi

        # write block, if value is inside a given band

        blockScale = scale * velocity 
        if velocity <= VMax and velocity >= VMin:
            if velocity < eps and velocity > -eps:
                continue
            else:
                dwg.add(dxf.insert2(blockdef=vectorsymbol, insert= (x, y),
                                    xscale=blockScale,
                                    yscale=blockScale,
                                    layer='0',
                                    color = colMono,
                                    rotation = phi))
                nOfVectors += 1  
    dwg.save()
    
    return nOfVectors
    
def writeT3S(nodes, mesh, fname):
    file = open(fname, 'w')
    file.write(':FileType\tt3s ASCII EnSim 1.0\n')
    file.write(':AttributeName 1 Elevation\n')
    file.write(':NodeCount {0}\n'.format(len(nodes)))
    file.write(':ElementCount {0}\n'.format(len(mesh)))
    file.write(':ElementType T3\n')
    file.write(':EndHeader\n')

    for nID in nodes:
        file.write('{0} {1} {2}\n'.format(nodes[nID][0], nodes[nID][1], nodes[nID][2]))
    for eID in mesh:
        file.write('{0} {1} {2}\n'.format(mesh[eID][0], mesh[eID][1], mesh[eID][2]))
    file.close()

def writeEWS(content, view, fname):
    file = open(fname, 'w')
    file.write(':FileType ews ASCII EnSim 1.0\n')
    file.write(':Application\tBlueKenue\n')
    file.write(':Version\t3.3.4\n')
    file.write(':IsMaximized\t1\n')
    file.write(':CurrentWorkingDirectory C:\Program Files\CHC\BlueKenue\n')
    file.write(':CustomColours 0x4e4e4e 0xffffff 0xffffff 0xffffff 0xffffff 0xffffff 0xffffff 0xffffff 0xffffff 0xffffff 0xffffff 0xffffff 0xffffff 0xffffff 0xffffff 0xffffff\n')
    file.write(ws.view2d)
    file.write(ws.view3d)
    file.write(content)
    file.write(view)
    file.close()

def readDXF(dxf, layer):

    def convertTuple(point, dim):
        if dim == 2:
            node = [point[0], point[1], 0.0]
        elif dim == 3:
            node = [point[0], point[1], point[2]]
        return node

    nodes = {}
    strings = {}
    nodecounter = 0
    stringcounter = 0
    pointstring = []
    
    layer_entities = [entity for entity in dxf.entities if entity.layer == layer]

#    print layer_entities[0].points
    

    for e in layer_entities:
        dxftype = e.dxftype
        if dxftype == 'POINT':
            nodes[nodecounter] = convertTuple(e.point, 3)
            pointstring.append(nodecounter)
            nodecounter +=1
        elif dxftype == 'LINE':
            nodes[nodecounter] = convertTuple(e.start, 3)
            nodes[nodecounter+1] = convertTuple(e.end, 3)
            strings[stringcounter] = [nodecounter, nodecounter+1]
            nodecounter += 2
            stringcounter += 1
        elif dxftype == 'LWPOLYLINE':
            strings[stringcounter] = []
            for point in e.points:             
                nodes[nodecounter] = convertTuple(point, 2)
                strings[stringcounter].append(nodecounter)
                nodecounter +=1
            stringcounter += 1
        elif dxftype == 'POLYLINE':
            strings[stringcounter] = []
            for point in e.points():             
                if e.mode == "polyline2d":
                    nodes[nodecounter] = convertTuple(point, 2)
                elif e.mode == "polyline3d":
                    nodes[nodecounter] = convertTuple(point, 3)
                strings[stringcounter].append(nodecounter)
                nodecounter +=1
            stringcounter += 1
    if len(pointstring) > 0:
        strings[len(strings)] = pointstring

    return nodes, strings