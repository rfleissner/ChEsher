
#ChEsher

ChEsher is an additional tool to <a href="http://www.nrc-cnrc.gc.ca/eng/solutions/advisory/blue_kenue_index.html">Blue Kenue&trade;</a> that is a pre and post processing software for the <a href="http://www.opentelemac.org/">open TELEMAC-MASCARET</a> system - an integrated suite of solvers for use in the field of free-surface flow of hydraulic modeling. The tool was created for engineering purposes with the aim to support hydraulic engineers in converting file formats, generating meshes and processing respectively visualizing results from a hydraulic simulation. 
The main freatures are:
<ul>
<li>converting geometries from and to DXF file format</li>
<li>converting geometries from and to Blue Kenue&trade; file formats</li>
<li>generating meshes from linear structures like dams, dikes, road corridors, embankments and, of course, channels</li>
<li>visualizing results (scalars and vectors) on a rasterized grid for DXF file format</li>
<li>generating contour plots for DXF file format
</ul>

<p>
<center>
<a href="pics/0_index.png" target="_blank">
<img src="pics/0_index_small.png"/>
</a>
</center>
</p>

<br>ChEsher is separated to various modules:
<ul>
<li><a href="1_DXF2BK.html">DXF2BK</a> provides transformations from the DXF format to geometric objects that can be red by Blue Kenue&trade;.</li>
<li><a href="2_BK2DXF.html">BK2DXF</a> transforms a 2D T3 Scalar Mesh to DXF format.</li>
<li><a href="3_Mesh.html">Mesh</a> creates channel meshes out of profiles and boundaries as well as breaklines if desired.</li>
<li><a href="4_LandXML.html">LandXML</a> transforms a 2D T3 Scalar Mesh to a LandXML surface that can be imported to a CAD program.</li>
<li><a href="5_ScalarDXF.html">ScalarDXF</a> creates a DXF raster with attributes of a 2D T3 Scalar Mesh, for example water depths or water surface differences.</li>
<li><a href="6_VectorDXF.html">VectorDXF</a> creates a DXF raster with vectors of a 2D T3 Vector Mesh, for example flow velocities.</li>
<li><a href="7_CS.html">CS</a> formats the control sections output file and creates a DXF file with the control sections.</li>
<li><a href="8_2DM2BK.html">2DM2BK</a> transforms the contents from a SMS Mesh File to a T3 Scalar Mesh and to 2D/3D Line Sets.</li>
<li><a href="9_Cont2DXF.html">Cont2DXF</a> creates a contour plot from a T3 Scalar Mesh and writes it to a DXF file.</li>
</ul>

<h2>Requirements</h2>
A solid knowledge in the use of Blue Kenue&trade; and in performing hydraulic simulations with Telemac 2d is required to take advantage from ChEsher.

<h2>Download & Install</h2>
ChEsher is an Open Source project written in Python 2.7.3 and comes under the GNU General Public License v2.0. Visit <a href="https://github.com/rfleissner/ChEsher">GitHub</a> to download the whole repository as ZIP. There are precompiled installers for windows available. For other operating systems you can use the source code and run ChEsher with Python, which then has to be installed on your operating system with all the necessary python packages.

<h2>How to use the documentation</h2>

Each module is documented separately and an example is added. To implement most of the examples it is necessary to run the Telemac 2d validation test case <b><i>donau</i></b> with the *.cas files in the examples folder at first. The *.cas files differ in the velocity diffusivity factor:
<ul>
<li>case A: VELOCITY DIFFUSIVITY = default</li>
<li>case B: VELOCITY DIFFUSIVITY = 10.0</li>
</ul>
The input files for all the examples can be found in the examples folder.
</body></html>
