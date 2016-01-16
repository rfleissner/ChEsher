<h1>ChEsher</h1>
<p><b>ChEsher</b> is an additional tool to <a href="http://www.nrc-cnrc.gc.ca/eng/solutions/advisory/blue_kenue_index.html">Blue Kenue&trade;</a> that is a pre and post processing software for the <a href="http://www.opentelemac.org/">open TELEMAC-MASCARET</a> system - an integrated suite of solvers for use in the field of free-surface flow of hydraulic modeling. The tool was created for engineering purposes with the aim to support hydraulic engineers in converting file formats, generating meshes and processing respectively visualizing results from a hydraulic simulation. 
The main freatures are:
<ul>
<li>converting geometries from and to DXF file format</li>
<li>converting geometries from and to Blue Kenue&trade; file formats</li>
<li>generating meshes from linear structures like dams, dikes, road corridors, embankments and, of course, channels</li>
<li>visualizing results (scalars and vectors) on a rasterized grid for DXF file format</li>
<li>generating contour plots for DXF file format
</ul>

ChEsher is separated to various modules:
<ul>
<li><b>DXF2BK</b> provides transformations from the DXF format to geometric objects that can be red by Blue Kenue&trade;.</li>
<li><b>BK2DXF</b> transforms a 2D T3 Scalar Mesh to DXF format.</li>
<li><b>Mesh</b> creates channel meshes out of profiles and boundaries as well as breaklines if desired.</li>
<li><b>LandXML</b> transforms a 2D T3 Scalar Mesh to a LandXML surface that can be imported to a CAD program.</li>
<li><b>ScalarDXF</b> creates a DXF raster with attributes of a 2D T3 Scalar Mesh, for example water depths or water surface differences.</li>
<li><b>VectorDXF</b> creates a DXF raster with vectors of a 2D T3 Vector Mesh, for example flow velocities.</li>
<li><b>CS</b> formats the control sections output file and creates a DXF file with the control sections.</li>
<li><b>2DM2BK</b> transforms the contents from a SMS Mesh File to a T3 Scalar Mesh and to 2D/3D Line Sets.</li>
<li><b>Cont2DXF</b> creates a contour plot from a T3 Scalar Mesh and writes it to a DXF file.</li>
</ul>

<h2>Requirements</h2>
A solid knowledge in the use of Blue Kenue&trade; and in performing hydraulic simulations with Telemac 2d is required to take advantage from ChEsher.

<h2>Download & Install</h2>
ChEsher is an Open Source project written in Python 2.7.3 and comes under the GNU General Public License v2.0. Get ChEsher by downloading the repository as ZIP. There are precompiled installers for windows available. For other operating systems you can use the source code and run ChEsher with Python, which then has to be installed on your operating system with all the necessary python packages.


