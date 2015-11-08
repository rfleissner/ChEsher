<html><body>
<h1>ChEsher</h1>
<p><b>ChEsher</b> is an additional tool to BlueKenue that is a pre and post processing software for the TELEMAC-MASCARET system which is an integrated suite of solvers for use in the field of free-surface flow of hydraulic modeling. The tool was created for engineering purposes with the aim to support hydraulic engineers in converting file formats, generating meshes and processing respectively visualizing results from a hydraulic simulation. 
The main freatures are:
<ul>
<li>converting geometries from and to dxf file format</li>
<li>converting geometries from and to BlueKenue file formats</li>
<li>generating meshes from linear structures like dams, dikes, road corridors, embankments and, of course, channels</li>
<li>visualizing results (scalars and vectors) on a rasterized grid</li>
</ul>

The tool was created for engineering purposes as support to perform flood analysis to derive flood protection measures. There it is necessary to create a triangulated surface from the terrain that includes dams, structures, road corridors, embankments and, of course, the river bed. Such linear structures can be meshed with ChEsher out of profiles, where also the elevation of the mesh is interpolated from the profiles.
Often, terrain analysis and the planning process is done by CAD software. So it was helpful to create an interface to CAD software, that can transform CAD objects to formats, that can be red by BlueKenue and that can transform BlueKenue formats and results from the analysis back to CAD software.
When planning flood protection projects, the first step is to analyse the status quo of the flood. Then, flood protection measures are derived and the last step is to analyse the future flood state. For water law agencies the influence of protection measures in form of differences of the water surface and the change in flood areas between the actual and the future state are relevant. Therefore colour ranges of water surface differences often are less accurate and concrete values are demanded, which can be produced by ChEsher.

<br>ChEsher is separated to various modules:
<ul>
<li><a href="1_DXF2BK.html">DXF2BK</a> provides transformations from the DXF format to geometric objects that can be red by BlueKenue.</li>
<li><a href="2_BK2DXF.html">BK2DXF</a> transforms a 2D T3 Scalar Mesh to DXF format.</li>
<li><a href="3_Mesh.html">Mesh</a> creates channel meshes out of profiles and boundaries as well as breaklines if desired.</li>
<li><a href="4_LandXML.html">LandXML</a> transforms a 2D T3 Scalar Mesh to a LandXML surface that can be imported to a CAD program.</li>
<li><a href="5_ScalarDXF.html">ScalarDXF</a> creates a DXF raster with attributes of a 2D T3 Scalar Mesh, for example water depths or water surface differences.</li>
<li><a href="6_VectorDXF.html">VectorDXF</a> creates a DXF raster with vectors of a 2D T3 Vector Mesh, for example flow velocities.</li>
<li><a href="7_CS.html">CS</a> formats the control sections output file and creates a DXF file with the control sections.</li>
<li><a href="8_2DM2BK.html">2DM2BK</a> transforms the contents of a SMS Mesh File to a T3 Scalar Mesh and to 2D/3D Line Sets.</li>
</ul>


<h2>Download & Install</h2>
ChEsher is an Open Source project written in Python 2.7.3 and comes under the GNU General Public Licence v2.0. Visit <a href="https://github.com/rfleissner/ChEsher">GitHub</a> to download the whole repository as ZIP. There are precompiled installers for windows available. For other operating systems you can use the source code and run ChEsher with Python, which then has to be installed on your operating system with all the necessary python packages.

<h2>How to use the documentation</h2>

Each module is documented separately and an example is added. To implement most of the examples, it is necessary to run the Telemac 2d validation test case <b>donau</b> with the cas-files in the examples folder at first. The input files from all the examples can be found in the examples folder.
</body></html>
