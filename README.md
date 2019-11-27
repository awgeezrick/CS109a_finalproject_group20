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

> [Summary](#summary)
> 
> [Data Structure](#data_structure)
> 
> [EDA](#eda)
> 
> [Models](#models)
> 
> [Scores and Comparisons](#scores_comparisons)
> 
> [Summary](#summary)

<table>
<thead>
<tr class="header">
<th><span id="summary" class="anchor"></span><strong>Summary</strong> <a href="#table_of_contents">(back to index)</a></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p><strong>Project Statement</strong></p>
<p>At its core, the project seeks to answer the question:</p>
<p><em>“How do I generate a desirable playlist for a listener?”</em></p>
<p>More specifically, the project seeks to answer the above question <em>given</em> a context consisting of one or many songs provided by the user. The result is a playlist of 20 songs that are similar to the song(s) provided by the user. The recommendations are primarily based on preferences from other users measured by other users’ playlists.</p></td>
</tr>
<tr class="even">
<td></td>
</tr>
</tbody>
</table>

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

<table>
<thead>
<tr class="header">
<th><span id="models" class="anchor"></span><strong>Models</strong> <a href="#table_of_contents">(back to index)</a></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>&lt;summary of models and explanations&gt;</td>
</tr>
<tr class="even">
<td><h1 id="spotify-recommender-model-types"><strong>Spotify Recommender Model Types</strong></h1>
<p>For recommendations, 2 types of recommendation strategies:</p>
<ol type="1">
<li><p><strong>Content-Based</strong></p></li>
</ol>
<blockquote>
<p>Predicts based on what a user has listened to in the past. Uses features of songs to find similar songs.</p>
</blockquote>
<ol start="2" type="1">
<li><p><strong>Collaborative</strong></p></li>
</ol>
<blockquote>
<p>Predicts based on what other listeners like Focuses on what songs other users liked who also liked a chosen song. </p>
</blockquote></td>
</tr>
<tr class="odd">
<td><p><strong>KNN-Classification</strong></p>
<p><strong>&lt;description of KNN classification&gt;</strong></p></td>
</tr>
<tr class="even">
<td></td>
</tr>
<tr class="odd">
<td><h2 id="section"></h2></td>
</tr>
<tr class="even">
<td><h2 id="word2vec">Word2Vec</h2>
<p>Word2Vec is a process that uses vectorized words to predict other words. It does this by ingesting a series of documents, parsing out the words, vectorizing the words and then using the vector representations to predict other words. The vectors are built in such a way that each word has a unique vector that is based on its usage in the documents. The result is a vector space filled with words where related words have vectors that are similar. This vector space is referred to an an <strong>embedding</strong>. This embedding is used in two common word prediction tasks: Skip-Gram and Continuous Bag of Words.</p>
<blockquote>
<p><strong>Skip-Gram</strong> <br />
The Skip-Gram model asks for a single word and then predicts words surrounding the word.</p>
<p><strong>Bag-of-Words</strong> <br />
The bag-of-words model asks for a series of words and will return the missing word.</p>
</blockquote>
<p>For the Spotify Recommender, we will use Word2Vec to assign vectors to Songs by providing the model with a series of playlists instead of documents.</p>
<p><strong>Embeddings</strong></p>
<p>The vectorized space of words is referred to as an embedding. This embedding is used to train a Skip-Gram or a Bag-of-Words model. The embedding without the models is quite useful. It represents a vectorized vocabulary of words where vectorized words can be added or subtracted from one another to find the sum or difference of their meanings. Synonyms of words are other vectors with that are nearby in the embedded space. Below, we will use this embedding to create a playlist without a model and compare it to playlists that are used with the models described above.</p>
<h3 id="making-a-playlist">Making a Playlist</h3>
<p>To make a playlist, we simply convert Songs to Vectors and then find new songs by finding other songs with similar vectors. To achieve this, we can use the Bag-of-Words or Skip-Gram approach as mentioned above. Provide a song, a Skip-Gram model can supply a playlist. Provide a list of songs, and Bag-of-Words model can give you the next song.</p>
<p>3 approaches using Word2Vec and Embeddings are explored:</p>
<h3 id="embeddings-from-playlists---song-id---unsupervised">1. Embeddings from Playlists - Song ID - Unsupervised</h3>
<blockquote>
<p>Here, we will take data from Spotify that included 1M playlists and the songs in each playlist. We'll use the Word2Vec process supplying playlists as documents and each song's unique id is used as the word. <br />
<br />
After the embedding is created, we can skip the creation of building and training a BOW or Skip-Gram model. All we need to do is find vectors that are similar to a song or a list of songs. </p>
</blockquote>
<h3 id="embeddings-from-playlists---song-id---bow">2. Embeddings from Playlists - Song ID - BOW</h3>
<blockquote>
<p>We can use the same embedding to create a BOW model.</p>
</blockquote>
<h3 id="embeddings-from-playlists---song-id---skip-gram">3. Embeddings from Playlists - Song ID - Skip-Gram</h3>
<blockquote>
<p>Let's use the embedding from the playlists and use Word2Vec to create a Skip-Gram model.</p>
</blockquote></td>
</tr>
<tr class="odd">
<td><h2 id="section-1"></h2></td>
</tr>
<tr class="even">
<td></td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><span id="scores_comparisons" class="anchor"></span><strong>Scores and Comparisons</strong> <a href="#table_of_contents">(back to index)</a></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>&lt;metrics for each model and comparisons&gt;</p>
<h3 id="r-precision">R-precision </h3>
<p>R-precision is the number of retrieved relevant tracks divided by the number of known relevant tracks (i.e., the number of withheld tracks):</p>
<p>R-precision=∣∣G∩R1:|G|∣∣|G|.</p>
<p>The metric is averaged across all playlists in the challenge set. This metric rewards total number of retrieved relevant tracks (regardless of order).</p>
<h3 id="normalized-discounted-cumulative-gain-ndcg">Normalized discounted cumulative gain (NDCG) </h3>
<p>Discounted cumulative gain (DCG) measures the ranking quality of the recommended tracks, increasing when relevant tracks are placed higher in the list. Normalized DCG (NDCG) is determined by calculating the DCG and dividing it by the ideal DCG in which the recommended tracks are perfectly ranked:</p>
<p>DCG=rel1+|R|∑i=2relilog2(i+1).</p>
<p>The ideal DCG or IDCG is, on our case, equal to:</p>
<p>IDCG=1+|G|∑i=21log2(i+1).</p>
<p>If the size of the set intersection of G and R, is empty, then the DCG is equal to 0. The NDCG metric is now calculated as:</p>
<p>NDCG=DCGIDCG.</p></td>
</tr>
<tr class="even">
<td></td>
</tr>
<tr class="odd">
<td></td>
</tr>
</tbody>
</table>

| **Conclusion** [(back to index)](#table_of_contents) |
| ---------------------------------------------------- |
| \<findings\>                                         |
|                                                      |
|                                                      |

**NOTE**:

To convert this to Git markdown:

pandoc -f docx -t gfm Spotify\\ Project-ProjectDocument.docx -o
README.md
