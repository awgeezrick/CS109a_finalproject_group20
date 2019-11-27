**Spotify Project**

**Team 20**

**Ankit Bhargava, Erik Subatis, Mark McDonald**

**TA Advisor**: Rashmi (<rjain29@gmail.com>)

**Project Repo**:
<https://github.com/subatis/CS109a_finalproject_group20>

**Project Database**:
<https://drive.google.com/drive/folders/14OBw3t3gKwPgxX3tx_ogHHpXpx6iWXRC>

<span id="table_of_contents" class="anchor"></span>**Table of
Contents:**

[Summary](#summary)

[Data Structure](#data_structure)

[EDA](#eda)

[Models](#models)

[Scores and
Comparisons](#scores_comparisons)

[Summary](#summary)

| <span id="summary" class="anchor"></span>**Summary** [(back to index)](#table_of_contents) |
| ------------------------------------------------------------------------------------------ |
| \<brief summary of the project \>                                                          |
|                                                                                            |
|                                                                                            |

<table>
<thead>
<tr class="header">
<th><strong>Data Structure</strong> <a href="#table_of_contents">(back to index)</a></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>&lt;explain data received and how it was organized&gt;</p>
<p><strong>Database</strong></p>
<p>The project data has been stored in a database for uniformity, speed and simplicity of access. In addition to the playlists provided, tables were added to include additional data for tracks and artists.</p>
<p><strong>Utility Functions and Project API</strong></p>
<p>A set of API wrappers were created to streamline access to Spotify data and the Team Database. These API’s simplify Spotify authentication and avoid the need to navigate arguments that are not relevant to the project.</p>
<p><strong>Data Inconsistencies and Corrections</strong></p>
<p>Various records needed to be deleted or changed after reviewing their validity. Some artist URL’s had changed in Spotify and some tracks were no longer available. These changes were not extensive and did not have a major impact on the usefulness of the data.</p></td>
</tr>
<tr class="even">
<td></td>
</tr>
<tr class="odd">
<td></td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><span id="eda" class="anchor"></span><strong>EDA</strong> <a href="#table_of_contents">(back to index)</a></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p><strong>Playlists</strong></p>
<p>The Playlists table is extensive with 999k playlists and 66M tracks</p>
<p><img src="media/image1.png" style="width:4.9759in;height:0.44884in" /></p>
<p>There are some outliers with very long lengths, but the average playlist is 50 songs long and the most common length is 20.</p>
<p><img src="media/image2.png" style="width:4.43462in;height:0.75in" /></p>
<p><img src="media/image3.png" style="width:4.62037in;height:1.87727in" /></p></td>
</tr>
<tr class="even">
<td><p><strong>Artists</strong></p>
<p>In the playlists, 296k unique artists exist:</p>
<p><img src="media/image4.png" style="width:5.25463in;height:0.47398in" /></p>
<p>By examining the number of appearances in playlists, we are able to determine the popularity of Artists based on our dataset. Spotify also supplies a field called ‘artist popularity’; however, we found that a majority of Artists in our dataset had a popularity of 0, so we will not rely on the Spotify popularity data.</p>
<p><img src="media/image5.png" style="width:3.62392in;height:3.05556in" /></p>
<p>Spotify supplies genres by artist. After extracting this data, we determined that over 60% of artists had no genre assigned by Spotify, so we will not rely on this data.</p></td>
</tr>
<tr class="odd">
<td><p><strong>Tracks</strong></p>
<p>2.2M unique tracks can be found in the playlists.</p>
<p><img src="media/image6.png" style="width:5.22804in;height:0.37963in" /></p>
<p>After querying data from Spotify, various additional useful fields are available for each track. Values are assigned to a significant portion of the population making these features useful for building recommendation lists. Distributions of these features are available in the accompanying notebook.</p></td>
</tr>
<tr class="even">
<td></td>
</tr>
</tbody>
</table>

| <span id="models" class="anchor"></span>**Models** [(back to index)](#table_of_contents) |
| ---------------------------------------------------------------------------------------- |
| \<summary of models and explanations\>                                                   |
|                                                                                          |
|                                                                                          |

| <span id="scores_comparisons" class="anchor"></span>**Scores and Comparisons** [(back to index)](#table_of_contents) |
| -------------------------------------------------------------------------------------------------------------------- |
| \<metrics for each model and comparisons\>                                                                           |
|                                                                                                                      |
|                                                                                                                      |

| **Conclusion** [(back to index)](#table_of_contents) |
| ---------------------------------------------------- |
| \<findings\>                                         |
|                                                      |
|                                                      |

**NOTE**:

To convert this to Git markdown:

pandoc -f docx -t gfm Spotify\\ Project-ProjectDocument.docx -o
README.md
