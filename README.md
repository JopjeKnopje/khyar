# Khyar

Quick and dirty web scraper for the [chai and conversation](https://www.chaiandconversation.com/persian-dictionary?page=1#dictionary-results)  dictionary. This website does not have a search engine for the dictionary. So I cobbled together this tool so you can download and search it locally in a JSON file.
I use [jless](https://github.com/PaulJuliusMartinez/jless) for this


## HTML Dict structure
```html
<table class="table vocab-list" data-controller="vocab">
<thread></thread>
<thead></thead>
<tbody>
		<tr>
			<!-- phonetic -->
			<td></td> 
			<!-- english -->
			<td></td>
			<!-- script -->
			<td></td>
			<!-- appears_in -->
			<td></td>
		</tr>
		<tr>
			<td></td>
			<td></td>
			<td></td>
			<td></td>
		</tr>
		...
	</tbody>
</table>
```


## Dev

Made with uv msgspec and httpx


prekcommi


